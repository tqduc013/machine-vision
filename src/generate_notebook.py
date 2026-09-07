import os
import json

os.makedirs("notebooks", exist_ok=True)

nb = {
    "cells": [
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "# 🔬 PHÒNG THÍ NGHIỆM AI ANOMALY DETECTION (PATCHCORE & MEMORY BANK)\n",
                "> **Mục tiêu:** Từng bước làm chủ thuật toán AI bắt khuyết tật bo mạch thực tế (DeepPCB) không cần dữ liệu lỗi.\n",
                "> **Quy trình chuẩn:** Thử nghiệm từng Cell trên Notebook (.ipynb) ➔ Đóng gói thành mã nguồn sản xuất (.py).\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 📦 BƯỚC 1: IMPORT THƯ VIỆN & THIẾT LẬP ĐƯỜNG DẪN DỮ LIỆU\n",
                "- `cv2`: Đọc ảnh, cắt patch, vẽ bounding box khoanh vùng lỗi.\n",
                "- `numpy`: Xử lý mảng ma trận vector đặc trưng và khoảng cách Euclidean.\n",
                "- `matplotlib.pyplot`: Hiển thị ảnh và bản đồ nhiệt (Heatmap) trực quan ngay dưới từng cell."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 1. Khai báo các thư viện cần thiết\n",
                "import os\n",
                "import cv2\n",
                "import numpy as np\n",
                "import matplotlib.pyplot as plt\n",
                "\n",
                "# 2. Cấu hình đường dẫn tới bộ dữ liệu bo mạch DeepPCB mà ta vừa tải về\n",
                "DATASET_DIR = os.path.join(\"..\", \"datasets\", \"pcb_defects\")\n",
                "TRAIN_DIR = os.path.join(DATASET_DIR, \"train_good\")       # 50 ảnh bo mạch chuẩn 100% OK\n",
                "TEST_DIR = os.path.join(DATASET_DIR, \"test_defects\")     # 50 ảnh bo mạch bị lỗi thật\n",
                "ANN_DIR = os.path.join(DATASET_DIR, \"annotations\")      # Tọa độ lỗi do kỹ sư đánh dấu\n",
                "\n",
                "print(\"[*] Thư mục dữ liệu chuẩn OK:\", os.path.abspath(TRAIN_DIR))\n",
                "print(\"[*] Thư mục dữ liệu lỗi thật:\", os.path.abspath(TEST_DIR))\n"
            ]
        },
        {
            "cell_type": "markdown",
            "metadata": {},
            "source": [
                "## 🖼️ BƯỚC 2: ĐỌC VÀ HIỂN THỊ ĐỐI CHIẾU (ẢNH CHUẨN vs ẢNH LỖI THẬT)\n",
                "- Ta lấy cặp ảnh mẫu đầu tiên: `00041000_temp.jpg` (Chuẩn) và `00041000_test.jpg` (Lỗi).\n",
                "- Trên ảnh lỗi, ta dùng đúng tọa độ vừa học: `(539, 259) -> (592, 316)` để vẽ một khung đỏ khoanh vết đứt mạch."
            ]
        },
        {
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [
                "# 1. Đọc ảnh mẫu bo mạch chuẩn (Template OK)\n",
                "img_ok = cv2.imread(os.path.join(TRAIN_DIR, \"00041000_temp.jpg\"))\n",
                "img_ok_rgb = cv2.cvtColor(img_ok, cv2.COLOR_BGR2RGB)\n",
                "\n",
                "# 2. Đọc ảnh mẫu bo mạch bị lỗi thật (Defective Test)\n",
                "img_ng = cv2.imread(os.path.join(TEST_DIR, \"00041000_test.jpg\"))\n",
                "img_ng_rgb = cv2.cvtColor(img_ng, cv2.COLOR_BGR2RGB)\n",
                "\n",
                "# 3. Vẽ khung đỏ bao quanh vết đứt mạch theo tọa độ ta vừa học:\n",
                "#    X1 = 539, Y1 = 259 (Góc Trên - Trái)\n",
                "#    X2 = 592, Y2 = 316 (Góc Dưới - Phải)\n",
                "#    Chiều Rộng = 592 - 539 = 53px, Chiều Cao = 316 - 259 = 57px\n",
                "cv2.rectangle(img_ng_rgb, (539, 259), (592, 316), (255, 0, 0), 3)\n",
                "\n",
                "# 4. Vẽ 2 bức ảnh cạnh nhau để so sánh trực quan bằng Matplotlib\n",
                "plt.figure(figsize=(12, 6))\n",
                "\n",
                "plt.subplot(1, 2, 1)\n",
                "plt.title(\"BO MACH CHUAN 100% OK (TEMPLATE)\", color=\"green\", fontsize=12, fontweight=\"bold\")\n",
                "plt.imshow(img_ok_rgb)\n",
                "plt.axis(\"off\")\n",
                "\n",
                "plt.subplot(1, 2, 2)\n",
                "plt.title(\"BO MACH BI DUT MACH (GROUND TRUTH)\", color=\"red\", fontsize=12, fontweight=\"bold\")\n",
                "plt.imshow(img_ng_rgb)\n",
                "plt.axis(\"off\")\n",
                "\n",
                "plt.tight_layout()\n",
                "plt.show()\n"
            ]
        }
    ],
    "metadata": {
        "language_info": {
            "name": "python"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 2
}

output_path = os.path.join("notebooks", "05_ai_anomaly_detection_lab.ipynb")
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(nb, f, ensure_ascii=False, indent=2)

print("[+] Da tao thanh cong notebook:", output_path)
