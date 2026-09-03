# -*- coding: utf-8 -*-
"""
=============================================================================
PHẦN MỀM VISION PC CONTROL CÔNG NGHIỆP ĐA LUỒNG + WEBSOCKET BRIDGE
Tích hợp:
  - TẦNG 1: Lắng nghe Trigger từ PLC (Socket TCP :5000)
  - TẦNG 2: Xử lý ảnh 4G ngầm (Worker Thread)
  - TẦNG 3: Bắt tay PLC phản hồi OK/NG
  - TẦNG 4: Ghi nhật ký CSV
  - TRẠM PHÁT WEBSOCKET: Bắn dữ liệu phán quyết thời gian thực lên Web 3D Dashboard (ws://127.0.0.1:8765)
=============================================================================
"""

import os
import sys
import time
import socket
import threading
import queue
import glob
import json
import asyncio
import cv2
import numpy as np
import websockets

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HOST_PLC = "127.0.0.1"
PORT_PLC = 5000
WS_PORT = 8765

SPEC_WIDTH = 220
SPEC_HEIGHT = 140
SPEC_TOLERANCE = 12

qr_detector = cv2.QRCodeDetector()
job_queue = queue.Queue(maxsize=50)

# Danh sách các Web Client đang kết nối
connected_websockets = set()
ws_loop = None

stats_lock = threading.Lock()
stats = {
    "total": 0,
    "ok": 0,
    "ng": 0,
    "last_cycle_time": 0.0
}

# -------------------------------------------------------------
# WEBSOCKET BROADCASTER (BẮN SỰ KIỆN LÊN GIAO DIỆN WEB 3D)
# -------------------------------------------------------------
async def ws_handler(websocket):
    connected_websockets.add(websocket)
    print(f"🌐 [WEBSOCKET] Đã có 1 Web Dashboard kết nối (Tổng: {len(connected_websockets)})")
    
    # Gửi ngay gói tin chào mừng & trạng thái hiện tại
    with stats_lock:
        yield_rate = (stats["ok"] / stats["total"] * 100) if stats["total"] > 0 else 100.0
        init_payload = {
            "type": "SYSTEM_STATUS",
            "msg": "CONNECTED_TO_PYTHON_BACKEND",
            "stats": {
                "total": stats["total"],
                "ok": stats["ok"],
                "ng": stats["ng"],
                "yieldRate": f"{yield_rate:.1f}",
                "cycleTime": f"{stats['last_cycle_time']:.2f}"
            }
        }
    await websocket.send(json.dumps(init_payload))

    try:
        async for message in websocket:
            # Nhận lệnh điều khiển thủ công từ Web nếu có
            pass
    except websockets.ConnectionClosed:
        pass
    finally:
        connected_websockets.remove(websocket)
        print(f"🌐 [WEBSOCKET] 1 Web Dashboard đã ngắt kết nối (Còn lại: {len(connected_websockets)})")

def broadcast_to_web(data_dict):
    if not connected_websockets or ws_loop is None:
        return
    message_json = json.dumps(data_dict)
    for ws in list(connected_websockets):
        asyncio.run_coroutine_threadsafe(ws.send(message_json), ws_loop)

def run_ws_server():
    global ws_loop
    ws_loop = asyncio.new_event_loop()
    asyncio.set_event_loop(ws_loop)
    
    async def start():
        async with websockets.serve(ws_handler, "127.0.0.1", WS_PORT):
            print(f"🌐 [WEBSOCKET SERVER] Đang phát sóng trực tiếp tại ws://127.0.0.1:{WS_PORT}")
            await asyncio.Future()

    ws_loop.run_until_complete(start())

# -------------------------------------------------------------
# THUẬT TOÁN VISION 4G LÕI
# -------------------------------------------------------------
def process_4g_inspection(image_path, product_id):
    t_start = time.perf_counter()
    img_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    if img_gray is None:
        return {"status": "NG", "reason": "READ_FAIL", "cycle_ms": 0.0, "serial": "NONE"}
        
    is_ok = True
    ng_reasons = []

    # 1. GUIDANCE
    blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)
    _, thresh = cv2.threshold(blurred, 60, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if not contours:
        return {"status": "NG", "reason": "NO_OBJECT", "cycle_ms": 0.0, "serial": "NONE"}
        
    main_contour = max(contours, key=cv2.contourArea)
    rect = cv2.minAreaRect(main_contour)
    (center_x, center_y), (rect_w, rect_h), angle = rect
    
    if rect_w < rect_h:
        rect_w, rect_h = rect_h, rect_w
        angle = angle + 90.0
        
    M = cv2.getRotationMatrix2D((center_x, center_y), angle, 1.0)
    straightened = cv2.warpAffine(img_gray, M, (img_gray.shape[1], img_gray.shape[0]), borderValue=35)
    
    x1 = max(0, int(center_x - rect_w // 2))
    y1 = max(0, int(center_y - rect_h // 2))
    x2 = min(straightened.shape[1], int(center_x + rect_w // 2))
    y2 = min(straightened.shape[0], int(center_y + rect_h // 2))
    chip_crop = straightened[y1:y2, x1:x2]

    # 2. IDENTIFICATION
    serial_text, _, _ = qr_detector.detectAndDecode(chip_crop)
    if not serial_text:
        serial_text, _, _ = qr_detector.detectAndDecode(straightened)
    if not serial_text:
        serial_text = "UNKNOWN_SERIAL"
        is_ok = False
        ng_reasons.append("QR_FAIL")

    # 3. GAUGING
    measured_w = int(rect_w)
    measured_h = int(rect_h)
    if abs(measured_w - SPEC_WIDTH) > SPEC_TOLERANCE or abs(measured_h - SPEC_HEIGHT) > SPEC_TOLERANCE:
        is_ok = False
        ng_reasons.append("DIMENSION_NG")

    # 4. INSPECTION
    has_chip_off = False
    has_scratch = False
    if chip_crop.size > 0 and chip_crop.shape[0] >= 40 and chip_crop.shape[1] >= 40:
        ch, cw = chip_crop.shape[:2]

        # A. Soi góc trên-phải (Top-Right) tìm lỗi mẻ góc
        corner_tr = chip_crop[0:20, cw-20:cw]
        if corner_tr.size > 0 and np.mean(corner_tr) < 70.0:
            is_ok = False
            has_chip_off = True
            ng_reasons.append("CHIP_OFF_NG")

        # B. Soi vùng nửa dưới thân chip tìm vết xước (tránh vùng chữ laser ở trên)
        scratch_roi = chip_crop[int(ch * 0.65):ch - 5, 10:cw - 10]
        if scratch_roi.size > 0:
            _, scratch_bin = cv2.threshold(scratch_roi, 80, 255, cv2.THRESH_BINARY_INV)
            scratch_cnts, _ = cv2.findContours(scratch_bin, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for sc in scratch_cnts:
                if cv2.contourArea(sc) > 15:
                    is_ok = False
                    has_scratch = True
                    ng_reasons.append("SCRATCH_NG")
                    break

    t_end = time.perf_counter()
    cycle_time_ms = (t_end - t_start) * 1000

    verdict_status = "OK" if is_ok else "NG"
    reason_str = "PASSED" if is_ok else "|".join(ng_reasons)
    
    return {
        "status": verdict_status,
        "reason": reason_str,
        "serial": serial_text,
        "cycle_ms": cycle_time_ms,
        "width": measured_w,
        "height": measured_h,
        "angle": angle,
        "hasScratch": has_scratch,
        "hasChipOff": has_chip_off
    }

# -------------------------------------------------------------
# WORKER THREAD (XỬ LÝ ẢNH & BẮN WEBSOCKET LÊN WEB)
# -------------------------------------------------------------
def vision_worker_thread(sock, sample_images, stop_event):
    sample_idx = 0
    os.makedirs("output", exist_ok=True)
    log_file_path = os.path.join("output", "production_log.csv")

    if not os.path.exists(log_file_path):
        with open(log_file_path, "w", encoding="utf-8") as f:
            f.write("Timestamp,ProductID,Serial,Width_px,Height_px,Angle_deg,Verdict,Reason,CycleTime_ms\n")

    while not stop_event.is_set():
        try:
            job = job_queue.get(timeout=0.5)
        except queue.Empty:
            continue

        prod_id = job["prod_id"]
        img_path = sample_images[sample_idx]
        sample_idx = (sample_idx + 1) % len(sample_images)

        # Chạy thuật toán 4G
        result = process_4g_inspection(img_path, prod_id)

        # Cập nhật thống kê
        with stats_lock:
            stats["total"] += 1
            if result["status"] == "OK":
                stats["ok"] += 1
            else:
                stats["ng"] += 1
            stats["last_cycle_time"] = result["cycle_ms"]
            yield_rate = (stats["ok"] / stats["total"]) * 100

        now_str = time.strftime("%H:%M:%S")

        # In Console
        status_color = "🟢 OK" if result["status"] == "OK" else "🔴 NG"
        print(f"\n[WORKER] ⚙️ Sản phẩm #{prod_id} -> {status_color} ({result['reason']}) | {result['cycle_ms']:.2f}ms | Serial: {result['serial']}")

        # Ghi CSV
        with open(log_file_path, "a", encoding="utf-8") as f:
            f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')},{prod_id},{result['serial']},{result.get('width', 0)},{result.get('height', 0)},{result.get('angle', 0):.1f},{result['status']},{result['reason']},{result['cycle_ms']:.2f}\n")

        # Bắn kết quả về cho PLC qua Socket
        response_msg = f"RESULT,ID={prod_id},STATUS={result['status']},DEFECT={result['reason']},CYCLE_MS={result['cycle_ms']:.2f}\n"
        try:
            sock.sendall(response_msg.encode('utf-8'))
        except Exception as e:
            print(f"  └─ ❌ [ERROR] Gửi PLC: {e}")

        # 🌐 BẮN TRỰC TIẾP LÊN GIAO DIỆN WEB 3D DASHBOARD QUA WEBSOCKET
        web_payload = {
            "type": "INSPECTION_RESULT",
            "prodId": prod_id,
            "serial": result["serial"],
            "width": result["width"],
            "height": result["height"],
            "angle": round(result["angle"], 1),
            "status": result["status"],
            "reason": result["reason"],
            "hasScratch": result["hasScratch"],
            "hasChipOff": result["hasChipOff"],
            "cycleTimeMs": f"{result['cycle_ms']:.2f}",
            "timestamp": now_str,
            "stats": {
                "total": stats["total"],
                "ok": stats["ok"],
                "ng": stats["ng"],
                "yieldRate": f"{yield_rate:.1f}"
            }
        }
        broadcast_to_web(web_payload)

        job_queue.task_done()

# -------------------------------------------------------------
# MAIN NETWORK CLIENT
# -------------------------------------------------------------
def run_vision_controller():
    print("=" * 65)
    print("🖥️ [VISION PC CONTROL] KHỞI ĐỘNG HỆ THỐNG ĐA LUỒNG + WEBSOCKET")
    print(f"📡 WebSocket Server phát sóng tại ws://127.0.0.1:{WS_PORT}")
    print("=" * 65)

    sample_images = sorted(glob.glob("samples_chip/*.png"))
    if not sample_images:
        print("❌ [ERROR] Không tìm thấy ảnh trong samples_chip/!")
        return

    # Khởi động WebSocket Server ở luồng riêng
    ws_thread = threading.Thread(target=run_ws_server, daemon=True)
    ws_thread.start()
    time.sleep(0.5)

    while True:
        print(f"\n🔗 Đang thử kết nối tới PLC Server tại {HOST_PLC}:{PORT_PLC}...")
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            client_socket.connect((HOST_PLC, PORT_PLC))
            print("✅ [VISION PC] Đã kết nối thành công tới PLC!")
        except Exception as e:
            print(f"⏳ [RETRY] Chưa thấy PLC Server online ({HOST_PLC}:{PORT_PLC}). Đang thử lại sau 2 giây...")
            client_socket.close()
            time.sleep(2)
            continue

        stop_event = threading.Event()
        worker = threading.Thread(target=vision_worker_thread, args=(client_socket, sample_images, stop_event), daemon=True)
        worker.start()

        print("🚀 Worker Thread & WebSocket Bridge đã sẵn sàng. Đang chờ Trigger từ PLC...\n")

        buffer = ""
        try:
            while True:
                data = client_socket.recv(1024).decode('utf-8')
                if not data:
                    print("⚠️ [VISION PC] PLC đã ngắt kết nối.")
                    break
                buffer += data
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if line.startswith("TRIGGER"):
                        parts = line.split(",")
                        prod_id = "0"
                        for p in parts:
                            if p.startswith("ID="):
                                prod_id = p.split("=")[1]

                        job_queue.put({"prod_id": prod_id})

        except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError) as e:
            print(f"⚠️ [VISION PC] Mất kết nối PLC ({e}). Đang chuẩn bị tự động kết nối lại...")
        except KeyboardInterrupt:
            print("\n🛑 [VISION PC] Dừng hệ thống...")
            stop_event.set()
            client_socket.close()
            break
        finally:
            stop_event.set()
            client_socket.close()
            time.sleep(2)

if __name__ == "__main__":
    run_vision_controller()
