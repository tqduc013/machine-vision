# 🏭 HỒ SƠ DỰ ÁN THỰC CHIẾN: HỆ THỐNG KIỂM ĐỊNH ĐAI ỐC CÔNG NGHIỆP MVTEC AD (PC CONTROL & AI VISION)

> **Tác giả:** Trần Quang Đức — Kỹ sư Khoa học Máy tính (Computer Science), UTEHY  
> **Target ứng tuyển:** Kỹ sư R&D Machine Vision / PC Control (.NET WPF & AI Vision)  
> **Mục tiêu chiến lược:** Thuyết phục tuyệt đối các công ty tự động hóa & FDI (Sejong Dynamics, Hyundai Kefico, RTC, Luxshare, Foxconn).

---

## 📌 1. TỔNG QUAN BÀI TOÁN (PROBLEM STATEMENT)

Trong dây chuyền sản xuất cơ khí ô tô và linh kiện chính xác, đai ốc kim loại (**Metal Nut**) là chi tiết quan trọng liên kết khung gầm và động cơ. Các lỗi sản phẩm xuất hiện ngẫu nhiên gồm:
1. **Lỗi hình học (Geometry & Gauging):** Đường kính trong/ngoài sai lệch dung sai micrometer, thiếu lỗ ren.
2. **Lỗi biến dạng tai ốc (Bent / Deformed):** 4 tai kẹp bị cong vênh trong quá trình dập nguội, không thể bắt ngàm lắp ráp tự động.
3. **Lỗi lật mặt (Flipped Part):** Đai ốc bị cấp ngược mặt vào phễu rung (vát mép chamfer và ren bị đảo chiều).
4. **Lỗi ngoại quan bề mặt (Surface Scratch & Color Oxidation):** Bề mặt bị xước do ma sát cơ khí hoặc bị oxy hóa/đổi màu do nhiệt luyện không đạt chuẩn.

**Tập dữ liệu chuẩn quốc tế:** Bộ dữ liệu MVTec AD (`metal_nut`) gồm 20 mẫu chuẩn (`train_good`) và 75 mẫu kiểm thử thực tế thuộc 5 nhóm (`good`, `scratch`, `bent`, `color`, `flip`).

---

## 🛠️ 2. KIẾN TRÚC PHẦN MỀM C# .NET 8 WPF (PC CONTROL APP)

Hệ thống được phát triển theo tiêu chuẩn công nghiệp chạy 24/7 trên máy tính công nghiệp (IPC):

```
                       ┌──────────────────────────────────────────────────┐
                       │             MÁY TÍNH CÔNG NGHIỆP (IPC)           │
                       │   .NET 8 (LTS) - WPF Industrial Dark UI (XAML)   │
                       └────────────────────────┬─────────────────────────┘
                                                │
                 ┌──────────────────────────────┴──────────────────────────────┐
                 ▼                                                             ▼
   ┌───────────────────────────┐                                 ┌───────────────────────────┐
   │  MainViewModel (MVVM)     │                                 │ MetalNutInspector Engine  │
   │  • DispatcherTimer (1.2s) │ ── (Zero RAM Leak: Mat Memory) ─▶ • Guidance: Hough + Angle │
   │  • Yield Rate & Counters  │                                 │ • Gauging: Din / Dout     │
   │  • PLC TCP/IP Socket Logs │ ◀── (DTO: InspectionResult) ────│ • Inspection: Defects     │
   └─────────────┬─────────────┘                                 └───────────────────────────┘
                 │
                 ▼
   ┌─────────────────────────────────────────────────────────────┐
   │ GIAO TIẾP TẦNG DƯỚI (PLC HANDSHAKE SIMULATION)              │
   │ • Bit Y0 = 1: PASS -> Băng chuyền chuyển tiếp sản phẩm      │
   │ • Bit Y1 = 1: NG   -> Kích hoạt xi lanh khí nén gạt hàng lỗi │
   └─────────────────────────────────────────────────────────────┘
```

### Điểm nhấn kỹ thuật ăn điểm với nhà tuyển dụng (Key Highlights):
1. **Kiến trúc MVVM phân tầng sạch sẽ:** `Models` (DTO), `ViewModels` (Điều phối luồng dữ liệu & thống kê), `Views` (XAML Dark Mode công nghiệp), `VisionEngine` (OpenCvSharp thuần thuật toán).
2. **Quản lý bộ nhớ tuyệt đối (Zero Memory Leak):** Xử lý ảnh công nghiệp chạy liên tục hàng triệu frame mỗi ngày. Mọi đối tượng OpenCV `Mat` đều được giải phóng qua `using var Mat` và chuyển đổi sang `BitmapImage` bằng stream bộ nhớ đóng băng (`bitmap.Freeze()`), đảm bảo RAM IPC không bị tràn.
3. **Mô phỏng Bắt tay PLC (Industrial Handshake):** Đồng bộ hóa tín hiệu I/O thông qua thông điệp TCP/IP chuẩn: gửi bit PASS sang PLC hoặc bit NG để kích hoạt van xi lanh gạt hàng lỗi vào thùng NG.

---

## 🔬 3. QUY TRÌNH XỬ LÝ ẢNH 4G (THE 4G PIPELINE)

| Bước 4G | Thuật toán triển khai trong C# | Ý nghĩa công nghiệp |
| :--- | :--- | :--- |
| **1. Guidance (Định vị)** | `Cv2.HoughCircles` + `Cv2.MinAreaRect` | Xác định tọa độ tâm lỗ ren $(X_c, Y_c)$ và góc xoay $\theta$ của 4 tai ốc để căn chỉnh vị trí. |
| **2. Gauging (Đo đạc)** | Caliper đa điểm từ biên dạng `Contour` | Đo đường kính trong danh định $D_{\text{in}} \in [140.0, 182.0]\text{px}$ và đường kính ngoài $D_{\text{out}} \in [605.0, 658.0]\text{px}$. Sai số dung sai tính bằng pixel quy đổi sang micrometer ($\mu m$). |
| **3. Inspection (Soi lỗi)** | `Cv2.ConvexityDefects` + HSV Saturation + Directional Morphology | - Tai cong vênh: Độ sâu khuyết tật bao lồi $\text{DefectDepth} > 92\text{px}$.<br>- Ngược mặt: Bán kính ren vát trong $D_{\text{in}} > 182\text{px}$.<br>- Biến tính màu: Độ bão hòa Saturation trung bình.<br>- Trầy xước: Bộ lọc BlackHat với kernel góc $45^\circ$ và $135^\circ$ trong vành tròn ren. |
| **4. Performance** | C# SIMD & P/Invoke OpenCvSharp C++ Core | **Thời gian chu kỳ (Cycle Time): $\approx 20\text{ms}/\text{sản phẩm}$** (đáp ứng xuất sắc tốc độ băng chuyền nhà máy 2500 - 3000 sản phẩm/phút). |

---

## 🧠 4. BÀI HỌC CHUYÊN SÂU: RULE-BASED VS. AI ANOMALY DETECTION

Khi đối thoại kỹ thuật với Trưởng phòng R&D hoặc Kỹ sư Trưởng (Lead Vision Engineer), đây là luận điểm thể hiện tư duy kiến trúc sư hệ thống:

1. **Thế mạnh & Giới hạn của Rule-based (OpenCV):**
   - *Thế mạnh:* Cực kỳ nhanh ($< 20\text{ms}$), chuẩn xác $100\%$ cho bài toán định vị (Guidance) và đo kích thước (Gauging).
   - *Giới hạn:* Đai ốc kim loại có vân tiện cơ khí đồng tâm (lathe turning marks) và độ phản chiếu kim loại cao. Nếu chỉ dùng ngưỡng cố định (Fixed Thresholding) cho lỗi trầy xước vi mô hoặc đốm ố màu, hệ thống rule-based dễ bị nhiễu bởi phản xạ ánh sáng hoặc góc xoay của sản phẩm.
2. **Giải pháp AI PatchCore Anomaly Detection (One-Class Learning):**
   - Chỉ cần huấn luyện trên mẫu chuẩn OK (`train_good`), hệ thống tự động học phân phối đặc trưng chuẩn (Golden Feature Distribution) vào một **Memory Bank**.
   - Khi có bất kỳ dị tật bất thường nào (xước, mẻ, biến màu), khoảng cách vector sẽ đột biến vượt ngưỡng mà không cần phải dán nhãn hàng nghìn ảnh lỗi trước đó.
   - Sử dụng công thức ma trận vectorization: $\|A - B\|^2 = \|A\|^2 - 2AB^T + \|B\|^2$ để tăng tốc suy luận từ $66\text{s} \to 0.5\text{s}$.
3. **Kiến trúc Hybrid tối ưu trong Nhà máy Thông minh (Smart Factory Best Practice):**
   - **Tầng 1 (Rule-based OpenCvSharp - 5ms):** Cắt lọc hình học nhanh: Đo $D_{\text{in}}, D_{\text{out}}$, kiểm tra góc xoay và loại bỏ ngay sản phẩm cong vênh hoặc mất lỗ.
   - **Tầng 2 (AI PatchCore - 15ms):** Sau khi ảnh đã được bẻ thẳng và định tâm (Alignment & Guidance), trích xuất đặc trưng bề mặt đưa qua Memory Bank để phán quyết dị tật ngoại quan.

---

## 🚀 5. HƯỚNG DẪN KHỞI CHẠY HỆ THỐNG TRÊN MÁY TÍNH

1. **Chạy ứng dụng C# .NET 8 WPF PC Control (Giao diện điều khiển công nghiệp):**
   ```powershell
   # Chạy trực tiếp từ thư mục dự án
   & "$HOME\AppData\Local\Microsoft\dotnet\dotnet.exe" run --project src/PCControlApp/PCControlApp.csproj
   ```
   *Thao tác:* Bấm nút `[▶ BĂNG CHUYỀN TỰ ĐỘNG]` để xem hệ thống quét liên tục các sản phẩm thật từ MVTec AD, cập nhật biểu đồ Yield Rate và ghi log bắt tay PLC thời gian thực.

2. **Chạy bộ kiểm thử định lượng tự động (Benchmark Console C#):**
   ```powershell
   & "$HOME\AppData\Local\Microsoft\dotnet\dotnet.exe" run --project src/VisionBenchmark/VisionBenchmark.csproj
   ```

3. **Chạy đánh giá AI Anomaly Detection & Xuất biểu đồ ROC (Python):**
   ```powershell
   python src/06_mvtec_metal_nut_anomaly_benchmark.py
   ```
   *Kết quả:* Biểu đồ báo cáo trực quan 4 ô chất lượng cao được lưu tại `docs/mvtec_metal_nut_anomaly_benchmark.png`.
