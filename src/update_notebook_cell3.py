import json
import os

nb_path = os.path.join("notebooks", "05_ai_anomaly_detection_lab.ipynb")
with open(nb_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

cell_md = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "## 🧩 BƯỚC 3: CƠ CHẾ PATCHCORE - CẮT ẢNH THÀNH 400 MẢNH GHÉP (PATCHES)\n",
        "- Kích thước ảnh: 640 x 640 pixel.\n",
        "- Kích thước mỗi mảnh Patch: 32 x 32 pixel.\n",
        "- Tổng số mảnh: (640 / 32) x (640 / 32) = 400 mảnh Patch!\n",
        "- Ta cắt 1 mảnh bình thường và 1 mảnh bị đứt mạch để quan sát dưới góc nhìn của kính lúp AI."
    ]
}

cell_code = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "# 1. Định nghĩa kích thước mảnh ghép\n",
        "PATCH_SIZE = 32  # 32 x 32 pixel\n",
        "\n",
        "# 2. Cắt 1 mảnh bình thường trên bo mạch chuẩn (X=128, Y=128)\n",
        "patch_normal = img_ok_rgb[128:128+PATCH_SIZE, 128:128+PATCH_SIZE]\n",
        "\n",
        "# 3. Cắt 1 mảnh bị đứt mạch trên bo mạch lỗi (X=544, Y=288 - nằm đúng trong hộp đỏ!)\n",
        "patch_defect = img_ng_rgb[288:288+PATCH_SIZE, 544:544+PATCH_SIZE]\n",
        "\n",
        "# 4. Hiển thị cận cảnh 2 mảnh ghép để mắt và AI cùng soi\n",
        "plt.figure(figsize=(8, 4))\n",
        "\n",
        "plt.subplot(1, 2, 1)\n",
        "plt.title('MANH CHUAN (32x32px) - Duong dong lien mach', color='green', fontweight='bold')\n",
        "plt.imshow(patch_normal)\n",
        "plt.axis('off')\n",
        "\n",
        "plt.subplot(1, 2, 2)\n",
        "plt.title('MANH BI LOI (32x32px) - Bi dut toac o giua', color='red', fontweight='bold')\n",
        "plt.imshow(patch_defect)\n",
        "plt.axis('off')\n",
        "\n",
        "plt.tight_layout()\n",
        "plt.show()\n",
        "\n",
        "print('[*] Buc anh 640x640 duoc chia thanh: (640/32) x (640/32) = 400 manh Patch!')\n"
    ]
}

if len(nb["cells"]) <= 5:
    nb["cells"].extend([cell_md, cell_code])
    with open(nb_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, ensure_ascii=False, indent=2)
    print("[+] Da cap nhat Cell 3 vao notebook thanh cong!")
else:
    print("[*] Notebook da co Cell 3.")
