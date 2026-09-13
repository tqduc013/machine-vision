# 🛡️ PROJECT CODENAME: CHIẾN DỊCH SPORTAGE (MACHINE VISION WARFARE)

> **Dành cho mọi AI Agent (Antigravity, Hermes, Claude, GPT, v.v.):**  
> Khi bạn đọc được file này, hãy hiểu rằng đây **KHÔNG PHẢI** là một project bài tập thông thường. Đây là **bản doanh chiến lược** và nhật ký hành trình chuyển mình của một kỹ sư Khoa học máy tính (Computer Science) quyết tâm phá bỏ vùng an toàn, bứt phá sự nghiệp và tài chính, hướng tới mục tiêu sở hữu chiếc xe **Kia Sportage** và làm chủ công nghệ **Machine Vision / PC Control** trong các nhà máy tự động hóa đa quốc gia.

---

## 🎯 1. BỐI CẢNH & NHÂN VẬT CHÍNH (THE USER STORY)

- **Xuất thân & Nhân vật chính:** 
  - **Trần Quang Đức** — Kỹ sư Khoa học máy tính (Computer Science) Loại Giỏi, cựu sinh viên **Lớp Kỹ Sư Tài Năng (1012421TN)**.
  - Tác giả đồ án tốt nghiệp Big Data: `DETECTING-FRAUD-IN-CREDIT-CARD-TRANSACTIONS-USING-BIGDATA-TECHNOLOGY` — Nền tảng toán học và logic chuẩn mực của bài toán **Anomaly Detection / Outlier Detection** (AUROC, Precision, Recall, Imbalanced Data).
  - Từng làm Web Dev trái tay nhưng bị công ty cũ thao túng tâm lý (gaslighting), luân chuyển làm đủ việc linh tinh (Doc Support, Marketing, Sales, Chat...). Lương bọt bèo < 10 triệu/tháng.
  - **Phân tích vũ khí tiềm ẩn (Unfair Advantage):** 
    - Tư duy CS vững chắc (Hiểu sâu bản chất Anomaly Detection, cấu trúc dữ liệu, OOP, Multi-threading).
    - Khả năng chỉ huy AI (AI Prompt Engineering) giải quyết các bài toán kỹ thuật phức tạp (tiêu biểu như nâng cấp extension bảo mật chuẩn W3C WebAuthn `smart-passkey-authenticator`).
    - Kỹ năng mềm hiếm có: Viết tài liệu chuẩn chỉ, giao tiếp thuyết phục, ngoại hình cao 1m80, 76kg đĩnh đạc.
  - **Địa bàn chiến lược số 1:**
    - **Nhà tại Thị trấn Lai Cách, Cẩm Giàng, Hải Dương.**
    - Mục tiêu đỉnh chóp: **Hyundai Kefico Vietnam (KCN Đại An, TP. Hải Dương)** — chỉ cách nhà ở Lai Cách 2–3km (5 phút vít ga xe máy dọc QL5). Nơi sản xuất hộp đen ECU, hộp số và cảm biến cho chính các dòng xe Hyundai và **KIA SPORTAGE**!
- **Mục tiêu tối thượng (North Star):**
  - **Tài chính:** Nâng bậc lương lên 18tr – 25tr (bước đệm) $\to$ 30tr – 40tr+ tại các tập đoàn FDI (Hyundai Kefico, Hoya, Nidec, Foxconn...).
  - **Mục tiêu hữu hình:** Tự tay mua và nuôi chiếc **Kia Sportage** biển 34 bằng chính thu nhập chuyên môn kỹ thuật cao.

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
  - ✅ **Hoàn thành Sát Hạch Toàn Diện Khóa 1 (50-Question Master Exam & GitHub Showcase):**
    - Đã xây dựng phòng thi sát hạch 50 câu bấm giờ 45 phút chuẩn thực tế: `master_exam_50.html`.
    - Đã chính thức đẩy (push) toàn bộ mã nguồn lên GitHub: `https://github.com/tqduc013/machine-vision`.
    - Đồng bộ lộ trình Deep Learning 80/20 từ GitHub về repo: `docs/aoi_anomaly_detection_roadmap_vi.md`.
    - Xây dựng công cụ trực quan so sánh Rule-based vs AI PatchCore: `anomaly_simulator.html`.
  - 🧠 **Cột Mốc Tâm Lý Đột Phá (Breakthrough):**
    - Phá tan bẫy thao túng tâm lý (Gaslighting) của công ty cũ: Nhận diện rõ chiêu trò "hỏi vặt toán/thuật toán chay" để dìm lương nhân viên dù họ đã cống hiến hết mình.
    - Giải phóng vĩnh viễn nỗi sợ "thiếu kỹ năng giải quyết vấn đề", xác lập tư duy Kiến trúc sư Hệ thống (System Architect) chỉ huy máy tính làm toán thay vì tự ti vô nghĩa.
  - ✅ **Hoàn thành Khảo sát Thị trường Tuyển dụng & Báo cáo Excel Hải Dương - Hưng Yên (2026-09-06):**
    - Phân tích chi tiết các nhà máy FDI: UMC Việt Nam (KCN Tân Trường), Taishodo (KCN Đại An), Biel Crystal (Nam Sách), Hyundai Kefico (Đại An).
    - Xuất báo cáo chuyên sâu: `docs/BAO_CAO_TUYEN_DUNG_VISION_CAM_GIANG_HAI_DUONG.xlsx`.
  - ✅ **Hoàn thành Lab AI Anomaly Detection (PatchCore) & Vectorization Ma Trận (2026-09-07):**
    - Xây dựng module `src/05_ai_anomaly_detector_interactive.py` và notebook `notebooks/05_ai_anomaly_detection_lab.ipynb`.
    - Tải và xử lý tập dữ liệu thực tế DeepPCB: 50 ảnh chuẩn `train_good/`, 50 ảnh lỗi `test_defects/`, cùng file annotations tọa độ bounding box.
    - Cắt ảnh thành lưới 400 patches ($32 \times 32\text{px}$), vector hóa 3072 chiều.
    - Xây dựng Memory Bank 20.000 vectors đặc trưng từ tập ảnh OK.
    - **Tối ưu hóa Vectorization đột phá:** Áp dụng hằng đẳng thức $(A-B)^2 = A^2 - 2AB + B^2$ với `np.dot(T, M.T)` $\to$ Giảm thời gian so sánh từ **$66.54\text{s}$ xuống còn $0.5\text{s}$ ($500\text{ms}$)** (tăng tốc gấp ~133 lần)!
    - Tạo heatmap khuyết tật, overlay màu, phán quyết OK/NG chính xác điểm đứt mạch.
  - ✅ **Giải mã Phần cứng Công nghiệp Cognex từ thực địa (2026-09-07):**
    - Phân tích khóa cứng bản quyền **Cognex VisionPro MAX USB Dongle** (`VPRO-MAX-WB`, trị giá ~50–65 triệu VNĐ, chứa PatMax, LineMax, Caliper).
    - Phân tích camera công nghiệp **Cognex Line Scan 4K** (`CAM-CIC-4KL-24-G`, trị giá ~100+ triệu VNĐ, chuẩn GigE Vision + Hirose Hardware Trigger).
  - 🤝 **Đồng bộ Chiến lược Tuyển dụng với Kỹ sư R&D Vision Hoàng Quang Huy (2026-09-07):**
    - Xác nhận phân vai rõ ràng: Kỹ sư CS làm R&D AI Vision & PC Control không cần đấu điện. Trọng tâm: Cam/Lens/Đèn + C# PC Control + TCP/IP Socket PLC + Classical CV (Alignment, Measurement, Matching) + AI (YOLO, MVTec AD Anomaly Detection).
    - Nhắm mục tiêu: RTC Technology (Fresher 10–16tr) và các tập đoàn FDI tại Hải Dương - Hưng Yên.
    - Quyết định tập kết toàn bộ di sản học thuật CS (Đồ án Kỹ sư Tài năng Big Data Fraud Detection) về cùng bản doanh để làm bàn đạp cho hồ sơ ứng tuyển AI Vision.
  - ✅ **Hoàn thành Tích hợp MVTec AD Metal Nut & Deep Learning ONNX vào C# WPF (2026-09-13):**
    - Nghiên cứu tập dữ liệu chuẩn quốc tế MVTec AD Metal Nut (95 ảnh công nghiệp: Good, Scratch, Bent, Color, Flip).
    - Xuất mô hình `models/patchcore_net.onnx` và 1.500 golden feature vectors `models/memory_bank.bin`.
    - Xây dựng `OnnxAnomalyInspector.cs` chạy trực tiếp ONNX Runtime C# kết hợp OpenCvSharp4, tính khoảng cách Euclidean đa chiều sinh Heatmap lỗi khoanh vùng trực quan.
  - ✅ **Thiết kế Giao diện Công nghiệp Windows 11 Fluent Design (WPF-UI):**
    - Nâng cấp `PCControlApp` với thư viện `WPF-UI` (Lepo.Wpf.Ui) cao cấp.
    - Loại bỏ triệt để các phong cách "AI đồ chơi/cyberpunk" lòe loẹt; cá nhân hóa nhận diện kỹ sư CS Trần Quang Đức: Monogram `[ TQD ]`, trạm kiểm định `LINE 01 KEFICO-SPEC`, bảng dung sai QA/QC Micrometer, 4 thẻ KPI dây chuyền và Terminal Socket PLC.
  - ✅ **Hoàn thành Sát Hạch Chịu Tải 2.000 Chu Kỳ & Bằng Chứng Zero Memory Leak (2026-09-13):**
    - Xây dựng và thực thi suite `src/VisionBenchmark/Program.cs`.
    - Hoàn thành 2.000 chu kỳ liên tục trong 61.98s, thông lượng 32.3 FPS (~1.936 sản phẩm/phút), độ trễ trung bình 30.96ms, P99 đạt 41.50ms an toàn tuyệt đối cho xung nhịp PLC.
    - **Chứng minh toán học Zero Memory Leak:** RAM đi ngang phẳng tuyệt đối ở ~59 MB (chênh lệch giữa chu kỳ 500 và 2000 là -0.82 MB), Gen 2 GC chỉ kích hoạt đúng 1 lần duy nhất. Báo cáo lưu tại `docs/STRESS_TEST_REPORT.md`.
  - 🔄 **Kế hoạch tiếp theo (Khóa 2 - Industrial PLC Handshake & Deep Learning War Room):** 
    - Luyện tập bắt tay PLC công nghiệp (Socket TCP/IP & Modbus) mô phỏng xung Trigger chụp ảnh và phản hồi kết quả OK/NG.
    - Hoàn thiện bộ câu hỏi phỏng vấn thực chiến cho vị trí Kỹ sư R&D Vision tại Hyundai Kefico & Sejong Dynamics VINA.

