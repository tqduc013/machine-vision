# %% [markdown]
# # 🔬 PHÒNG THÍ NGHIỆM AI ANOMALY DETECTION (PATCHCORE & MEMORY BANK)
# Chạy từng Cell độc lập bằng cách bấm nút [▶ Run Cell] ở ngay phía trên từng khối mã!

# %% [markdown]
# ### BƯỚC 1: KHAI BÁO THƯ VIỆN & ĐƯỜNG DẪN DỮ LIỆU
# - cv2: Đọc và xử lý ảnh bo mạch
# - numpy: Tính toán vector ma trận đặc trưng
# - matplotlib.pyplot: Hiển thị ảnh trực quan

# %%
import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

# Trỏ đúng vào thư mục 50 cặp ảnh bo mạch thực tế ta vừa tải
DATASET_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "pcb_defects")
TRAIN_DIR = os.path.join(DATASET_DIR, "train_good")       # 50 ảnh chuẩn OK
TEST_DIR = os.path.join(DATASET_DIR, "test_defects")     # 50 ảnh lỗi thật

print("[+] Du lieu san sang!")
print("    Thu muc anh OK:", TRAIN_DIR)
print("    Thu muc anh NG:", TEST_DIR)


# %% [markdown]
# ### BƯỚC 2: ĐỌC ẢNH & KHOANH VÙNG VẾT ĐỨT MẠCH THEO TỌA ĐỘ VỪA HỌC
# - Bo mạch chuẩn: 00041000_temp.jpg
# - Bo mạch lỗi thật: 00041000_test.jpg
# - Tọa độ vết đứt mạch: X1 = 539, Y1 = 259 | X2 = 592, Y2 = 316

# %%
# 1. Đọc tấm ảnh chuẩn (Golden Template)
img_ok = cv2.imread(os.path.join(TRAIN_DIR, "00041000_temp.jpg"))
img_ok_rgb = cv2.cvtColor(img_ok, cv2.COLOR_BGR2RGB)

# 2. Đọc tấm ảnh lỗi thật
img_ng = cv2.imread(os.path.join(TEST_DIR, "00041000_test.jpg"))
img_ng_rgb = cv2.cvtColor(img_ng, cv2.COLOR_BGR2RGB)

# 3. Dùng công thức "2 trừ 1" ta vừa luyện:
#    X1 = 539, Y1 = 259 (Góc Trên - Trái)
#    X2 = 592, Y2 = 316 (Góc Dưới - Phải)
#    Chiều rộng = 592 - 539 = 53px, Chiều cao = 316 - 259 = 57px
cv2.rectangle(img_ng_rgb, (539, 259), (592, 316), (255, 0, 0), 3)

# 4. Hiển thị 2 ảnh cạnh nhau
plt.figure(figsize=(12, 6))

plt.subplot(1, 2, 1)
plt.title("BO MACH CHUAN 100% OK", color="green", fontsize=12, fontweight="bold")
plt.imshow(img_ok_rgb)
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title("BO MACH BI DUT MACH (GROUND TRUTH)", color="red", fontsize=12, fontweight="bold")
plt.imshow(img_ng_rgb)
plt.axis("off")

plt.tight_layout()
plt.show()


# %% [markdown]
# ### BƯỚC 3: CƠ CHẾ PATCHCORE - CẮT ẢNH THÀNH 400 MẢNH GHÉP NHỎ (PATCHES)
# - Kích thước ảnh: 640 x 640 pixel.
# - Chọn kích thước mỗi mảnh Patch: 32 x 32 pixel.
# - Số lượng mảnh: 640 / 32 = 20 mảnh ngang x 20 mảnh dọc = 400 mảnh tất cả!
# - Ta sẽ trích xuất thử:
#   1. Một mảnh BÌNH THƯỜNG (ở tọa độ X=128, Y=128)
#   2. Một mảnh BỊ ĐỨT MẠCH (ngay vị trí X=544, Y=288) để kính lúp AI soi sự khác biệt!

# %%
PATCH_SIZE = 32  # Kích thước mỗi mảnh ghép (32 x 32 pixel)

# 1. Cắt 1 mảnh bình thường trên bo mạch chuẩn (Vị trí X=128, Y=128)
patch_normal = img_ok_rgb[128:128+PATCH_SIZE, 128:128+PATCH_SIZE]

# 2. Cắt 1 mảnh bị đứt mạch trên bo mạch lỗi (Vị trí X=544, Y=288 - nằm trúng hộp đỏ!)
patch_defect = img_ng_rgb[288:288+PATCH_SIZE, 544:544+PATCH_SIZE]

# 3. Phóng to 2 mảnh ghép để nhìn cận cảnh dưới "kính lúp của AI"
plt.figure(figsize=(8, 4))

plt.subplot(1, 2, 1)
plt.title(f"MANH CHUAN ({PATCH_SIZE}x{PATCH_SIZE}px)\n(Duong dong lien mach)", color="green", fontweight="bold")
plt.imshow(patch_normal)
plt.axis("off")

plt.subplot(1, 2, 2)
plt.title(f"MANH BI LOI ({PATCH_SIZE}x{PATCH_SIZE}px)\n(Bi dut toac o giua)", color="red", fontweight="bold")
plt.imshow(patch_defect)
plt.axis("off")

plt.tight_layout()
plt.show()

print(f"[+] Mot buc anh 640x640 duoc cat thanh: (640/32) x (640/32) = 400 manh Patch!")


# %% [markdown]
# ### BƯỚC 4: XÂY DỰNG MEMORY BANK (KHO KÝ ỨC CHUẨN)
#
# Đây là trái tim của thuật toán PatchCore!
# Ta đọc toàn bộ 50 ảnh bo mạch chuẩn OK trong train_good/.
# Mỗi ảnh được cắt thành 400 mảnh Patch (32x32 pixel).
# Mỗi mảnh Patch được "ép dẹt" thành 1 hàng số (vector):
#   - 32 x 32 pixel x 3 kênh màu RGB = 3072 con số mô tả 1 mảnh.
# Toàn bộ 50 x 400 = 20.000 vector được gom lại thành bảng Memory Bank.
# Ví dụ: Memory Bank giống như một cuốn sổ ghi chép 20.000 dòng,
# mỗi dòng là "hình ảnh đặc trưng của 1 mảnh bo mạch bình thường".

# %%
import time

PATCH_SIZE = 32   # Kích thước mỗi mảnh vuông (pixel)
NUM_GRIDS = 640 // PATCH_SIZE  # 640 / 32 = 20 ô mỗi chiều

memory_bank = []  # Danh sách rỗng - sẽ chứa toàn bộ vector đặc trưng của ảnh OK

# Lấy danh sách tất cả ảnh chuẩn trong thư mục train_good/
ok_files = sorted([f for f in os.listdir(TRAIN_DIR) if f.endswith('.jpg')])
print(f"[*] Bat dau nap {len(ok_files)} anh chuan OK vao Memory Bank...")

t_start = time.time()

for fname in ok_files:
    # 1. Đọc từng ảnh chuẩn
    img = cv2.imread(os.path.join(TRAIN_DIR, fname))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # 2. Cắt ảnh thành lưới NUM_GRIDS x NUM_GRIDS mảnh Patch
    for row in range(NUM_GRIDS):      # Duyệt từng hàng (Y)
        for col in range(NUM_GRIDS):  # Duyệt từng cột (X)
            y = row * PATCH_SIZE      # Tọa độ Y bắt đầu của mảnh
            x = col * PATCH_SIZE      # Tọa độ X bắt đầu của mảnh

            # 3. Cắt ra 1 mảnh Patch (32 x 32 pixel)
            patch = img[y:y + PATCH_SIZE, x:x + PATCH_SIZE]

            # 4. "Ép dẹt" mảnh Patch thành 1 hàng số phẳng (vector 3072 chiều)
            #    32 x 32 x 3 = 3072 con số mô tả toàn bộ màu sắc của mảnh đó
            vector = patch.flatten().astype(np.float32)

            # 5. Chuẩn hóa về [0, 1] để các con số không bị quá lớn
            vector = vector / 255.0

            # 6. Lưu vector này vào Memory Bank
            memory_bank.append(vector)

# 7. Chuyển Memory Bank từ danh sách sang ma trận NumPy để tính toán nhanh hơn
memory_bank = np.array(memory_bank)  # Shape: (20000, 3072)

t_end = time.time()

print(f"[+] MEMORY BANK DA XAY DUNG XONG!")
print(f"    - So anh chuan OK: {len(ok_files)}")
print(f"    - So Patch moi anh: {NUM_GRIDS} x {NUM_GRIDS} = {NUM_GRIDS * NUM_GRIDS}")
print(f"    - Tong so vector trong Memory Bank: {memory_bank.shape[0]:,}")
print(f"    - Kich thuoc moi vector: {memory_bank.shape[1]} chieu (32 x 32 x 3 = 3072)")
print(f"    - Thoi gian xay dung: {t_end - t_start:.2f} giay")
print(f"    - Dung luong RAM su dung: {memory_bank.nbytes / (1024 * 1024):.1f} MB")


# %% [markdown]
# ### BƯỚC 5: SO KHOẢNG CÁCH → VẼ HEATMAP → PHÁN QUYẾT OK/NG
#
# Đây là bước phán quyết cuối cùng của AI!
# Quy trình cho từng mảnh Patch của ảnh lỗi:
#   1. Lấy vector đặc trưng của Patch đó (3072 con số).
#   2. Tính khoảng cách tới TẤT CẢ 20.000 vector trong Memory Bank.
#   3. Lấy khoảng cách NHỎ NHẤT (gần nhất - Nearest Neighbor Distance).
#   4. Khoảng cách nhỏ → Patch bình thường (tô màu xanh/lạnh).
#   5. Khoảng cách lớn → Patch bất thường (tô màu đỏ/nóng).
#   → Ghép tất cả 400 ô lại = ANOMALY HEATMAP!

# %%
# 1. Đọc ảnh lỗi thật cần kiểm tra
img_test = cv2.imread(os.path.join(TEST_DIR, "00041000_test.jpg"))
img_test_rgb = cv2.cvtColor(img_test, cv2.COLOR_BGR2RGB)

# 2. VECTORIZATION CÔNG NGHIỆP: TÍNH TOÁN SONG SONG TOÀN BỘ 400 PATCH
#    Thay vì chạy 400 lần vòng lặp for (mất 54 giây), ta dùng công thức hằng đẳng thức:
#    (A - B)^2 = A^2 - 2AB + B^2
#    Phép nhân ma trận np.dot() chạy bằng đa luồng CPU (SIMD/BLAS) chỉ mất ~0.15 giây!

print("[*] AI dang so sanh 400 Patch voi 20.000 vector bang VECTORIZATION...")
t_start = time.time()

# Cắt toàn bộ 400 Patch cùng lúc thành ma trận T: Shape (400, 3072)
patches = [img_test_rgb[r * PATCH_SIZE:(r + 1) * PATCH_SIZE, c * PATCH_SIZE:(c + 1) * PATCH_SIZE].flatten().astype(np.float32) / 255.0
           for r in range(NUM_GRIDS) for c in range(NUM_GRIDS)]
T = np.array(patches)  # (400, 3072)
M = memory_bank        # (20000, 3072)

# Khai triển hằng đẳng thức ma trận:
T_sq = np.sum(T ** 2, axis=1, keepdims=True)            # Shape (400, 1)
M_sq = np.sum(M ** 2, axis=1, keepdims=True).T          # Shape (1, 20000)
dot = np.dot(T, M.T)                                    # Phép nhân ma trận 400x3072 x 3072x20000 -> Shape (400, 20000)

# Ma trận khoảng cách bình phương (Pairwise Squared Euclidean Distance)
dist_sq = np.maximum(T_sq - 2 * dot + M_sq, 0.0)

# Lấy khoảng cách nhỏ nhất (Nearest Neighbor) cho từng Patch trong 400 ô
min_dist = np.sqrt(np.min(dist_sq, axis=1))

# Đưa ngược lại ma trận 2D lưới (20 x 20)
anomaly_map = min_dist.reshape(NUM_GRIDS, NUM_GRIDS)

t_end = time.time()
elapsed = t_end - t_start
print(f"[+] VECTORIZATION HOAN TAT!")
print(f"    - Thoi gian so sanh: {elapsed:.4f} giay ({elapsed * 1000:.1f} ms) ⚡⚡⚡")
print(f"    - Nhanh gap ~{54.18 / elapsed:.0f} LAN so voi vong lap for cu!")

# 7. Phóng to Heatmap từ 20x20 lên 640x640 để khớp kích thước ảnh gốc
heatmap = cv2.resize(anomaly_map, (640, 640), interpolation=cv2.INTER_LINEAR)
heatmap_norm = cv2.normalize(heatmap, None, 0, 255, cv2.NORM_MINMAX).astype(np.uint8)
heatmap_color = cv2.applyColorMap(heatmap_norm, cv2.COLORMAP_JET)  # Tô màu nóng-lạnh
heatmap_color_rgb = cv2.cvtColor(heatmap_color, cv2.COLOR_BGR2RGB)

# 8. Ghép Heatmap đè lên ảnh gốc để thấy lỗi nằm ở đâu
overlay = cv2.addWeighted(img_test_rgb, 0.5, heatmap_color_rgb, 0.5, 0)

# 9. Vẽ kết quả: Ảnh gốc | Heatmap | Overlay
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.title("ANH BO MACH LOI (THUC TE)", color="gray", fontweight="bold")
plt.imshow(img_test_rgb)
plt.axis("off")

plt.subplot(1, 3, 2)
plt.title("ANOMALY HEATMAP\n(Do = Lo, Xanh = Binh Thuong)", color="red", fontweight="bold")
plt.imshow(heatmap_color_rgb)
plt.axis("off")

plt.subplot(1, 3, 3)
plt.title("OVERLAY: LOI DUOC TO MAU TREN ANH THAT", color="darkorange", fontweight="bold")
plt.imshow(overlay)
plt.axis("off")

plt.tight_layout()
plt.show()

# 10. Phán quyết OK / NG dựa trên điểm anomaly cao nhất
max_score = np.max(anomaly_map)
THRESHOLD = np.percentile(anomaly_map, 90)  # Ngưỡng: top 10% điểm cao nhất
print(f"\n{'='*50}")
print(f"[PHAN QUYET AI] Diem bat thuong cao nhat: {max_score:.4f}")
print(f"[NGUONG NG]     Nguong phan quyet: {THRESHOLD:.4f}")
if max_score > THRESHOLD:
    print(f"[KET QUA]       >>> NG (HANG LOI) <<< - Phat hien di thuong!")
else:
    print(f"[KET QUA]       >>> OK (HANG CHUAN) <<<")
print(f"{'='*50}")

