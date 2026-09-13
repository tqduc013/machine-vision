using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using Microsoft.ML.OnnxRuntime;
using Microsoft.ML.OnnxRuntime.Tensors;
using OpenCvSharp;
using PCControlApp.Models;

namespace PCControlApp.VisionEngine
{
    /// <summary>
    /// BỘ NÃO AI DEEP LEARNING ANOMALY DETECTION (ONNX RUNTIME)
    /// Triển khai thuật toán PatchCore Memory Bank SOTA hoàn toàn trong C# .NET 8:
    /// 1. Trích xuất đặc trưng đa tầng qua mạng Convolutional ONNX (256x256 -> 64x32x32)
    /// 2. So khớp vector L2 Normalized với Golden Memory Bank
    /// 3. Tạo bản đồ nhiệt khuyết tật (Anomaly Heatmap Colormap JET)
    /// 4. Phán quyết phân loại bất thường không cần mẫu lỗi (One-Class Learning)
    /// </summary>
    public class OnnxAnomalyInspector : IDisposable
    {
        private readonly InferenceSession? _session;
        private readonly float[] _memoryBank;
        private readonly int _bankCount = 0;
        private readonly int _featureDim = 64;
        private readonly double _anomalyThreshold = 0.645;
        private readonly bool _isLoaded = false;

        public bool IsLoaded => _isLoaded;
        public double Threshold => _anomalyThreshold;

        public OnnxAnomalyInspector()
        {
            try
            {
                string baseDir = AppDomain.CurrentDomain.BaseDirectory;
                string projectRoot = Path.GetFullPath(Path.Combine(baseDir, "..", "..", "..", "..", ".."));
                string modelsDir = Path.Combine(projectRoot, "models");

                if (!Directory.Exists(modelsDir))
                {
                    modelsDir = Path.Combine(Directory.GetCurrentDirectory(), "models");
                }
                if (!Directory.Exists(modelsDir))
                {
                    modelsDir = @"d:\Projects\Machine-Vision\models";
                }

                string onnxPath = Path.Combine(modelsDir, "patchcore_net.onnx");
                string bankPath = Path.Combine(modelsDir, "memory_bank.bin");

                if (File.Exists(onnxPath) && File.Exists(bankPath))
                {
                    var options = new SessionOptions();
                    options.IntraOpNumThreads = Environment.ProcessorCount;
                    _session = new InferenceSession(onnxPath, options);

                    byte[] bytes = File.ReadAllBytes(bankPath);
                    _bankCount = bytes.Length / (_featureDim * sizeof(float));
                    _memoryBank = new float[_bankCount * _featureDim];
                    Buffer.BlockCopy(bytes, 0, _memoryBank, 0, bytes.Length);

                    _isLoaded = true;
                }
                else
                {
                    _memoryBank = Array.Empty<float>();
                }
            }
            catch
            {
                _memoryBank = Array.Empty<float>();
                _isLoaded = false;
            }
        }

        /// <summary>
        /// Thực thi phán quyết AI Anomaly Detection trên một ảnh sản phẩm
        /// </summary>
        public InspectionResult Inspect(string imagePath, int productId, out Mat annotatedMat)
        {
            var sw = Stopwatch.StartNew();

            using var src = Cv2.ImRead(imagePath, ImreadModes.Color);
            if (src.Empty() || !_isLoaded || _session == null)
            {
                annotatedMat = new Mat(700, 700, MatType.CV_8UC3, Scalar.Black);
                return new InspectionResult
                {
                    ProductId = productId,
                    PartType = "MVTec Metal Nut",
                    Mode = "AI Deep Learning (ONNX)",
                    IsOk = false,
                    DefectReason = _isLoaded ? "Image Empty" : "ONNX Model Not Found",
                    CycleTimeMs = sw.Elapsed.TotalMilliseconds
                };
            }

            int origW = src.Width;
            int origH = src.Height;

            // 1. Tiền xử lý ảnh theo chuẩn Deep Learning: RGB, Resize 256x256, ImageNet Normalization
            using var rgb = new Mat();
            Cv2.CvtColor(src, rgb, ColorConversionCodes.BGR2RGB);

            using var resized = new Mat();
            Cv2.Resize(rgb, resized, new Size(256, 256));

            var inputTensor = new DenseTensor<float>(new[] { 1, 3, 256, 256 });
            float[] mean = { 0.485f, 0.456f, 0.406f };
            float[] std = { 0.229f, 0.224f, 0.225f };

            for (int y = 0; y < 256; y++)
            {
                for (int x = 0; x < 256; x++)
                {
                    Vec3b pixel = resized.At<Vec3b>(y, x);
                    inputTensor[0, 0, y, x] = ((pixel.Item0 / 255.0f) - mean[0]) / std[0]; // R
                    inputTensor[0, 1, y, x] = ((pixel.Item1 / 255.0f) - mean[1]) / std[1]; // G
                    inputTensor[0, 2, y, x] = ((pixel.Item2 / 255.0f) - mean[2]) / std[2]; // B
                }
            }

            // 2. Chạy suy luận mạng nơ-ron qua Microsoft.ML.OnnxRuntime
            var inputs = new List<NamedOnnxValue>
            {
                NamedOnnxValue.CreateFromTensor("input", inputTensor)
            };

            using var runResults = _session.Run(inputs);
            var outputTensor = runResults.First().AsTensor<float>(); // Shape: [1, 64, 32, 32]

            // 3. Tính toán ma trận khoảng cách Euclid tới Memory Bank
            int gridSize = 32;
            int numPatches = gridSize * gridSize; // 1024 patches
            float[,] patchDistances = new float[gridSize, gridSize];
            List<float> allPatchScores = new List<float>(numPatches);

            float[] currentVec = new float[_featureDim];

            for (int py = 0; py < gridSize; py++)
            {
                for (int px = 0; px < gridSize; px++)
                {
                    // Lấy vector 64 chiều tại ô (py, px)
                    float sumSq = 0.0f;
                    for (int c = 0; c < _featureDim; c++)
                    {
                        float v = outputTensor[0, c, py, px];
                        currentVec[c] = v;
                        sumSq += v * v;
                    }

                    // L2 Normalization
                    float norm = MathF.Sqrt(sumSq) + 1e-7f;
                    for (int c = 0; c < _featureDim; c++)
                    {
                        currentVec[c] /= norm;
                    }

                    // Tìm khoảng cách nhỏ nhất tới bất kỳ vector nào trong Memory Bank
                    // ||u - v||^2 = ||u||^2 - 2(u.v) + ||v||^2 = 2 - 2(u.v)
                    float maxDot = -1.0f;
                    int bankOffset = 0;
                    for (int b = 0; b < _bankCount; b++)
                    {
                        float dot = 0.0f;
                        for (int c = 0; c < _featureDim; c++)
                        {
                            dot += currentVec[c] * _memoryBank[bankOffset + c];
                        }
                        if (dot > maxDot) maxDot = dot;
                        bankOffset += _featureDim;
                    }

                    float dist = MathF.Sqrt(MathF.Max(2.0f - 2.0f * maxDot, 0.0f));
                    patchDistances[py, px] = dist;
                    allPatchScores.Add(dist);
                }
            }

            // 4. Tính toán Anomaly Score toàn bức ảnh (Top 3% khoảng cách dị tật lớn nhất)
            allPatchScores.Sort();
            int topK = Math.Max(1, (int)(numPatches * 0.03));
            double anomalyScore = 0.0;
            for (int i = numPatches - topK; i < numPatches; i++)
            {
                anomalyScore += allPatchScores[i];
            }
            anomalyScore /= topK;

            // 5. Tạo bản đồ nhiệt trực quan (Anomaly Heatmap Colormap JET)
            using var heatMatSmall = new Mat(gridSize, gridSize, MatType.CV_8UC1);
            float minD = allPatchScores[0];
            float maxD = allPatchScores[numPatches - 1];
            float range = (maxD - minD) > 1e-5f ? (maxD - minD) : 1.0f;

            for (int py = 0; py < gridSize; py++)
            {
                for (int px = 0; px < gridSize; px++)
                {
                    float normalized = (patchDistances[py, px] - minD) / range;
                    byte pixelVal = (byte)Math.Clamp((int)(normalized * 255.0f), 0, 255);
                    heatMatSmall.Set(py, px, pixelVal);
                }
            }

            // 5. Tạo bản đồ nhiệt trực quan tinh tế (Chỉ phủ màu trên thân đai ốc, không làm bẩn nền đen)
            using var grayNut = new Mat();
            Cv2.CvtColor(src, grayNut, ColorConversionCodes.BGR2GRAY);
            using var nutMask = new Mat();
            Cv2.Threshold(grayNut, nutMask, 25, 255, ThresholdTypes.Binary);

            using var heatMatFull = new Mat();
            Cv2.Resize(heatMatSmall, heatMatFull, new Size(origW, origH), 0, 0, InterpolationFlags.Cubic);

            using var heatMasked = new Mat();
            Cv2.BitwiseAnd(heatMatFull, nutMask, heatMasked);

            using var heatColor = new Mat();
            Cv2.ApplyColorMap(heatMasked, heatColor, ColormapTypes.Jet);

            annotatedMat = src.Clone();
            // Trộn màu nhẹ nhàng (30%) chỉ trên vùng thân đai ốc
            Cv2.AddWeighted(src, 0.70, heatColor, 0.30, 0, annotatedMat);

            // Giữ nền đen nguyên bản trong trẻo
            using var invMask = new Mat();
            Cv2.BitwiseNot(nutMask, invMask);
            src.CopyTo(annotatedMat, invMask);

            // 6. Phán quyết phân loại
            bool isOk = anomalyScore < _anomalyThreshold;
            string defectType = isOk ? "None" : "Surface Anomaly (AI)";
            string defectReason = isOk ? "PASSED" : $"NG: Di tat AI vuot nguong (Score={anomalyScore:F3} > {_anomalyThreshold:F3})";

            sw.Stop();

            return new InspectionResult
            {
                ProductId = productId,
                PartType = "MVTec Metal Nut",
                SerialNumber = $"AI-NUT-{productId:D4}",
                Mode = "AI Deep Learning (ONNX)",
                IsOk = isOk,
                DefectType = defectType,
                DefectReason = defectReason,
                AnomalyScore = anomalyScore,
                CycleTimeMs = sw.Elapsed.TotalMilliseconds
            };
        }

        public void Dispose()
        {
            _session?.Dispose();
        }
    }
}
