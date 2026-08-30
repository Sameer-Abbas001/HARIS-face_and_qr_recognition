# 🏛️ HARIS Technical Architecture & Engineering Specifications

This document outlines the system architecture, mathematical algorithms, computer vision pipelines, and graphical interface mechanics powering the **HARIS** (High-Accuracy Recognition & Identity System) platform.

---

## 1. System Pipeline Overview

HARIS operates as an integrated four-stage pipeline:

```
┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐       ┌─────────────────┐
│   1. Capture    │  ──>  │   2. Training   │  ──>  │ 3. Credential   │  ──>  │ 4. Verification │
│  (Haar Cascade) │       │     (LBPH)      │       │ (Level-H QR/ID) │       │   (Dual Core)   │
└─────────────────┘       └─────────────────┘       └─────────────────┘       └─────────────────┘
```

---

## 2. Computer Vision & Recognition Algorithms

### 2.1 Haar Feature-based Cascade Face Detection
- **Mechanism**: Evaluates rectangular Haar features using Integral Image calculation for rapid rectangular area sum computations.
- **Cascade Classifier**: Multi-stage rejection cascade configured with:
  - `scaleFactor = 1.1` to 1.3: Image scale reduction ratio per pyramid level.
  - `minNeighbors = 5`: Threshold for candidate bounding boxes to suppress false positives.
  - `minSize = (80, 80)`: Eliminates small background noise artifacts.

### 2.2 Local Binary Pattern Histograms (LBPH) Face Recognizer
Unlike standard Eigenfaces or Fisherfaces which capture global pixel variations sensitive to lighting, LBPH computes local spatial structure:
1. **Neighborhood Thresholding**: For each pixel $p_c$ in a grayscale region, compare against its 8 circular neighbors $p_n$:
   $$s(p_n - p_c) = \begin{cases} 1 & \text{if } p_n \ge p_c \\ 0 & \text{if } p_n < p_c \end{cases}$$
2. **Binary Weighting**: Convert the binary sequence to a decimal LBP value:
   $$LBP(x_c, y_c) = \sum_{n=0}^{7} s(p_n - p_c) \cdot 2^n$$
3. **Grid Division & Histograms**: The face is divided into localized grids (e.g., $8 \times 8$), creating spatial histograms that are concatenated into a high-dimensional feature vector.
4. **Distance Metric**: Euclidean / Chi-Square distance scoring calculates similarity against stored user histograms.
5. **Confidence Conversion**: Raw Chi-Square distance $D$ is mapped to an intuitive percentage:
   $$\text{Confidence} = \max(0, \min(100, 100 - D))$$

---

## 3. High-Error-Correction QR Code & Badge Generation

### 3.1 Reed-Solomon Error Correction (Level H)
- Standard QR codes fail when obscured. HARIS enforces **Level H (High)** error correction:
  - **Recovery Capacity**: ~30% of data codewords can be restored if destroyed or occluded.
  - **Center Embedding**: A circular/rounded portrait occupying $\approx 25-26\%$ of the QR matrix area is placed in the center without corrupting the barcode scan decoding.

### 3.2 Cybernetic Badge Rendering (`qr_generator.py`)
- Programmatically synthesized using **Pillow (PIL)** at $540 \times 780$ resolution.
- Composed of:
  - Double rounded stroke card contour with neon border (`#38bdf8`).
  - Header branding and biometric pass status pill (`#10b981`).
  - Rescaled user portrait with glowing border container.
  - Rendered Level-H QR code token.
  - Unique cryptographic token identification string (`HARIS-SEC-XXXXXX`).

---

## 4. Real-Time Access Core HUD Engine (`Detector.py`)

- **Dual-Threaded Verification**:
  - Thread 1: Grayscale Haar face tracking + LBPH distance inference.
  - Thread 2: `cv2.QRCodeDetector` polygon detection and payload parsing (`HARIS:USER:<name>`).
- **Temporal Match Smoothing**:
  - Employs a consecutive match counter (`REQUIRED_MATCHES = 15`) to eliminate momentary false triggers.
  - Displays real-time neon bracket corners, confidence readout, and cached reference photo overlay on the HUD.

---

## 5. UI Architecture & Particle Physics Engine (`app-gui.py`)

### 5.1 Glassmorphic Cyberpunk Theme
- Built using **Tkinter** with custom Canvas rendering.
- **Particle System**:
  - Spawns interactive particles $(x, y, vx, vy, radius)$.
  - Calculates inter-particle distance; draws proximity connecting lines when distance $< 120\text{px}$ with dynamic alpha opacity.
- **Color Transition Engine**:
  - Non-blocking asynchronous color fade engine (`animate_color_fade`) interpolating RGB values across UI element states (`#0f172a` $\to$ `#1e293b` $\to$ `#38bdf8`).
- **Telemetry Loop**:
  - Dynamic CPU/Memory load emulation, uptime timer, and active security status badges.
