# -*- coding: utf-8 -*-
"""
=============================================================================
HE THONG KIEM TRA AOI HOAN CHINH (TRON VEN QUY TRINH 4 CHU G)
Doi tuong: Chip ban dan (IC Package Inspection)
Quy trinh 4 buoc chuan nha may FDI:
  1. GUIDANCE: Dinh vi vi tri tam (X, Y) va goc nghieng -> Xoay chip thang lai 0 do
  2. IDENTIFICATION: Doc ma QR Code in tren chip de lay so Serial
  3. GAUGING: Do chieu dai, chieu rong cua chip (Dung sai +-10 pixel)
  4. INSPECTION: Soi loi me goc (Chipped corner) va loi xuoc be mat (Scratch)
=============================================================================
"""

import os
import sys
import time
import glob
import cv2
import numpy as np

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# TIEU CHUAN SAN PHAM (SPECS)
SPEC_WIDTH = 220        # Chieu dai chuan (pixel)
SPEC_HEIGHT = 140       # Chieu rong chuan (pixel)
SPEC_TOLERANCE = 12     # Dung sai cho phep (+- 12 pixel)

qr_detector = cv2.QRCodeDetector()

def inspect_chip_4g(image_path, output_dir="output_chip"):
    os.makedirs(output_dir, exist_ok=True)
    start_time = time.perf_counter()
    
    img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img_gray is None:
        print(f"[ERROR] Khong doc duoc anh: {image_path}")
        return
    
    img_result = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    is_ok = True
    ng_reasons = []
    
    # -------------------------------------------------------------
    # 1️⃣ BƯỚC 1: GUIDANCE (Định vị & Xoay thẳng sản phẩm)
    # -------------------------------------------------------------
    # Tách nền (Magic Wand)
    blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print(f"[FAIL] Khong tim thay chip trong anh: {image_path}")
        return
        
    main_contour = max(contours, key=cv2.contourArea)
    
    # Tim hinh chu nhat bao quanh xoay goc (MinAreaRect)
    rect = cv2.minAreaRect(main_contour)
    (center_x, center_y), (rect_w, rect_h), angle = rect
    
    # Hieu chinh goc xoay de chieu dai luon nam ngang
    if rect_w < rect_h:
        rect_w, rect_h = rect_h, rect_w
        angle = angle + 90.0
        
    # Thuc hien phep xoay anh ve 0 do (Straighten the image)
    M = cv2.getRotationMatrix2D((center_x, center_y), angle, 1.0)
    straightened = cv2.warpAffine(img_gray, M, (img_gray.shape[1], img_gray.shape[0]), borderValue=35)
    
    # Crop lay rieng con chip da duoc xoay thang
    x1 = max(0, int(center_x - rect_w // 2))
    y1 = max(0, int(center_y - rect_h // 2))
    x2 = min(straightened.shape[1], int(center_x + rect_w // 2))
    y2 = min(straightened.shape[0], int(center_y + rect_h // 2))
    chip_crop = straightened[y1:y2, x1:x2]

    # -------------------------------------------------------------
    # 2️⃣ BƯỚC 2: IDENTIFICATION (Đọc mã QR Serial)
    # -------------------------------------------------------------
    serial_text, decoded_info, _ = qr_detector.detectAndDecode(chip_crop)
    if not serial_text:
        # Neu crop hoi sat, thu doc tren toan bo anh da xoay
        serial_text, decoded_info, _ = qr_detector.detectAndDecode(straightened)
        
    if not serial_text:
        serial_text = "UNKNOWN_QR"
        is_ok = False
        ng_reasons.append("Loi doc ma QR (QR Code Decode Failed)")

    # -------------------------------------------------------------
    # 3️⃣ BƯỚC 3: GAUGING (Đo đạc kích thước)
    # -------------------------------------------------------------
    measured_w = int(rect_w)
    measured_h = int(rect_h)
    
    diff_w = abs(measured_w - SPEC_WIDTH)
    diff_h = abs(measured_h - SPEC_HEIGHT)
    
    if diff_w > SPEC_TOLERANCE or diff_h > SPEC_TOLERANCE:
        is_ok = False
        ng_reasons.append(f"Sai kich thuoc: {measured_w}x{measured_h}px (Spec: {SPEC_WIDTH}x{SPEC_HEIGHT})")

    # -------------------------------------------------------------
    # 4️⃣ BƯỚC 4: INSPECTION (Soi lỗi xước & mẻ góc)
    # -------------------------------------------------------------
    # Kiem tra 4 goc cua con chip da xoay thang (Corner Integrity Check)
    if chip_crop.size > 0:
        ch_h, ch_w = chip_crop.shape
        corner_size = 12
        # 4 vung goc: Tren-Trai, Tren-Phai, Duoi-Trai, Duoi-Phai
        corners = {
            "Goc Tren-Trai": chip_crop[0:corner_size, 0:corner_size],
            "Goc Tren-Phai": chip_crop[0:corner_size, ch_w-corner_size:ch_w],
            "Goc Duoi-Trai": chip_crop[ch_h-corner_size:ch_h, 0:corner_size],
            "Goc Duoi-Phai": chip_crop[ch_h-corner_size:ch_h, ch_w-corner_size:ch_w]
        }
        for corner_name, c_img in corners.items():
            if c_img.size > 0:
                # Goc chip phai la vat the (sang hon 60), neu toan mau toi nen (<60) la bi me goc
                avg_val = np.mean(c_img)
                if avg_val < 70: # Bi khuyet mat goc
                    is_ok = False
                    ng_reasons.append(f"Loi me/sut goc chip ({corner_name})")

        # Kiem tra vet xuoc tren vung than chip crop
        scratch_roi = chip_crop[int(ch_h*0.65):ch_h-5, 10:ch_w-10] # Vung nua duoi than chip
        if scratch_roi.size > 0:
            _, scratch_bin = cv2.threshold(scratch_roi, 80, 255, cv2.THRESH_BINARY_INV)
            scratch_cnts, _ = cv2.findContours(scratch_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for sc in scratch_cnts:
                if cv2.contourArea(sc) > 15: # Co vet xuoc dai
                    is_ok = False
                    ng_reasons.append("Loi xuoc be mat than chip (Surface Scratch Detected)")
                    break

    # -------------------------------------------------------------
    # TỔNG HỢP VÀ VẼ KẾT QUẢ TRỰC QUAN LÊN ẢNH
    # -------------------------------------------------------------
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    
    # Ve khung bao xoay quanh con chip tren anh goc
    box = cv2.boxPoints(rect)
    box = np.int32(box)
    box_color = (0, 255, 0) if is_ok else (0, 0, 255)
    cv2.drawContours(img_result, [box], 0, box_color, 2)
    
    # Header ket qua
    status_text = "STATUS: OK" if is_ok else "STATUS: NG"
    header_color = (0, 160, 0) if is_ok else (0, 0, 220)
    cv2.rectangle(img_result, (0, 0), (600, 85), (25, 25, 25), -1)
    
    cv2.putText(img_result, f"{status_text} | ID: {serial_text}", (15, 30),
                cv2.FONT_HERSHEY_DUPLEX, 0.75, header_color, 2)
    cv2.putText(img_result, f"Goc nghieng: {angle:.1f} deg | Size: {measured_w}x{measured_h} px | Time: {elapsed_ms:.2f} ms", 
                (15, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.48, (200, 200, 200), 1)
    cv2.putText(img_result, f"Pipeline: 1.Guidance -> 2.QR -> 3.Gauging -> 4.Inspection", (15, 75), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.42, (180, 180, 180), 1)

    # In ly do loi neu NG
    if not is_ok:
        for idx, r in enumerate(ng_reasons):
            cv2.putText(img_result, f"[NG] {r}", (15, 540 + (idx * 22)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)

    # Chen anh chip da xoay thang vao goc duoi ben phai lam preview
    if chip_crop.size > 0:
        preview_h, preview_w = 70, 110
        preview = cv2.resize(chip_crop, (preview_w, preview_h))
        preview_bgr = cv2.cvtColor(preview, cv2.COLOR_GRAY2BGR)
        cv2.rectangle(img_result, (470, 510), (470 + preview_w + 4, 510 + preview_h + 4), (200, 200, 200), 1)
        img_result[512:512+preview_h, 472:472+preview_w] = preview_bgr
        cv2.putText(img_result, "Straight View", (472, 505), cv2.FONT_HERSHEY_SIMPLEX, 0.38, (200, 200, 200), 1)

    # Luu file
    base_name = os.path.basename(image_path)
    save_path = os.path.join(output_dir, f"result_{base_name}")
    cv2.imwrite(save_path, img_result)
    
    print(f"[{'PASS' if is_ok else 'FAIL'}] {base_name:<32} | {status_text:<12} | QR: {serial_text:<20} | Time: {elapsed_ms:5.2f} ms")
    if ng_reasons:
        for r in ng_reasons:
            print(f"       --> {r}")

def main():
    print("=" * 85)
    print("HE THONG AOI CONG NGHIEP - KIEM TRA TOAN DIEN 4 CHU G (GUIDANCE - ID - GAUGING - INSPECTION)")
    print("=" * 85)
    
    sample_files = sorted(glob.glob("samples_chip/*.png"))
    if not sample_files:
        print("[WARNING] Chua co anh mau. Dang sinh anh chip mau...")
        import generate_chip_samples
        generate_chip_samples.generate_chip_samples()
        sample_files = sorted(glob.glob("samples_chip/*.png"))
        
    for img_p in sample_files:
        inspect_chip_4g(img_p)
        
    print("=" * 85)
    print(f"[HOAN TAT] Toan bo anh ket qua 4G da duoc luu tai: 'output_chip/'")
    print("=" * 85)

if __name__ == "__main__":
    main()
