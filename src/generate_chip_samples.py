# -*- coding: utf-8 -*-
"""
Script tao anh mau chip ban dan / IC cong nghiep co chua ma QR (Chip Sample Generator)
Tao cac mau chip nam nghieng cac goc khac nhau (-30 do, +25 do, +45 do):
  - Mau 1: Chip chuan (OK)
  - Mau 2: Chip loi xuoc be mat (NG - Scratch)
  - Mau 3: Chip loi me goc / sai kich thuoc (NG - Chipped Corner)
"""

import os
import sys
import cv2
import qrcode
import numpy as np

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def create_chip_image(serial_text, has_scratch=False, has_chip=False, size=(220, 140)):
    # 1. Tao con chip thang 0 do tren nen xam kim loai
    chip = np.full((size[1], size[0]), 180, dtype=np.uint8)
    
    # Tao vien den silicon quanh chip
    cv2.rectangle(chip, (0, 0), (size[0]-1, size[1]-1), 50, 4)
    
    # 2. Sinh ma QR Code tu dong
    qr = qrcode.QRCode(version=1, box_size=2, border=1)
    qr.add_data(serial_text)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    qr_np = np.array(qr_img.convert('L'))
    
    # Dan ma QR vao goc trai con chip
    qh, qw = qr_np.shape
    chip[20:20+qh, 20:20+qw] = qr_np
    
    # In chu ky hieu len chip
    cv2.putText(chip, "IC-A18 PRO", (20 + qw + 10, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.45, 30, 1)
    cv2.putText(chip, "2026-FDI", (20 + qw + 10, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.4, 60, 1)
    
    # 3. Tao khuyet tat neu co
    if has_scratch:
        cv2.line(chip, (30, 110), (190, 125), 30, 2) # Vet xuoc ngang than chip
    if has_chip:
        cv2.circle(chip, (size[0]-5, 10), 18, 40, -1)  # Me mat mot goc
        
    return chip

def place_and_rotate_chip(chip, angle, canvas_size=(600, 600)):
    # Dat chip vao giua canvas toi mau va xoay goc bat ky
    canvas = np.full(canvas_size, 35, dtype=np.uint8) # Nen bang chuyen
    cx, cy = canvas_size[0] // 2, canvas_size[1] // 2
    ch, cw = chip.shape
    
    # Dan chip vao giua canvas
    x1, y1 = cx - cw // 2, cy - ch // 2
    canvas[y1:y1+ch, x1:x1+cw] = chip
    
    # Xoay canvas quanh tam (cx, cy)
    M = cv2.getRotationMatrix2D((cx, cy), angle, 1.0)
    rotated = cv2.warpAffine(canvas, M, canvas_size, borderValue=35)
    
    # Them chut nhieu quang hoc
    noise = np.random.normal(0, 2, canvas_size).astype(np.int16)
    result = np.clip(rotated.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return result

def generate_chip_samples(output_dir="samples_chip"):
    os.makedirs(output_dir, exist_ok=True)
    
    # 1. Chip OK - Xoay nghieng +25 do
    chip1 = create_chip_image("SN-APPLE-A18-001")
    img1 = place_and_rotate_chip(chip1, angle=25)
    cv2.imwrite(os.path.join(output_dir, "chip_01_OK_tilted25.png"), img1)
    
    # 2. Chip NG Scratch - Xoay nghieng -35 do (Loi xuoc)
    chip2 = create_chip_image("SN-APPLE-A18-002", has_scratch=True)
    img2 = place_and_rotate_chip(chip2, angle=-35)
    cv2.imwrite(os.path.join(output_dir, "chip_02_NG_scratch_tilted35.png"), img2)
    
    # 3. Chip NG Chipped - Xoay nghieng +50 do (Loi me goc)
    chip3 = create_chip_image("SN-APPLE-A18-003", has_chip=True)
    img3 = place_and_rotate_chip(chip3, angle=50)
    cv2.imwrite(os.path.join(output_dir, "chip_03_NG_chip_tilted50.png"), img3)
    
    print(f"[OK] Da tao thanh cong 3 anh mau Chip ban dan nghieng trong thu muc: '{output_dir}'")

if __name__ == "__main__":
    generate_chip_samples()
