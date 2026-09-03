using System;
using System.Collections.ObjectModel;
using System.IO;
using System.Threading.Tasks;
using System.Windows.Media.Imaging;
using System.Windows.Threading;
using CommunityToolkit.Mvvm.ComponentModel;
using CommunityToolkit.Mvvm.Input;
using PCControlApp.Models;
using PCControlApp.VisionEngine;

namespace PCControlApp.ViewModels
{
    /// <summary>
    /// BỘ NÃO ĐIỀU PHỐI (VIEWMODEL) THEO KIẾN TRÚC MVVM
    /// Tách biệt hoàn toàn Logic xử lý và Giao diện hiển thị
    /// </summary>
    public partial class MainViewModel : ObservableObject
    {
        private readonly ChipInspector _inspector;
        private readonly string[] _sampleImagePaths;
        private int _sampleIndex = 0;
        private int _currentProductId = 100;
        private readonly DispatcherTimer _autoRunTimer;

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
        private string _yieldRateColor = "#22C55E";

        [ObservableProperty]
        private bool _isAutoRunning = false;

        [ObservableProperty]
        private string _autoRunButtonText = "▶ BĂNG CHUYỀN TỰ ĐỘNG";

        [ObservableProperty]
        private BitmapImage _displayImage;

        [ObservableProperty]
        private string _statusLog = "Sẵn sàng hoạt động (Ready). Chờ lệnh Trigger...";

        public ObservableCollection<string> PlcLogs { get; } = new ObservableCollection<string>();

        public MainViewModel()
        {
            _inspector = new ChipInspector();

            // Tìm các ảnh mẫu trong thư mục samples_chip
            string baseDir = AppDomain.CurrentDomain.BaseDirectory;
            string projectRoot = Path.GetFullPath(Path.Combine(baseDir, "..", "..", "..", "..", ".."));
            string sampleDir = Path.Combine(projectRoot, "samples_chip");

            if (Directory.Exists(sampleDir))
            {
                _sampleImagePaths = Directory.GetFiles(sampleDir, "*.png");
            }
            else
            {
                _sampleImagePaths = Array.Empty<string>();
            }

            _currentResult = new InspectionResult
            {
                ProductId = 100,
                IsOk = true,
                SerialNumber = "SN-APPLE-A18-PRO-INITIAL",
                Width = 220.0,
                Height = 140.0,
                Angle = 0.0,
                CycleTimeMs = 0.0
            };

            _autoRunTimer = new DispatcherTimer
            {
                Interval = TimeSpan.FromMilliseconds(1600)
            };
            _autoRunTimer.Tick += (s, e) => TriggerInspection();

            AddLog("Hệ thống Vision PC Control C# .NET 8 khởi động thành công!");
            AddLog("Worker Pool OpenCvSharp sẵn sàng xử lý 4G Pipeline.");

            // Tải ảnh đầu tiên lên màn hình
            if (_sampleImagePaths.Length > 0)
            {
                LoadImageToDisplay(_sampleImagePaths[0]);
            }
        }

        [RelayCommand]
        public void TriggerInspection()
        {
            if (_sampleImagePaths == null || _sampleImagePaths.Length == 0)
            {
                AddLog("⚠️ Không tìm thấy ảnh mẫu trong thư mục samples_chip!");
                return;
            }

            _currentProductId++;
            string imgPath = _sampleImagePaths[_sampleIndex];
            _sampleIndex = (_sampleIndex + 1) % _sampleImagePaths.Length;

            // Xử lý ảnh 4G ngầm
            var res = _inspector.Inspect(imgPath, _currentProductId);
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
            YieldRateColor = rate >= 95.0 ? "#22C55E" : "#EF4444";

            // Hiển thị ảnh
            LoadImageToDisplay(imgPath);

            // Log PLC Handshake
            string statusStr = res.IsOk ? "OK -> [BIT Y0=1]" : $"NG ({res.DefectReason}) -> [BIT Y1=1 GẠT PHẾ PHẨM]";
            AddLog($"[TRIGGER #{res.ProductId}] 4G ({res.CycleTimeMs:F2}ms) -> {statusStr}");
        }

        [RelayCommand]
        public void ToggleAutoRun()
        {
            IsAutoRunning = !IsAutoRunning;
            if (IsAutoRunning)
            {
                AutoRunButtonText = "⏸ DỪNG BĂNG CHUYỀN";
                AddLog("▶ BĂNG CHUYỀN TỰ ĐỘNG BẮT ĐẦU CHẠY (Chu kỳ 1.6s)...");
                TriggerInspection();
                _autoRunTimer.Start();
            }
            else
            {
                AutoRunButtonText = "▶ BĂNG CHUYỀN TỰ ĐỘNG";
                _autoRunTimer.Stop();
                AddLog("⏸ Băng chuyền đã tạm dừng.");
            }
        }

        [RelayCommand]
        public void ResetStats()
        {
            TotalCount = 0;
            OkCount = 0;
            NgCount = 0;
            YieldRate = "100.0%";
            YieldRateColor = "#22C55E";
            PlcLogs.Clear();
            AddLog("🔄 Đã Reset toàn bộ bộ đếm ca sản xuất về 0.");
        }

        private void LoadImageToDisplay(string path)
        {
            try
            {
                var bitmap = new BitmapImage();
                bitmap.BeginInit();
                bitmap.CacheOption = BitmapCacheOption.OnLoad;
                bitmap.UriSource = new Uri(path);
                bitmap.EndInit();
                bitmap.Freeze();
                DisplayImage = bitmap;
            }
            catch
            {
                // Bỏ qua lỗi load ảnh giao diện
            }
        }

        private void AddLog(string msg)
        {
            string timeStr = DateTime.Now.ToString("HH:mm:ss");
            PlcLogs.Insert(0, $"[{timeStr}] {msg}");
            if (PlcLogs.Count > 50)
            {
                PlcLogs.RemoveAt(PlcLogs.Count - 1);
            }
        }
    }
}
