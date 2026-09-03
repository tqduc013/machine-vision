# -*- coding: utf-8 -*-
"""
Script sinh anh mau cong nghiep gia lap (Industrial Sample Generator)
Tao cac san pham mau: Vong dem kim loai (Washer)
Bao gom: Mau chuan (OK) va Cac mau loi ngoai quan (NG - XUOC, ME VIEN, SAI KICH THUOC)
"""

import os
import sys
import cv2
import numpy as np

# Dam bao in tieng Viet hoac UTF-8 khong bi loi tren Windows console
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def generate_samples(output_dir="samples"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. MAU OK - Vong dem kim loai tieu chuan
    img_ok = np.full((500, 500), 40, dtype=np.uint8) # Nen toi
    cv2.circle(img_ok, (250, 250), 150, 200, -1)     # Vanh ngoai R=150
    cv2.circle(img_ok, (250, 250), 70, 40, -1)       # Lo trong R=70
    noise = np.random.normal(0, 2, img_ok.shape).astype(np.int16)
    img_ok = np.clip(img_ok.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    cv2.imwrite(os.path.join(output_dir, "sample_01_OK.png"), img_ok)

    # 2. MAU NG_01 - Loi xuoc be mat (Surface Scratch)
    img_ng1 = img_ok.copy()
    cv2.line(img_ng1, (200, 160), (310, 210), 50, 3)
    cv2.imwrite(os.path.join(output_dir, "sample_02_NG_scratch.png"), img_ng1)

    # 3. MAU NG_02 - Loi me/khuyet canh ngoai (Chip Defect)
    img_ng2 = img_ok.copy()
    cv2.circle(img_ng2, (390, 250), 25, 40, -1)
    cv2.imwrite(os.path.join(output_dir, "sample_03_NG_chip.png"), img_ng2)

    # 4. MAU NG_03 - Loi sai kich thuoc (Undersize)
    img_ng3 = np.full((500, 500), 40, dtype=np.uint8)
    cv2.circle(img_ng3, (250, 250), 120, 200, -1)    # R=120 thay vi 150
    cv2.circle(img_ng3, (250, 250), 70, 40, -1)
    cv2.imwrite(os.path.join(output_dir, "sample_04_NG_undersize.png"), img_ng3)

    print(f"[OK] Da tao thanh cong 4 anh mau cong nghiep trong thu muc: '{output_dir}'")

if __name__ == "__main__":
    generate_samples()
