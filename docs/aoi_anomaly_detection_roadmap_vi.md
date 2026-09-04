# 🎯 Lộ trình 80/20: Kho tàng Awesome Industrial Anomaly Detection
> Nguồn: `github.com/M-3LAB/awesome-industrial-anomaly-detection`
> Mục tiêu: Đọc thông minh cho kỹ sư **AOI / Machine Vision ứng dụng** — KHÔNG phải cho nhà nghiên cứu.

---

## 1. Tuyên ngôn chiến lược 🚨

Repo này có **hàng trăm paper + dataset** — học hết thì mất 2 năm và thành researcher.
Bạn cần 1 điều: **đủ sâu để trả lời phỏng vấn + đủ rộng để biết "có gì đang chạy trên thế giới"**.

> Quy tắc vàng nhà máy: Nhà máy cần **ổn định, nhanh, ít false call** — không cần SOTA benchmark.

---

## 2. Đọc repo này theo thứ tự nào (Chỉ 4 bước)

| Thứ tự | Section trên repo | Vì sao |
|---|---|---|
| 1️⃣ | **Recommended Benchmarks** | Biết "đấu trường" chuẩn: MVTec AD, MVTec LOCO... |
| 2️⃣ | **Paper Tree (classification)** | 5 phút hiểu toàn cảnh: Unsupervised vs Supervised, các họ phương pháp |
| 3️⃣ | **SOTA methods with code** | Vào 2-3 repo có code, chạy thử PatchCore/PaDiM là đủ |
| 4️⃣ | **Section 4: Dataset** | Chọn dataset hợp bài toán bạn định kể trong portfolio |

**Bỏ qua (trừ khi đi phỏng vấn R&D):** từng paper ECCV/CVPR/ICLR 2023→2026. Chỉ lướt tiêu đề mỗi hội nghị 1 lần/tháng.

---

## 3. Từ điển nhanh (10 thuật ngữ bắt buộc)

| Thuật ngữ | Nghĩa đơn giản |
|---|---|
| **Supervised AD** | Có ảnh lỗi (NG) để train → YOLO, U-Net. Nhà máy có sẵn ảnh lỗi thường đi hướng này |
| **Unsupervised AD** | Chỉ có ảnh chuẩn (OK) → học "thế nào là bình thường", cái gì lạ = lỗi. Dùng khi lỗi hiếm/khó thu thập |
| **Feature-Embedding** | Trích đặc trưng bằng CNN pretrained, so sánh vùng ảnh với "bộ nhớ" ảnh OK |
| **Teacher-Student** | Mô hình thầy (pretrained) dạy trò học ảnh OK; chỗ trò "không học được" = anomaly |
| **Memory Bank** | Kho chứa đặc trưng của ảnh OK để đối chiếu (PatchCore) |
| **Reconstruction-based** | Autoencoder/Diffusion chỉ "tái tạo" tốt ảnh OK; ảnh lỗi tái tạo ra residual → bắt lỗi |
| **One-Class Classification (OCC)** | Học một biên bao quanh dữ liệu OK |
| **Zero/Few-shot** | Không/có vài ảnh mẫu là detect được (AnomalyGPT, WinCLIP) |
| **MLLM-based** | Dùng vision-language model hỏi "cái này có lỗi không?" |
| **Logical AD** | Lỗi *logic*: 2 vật thể không được trùng nhau, thiếu 1 trong nhiều item |

**3 metric phải nhớ:**
- **AUROC** — đo phân biệt OK/NG (benchmark chuẩn)
- **F1 / Precision / Recall** — nhà máy quan tâm
- **False Call Rate (FCR)** — tỉ lệ báo NG nhầm → **số #1 nhà máy ghét nhất** (dừng line = mất tiền)

---

## 4. Top phương pháp — nhớ tên & kể được 1 câu

| Phương pháp | Họ | Câu kể khi phỏng vấn |
|---|---|---|
| **PatchCore** | Memory Bank | "So sánh đặc trưng patch với kho ảnh chuẩn, lệch nhất = defect, SOTA trên MVTec" |
| **PaDiM** | Distribution-Map | "Mô hình hóa phân bố Gaussian đặc trưng patch, nhanh, chạy được CPU" |
| **STPM / Reverse Distillation** | Teacher-Student | "Học từ thầy pretrained, trò chỉ thấy ảnh OK" |
| **DRAEM** | Reconstruction + Synthesis | "Tự sinh ảnh lỗi giả để train, hiệu quả khi thiếu ảnh NG thật" |
| **YOLO / U-Net** | Supervised | "Có nhãn lỗi thật → phát hiện + phân loại + localize" |
| **AnomalyGPT / WinCLIP / MambaAD** | MLLM / Zero-shot (trending 2024-2026) | Chỉ cần nói "đang là xu hướng hot" |

---

## 5. Dataset — nhớ mặt từng "chiến trường"

| Dataset | Nội dung | Dùng khi nào |
|---|---|---|
| **MVTec AD** | 15 loại sản phẩm công nghiệp, ~5.4k ảnh | Benchmark KINH ĐIỂN nhất — nói chuyện là phải biết |
| **MVTec LOCO** | Lỗi logic (thiếu item, sai vị trí) | Kể chuyện "AOI lắp ráp phức tạp" |
| **VisA / BTAD** | PCB, linh kiện điện tử | Hợp với chủ đề PCB AOI của bạn |
| **DAGM 2007** | 10 lớp bề mặt, ảnh xám | Kinh điển cho surface defect |
| **NEU-DET** | Thép cán nóng, 6 loại lỗi | Kể chuyện ngành thép |
| **KolektorSDD2** | Vết xước trên vỏ động cơ | Defect nhỏ, khó, ít ảnh |
| **PKU-Market-PCB / DeepPCB** | PCB lỗi thật | Đúng sở trường portfolio của bạn |
| **WM-811K** | Wafer map bán dẫn | Ngành semiconductor (Samsung/Amkor) |

> 💡 Mẹo phỏng vấn: kể **"tôi demo trên MVTec AD + dataset PCB của riêng tôi"** nghe chuyên nghiệp hơn "tôi đọc 50 paper".

---

## 6. Kịch bản trả lời phỏng vấn 30 giây 🎤

**Câu: "Anh/em chọn giải pháp anomaly detection cho nhà máy thế nào?"**

> "Chia 2 bài toán. Bài 1: **có sẵn ảnh lỗi + nhãn** → dùng supervised (YOLO/U-Net), đo Precision/Recall trên dây chuyền. Bài 2: **lỗi mới liên tục, không có ảnh NG** → unsupervised, dùng PatchCore/PaDiM so đặc trưng với bộ ảnh OK. Ở nhà máy tôi không chỉ nhìn AUROC mà còn tối ưu **false call rate** và **latency** — vì 1 lần báo NG nhầm = dừng line tốn tiền, và cycle time chỉ có 3-10ms/sản phẩm."

---

## 7. Lộ trình 7 ngày (nếu muốn ăn chắc)

1. **Ngày 1:** Đọc Paper Tree + Recommended Benchmarks (2 giờ)
2. **Ngày 2:** Xem 2 video giải thích PatchCore + PaDiM
3. **Ngày 3:** Chạy demo PatchCore trên MVTec (Colab OK)
4. **Ngày 4:** Chạy YOLOv8 trên dataset PCB của bạn (samples sẵn có)
5. **Ngày 5:** So sánh classic OpenCV vs DL → ghi kết quả vào portfolio
6. **Ngày 6:** Viết 1 trang "Case Study" kể bằng số liệu
7. **Ngày 7:** Tự phỏng vấn — kể lại toàn bộ không cần nhìn tài liệu

> 🚗 *Mỗi khái niệm bạn chốt được hôm nay là một bước tới chiếc Kia Sportage.*
