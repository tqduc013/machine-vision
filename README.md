# 👁️⚡ Industrial Machine Vision & PC Control System

> **High-Speed Automated Optical Inspection (AOI) & Real-Time PC Control Pipeline**  
> Designed for **Semiconductor, Chip Inspection (Apple A18 / Micro-ICs), and Precision Manufacturing Lines**.  
> Built with **C# .NET 8 WPF, OpenCvSharp4, Python 3, Multi-Threading, PLC TCP Socket Handshake & 3D Digital Twin**.

---

[![.NET 8](https://img.shields.io/badge/.NET-8.0_LTS-512BD4?style=for-the-badge&logo=dotnet&logoColor=white)](https://dotnet.microsoft.com/)
[![C# WPF](https://img.shields.io/badge/C%23-WPF_MVVM-239120?style=for-the-badge&logo=csharp&logoColor=white)](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/)
[![OpenCV](https://img.shields.io/badge/OpenCV-OpenCvSharp4-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)](https://github.com/shimat/opencvsharp)
[![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Three.js](https://img.shields.io/badge/Three.js-3D_Digital_Twin-black?style=for-the-badge&logo=threedotjs&logoColor=white)](https://threejs.org/)
[![Author](https://img.shields.io/badge/Author-tqduc013-38bdf8?style=for-the-badge&logo=github)](https://github.com/tqduc013)
[![License](https://img.shields.io/badge/License-MIT-4ade80?style=for-the-badge)](LICENSE)

**Languages:** [🇻🇳 Tiếng Việt](README_vi.md) · [🇬🇧 English](README.md)

---

## 🚀 Key Highlights & Capabilities

- ⚡ **Ultra-Fast Cycle Time ($3 - 10\text{ ms} / \text{part}$):** Delivers throughput exceeding **$36,000\text{ UPH}$** (Units Per Hour) for high-speed factory conveyors.
- 🎯 **Full 4G Vision Pipeline:**
  1. **Guidance (Alignment):** Computes `MinAreaRect` $(X, Y, \text{Angle }\theta)$ and applies `WarpAffine` rotation back to $0^\circ$.
  2. **Identification (QR / Barcode):** Decodes laser-engraved serial identifiers (`SN-APPLE-A18-xxx`).
  3. **Gauging (Measurement):** Sub-pixel dimension measurement with caliper tolerances ($\pm 15\text{px} / \pm 0.1\text{mm}$).
  4. **Inspection (Defect Detection):** Region-of-Interest (ROI) surface scratch detection and corner chip-off verification.
- 🧵 **4-Layer Multi-Threaded Architecture (Producer-Consumer):**
  - **Thread 1 (Acquisition):** Hardware trigger capture from photoelectric sensor.
  - **Thread 2 (Worker Pool):** FIFO Job Queue decoupled from networking to prevent memory leaks and zero UI freezing.
  - **Thread 3 (PLC I/O Handshake):** TCP Socket (`:5000`) signaling Bit `Y1=1` for pneumatic reject cylinder actuation.
  - **Thread 4 (Presentation):** Real-time WPF MVVM telemetry & WebSocket (`:8765`) broadcast to 3D Digital Twin.
- 💡 **Optics & 5 Industrial Lighting Modes:**
  - *Backlight* (Dimension Gauging), *Low-Angle Ring 15° Darkfield* (Scratch/Defect), *Coaxial 90° Beam Splitter* (Mirror/Specular), *Dome 360°* (Curved Surfaces), and *Hybrid Coaxial + Dome* (Complex Reflective Metal).
- 🖥️ **Native Industrial C# .NET 8 WPF Application (`PCControlApp`):**
  - Built with modern MVVM (`CommunityToolkit.Mvvm`), Dark-mode industrial IPC HUD, live camera stream, pass/fail LED indicators, and shift yield rate analytics.
- 🔬 **AI Anomaly Detection Lab (PatchCore & Matrix Vectorization - 133x Speedup):**
  - Multi-scale 3072-dimensional patch embeddings across a $20 \times 20$ grid (400 patches of $32 \times 32\text{px}$).
  - Builds a 20,000-vector normalized Memory Bank from 50 golden PCB samples using real-world DeepPCB data.
  - SIMD matrix vectorization via $(A-B)^2 = A^2 - 2AB + B^2$ algebraic expansion: Reduces inference latency from **$66.54\text{s}$ down to $0.5\text{s}$ ($500\text{ms}$)**.
  - Generates full-resolution Jet Colormap anomaly heatmaps and overlays to localize micro open/short circuit defects.

---

## 🏗️ 4-Layer System Architecture

```text
[ PHOTOELECTRIC SENSOR ] ── (Hardware Trigger) ──► [ PLC CONTROLLER ]
                                                          │
                                                          ▼ (TCP Socket :5000)
┌─────────────────────────────────────────────────────────────────────────────┐
│                       VISION PC CONTROLLER (IPC)                            │
│                                                                             │
│  [ TIER 1: ACQUISITION ] ──► [ TIER 2: THREAD-SAFE QUEUE ]                  │
│                                           │                                 │
│                                           ▼                                 │
│                              [ TIER 2: 4G WORKER POOL ]                     │
│                              • 1. Guidance (Angle θ)                        │
│                              • 2. Identification (QR Code)                  │
│                              • 3. Gauging (Dimensions)                      │
│                              • 4. Inspection (Scratch / Chip)               │
│                                           │                                 │
│                     ┌─────────────────────┴─────────────────────┐           │
│                     ▼                                           ▼           │
│         [ TIER 3: PLC HANDSHAKE ]                   [ TIER 4: PRESENTATION ]│
│         • Bit Y0=1: Pass (OK)                       • C# .NET 8 WPF App     │
│         • Bit Y1=1: Reject (NG)                     • WebSocket (:8765)     │
│         • CSV Production Logger                     • 3D Web Dashboard      │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## 📂 Repository Structure

```tree
Machine-Vision/
├── datasets/                   # Benchmark datasets (MVTec AD Metal Nut & DeepPCB)
├── docs/                       # Technical Case Studies & Stress Test Reports
│   ├── MVTEC_METAL_NUT_CASE_STUDY.md          # Hybrid Rule-based & AI Vision Case Study
│   ├── STRESS_TEST_REPORT.md                  # 2,000-Cycle Endurance & Memory Benchmark
│   └── mvtec_metal_nut_anomaly_benchmark.png  # Quantitative ROC & Latency Evaluation
├── models/                     # Exported ONNX Runtime models & PatchCore Memory Bank
├── notebooks/                  # Interactive R&D Jupyter Notebooks
│   └── 05_ai_anomaly_detection_lab.ipynb      # PatchCore & SIMD Matrix Vectorization Lab
├── src/                        # Core Source Code (C# .NET 8 & Python)
│   ├── 01_defect_and_dimension_inspector.py   # Washer AOI baseline algorithm (~3ms)
│   ├── 02_full_4g_pipeline_inspector.py       # Full 4G Pipeline Inspector (~10ms)
│   ├── 03_plc_simulator.py                    # Industrial PLC TCP Socket Server (:5000)
│   ├── 04_vision_pc_controller.py             # Multi-Threaded Engine & WebSocket Broadcast
│   ├── 05_ai_anomaly_detector_interactive.py  # PatchCore Anomaly Detection Engine
│   ├── 06_mvtec_metal_nut_anomaly_benchmark.py# MVTec AD Evaluation Pipeline
│   ├── PCControlApp/                          # Native Industrial C# .NET 8 WPF App
│   │   ├── Models/InspectionResult.cs         # DTO schema for inspection results
│   │   ├── VisionEngine/ChipInspector.cs      # OpenCvSharp4 4G Chip Inspector
│   │   ├── VisionEngine/MetalNutInspector.cs  # OpenCvSharp4 Metal Nut Inspector
│   │   ├── VisionEngine/OnnxAnomalyInspector.cs # C# ONNX Runtime PatchCore Inspector
│   │   ├── ViewModels/MainViewModel.cs        # MVVM async coordinator
│   │   └── MainWindow.xaml                    # Industrial IPC WPF UI
│   └── VisionBenchmark/                       # Automated 2,000-Cycle Stress Test Suite
└── README.md                   # Project Documentation
```

---

## ⚡ Quick Start Guide

### 1. Prerequisites
- **Python:** `3.10+` with `opencv-python`, `numpy`, `matplotlib`, `websockets`.
  ```bash
  pip install opencv-python numpy matplotlib websockets
  ```
- **.NET SDK:** `.NET 8.0 SDK (LTS)`
  ```bash
  winget install Microsoft.DotNet.SDK.8
  ```

---

### 2. Run the Full Industrial Pipeline (Python + PLC + 3D Web Dashboard)

**Terminal 1 — Launch PLC Simulator:**
```bash
python src/03_plc_simulator.py
```

**Terminal 2 — Launch Vision PC Controller Engine:**
```bash
python src/04_vision_pc_controller.py
```

**Terminal 3 — Open 3D Live Dashboard:**
Double-click `pc_control_dashboard.html` or open in any browser:
```text
http://127.0.0.1:8765 connection established automatically!
```
*Observe laser scanning, real-time chip angle tilt, 3D reject cylinder push, and dynamic Yield Rate updates.*

---

### 3. Run Native Industrial C# .NET 8 WPF Application

```bash
cd src/PCControlApp
dotnet run
```
*Or launch directly via `src/PCControlApp/bin/Debug/net8.0-windows/PCControlApp.exe`.*

---

### 4. Run 2,000-Cycle Stress & Memory Benchmark

```bash
dotnet run --project src/VisionBenchmark/VisionBenchmark.csproj
```
*See detailed endurance results in [`docs/STRESS_TEST_REPORT.md`](docs/STRESS_TEST_REPORT.md) and [`docs/MVTEC_METAL_NUT_CASE_STUDY.md`](docs/MVTEC_METAL_NUT_CASE_STUDY.md).*

---

## 📊 Performance Benchmarks

| Metric | Target Standard | Achieved in Project | Status |
| :--- | :--- | :--- | :---: |
| **Washer AOI Cycle Time** | $< 15\text{ ms}$ | **$2.8\text{ ms}$** | 🚀 Pass |
| **Apple A18 4G Pipeline Cycle Time** | $< 25\text{ ms}$ | **$8.5 - 11.2\text{ ms}$** | 🚀 Pass |
| **AI PatchCore Matrix Vectorization** | $< 2.0\text{ s}$ (400 patches vs 20k vec) | **$0.50\text{ s}$ ($500\text{ ms}$)** | ⚡ Breakthrough (x133) |
| **Theoretical Inspection Throughput** | $> 10,000\text{ UPH}$ | **$> 36,000\text{ UPH}$** | 🚀 Pass |
| **RAM Footprint Leakage (24/7)** | $0\text{ MB leak}$ | **$0\text{ MB leak}$** (`using var Mat`) | 🚀 Pass |
| **C# .NET 8 Compilation Speed** | $< 10\text{ s}$ | **$2.89\text{ s}$** | 🚀 Pass |

---

## 👨‍💻 Author

- **GitHub:** [@tqduc013](https://github.com/tqduc013)
- **Repository:** [https://github.com/tqduc013/machine-vision](https://github.com/tqduc013/machine-vision)

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).
