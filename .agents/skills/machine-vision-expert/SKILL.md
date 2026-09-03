---
name: machine-vision-expert
description: >-
  Kỹ năng chuyên gia về Thị giác máy tính công nghiệp (Industrial Machine Vision),
  PC Control (C# .NET, WPF, C++, Python), Quang học công nghiệp (Lens, Camera, Lighting),
  giao tiếp PLC (Modbus, Socket TCP/IP) và chiến lược nâng cao thu nhập cho kỹ sư Computer Science.
---

# Machine Vision & Industrial PC Control Expert Skill

Skill này được thiết kế để dẫn đường cho kỹ sư phần mềm (đặc biệt là nền tảng Khoa học máy tính) làm chủ hệ thống kiểm tra ngoại quan tự động (AOI / Machine Vision) trong môi trường sản xuất công nghiệp chuẩn quốc tế.

---

## 1. NGUYÊN TẮC THIẾT KẾ PHẦN MỀM CÔNG NGHIỆP (INDUSTRIAL-GRADE ARCHITECTURE)

Trong nhà xưởng, một phần mềm Machine Vision phải chạy liên tục 24/7/365 không được sập, không rò rỉ RAM (Memory Leak), và độ trễ phản hồi (Latency) phải tính bằng mili-giây (ms).

### Kiến trúc Đa luồng Bắt buộc (Pipeline Multi-Threading)
Một ứng dụng PC Control chuẩn bắt buộc phải chia thành 4 tầng độc lập:
1. **Camera Acquisition Layer:** Nhận hardware trigger từ cảm biến/PLC qua cổng I/O hoặc line trigger của camera GigE/USB3. Bắn frame vào Ring Buffer hoặc Blocking Queue.
2. **Processing Layer (Worker Pool):** Lấy frame từ hàng đợi, thực hiện thuật toán xử lý ảnh (OpenCvSharp / C++ DLL / Halcon / TensorRT). Trả về kết quả: Struct `{ IsOk: bool, Defects: List<Defect>, ProcessingTimeMs: double, MeasurementData: ... }`.
3. **PLC / IO Communication Layer:** Giao tiếp PLC qua Socket TCP/IP, Modbus TCP, hoặc card I/O (Advantech, Adlink). Gửi xung tín hiệu gạt hàng lỗi (Rejector) kịp thời trước khi sản phẩm trôi qua băng chuyền.
4. **UI Presentation Layer (WPF / WinForms):** Chỉ lắng nghe event để render ảnh và cập nhật biểu đồ thống kê (Yield rate, OK count, NG count). Tuyệt đối không tính toán nặng trên UI Thread để tránh đơ giao diện.

---

## 2. BỘ CÔNG THỨC QUANG HỌC & CHỌN THIẾT BỊ (OPTICS & HARDWARE DESIGN)

Khi đi phỏng vấn hoặc triển khai dự án, bạn sẽ cần tính toán chọn Lens và Camera:

### Công thức tính tiêu cự Lens (Focal Length $f$):
$$f = \frac{WD \times \text{Sensor Size}}{FOV}$$
Trong đó:
- **FOV (Field of View):** Vùng nhìn thấy của sản phẩm (ví dụ $100\text{mm} \times 80\text{mm}$).
- **WD (Working Distance):** Khoảng cách từ thấu kính đến bề mặt sản phẩm (ví dụ $300\text{mm}$).
- **Sensor Size:** Kích thước chip cảm biến của camera (ví dụ $1/1.8"$, $2/3"$, $1"$).

### Độ phân giải hệ thống (Resolution & Accuracy):
$$\text{Pixel Size trên vật thể} = \frac{FOV}{\text{Độ phân giải pixel camera}}$$
*Nguyên tắc:* Để đo đạc chính xác hoặc phát hiện lỗi có kích thước $X$, kích thước 1 pixel tối thiểu phải bằng $X / 3$ đến $X / 5$ (3 đến 5 pixels trên một khuyết tật).

### Chọn loại đèn chiếu sáng (Industrial Lighting):
- **Bề mặt kim loại bóng, gương (Highly Reflective):** Dùng **Coaxial Light** (đèn đồng trục) hoặc **Dome Light** (đèn vòm tán xạ) để triệt tiêu đốm lóa.
- **Đo kích thước, soi biên dạng (Metrology/Profile):** Dùng **Backlight** (đèn chiếu đáy/ngược sáng) để tạo bóng đen sắc nét viền ngoài.
- **Kiểm tra xước bề mặt, chữ nổi (Surface Scratch, Embossed Text):** Dùng **Low Angle Ring Light** (đèn vòng góc thấp) để tạo bóng đổ tại vị trí lỗi.

---

## 3. THƯ VIỆN & THUẬT TOÁN CỐT LÕI

### Rule-based Vision (OpenCV / OpenCvSharp):
- **Tiền xử lý:** Gaussian Blur, Median Blur, CLAHE (cân bằng sáng thích nghi).
- **Phân ngưỡng (Segmentation):** Otsu Thresholding, Adaptive Thresholding.
- **Hình thái học (Morphology):** Dilation, Erosion, Opening (khử nhiễu trắng), Closing (lấp lỗ đen).
- **Tìm biên & Đo đạc:** Canny, FindContours, Convex Hull, MinAreaRect, HoughLines/Circles.
- **Đo khoảng cách chính xác (Caliper):** Đo khoảng cách giữa 2 cạnh sắc nét bằng cách phân tích profile đạo hàm cường độ sáng (Sub-pixel edge detection).
- **So khớp mẫu (Pattern Matching):** `cv2.matchTemplate` kết hợp kim tự tháp ảnh (Image Pyramid) để tăng tốc độ.

### Deep Learning công nghiệp:
- Phát hiện dị tật phức tạp không đồng nhất (vết bẩn, rách màng, nứt gốm): Dùng **YOLOv8/v10/v11** hoặc mô hình không cần gán nhãn lỗi **Anomaly Detection (PatchCore, Padim - Anomalib)**.

---

## 4. CHIẾN LƯỢC NÂNG TẦM SỰ NGHIỆP & TÀI CHÍNH (ROAD TO KIA SPORTAGE)

1. **Giai đoạn 1 (Tháng 1 - 3): Xây dựng Portfolio thực chiến**
   - Viết trọn vẹn 1 hệ thống kiểm tra ngoại quan giả lập (C# WPF + OpenCvSharp + Giả lập PLC TCP/IP).
   - Có giao diện chuyên nghiệp, cấu hình ngưỡng động, lưu ảnh lỗi NG ra folder theo ngày giờ, vẽ bounding box.
2. **Giai đoạn 2 (Tháng 4 - 6): Săn việc & Phỏng vấn công ty Đa quốc gia**
   - Target: Sejong Dynamics, Hansol, Jahwa, Foxconn, Cognex Vietnam, Basler Vietnam, Advantech, các công ty tự động hóa Bắc Ninh/Bắc Giang/Hải Phòng/Hà Nội/Sài Gòn/Bình Dương.
   - Khi phỏng vấn: Mang laptop mở demo C# chạy trơn tru $\to$ 90% nhà tuyển dụng sẽ bị thuyết phục ngay tại chỗ.
   - Đàm phán mức lương khởi điểm: 12 - 18 triệu VNĐ.
3. **Giai đoạn 3 (Năm thứ 2 - 3): Bứt phá thu nhập lên 25 - 40 triệu**
   - Nắm toàn bộ quy trình thiết kế từ chọn camera, tính lens, test đèn, lập trình PC Control, tích hợp robot/băng chuyền.
   - Nhận thêm dự án ngoài (Freelance máy AOI cho xưởng nhỏ) hoặc thăng tiến lên Tech Lead/Project Manager.
   - **Hiện thực hóa mục tiêu mua Kia Sportage!**

---

## 5. TỪ ĐIỂN THUẬT NGỮ CHUYÊN NGÀNH THỰC CHIẾN (INDUSTRIAL VISION GLOSSARY)

| Thuật ngữ tiếng Anh | Dịch nghĩa xưởng máy | Bản chất dễ nhớ (Không số má rườm rà) |
| :--- | :--- | :--- |
| **AOI** *(Automated Optical Inspection)* | Kiểm tra quang học tự động | Dùng Camera + Đèn + Máy tính thay mắt người để soi lỗi sản phẩm trên băng chuyền. |
| **ROI** *(Region of Interest)* | Vùng quan tâm | Khoanh một cái hộp chữ nhật trên ảnh chỉ để soi đúng chỗ cần soi (giúp code chạy nhanh gấp 10 lần, không bị bắt nhầm nền xung quanh). |
| **Thresholding & Binarization** | Phân ngưỡng & Nhị phân hóa | Đổi ảnh từ xám (nhiều sắc độ xám) sang đúng **2 màu Đen - Trắng tinh khiết** dựa trên 1 con số ranh giới (ngưỡng). |
| **Trigger** | Lệnh kích hoạt chụp ảnh | Cảm biến thấy sản phẩm chạy tới $\to$ "bóp cò" một phát để Camera chớp sáng chụp 1 bức ảnh. |
| **Exposure Time** | Thời gian phơi sáng (mở màn trập) | Thời gian camera mở mắt để hứng sáng (tính bằng micro-giây $\mu s$). Phơi sáng lâu $\to$ ảnh sáng nhưng bị nhòe chuyển động; Phơi sáng cực ngắn $\to$ ảnh đóng băng chuyển động sản phẩm. |
| **Gain** | Hệ số khuếch đại điện tử | "Tăng volume" độ sáng bằng phần mềm/mạch điện tử khi đèn bị yếu (Lưu ý: Tăng Gain quá cao sẽ làm ảnh bị nhiễu hạt mè / Noise). |
| **Pixel Resolution / Calibration** | Tỷ lệ quy đổi $\text{mm}/\text{pixel}$ | Chiếc thước đo: 1 pixel trên ảnh bằng bao nhiêu milimet ngoài đời (Ví dụ: $1\text{px} = 0.1\text{mm} \to$ đo được $200\text{px}$ tức là sản phẩm dài $20\text{mm}$). |
| **Yield Rate (%)** | Tỷ lệ sản phẩm đạt chuẩn (OK) | $\frac{\text{Số lượng hàng OK}}{\text{Tổng sản phẩm đã chạy}} \times 100\%$. |
| **Cycle Time (ms)** | Thời gian chu kỳ 1 sản phẩm | Thời gian từ lúc Trigger chụp ảnh đến lúc thuật toán phán quyết OK/NG và báo xong về PLC (thường yêu cầu $< 20\text{ms}$). |
| **False Alarm (Overkill)** | Báo lỗi nhầm / NG giả | Hàng thực tế chuẩn OK nhưng máy soi quá nhạy nên bắt nhầm thành NG (Gây tốn công người đi kiểm tra lại). |
| **Escape (Underkill)** | Lọt lỗi / Bỏ sót | Hàng bị lỗi NG thật nhưng máy lại cho qua thành OK (**Lỗi tối kỵ** vì hàng lỗi sẽ lọt đến tay khách hàng). |

