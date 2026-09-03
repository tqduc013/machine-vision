# -*- coding: utf-8 -*-
"""
=============================================================================
CHUONG TRINH KIEM TRA NGOAI QUAN CONG NGHIEP (INDUSTRIAL AOI INSPECTOR - V1)
Bai toan: Kiem tra vong dem kim loai (Metal Washer Inspection)
Nhiem vu:
  1. Do duong kinh ngoai & duong kinh trong (Metrology Measurement)
  2. Phat hien me vien / khuyet tat hinh hoc (Geometric Chip Defect)
  3. Phat hien vet xuoc be mat (Surface Scratch Defect)
  4. Danh gia OK / NG va do thoi gian chu ky xu ly (Processing Time / Takt Time)
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

# CAU HINH TIEU CHUAN SAN PHAM (STANDARD SPECS)
SPEC_OUTER_RADIUS = 150       # Ban kinh ngoai tieu chuan (pixel)
SPEC_RADIUS_TOLERANCE = 10    # Dung sai cho phep (+- 10 pixel)
SPEC_INNER_RADIUS = 70        # Ban kinh trong tieu chuan (pixel)
SPEC_MIN_CIRCULARITY = 0.88   # Do tron toi thieu (pixel roi rac circularity ~ 0.90)
MAX_SCRATCH_AREA = 20         # Dien tich khuyet tat xuoc be mat toi da cho phep (pixel)

def inspect_product(image_path, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)
    start_time = time.perf_counter()
    
    # 1. DOC ANH (Tuong duong Frame Grabber tu Camera)
    img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img_gray is None:
        print(f"[ERROR] Khong the doc anh tu: {image_path}")
        return
    
    # Tao anh BGR de ve ket qua truc quan
    img_result = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2BGR)
    
    is_ok = True
    ng_reasons = []
    
    # 2. TIEN XU LY (Preprocessing): Loc nhieu Gauss
    blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)
    
    # 3. PHAN NGUONG NHI PHAN (Otsu Thresholding): Tach san pham khoi nen
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # 4. TIM CONTOUR (Tim duong bien ngoai va lo trong)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        is_ok = False
        ng_reasons.append("Khong tim thay san pham (No Product Found)")
    else:
        # Tim contour lon nhat (Vanh ngoai san pham)
        outer_contour = max(contours, key=cv2.contourArea)
        outer_area = cv2.contourArea(outer_contour)
        
        # A. DO DUONG KINH NGOAI (Outer Diameter Measurement)
        (x, y), radius = cv2.minEnclosingCircle(outer_contour)
        center = (int(x), int(y))
        radius = int(radius)
        
        # Kiem tra do tron (Circularity: 4 * pi * Area / Perimeter^2)
        perimeter = cv2.arcLength(outer_contour, True)
        circularity = (4 * np.pi * outer_area) / (perimeter * perimeter) if perimeter > 0 else 0
        
        # Kiem tra dung sai kich thuoc
        if abs(radius - SPEC_OUTER_RADIUS) > SPEC_RADIUS_TOLERANCE:
            is_ok = False
            ng_reasons.append(f"Sai kich thuoc: R={radius}px (Spec: {SPEC_OUTER_RADIUS}+-{SPEC_RADIUS_TOLERANCE})")
            
        # Kiem tra me vien / bien dang
        if circularity < SPEC_MIN_CIRCULARITY:
            is_ok = False
            ng_reasons.append(f"Loi me vien/Bien dang (Do tron: {circularity:.3f} < {SPEC_MIN_CIRCULARITY})")
            
        # B. KIEM TRA VET XUOC BE MAT (Surface Scratch Inspection)
        # Tao Mask vung than san pham (Bo di vien ngoai va lo trong 5 pixel de tranh nhieu bien)
        product_mask = np.zeros_like(img_gray)
        cv2.drawContours(product_mask, [outer_contour], -1, 255, -1)
        # Xoa phan lo trong ra khoi mask
        inner_mask = np.zeros_like(img_gray)
        cv2.circle(inner_mask, center, SPEC_INNER_RADIUS + 5, 255, -1)
        body_mask = cv2.bitwise_and(product_mask, cv2.bitwise_not(inner_mask))
        # Thu hep mask them 4 pixel de khong bat nham vien ngoai
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        body_mask = cv2.erode(body_mask, kernel)
        
        # Tim cac diem toi bat thuong tren than kim loai sang (vet xuoc)
        mean_val = cv2.mean(img_gray, mask=body_mask)[0]
        scratch_thresh = int(mean_val * 0.6) # Diem toi hon 40% muc sang trung binh
        
        _, scratch_bin = cv2.threshold(img_gray, scratch_thresh, 255, cv2.THRESH_BINARY_INV)
        scratch_bin = cv2.bitwise_and(scratch_bin, scratch_bin, mask=body_mask)
        
        scratch_contours, _ = cv2.findContours(scratch_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        scratch_found = False
        for sc in scratch_contours:
            if cv2.contourArea(sc) > MAX_SCRATCH_AREA:
                scratch_found = True
                cv2.drawContours(img_result, [sc], -1, (0, 0, 255), 2) # Khoanh do vet xuoc
                
        if scratch_found:
            is_ok = False
            ng_reasons.append("Loi xuoc be mat (Surface Scratch Detected)")

        # VE KET QUA LEN ANH
        color = (0, 255, 0) if is_ok else (0, 0, 255) # Xanh = OK, Do = NG
        status_text = "STATUS: OK" if is_ok else "STATUS: NG"
        
        # Ve duong tron bao va tam
        cv2.circle(img_result, center, radius, color, 2)
        cv2.circle(img_result, center, 3, (255, 0, 0), -1)
        cv2.putText(img_result, f"R = {radius} px", (center[0] - 40, center[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 0), 2)
        cv2.putText(img_result, f"Circularity: {circularity:.3f}", (center[0] - 65, center[1] + 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # 5. TINH TOAN THOI GIAN XU LY (Processing Time)
    elapsed_ms = (time.perf_counter() - start_time) * 1000.0
    
    # Ve Header ket qua cong nghiep
    header_color = (0, 150, 0) if is_ok else (0, 0, 200)
    cv2.rectangle(img_result, (0, 0), (500, 70), (30, 30, 30), -1)
    cv2.putText(img_result, status_text, (15, 30), cv2.FONT_HERSHEY_DUPLEX, 0.9, header_color, 2)
    cv2.putText(img_result, f"Cycle Time: {elapsed_ms:.2f} ms", (15, 55), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), 1)
    
    # Neu NG thi ghi ro ly do
    if not is_ok:
        for idx, reason in enumerate(ng_reasons):
            cv2.putText(img_result, f"- {reason}", (15, 450 + (idx * 20)), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 1)
            
    # Luu ket qua
    base_name = os.path.basename(image_path)
    save_path = os.path.join(output_dir, f"result_{base_name}")
    cv2.imwrite(save_path, img_result)
    
    print(f"[{'PASS' if is_ok else 'FAIL'}] {base_name:<30} | {status_text:<12} | Time: {elapsed_ms:5.2f} ms")
    if ng_reasons:
        for r in ng_reasons:
            print(f"       --> Ly do NG: {r}")

def main():
    print("=" * 75)
    print("HE THONG KIEM TRA NGOAI QUAN TU DONG (AOI INSPECTOR) - RUNNING...")
    print("=" * 75)
    
    sample_files = sorted(glob.glob("samples/*.png"))
    if not sample_files:
        print("[WARNING] Chua co anh mau trong thu muc samples/. Dang tao mau...")
        import generate_samples
        generate_samples.generate_samples()
        sample_files = sorted(glob.glob("samples/*.png"))
        
    for img_p in sample_files:
        inspect_product(img_p)
        
    print("=" * 75)
    print(f"[HOAN TAT] Toan bo anh ket qua da duoc luu tai thu muc: 'output/'")
    print("=" * 75)

if __name__ == "__main__":
    main()
