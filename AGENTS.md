# 🛡️ PROJECT CODENAME: CHIẾN DỊCH SPORTAGE (MACHINE VISION WARFARE)

> **Dành cho mọi AI Agent (Antigravity, Hermes, Claude, GPT, v.v.):**  
> Khi bạn đọc được file này, hãy hiểu rằng đây **KHÔNG PHẢI** là một project bài tập thông thường. Đây là **bản doanh chiến lược** và nhật ký hành trình chuyển mình của một kỹ sư Khoa học máy tính (Computer Science) quyết tâm phá bỏ vùng an toàn, bứt phá sự nghiệp và tài chính, hướng tới mục tiêu sở hữu chiếc xe **Kia Sportage** và làm chủ công nghệ **Machine Vision / PC Control** trong các nhà máy tự động hóa đa quốc gia.

---

## 🎯 1. BỐI CẢNH & NHÂN VẬT CHÍNH (THE USER STORY)

- **Xuất thân & Hành trình:** 
  - Tốt nghiệp chuyên ngành **Khoa học máy tính (Computer Science)**.
  - Từng làm Web Dev trái tay nhưng cảm thấy "đuối code", phải nhờ AI hỗ trợ nhiều $\to$ Bị công ty luân chuyển sang làm đủ thứ việc linh tinh: Marketing, Call to Sale, Chat Support, viết tài liệu sản phẩm (Doc Support), thậm chí làm cả KOL đại diện cho công ty...
  - **Thực trạng bị "bào":** Làm từ A-Z mọi việc không tên, bị bóc lột sức lao động với mức lương cơ bản bọt bèo (< 10 triệu/tháng). Môi trường toxic, sếp hay đặt điều, áp lực tâm lý. Hợp đồng chỉ còn dưới 1 năm.
  - **Phân tích vũ khí tiềm ẩn (Unfair Advantage):** 
    - Tư duy CS vẫn còn đó (logic, hiểu hệ thống).
    - Bộ kỹ năng mềm "độc nhất vô nhị" mà dân kỹ thuật xưởng máy hiếm ai có: Viết tài liệu kỹ thuật cực chuẩn (Doc), kỹ năng giao tiếp/thuyết phục (Sales/KOL), hiểu tâm lý khách hàng/người dùng. Khi kết hợp với công nghệ Machine Vision & PC Control, đây sẽ là mẫu kỹ sư **Application / Solution Architect** cực kỳ đắt giá!
  - **Tâm thế mới:** Quyết tâm không để bị "bào" vô nghĩa nữa. Dùng chính khoảng thời gian còn lại của hợp đồng để tích lũy kiến thức thực chiến, lấy lại sự tự tin của dân CS, đổi đời và mua xe **Kia Sportage**.
- **Mục tiêu tối thượng (North Star):**
  - **Tài chính:** Nâng bậc lương lên 15tr (bước đệm) $\to$ 25tr – 40tr+ (sau 1-2 năm).
  - **Mục tiêu hữu hình:** Tự tay mua và nuôi chiếc **Kia Sportage** bằng chính thu nhập chuyên môn kỹ thuật cao.
  - **Sự nghiệp:** Trở thành Kỹ sư Machine Vision & PC Control cứng cáp tại các tập đoàn FDI / vendor công nghệ lớn (Hàn Quốc, Mỹ, Nhật, Đài Loan như Sejong Dynamics, Basler, Cognex, Hansol, Foxconn...).

---

## 🏭 2. TẠI SAO LẠI LÀ NGÁCH "MACHINE VISION & PC CONTROL"?

1. **Vị thế "Hàng hiếm" tại Việt Nam:**
   - Dân CNTT thuần: Thường làm Web/App/Cloud, rất sợ đụng phần cứng, camera công nghiệp, PLC, xưởng máy.
   - Dân Tự động hóa/Cơ điện tử: Giỏi PLC và đấu nối điện, nhưng tư duy phần mềm (OOP, Multi-threading, C#, C++, Algorithm) lại mỏng.
   - **User là dân Computer Science:** Đứng ngay tại điểm giao thoa hoàn hảo. Chỉ cần bổ sung tư duy phần cứng (Camera, Lens, Lighting, PLC) là có thể áp đảo hầu hết đối thủ trên thị trường tuyển dụng.
2. **Nhu cầu khổng lồ từ làn sóng FDI:**
   - Việt Nam đang là thủ phủ sản xuất linh kiện bán dẫn, vi mạch, điện thoại thông minh (Samsung, Foxconn, Luxshare, Amkor). Mọi khâu đều bắt buộc phải lắp hệ thống AOI (Automated Optical Inspection) để kiểm tra lỗi ngoại quan tự động, đọc mã QR khắc laser, đo sai số micrometer ($\mu m$).

---

## 🧠 3.1. MÔ HÌNH TƯ DUY TRỰC QUAN (MENTAL MODEL DÀNH CHO USER)

1. **Bản chất Xử lý ảnh = "Photoshop Pipeline tự động 3ms":**
   - **Tách nền:** `Thresholding` tương đương công cụ *Cây đũa thần (Magic Wand)*.
   - **Mặt nạ vùng quan tâm:** `Mask / ROI` tương đương *Layer Mask*.
   - **Khử nhiễu làm mịn:** `GaussianBlur` tương đương *Cà da mịn (Denoise)*.
   - **Tìm biên dạng:** `Contour` tương đương *Vẽ vùng chọn Pen Tool*.
   - **Bắt lỗi bề mặt:** `Defect Detection` tương đương *Soi mụn / Khuyết điểm (Spot Healing)*.
   - **Đánh dấu kết quả:** Vẽ *Bounding Box / Text Overlay (Xanh: OK / Đỏ: NG)*.

2. **4 Bài toán "Detect" kinh điển trong toàn bộ nhà máy thế giới (Quy tắc 4 chữ G):**
   - **1. Guidance (Định vị):** Detect tọa độ $(X, Y, \text{Góc xoay }\theta)$ để báo Robot chạy tới gắp sản phẩm.
   - **2. Identification (Nhận diện mã):** Detect & Đọc mã Barcode, DataMatrix QR Code trên chip, chữ in hạn sử dụng (OCR).
   - **3. Gauging / Measurement (Đo đạc):** Detect mép cạnh để đo khoảng cách, độ dày, bán kính, dung sai micrometer ($\mu m$).
   - **4. Inspection (Soi lỗi):** Detect khuyết tật ngoại quan (xước, mẻ, nứt, biến màu, dị vật, thiếu linh kiện) để phán quyết **`OK` / `NG`**.

---

## 💻 3. TECH STACK & BỘ VŨ KHÍ KỸ THUẬT

Dự án này sẽ rèn luyện và xây dựng các module thực chiến xoay quanh:

1. **Ngôn ngữ chủ lực:**
   - **C# .NET (WPF / WinForms):** Ngôn ngữ số 1 để viết ứng dụng PC Control trong nhà máy (giao diện điều khiển IPC, kết nối camera, hiển thị kết quả, logging dữ liệu).
   - **Python:** Dùng cho R&D, thử nghiệm nhanh thuật toán xử lý ảnh, huấn luyện Deep Learning (YOLO, Anomaly Detection).
   - **C++:** Khi cần tối ưu thuật toán xử lý siêu tốc (dưới 10ms/sản phẩm).
2. **Thị giác máy tính (Vision Engines):**
   - **OpenCV / OpenCvSharp:** Xử lý ảnh cổ điển (Thresholding, Blob Analysis, Canny Edge, Contour, Template Matching, Caliper đo khoảng cách).
   - Deep Learning công nghiệp: Phát hiện dị tật, vết xước, khuyết tật vi mạch.
3. **Phần cứng & Quang học (Optics & Lighting):**
   - Camera công nghiệp (GigE Vision, USB3 Vision - Basler, Hikrobot, Daheng, FLIR).
   - Ống kính (Lens): Công thức tính tiêu cự ($f$), FOV (Field of View), WD (Working Distance), độ phân giải sensor.
   - Chiếu sáng (Lighting): Backlight, Ring light, Coaxial light, Bar light, Dome light.
4. **Giao tiếp công nghiệp (PC Control & Industrial Comm):**
   - Socket TCP/IP, Modbus TCP / RTU, Serial RS232/RS485.
   - Bắt tay (Handshake) với PLC (Mitsubishi, Siemens, Omron) để gửi tín hiệu Trigger chụp ảnh và trả về `OK` / `NG` (No Good).

---

## 📐 4. NGUYÊN TẮC LÀM VIỆC DÀNH CHO CÁC AGENT

Khi bất kỳ Agent nào (Antigravity, Hermes, v.v.) hỗ trợ User trong repo này:
1. **Tuyệt đối không viết code "đồ chơi" (Toy code):** Code phải chuẩn phong cách công nghiệp:
   - Có kiến trúc đa luồng (Multi-threading tách biệt UI, Camera Grabber, Image Processing, PLC Communication).
   - Có cơ chế xử lý ngoại lệ (Try-Catch), log lỗi chi tiết ra file text/CSV.
   - Tối ưu bộ nhớ, giải phóng bộ nhớ (Dispose Bitmap/Mat) để tránh Memory Leak khiến phần mềm sập sau 24/7 chạy máy.
2. **Thái độ đồng hành:**
   - Thẳng thắn, thực tế, kỷ luật, truyền động lực mạnh mẽ.
   - Nhắc nhở về mục tiêu: **"Mỗi dòng code viết ra hôm nay là một bước tiến gần hơn tới chiếc Kia Sportage."**
3. **Cấu trúc thư mục chuẩn bị triển khai:**
   - `src/`: Mã nguồn ứng dụng C# (.NET/WPF) và Python.
   - `docs/`: Tài liệu kỹ thuật, công thức quang học, cẩm nang phỏng vấn.
   - `samples/`: Bộ ảnh mẫu sản phẩm lỗi (PCB lỗi, ốc vít lệch, linh kiện xước) để kiểm thử thuật toán.
   - `simulators/`: Tool giả lập PLC và Camera công nghiệp khi chưa có phần cứng vật lý.

---

## 📜 5. NHẬT KÝ CHIẾN DỊCH & TIẾN ĐỘ THỰC CHIẾN (WAR LOG)

- **2026-08-31:**
  - ✅ **Khởi động:** Xác định mục tiêu đổi đời, phá bỏ tâm lý "gắn bó né tránh / sĩ diện hão", đặt mục tiêu **Kia Sportage** & lương 25-40tr.
  - ✅ **Kiểm tra hạ tầng:** Xác nhận máy đã có `Python 3.14`, cài đặt thành công `opencv-python`, `numpy`, `matplotlib`.
  - ✅ **Hoàn thành Milestone 1 (First AOI Algorithm):** 
    - Đã viết module `src/01_defect_and_dimension_inspector.py` kiểm tra ngoại quan vòng đệm kim loại.
    - Xử lý hoàn hảo 4 trường hợp: Mẫu chuẩn (OK), Mẫu xước bề mặt (NG), Mẫu mẻ vành (NG), Mẫu sai kích thước (NG).
    - **Tốc độ xử lý siêu tốc:** $\approx 3\text{ms} / \text{sản phẩm}$ (đạt chuẩn thời gian chu kỳ nhà máy cao cấp).
  - ✅ **Hoàn thành Milestone 2 (Full 4G Pipeline - Guidance, ID, Gauging, Inspection):**
    - Đã viết module `src/02_full_4g_pipeline_inspector.py` kiểm tra chip bán dẫn Apple A18 bị xoay nghiêng các góc (+25°, -35°, +50°).
    - **1. Guidance:** Tự động định vị tâm và góc nghiêng $\theta$, xoay thẳng ảnh về 0°.
    - **2. Identification:** Đọc chính xác mã QR Code Serial (`SN-APPLE-A18-xxx`).
    - **3. Gauging:** Đo kích thước $220 \times 140\text{px}$.
    - **4. Inspection:** Bắt chính xác lỗi xước thân chip và mẻ góc trên-phải.
    - **Tốc độ toàn bộ chu trình 4G:** $\approx 10\text{ms} / \text{sản phẩm}$!
  - ✅ **Hoàn thành Milestone 3 (Industrial Lighting Mastery & Ray-Tracing Simulator):**
    - Làm chủ 5 loại đèn công nghiệp kinh điển: Backlight (Gauging), Low-Angle Ring 15° (Darkfield Inspection), Coaxial (Mirror/Specular), Dome (Curved/Diffused), và Coaxial + Dome Hybrid (Trùm cuối kim loại phức tạp).
    - Xuất video minh họa Full HD tiếng Việt: `lighting_mastery_demo_vi.mp4`.
    - Xây dựng thành công bộ mô phỏng quang học tương tác 2D `lighting_simulator.html` ngay tại root dự án với chuyển động hạt photon ray-tracing thời gian thực.
  - 🔄 **Kế hoạch tiếp theo (Milestone 4 - Buổi chiều):** 
    - Khởi động Mini-Quiz 3 câu chốt hạ phần Quang học.
    - Tiến vào xây dựng kiến trúc ứng dụng PC Control công nghiệp (C# / WPF / Python UI) kết nối Camera và xử lý trực tiếp.
  - ✅ **Hoàn thành Milestone 7 (Full Industrial C# .NET 8 WPF PC Control Application):**
    - Đã thiết lập hoàn chỉnh môi trường **.NET 8 SDK (LTS)** và tích hợp thư viện **OpenCvSharp4** + **CommunityToolkit.Mvvm** trong dự án `src/PCControlApp`.
    - Đã lập trình trọn gói 3 tầng kiến trúc chuẩn công nghiệp:
      1. `Models/InspectionResult.cs`: Cấu trúc dữ liệu DTO phán quyết chi tiết (Serial, Angle, Width, Height, IsOk, DefectReason, CycleTimeMs).
      2. `VisionEngine/ChipInspector.cs`: Thuật toán 4G Pipeline (Guidance, ID, Gauging, Inspection) bằng C# OpenCvSharp với cơ chế giải phóng bộ nhớ RAM tức thì (`using var Mat`).
      3. `ViewModels/MainViewModel.cs`: Bộ não MVVM điều phối đa luồng, tự động tính toán Yield Rate, Cycle Time và kết nối lệnh Trigger.
      4. `Views/MainWindow.xaml`: Giao diện Dark Mode IPC công nghiệp bằng ngôn ngữ thẻ XAML cao cấp.
    - **Tốc độ biên dịch siêu tốc:** Build thành công $100\%$ không lỗi trong **$2.89\text{ giây}$**!
    - File chạy thực thi đã sẵn sàng: `src/PCControlApp/bin/Debug/net8.0-windows/PCControlApp.exe`.
  - 🔄 **Kế hoạch tiếp theo (Milestone 8):** 
    - Luyện tập kịch bản phỏng vấn kỹ thuật & Portfolio Showcase (Tổng duyệt Chiến dịch Sportage).
