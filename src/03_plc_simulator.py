# -*- coding: utf-8 -*-
"""
=============================================================================
BỘ GIẢ LẬP PLC CÔNG NGHIỆP (INDUSTRIAL PLC SIMULATOR - SOCKET SERVER)
Mô phỏng PLC Mitsubishi / Siemens / Omron trong nhà máy:
  - Mở cổng Socket TCP/IP Server tại 127.0.0.1:5000
  - Chờ phần mềm Vision PC Control kết nối vào
  - Định kỳ (1.5s) phát hiện sản phẩm tới -> Gửi lệnh TRIGGER sang Vision PC
  - Nhận lại phán quyết OK/NG từ Vision PC -> Điều khiển xi-lanh gạt hàng
=============================================================================
"""

import socket
import time
import sys

if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

HOST = "127.0.0.1"
PORT = 5000

def run_plc_simulator():
    print("=" * 65)
    print("🏭 [PLC SIMULATOR] KHỞI ĐỘNG HỘP ĐIỀU KHIỂN PLC CÔNG NGHIỆP")
    print(f"📡 Đang mở cổng Socket Server tại {HOST}:{PORT}...")
    print("⏳ Chờ phần mềm Vision PC Control kết nối...")
    print("=" * 65)

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)

    product_id = 100
    try:
        while True:
            print("\n⏳ [PLC SERVER] Đang lắng nghe kết nối từ Vision PC...")
            conn, addr = server_socket.accept()
            print(f"✅ [PLC] Đã kết nối thành công với Vision PC tại địa chỉ: {addr}")
            print("🚀 Bắt đầu kích hoạt cảm biến quang & băng chuyền...\n")
            time.sleep(0.5)

            try:
                while True:
                    product_id += 1
                    trigger_msg = f"TRIGGER,ID={product_id}\n"
                    
                    print("-" * 65)
                    print(f"👀 [PLC SENSOR] Cảm biến phát hiện sản phẩm #{product_id} tới vị trí Camera!")
                    print(f"⚡ [PLC -> VISION] Gửi lệnh bóp cò: '{trigger_msg.strip()}'")
                    
                    conn.sendall(trigger_msg.encode('utf-8'))
                    t_send = time.perf_counter()

                    data = conn.recv(1024).decode('utf-8').strip()
                    t_recv = time.perf_counter()
                    response_time_ms = (t_recv - t_send) * 1000

                    if not data:
                        print("⚠️ [PLC] Vision PC đã ngắt kết nối.")
                        break

                    print(f"📩 [VISION -> PLC] Nhận kết quả: '{data}' ({response_time_ms:.2f}ms)")

                    if "STATUS=OK" in data:
                        print(f"🟢 [PLC ACTUATOR] HÀNG ĐẠT (OK) -> Mở cổng cho qua [BIT Y0=1]")
                    elif "STATUS=NG" in data:
                        print(f"🔴 [PLC ACTUATOR] ⚠️ HÀNG LỖI (NG) -> KÍCH HOẠT XI-LANH GẠT PHẾ PHẨM [BIT Y1=1]")

                    time.sleep(1.8)
            except (ConnectionResetError, ConnectionAbortedError, BrokenPipeError):
                print("⚠️ [PLC] Mất kết nối đột ngột với Vision PC. Đang chờ kết nối mới...")
            finally:
                conn.close()

    except KeyboardInterrupt:
        print("\n🛑 [PLC] Đã dừng bộ giả lập PLC theo yêu cầu người dùng.")
    except Exception as e:
        print(f"\n❌ [PLC ERROR] Lỗi: {e}")
    finally:
        server_socket.close()
        print("🔌 [PLC] Đã đóng cổng Socket Server.")

if __name__ == "__main__":
    run_plc_simulator()
