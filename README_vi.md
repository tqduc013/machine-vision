# Hệ Thống Thị Giác Máy Tính & PC Control (Machine Vision & PC Control)

Dự án nghiên cứu và mô phỏng hệ thống Kiểm tra Quang học Tự động (AOI) kết hợp giao diện điều khiển máy tính công nghiệp (PC Control), xây dựng bằng **C# (.NET 8 WPF, OpenCvSharp4, ONNX Runtime)** và **Python (OpenCV, NumPy)**.

**Ngôn ngữ:** [English](README.md) | [Tiếng Việt](README_vi.md)

---

## Tổng Quan Dự Án

Repository này bao gồm mã nguồn thực nghiệm và bộ kiểm thử hiệu năng cho các bài toán xử lý ảnh công nghiệp:

- **Quy trình Xử lý ảnh 4G (Classical Computer Vision):**
  - **Guidance (Định vị):** Xác định tâm và góc xoay sản phẩm (`MinAreaRect`, `HoughCircles`, `WarpAffine`).
  - **Identification (Nhận diện):** Giải mã QR Code / DataMatrix trên linh kiện.
  - **Gauging (Đo đạc):** Đo đường kính trong/ngoài và kiểm tra dung sai kích thước.
  - **Inspection (Kiểm tra lỗi):** Phát hiện vết xước bề mặt, sứt mẻ góc và biến dạng hình học.
- **Phát hiện Bất thường bằng AI (PatchCore Anomaly Detection + ONNX):**
  - Trích xuất đặc trưng ảnh qua mạng CNN và đối chiếu với kho mẫu chuẩn (Memory Bank) trên tập dữ liệu `MVTec AD Metal Nut` và `DeepPCB`.
  - Tính toán khoảng cách vector ma trận tạo bản đồ nhiệt (Heatmap) khoanh vùng vị trí lỗi.
- **Ứng dụng Điều khiển C# WPF (`src/PCControlApp`):**
  - Giao diện desktop viết bằng C# .NET 8 WPF theo mô hình MVVM.
  - Hiển thị luồng kiểm tra ảnh, phán quyết `OK` / `NG`, thống kê tỉ lệ đạt (Yield Rate) và giả lập giao tiếp TCP/IP với PLC.
- **Kiểm thử Chịu tải & Bộ nhớ (`src/VisionBenchmark`):**
  - Chạy kiểm thử liên tục 2.000 chu kỳ để đo độ trễ (Latency) và kiểm chứng việc giải phóng bộ nhớ OpenCV `Mat` không gây rò rỉ RAM.

---

## Cấu Trúc Thư Mục

```text
Machine-Vision/
├── datasets/                  # Dữ liệu mẫu (MVTec AD Metal Nut & DeepPCB)
├── docs/                      # Tài liệu phân tích kỹ thuật & báo cáo benchmark
│   ├── MVTEC_METAL_NUT_CASE_STUDY.md
│   ├── STRESS_TEST_REPORT.md
│   └── mvtec_metal_nut_anomaly_benchmark.png
├── models/                    # Mô hình ONNX & dữ liệu Memory Bank
├── notebooks/                 # Jupyter Notebook thử nghiệm thuật toán
│   └── 05_ai_anomaly_detection_lab.ipynb
├── src/
│   ├── PCControlApp/          # Ứng dụng C# .NET 8 WPF PC Control
│   ├── VisionBenchmark/       # Công cụ benchmark hiệu năng & bộ nhớ (2.000 chu kỳ)
│   ├── 01_defect_and_dimension_inspector.py
│   ├── 02_full_4g_pipeline_inspector.py
│   ├── 03_plc_simulator.py
│   ├── 04_vision_pc_controller.py
│   ├── 05_ai_anomaly_detector_interactive.py
│   └── 06_mvtec_metal_nut_anomaly_benchmark.py
├── LICENSE
└── README.md
```

---

## Hướng Dẫn Chạy Dự Án

### Yêu cầu môi trường

- **.NET 8.0 SDK** (để chạy ứng dụng C# WPF và bộ công cụ Benchmark)
- **Python 3.10+** (để chạy các script thử nghiệm thuật toán)
  ```bash
  pip install opencv-python numpy matplotlib websockets
  ```

### 1. Chạy ứng dụng C# WPF PC Control

```bash
dotnet run --project src/PCControlApp/PCControlApp.csproj
```

### 2. Chạy kiểm thử chịu tải 2.000 chu kỳ (Benchmark)

```bash
dotnet run --project src/VisionBenchmark/VisionBenchmark.csproj
```

### 3. Chạy các script Python và giả lập PLC

```bash
# Terminal 1: Khởi động giả lập PLC qua cổng TCP (:5000)
python src/03_plc_simulator.py

# Terminal 2: Chạy bộ điều khiển xử lý ảnh Python
python src/04_vision_pc_controller.py
```

---

## Kết Quả Đo Kiểm Hiệu Năng (MVTec AD Metal Nut)

Kết quả thực nghiệm qua 2.000 chu kỳ kiểm tra liên tiếp (chi tiết tại [`docs/STRESS_TEST_REPORT.md`](docs/STRESS_TEST_REPORT.md)):

| Chỉ số | Kết quả đo được | Ghi chú |
| :--- | :--- | :--- |
| **Tổng số chu kỳ** | 2.000 chu kỳ | Hoàn thành trong 61.98 giây |
| **Thông lượng (Throughput)** | 32.3 FPS (~1.936 PPM) | Chạy trực tiếp trên CPU |
| **Thời gian xử lý trung bình** | 30.96 ms / ảnh | Bao gồm toàn bộ quy trình xử lý |
| **Độ trễ P99** | 41.50 ms | Đảm bảo đồng bộ tín hiệu PLC |
| **Mức tiêu thụ RAM** | Ổn định ở ~59.5 MB | Không rò rỉ bộ nhớ (Zero Memory Leak) |

---

## Giấy Phép

Dự án được phát hành theo giấy phép [MIT License](LICENSE).
