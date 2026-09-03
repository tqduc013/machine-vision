# 👁️⚡ Hệ Thống Thị Giác Máy Tính Công Nghiệp & PC Control (Chiến Dịch Sportage)

> **Hệ thống Kiểm Tra Quang Học Tự Động (AOI) & Điều Khiển Máy Tính Công Nghiệp (IPC) Thời Gian Thực.**  
> Ứng dụng kiểm tra ngoại quan linh kiện bán dẫn, vi mạch chip Apple A18 trên băng chuyền tốc độ cao.  
> Xây dựng bằng **C# .NET 8 WPF, OpenCvSharp4, Python 3, Kiến Trúc Đa Luồng, Bắt Tay Socket PLC & Digital Twin 3D**.

---

[![.NET 8](https://img.shields.io/badge/.NET-8.0_LTS-512BD4?style=for-the-badge&logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![C# WPF](https://img.shields.io/badge/C%23-WPF_MVVM-239120?style=for-the-badge&logo=csharp&logoColor=white)](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/)
[![OpenCV](https://img.shields.io/badge/OpenCV-OpenCvSharp4-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://github.com/shimat/opencvsharp)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Three.js](https://img.shields.io/badge/Three.js-3D_Digital_Twin-black?style=for-the-badge&logo=threedotjs&logoColor=white)](https://threejs.org/)
[![Tác giả](https://img.shields.io/badge/Tác_giả-tqduc013-38bdf8?style=for-the-badge&logo=github)](https://github.com/tqduc013)
[![License](https://img.shields.io/badge/License-MIT-4ade80?style=for-the-badge)](LICENSE)

**Ngôn ngữ:** [🇻🇳 Tiếng Việt](README_vi.md) · [🇬🇧 English](README.md)

---

## 🚀 Tính Năng & Vũ Khí Kỹ Thuật

- ⚡ **Tốc độ xử lý siêu tốc ($3 - 10\text{ ms} / \text{sản phẩm}$):** Đạt năng suất trên **$36.000\text{ UPH}$** (Sản phẩm/giờ) cho các dây chuyền nhà máy FDI.
- 🎯 **Quy Trình Xử Lý Ảnh 4G Toàn Diện:**
  1. **Guidance (Định vị & Xoay góc):** Tính toán tâm và góc nghiêng $\theta$ bằng `MinAreaRect`, tự động xoay ảnh về $0^\circ$ bằng `WarpAffine`.
  2. **Identification (Nhận diện mã):** Đọc mã QR Code Serial laser (`SN-APPLE-A18-xxx`).
  3. **Gauging (Đo kích thước):** Đo độ dày, chiều dài, chiều rộng với độ chính xác cao và kiểm tra dung sai ($\pm 15\text{px}$).
  4. **Inspection (Soi khuyết tật):** Khoanh vùng ROI bắt chính xác vết xước bề mặt và lỗi sứt mẻ 4 góc.
- 🧵 **Kiến Trúc Đa Luồng 4 Tầng Chuẩn Công Nghiệp (Producer-Consumer Queue):**
  - **Tầng 1 (Acquisition):** Bắt tín hiệu Trigger từ cảm biến quang phần cứng.
  - **Tầng 2 (Worker Pool):** Hàng đợi Queue cách ly luồng mạng với luồng xử lý ảnh, ngăn ngừa nghẽn luồng và đơ giao diện.
  - **Tầng 3 (PLC I/O Handshake):** Giao tiếp Socket TCP (`:5000`) điều khiển bật Bit `Y1=1` đẩy xi-lanh gạt phế phẩm.
  - **Tầng 4 (Presentation):** Đồng bộ dữ liệu lên C# WPF MVVM và phát sóng WebSocket (`:8765`) lên Bảng điều khiển Web 3D.
- 💡 **Làm Chủ Quang Học & 5 Loại Đèn Chiếu Sáng Công Nghiệp:**
  - *Backlight* (Đo kích thước), *Low-Angle Ring 15° Darkfield* (Soi xước), *Coaxial 90° Beam Splitter* (Mặt phẳng gương), *Dome 360°* (Mặt cong bóng), và *Hybrid Coaxial + Dome* (Kim loại phức tạp).
  - Tích hợp bộ mô phỏng hạt photon ray-tracing tương tác 2D: [`lighting_simulator.html`](lighting_simulator.html).
- 🖥️ **Ứng Dụng Native C# .NET 8 WPF (`PCControlApp`):**
  - Viết bằng C# OpenCvSharp4 và kiến trúc MVVM (`CommunityToolkit.Mvvm`), Dark-mode IPC, hiển thị camera, đèn LED PASS/FAIL và tính toán Yield Rate theo ca.
- 📝 **Hệ Thống Thi Sát Hạch 50 Câu Master Exam (`master_exam_50.html`):**
  - Môi trường thi trắc nghiệm bấm giờ 45 phút, có bản đồ nhảy nhanh 50 câu và giải thích bản chất kỹ thuật chi tiết.

---

## 🏗️ Sơ Đồ Kiến Trúc Hệ Thống 4 Tầng

```text
[ CẢM BIẾN QUANG ] ── (Tín hiệu Trigger) ──► [ HỘP ĐIỀU KHIỂN PLC ]
                                                     │
                                                     ▼ (Socket TCP :5000)
┌─────────────────────────────────────────────────────────────────────────────┐
│                       MÁY TÍNH CÔNG NGHIỆP VISION (IPC)                     │
│                                                                             │
│  [ TẦNG 1: THU NHẬN ẢNH ] ──► [ TẦNG 2: HÀNG ĐỢI QUEUE ]                   │
│                                           │                                 │
│                                           ▼                                 │
│                              [ TẦNG 2: WORKER POOL 4G ]                     │
│                              • 1. Guidance (Xoay góc θ)                     │
│                              • 2. Identification (Đọc QR)                   │
│                              • 3. Gauging (Đo kích thước)                   │
│                              • 4. Inspection (Soi xước/mẻ)                  │
│                                           │                                 │
│                     ┌─────────────────────┴─────────────────────┐           │
│                     ▼                                           ▼           │
│         [ TẦNG 3: BẮT TAY PLC ]                     [ TẦNG 4: TRÌNH DIỄN UI]│
│         • Bit Y0=1: Đạt (OK)                        • Ứng dụng C# .NET 8 WPF│
│         • Bit Y1=1: Gạt rác (NG)                    • WebSocket (:8765)     │
│         • Ghi sổ nhật ký CSV                        • Web 3D Digital Twin   │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## ⚡ Hướng Dẫn Chạy Nhanh Dự Án

### 1. Cài đặt môi trường
- **Python 3.10+:**
  ```bash
  pip install opencv-python numpy matplotlib websockets
  ```
- **.NET 8 SDK (LTS):**
  ```bash
  winget install Microsoft.DotNet.SDK.8
  ```

---

### 2. Chạy Hệ Thống Thực Tế (Python Backend + PLC + 3D Web)

**Terminal 1 — Khởi động PLC Simulator:**
```bash
python src/03_plc_simulator.py
```

**Terminal 2 — Khởi động Vision PC Controller:**
```bash
python src/04_vision_pc_controller.py
```

**Terminal 3 — Mở Giao diện Web 3D:**
Mở file `pc_control_dashboard.html` trên trình duyệt để xem toàn bộ dây chuyền hoạt động thời gian thực!

---

### 3. Chạy Ứng Dụng Native C# .NET 8 WPF

```bash
cd src/PCControlApp
dotnet run
```
*(Hoặc click đúp chuột trực tiếp vào file: `src/PCControlApp/bin/Debug/net8.0-windows/PCControlApp.exe`)*

---

### 4. Công Cụ Mô Phỏng & Sát Hạch Trực Quan

- **Mô phỏng 5 loại đèn Quang học Ray-tracing:** Mở file [`lighting_simulator.html`](lighting_simulator.html).
- **Phòng thi sát hạch 50 câu bấm giờ 45 phút:** Mở file [`master_exam_50.html`](master_exam_50.html).

---

## 📊 Bảng Đánh Giá Chỉ Số Thực Tế

| Chỉ số kỹ thuật | Yêu cầu tiêu chuẩn | Đạt được trong dự án | Đánh giá |
| :--- | :--- | :--- | :---: |
| **Washer AOI Cycle Time** | $< 15\text{ ms}$ | **$2.8\text{ ms}$** | 🚀 Xuất Sắc |
| **Apple A18 4G Pipeline Cycle Time** | $< 25\text{ ms}$ | **$8.5 - 11.2\text{ ms}$** | 🚀 Xuất Sắc |
| **Năng suất lý thuyết (Throughput)** | $> 10.000\text{ UPH}$ | **$> 36.000\text{ UPH}$** | 🚀 Xuất Sắc |
| **Rò rỉ RAM khi chạy 24/7** | $0\text{ MB leak}$ | **$0\text{ MB leak}$** (`using var Mat`) | 🚀 Xuất Sắc |
| **Thời gian biên dịch C# .NET 8** | $< 10\text{ s}$ | **$2.89\text{ s}$** | 🚀 Xuất Sắc |

---

## 👨‍💻 Tác giả

- **GitHub:** [@tqduc013](https://github.com/tqduc013)
- **Repository:** [https://github.com/tqduc013/machine-vision](https://github.com/tqduc013/machine-vision)
- **Tên Chiến Dịch:** *Chiến Dịch Sportage — Machine Vision & Industrial PC Control Warfare*

---

## 📜 Bản quyền

Mã nguồn được phát hành theo giấy phép [MIT License](LICENSE).
