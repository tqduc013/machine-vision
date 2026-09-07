import os
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE_URL = "https://raw.githubusercontent.com/tangsanli5201/DeepPCB/master/PCBData/group00041"
TARGET_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "datasets", "pcb_defects")

TRAIN_DIR = os.path.join(TARGET_DIR, "train_good")
TEST_DIR = os.path.join(TARGET_DIR, "test_defects")
ANNOTATION_DIR = os.path.join(TARGET_DIR, "annotations")

for d in [TRAIN_DIR, TEST_DIR, ANNOTATION_DIR]:
    os.makedirs(d, exist_ok=True)

def download_file(url, save_path):
    try:
        if os.path.exists(save_path) and os.path.getsize(save_path) > 0:
            return True
        urllib.request.urlretrieve(url, save_path)
        return True
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main(num_pairs=50):
    print(f"[*] Bat dau tai {num_pairs} cap anh bo mach PCB thuc te...")
    print(f"[*] Thu muc luu: {TARGET_DIR}")
    
    tasks = []
    # group00041 files: 00041000 to 00041099
    with ThreadPoolExecutor(max_workers=10) as executor:
        for i in range(num_pairs):
            idx_str = f"00041{i:03d}"
            
            # 1. Template (Good) image
            temp_url = f"{BASE_URL}/00041/{idx_str}_temp.jpg"
            temp_path = os.path.join(TRAIN_DIR, f"{idx_str}_temp.jpg")
            tasks.append(executor.submit(download_file, temp_url, temp_path))
            
            # 2. Test (Defect) image
            test_url = f"{BASE_URL}/00041/{idx_str}_test.jpg"
            test_path = os.path.join(TEST_DIR, f"{idx_str}_test.jpg")
            tasks.append(executor.submit(download_file, test_url, test_path))
            
            # 3. Annotation file
            ann_url = f"{BASE_URL}/00041_not/{idx_str}.txt"
            ann_path = os.path.join(ANNOTATION_DIR, f"{idx_str}.txt")
            tasks.append(executor.submit(download_file, ann_url, ann_path))
            
        success_count = sum(1 for t in tasks if t.result())
        
    total_size = 0
    for root, _, files in os.walk(TARGET_DIR):
        for f in files:
            total_size += os.path.getsize(os.path.join(root, f))
            
    print(f"[+] Hoan tat tai {success_count}/{len(tasks)} files!")
    print(f"[+] Tong dung luong dataset tren o dia: {total_size / (1024 * 1024):.2f} MB")

if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 50
    main(n)
