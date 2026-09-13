using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.IO;
using System.Linq;
using System.Windows.Media.Imaging;
using System.Windows.Threading;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using OpenCvSharp;
using PCControlApp.Models;
using PCControlApp.VisionEngine;

namespace PCControlApp.ViewModels
{
    /// <summary>
    /// BỘ NÃO ĐIỀU PHỐI (VIEWMODEL) THEO KIẾN TRÚC MVVM
    /// Tích hợp MVTec Metal Nut Inspector và bộ dữ liệu công nghiệp thật 100%
    /// </summary>
    public partial class MainViewModel : ObservableObject
    {
        private readonly MetalNutInspector _nutInspector;
        private readonly OnnxAnomalyInspector _onnxInspector;
        private readonly List<string> _sampleImagePaths = new List<string>();
        private int _sampleIndex = 0;
        private int _currentProductId = 1000;
        private readonly DispatcherTimer _autoRunTimer;

        [ObservableProperty]
        private bool _isAiMode = false;

        [ObservableProperty]
        private string _currentModeName = "Thước kẹp Caliper (Rule-based)";

        [ObservableProperty]
        private string _modeButtonText = "Chuyển sang: AI Vision (ONNX)";

        [ObservableProperty]
        private InspectionResult _currentResult;

        [ObservableProperty]
        private int _totalCount = 0;

        [ObservableProperty]
        private int _okCount = 0;

        [ObservableProperty]
        private int _ngCount = 0;

        [ObservableProperty]
        private string _yieldRate = "100.0%";

        [ObservableProperty]
        private string _yieldRateColor = "#10B981";

        [ObservableProperty]
        private bool _isAutoRunning = false;

        [ObservableProperty]
        private string _autoRunButtonText = "Chạy liên tục";

        [ObservableProperty]
        private BitmapImage? _displayImage;

        [ObservableProperty]
        private string _statusLog = "Hệ thống sẵn sàng. Chờ lệnh Trigger...";

        public ObservableCollection<string> PlcLogs { get; } = new ObservableCollection<string>();

        public MainViewModel()
        {
            _nutInspector = new MetalNutInspector();
            _onnxInspector = new OnnxAnomalyInspector();

            // Tìm và nạp ảnh từ tập dữ liệu công nghiệp MVTec AD
            string baseDir = AppDomain.CurrentDomain.BaseDirectory;
            string projectRoot = Path.GetFullPath(Path.Combine(baseDir, "..", "..", "..", "..", ".."));
            string mvtecDir = Path.Combine(projectRoot, "datasets", "mvtec_metal_nut");

            if (!Directory.Exists(mvtecDir))
            {
                mvtecDir = Path.Combine(Directory.GetCurrentDirectory(), "datasets", "mvtec_metal_nut");
            }
            if (!Directory.Exists(mvtecDir))
            {
                mvtecDir = @"d:\Projects\Machine-Vision\datasets\mvtec_metal_nut";
            }

            if (Directory.Exists(mvtecDir))
            {
                var goods = Directory.GetFiles(Path.Combine(mvtecDir, "test_good"), "*.png");
                var scratches = Directory.GetFiles(Path.Combine(mvtecDir, "test_scratch"), "*.png");
                var bents = Directory.GetFiles(Path.Combine(mvtecDir, "test_bent"), "*.png");
                var colors = Directory.GetFiles(Path.Combine(mvtecDir, "test_color"), "*.png");
                var flips = Directory.GetFiles(Path.Combine(mvtecDir, "test_flip"), "*.png");

                // Đan xen mẫu OK và các loại lỗi để mô phỏng dây chuyền thực tế
                int maxLen = Math.Max(goods.Length, Math.Max(scratches.Length, Math.Max(bents.Length, Math.Max(colors.Length, flips.Length))));
                for (int i = 0; i < maxLen; i++)
                {
                    if (i < goods.Length) _sampleImagePaths.Add(goods[i]);
                    if (i < scratches.Length) _sampleImagePaths.Add(scratches[i]);
                    if (i < goods.Length - 1) _sampleImagePaths.Add(goods[i + 1]);
                    if (i < bents.Length) _sampleImagePaths.Add(bents[i]);
                    if (i < colors.Length) _sampleImagePaths.Add(colors[i]);
                    if (i < flips.Length) _sampleImagePaths.Add(flips[i]);
                }
            }

            _currentResult = new InspectionResult
            {
                ProductId = 1000,
                PartType = "MVTec Metal Nut",
                SerialNumber = "NUT-MVTEC-0000",
                IsOk = true,
                InnerDiameter = 155.0,
                OuterDiameter = 630.0,
                Angle = 0.0,
                CycleTimeMs = 0.0,
                DefectReason = "STANDBY"
            };

            _autoRunTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(1200)
            };
            _autoRunTimer.Tick += (s, e) => TriggerInspection();

            AddLog("Hệ thống Vision PC Control C# .NET 8 khởi động thành công!");
            AddLog($"Đã nạp {_sampleImagePaths.Count} mẫu đai ốc từ MVTec AD Dataset.");
            AddLog("Worker Pool OpenCvSharp sẵn sàng xử lý 4G Pipeline.");

            // Kích hoạt kiểm tra mẫu đầu tiên
            if (_sampleImagePaths.Count > 0)
            {
                TriggerInspection();
            }
        }

        [RelayCommand]
        public void ToggleAlgorithmMode()
        {
            IsAiMode = !IsAiMode;
            if (IsAiMode)
            {
                CurrentModeName = "Mạng nơ-ron đặc trưng (PatchCore ONNX)";
                ModeButtonText = "Chuyển sang: Thước kẹp Caliper";
                AddLog("[HỆ THỐNG] Đã chuyển đổi phương pháp: Mạng nơ-ron đặc trưng PatchCore ONNX.");
            }
            else
            {
                CurrentModeName = "Thước kẹp Caliper (Rule-based)";
                ModeButtonText = "Chuyển sang: AI Vision (ONNX)";
                AddLog("[HỆ THỐNG] Đã chuyển đổi phương pháp: Thước kẹp Caliper quang học.");
            }
        }

        [RelayCommand]
        public void TriggerInspection()
        {
            if (_sampleImagePaths.Count == 0)
            {
                AddLog("[CẢNH BÁO] Không tìm thấy ảnh trong thư mục datasets/mvtec_metal_nut!");
                return;
            }

            _currentProductId++;
            string imgPath = _sampleImagePaths[_sampleIndex];
            _sampleIndex = (_sampleIndex + 1) % _sampleImagePaths.Count;

            // Xử lý Vision Engine theo chế độ được chọn
            Mat annotatedMat;
            InspectionResult res;
            if (IsAiMode && _onnxInspector.IsLoaded)
            {
                res = _onnxInspector.Inspect(imgPath, _currentProductId, out annotatedMat);
            }
            else
            {
                res = _nutInspector.Inspect(imgPath, _currentProductId, out annotatedMat);
            }
            CurrentResult = res;

            // Cập nhật thống kê
            TotalCount++;
            if (res.IsOk)
            {
                OkCount++;
            }
            else
            {
                NgCount++;
            }

            double rate = TotalCount > 0 ? (OkCount * 100.0 / TotalCount) : 100.0;
            YieldRate = $"{rate:F1}%";
            YieldRateColor = rate >= 90.0 ? "#10B981" : "#EF4444";

            // Hiển thị ảnh có vẽ overlay trực tiếp
            using (annotatedMat)
            {
                DisplayImage = MatToBitmapImage(annotatedMat);
            }

            // Ghi log giao tiếp PLC (Bắt tay Socket TCP/IP)
            string plcSignal = res.IsOk ? "Y0=1 (PASS BĂNG CHUYỀN)" : $"Y1=1 (KÍCH XI LANH LOẠI BỎ LỖI: {res.DefectType})";
            AddLog($"[TRIG #{res.ProductId}] {res.CycleTimeMs:F1}ms | {res.VerdictText} -> PLC {plcSignal}");
        }

        [RelayCommand]
        public void ToggleAutoRun()
        {
            IsAutoRunning = !IsAutoRunning;
            if (IsAutoRunning)
            {
                AutoRunButtonText = "Dừng băng chuyền";
                AddLog("[BĂNG CHUYỀN] Bắt đầu quét chu kỳ tự động (1.2s/sản phẩm)...");
                _autoRunTimer.Start();
            }
            else
            {
                AutoRunButtonText = "Chạy liên tục";
                _autoRunTimer.Stop();
                AddLog("[BĂNG CHUYỀN] Đã tạm dừng hoạt động.");
            }
        }

        [RelayCommand]
        public void ResetStats()
        {
            TotalCount = 0;
            OkCount = 0;
            NgCount = 0;
            YieldRate = "100.0%";
            YieldRateColor = "#10B981";
            PlcLogs.Clear();
            AddLog("🔄 Đã Reset toàn bộ bộ đếm ca sản xuất về 0.");
        }

        /// <summary>
        /// Chuyển đổi an toàn OpenCvSharp.Mat sang WPF BitmapImage (Zero RAM Leak)
        /// </summary>
        private BitmapImage MatToBitmapImage(Mat mat)
        {
            using var mem = mat.ToMemoryStream(".png");
            var bitmap = new BitmapImage();
            bitmap.BeginInit();
            bitmap.CacheOption = BitmapCacheOption.OnLoad;
            bitmap.StreamSource = mem;
            bitmap.EndInit();
            bitmap.Freeze();
            return bitmap;
        }

        private void AddLog(string msg)
        {
            string timeStr = DateTime.Now.ToString("HH:mm:ss");
            PlcLogs.Insert(0, $"[{timeStr}] {msg}");
            if (PlcLogs.Count > 60)
            {
                PlcLogs.RemoveAt(PlcLogs.Count - 1);
            }
        }
    }
}
