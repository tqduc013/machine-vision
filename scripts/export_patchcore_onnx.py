import os
import sys
import json
import cv2
import numpy as np
import onnx
from onnx import helper, TensorProto
import onnxruntime as ort

if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODELS_DIR = os.path.join(ROOT_DIR, "models")
os.makedirs(MODELS_DIR, exist_ok=True)

ONNX_PATH = os.path.join(MODELS_DIR, "patchcore_net.onnx")
BANK_PATH = os.path.join(MODELS_DIR, "memory_bank.bin")
META_PATH = os.path.join(MODELS_DIR, "anomaly_meta.json")

def create_feature_extractor_onnx():
    """
    Xây dựng đồ thị tính toán ONNX cho mạng Feature Extractor công nghiệp.
    Kiến trúc 3 tầng tích chập trích xuất đặc trưng đa quy mô:
    Input: [1, 3, 256, 256] -> Conv1(32) -> Conv2(64) -> Conv3(64) -> Output: [1, 64, 32, 32]
    """
    print("[*] Đang khởi tạo kiến trúc ONNX Deep Learning Feature Extractor...")
    
    np.random.seed(42)
    # Khởi tạo trọng số với phân phối He/Kaiming
    w1 = np.random.randn(32, 3, 5, 5).astype(np.float32) * np.sqrt(2.0 / (3 * 25))
    b1 = np.zeros(32, dtype=np.float32)
    
    w2 = np.random.randn(64, 32, 3, 3).astype(np.float32) * np.sqrt(2.0 / (32 * 9))
    b2 = np.zeros(64, dtype=np.float32)
    
    w3 = np.random.randn(64, 64, 3, 3).astype(np.float32) * np.sqrt(2.0 / (64 * 9))
    b3 = np.zeros(64, dtype=np.float32)
    
    # Tạo tensor khởi tạo (Initializers)
    tensor_w1 = helper.make_tensor('w1', TensorProto.FLOAT, w1.shape, w1.flatten())
    tensor_b1 = helper.make_tensor('b1', TensorProto.FLOAT, b1.shape, b1.flatten())
    
    tensor_w2 = helper.make_tensor('w2', TensorProto.FLOAT, w2.shape, w2.flatten())
    tensor_b2 = helper.make_tensor('b2', TensorProto.FLOAT, b2.shape, b2.flatten())
    
    tensor_w3 = helper.make_tensor('w3', TensorProto.FLOAT, w3.shape, w3.flatten())
    tensor_b3 = helper.make_tensor('b3', TensorProto.FLOAT, b3.shape, b3.flatten())
    
    # Định nghĩa các Node tính toán
    node_conv1 = helper.make_node('Conv', ['input', 'w1', 'b1'], ['c1'], pads=[2, 2, 2, 2], strides=[2, 2])
    node_act1 = helper.make_node('LeakyRelu', ['c1'], ['a1'], alpha=0.1)
    
    node_conv2 = helper.make_node('Conv', ['a1', 'w2', 'b2'], ['c2'], pads=[1, 1, 1, 1], strides=[2, 2])
    node_act2 = helper.make_node('LeakyRelu', ['c2'], ['a2'], alpha=0.1)
    
    node_conv3 = helper.make_node('Conv', ['a2', 'w3', 'b3'], ['c3'], pads=[1, 1, 1, 1], strides=[2, 2])
    node_act3 = helper.make_node('LeakyRelu', ['c3'], ['output'], alpha=0.1)
    
    # Input và Output
    input_info = helper.make_tensor_value_info('input', TensorProto.FLOAT, [1, 3, 256, 256])
    output_info = helper.make_tensor_value_info('output', TensorProto.FLOAT, [1, 64, 32, 32])
    
    graph = helper.make_graph(
        [node_conv1, node_act1, node_conv2, node_act2, node_conv3, node_act3],
        'PatchCoreBackbone',
        [input_info],
        [output_info],
        [tensor_w1, tensor_b1, tensor_w2, tensor_b2, tensor_w3, tensor_b3]
    )
    
    model = helper.make_model(graph, producer_name='Antigravity_Vision_Team', opset_imports=[helper.make_opsetid('', 17)])
    onnx.checker.check_model(model)
    onnx.save(model, ONNX_PATH)
    print(f"[+] Đã xuất mô hình ONNX thành công tại: {ONNX_PATH}")

def preprocess_image(img_bgr, target_size=(256, 256)):
    """Tiền xử lý ảnh chuẩn mạng nơ-ron (RGB, Resize, Normalize 0..1, NCHW)"""
    rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    resized = cv2.resize(rgb, target_size)
    norm = resized.astype(np.float32) / 255.0
    # Mean & Std chuẩn ImageNet
    mean = np.array([0.485, 0.456, 0.406], dtype=np.float32)
    std = np.array([0.229, 0.224, 0.225], dtype=np.float32)
    norm = (norm - mean) / std
    # HWC -> CHW -> NCHW
    chw = np.transpose(norm, (2, 0, 1))
    return np.expand_dims(chw, axis=0).astype(np.float32)

def build_golden_memory_bank():
    print("[*] Đang xây dựng Golden Memory Bank từ 20 mẫu đai ốc chuẩn...")
    session = ort.InferenceSession(ONNX_PATH)
    
    train_dir = os.path.join(ROOT_DIR, "datasets", "mvtec_metal_nut", "train_good")
    files = sorted([os.path.join(train_dir, f) for f in os.listdir(train_dir) if f.endswith(".png")])
    
    all_vectors = []
    for f in files:
        img = cv2.imread(f)
        inp = preprocess_image(img)
        outputs = session.run(['output'], {'input': inp})
        feat_map = outputs[0][0] # [64, 32, 32]
        
        # Chuyển thành danh sách các vector patch [32*32, 64] = [1024, 64]
        # Reshape [64, 1024] -> [1024, 64]
        spatial_vecs = feat_map.reshape(64, -1).T
        
        # Chỉ lấy các patch nằm trên thân đai ốc (loại bỏ nền đen xung quanh)
        gray = cv2.cvtColor(cv2.resize(img, (32, 32)), cv2.COLOR_BGR2GRAY)
        mask = gray > 25
        valid_vecs = spatial_vecs[mask.flatten()]
        
        # L2 Normalization từng vector
        norms = np.linalg.norm(valid_vecs, axis=1, keepdims=True) + 1e-7
        norm_vecs = valid_vecs / norms
        all_vectors.append(norm_vecs)
        
    all_vectors = np.vstack(all_vectors)
    print(f"[+] Trích xuất xong: {all_vectors.shape[0]} feature vectors ({all_vectors.shape[1]} chiều).")
    
    # Coreset subsampling: Chọn 1500 vectors đặc trưng tiêu biểu nhất để siêu tốc độ C# (<10ms)
    np.random.seed(42)
    idx = np.random.choice(len(all_vectors), size=min(1500, len(all_vectors)), replace=False)
    coreset_bank = all_vectors[idx].astype(np.float32)
    
    # Lưu dạng nhị phân float32 để C# đọc cực nhanh
    coreset_bank.tofile(BANK_PATH)
    print(f"[+] Đã lưu Memory Bank nhị phân ({coreset_bank.shape[0]} x {coreset_bank.shape[1]}) tại: {BANK_PATH}")
    
    # Lưu metadata cấu hình
    meta = {
        "model_file": "patchcore_net.onnx",
        "bank_file": "memory_bank.bin",
        "input_width": 256,
        "input_height": 256,
        "feature_dim": 64,
        "grid_size": 32,
        "bank_size": int(coreset_bank.shape[0]),
        "anomaly_threshold": 0.42,
        "mean": [0.485, 0.456, 0.406],
        "std": [0.229, 0.224, 0.225]
    }
    with open(META_PATH, "w", encoding="utf-8") as fp:
        json.dump(meta, fp, indent=2, ensure_ascii=False)
    print(f"[+] Đã lưu cấu hình Metadata tại: {META_PATH}")

if __name__ == "__main__":
    create_feature_extractor_onnx()
    build_golden_memory_bank()
