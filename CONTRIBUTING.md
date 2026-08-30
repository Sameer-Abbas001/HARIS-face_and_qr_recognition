# 🤝 Contributing to HARIS

Thank you for your interest in contributing to **HARIS (High-Accuracy Recognition & Identity System)**! We welcome contributions from developers, researchers, and computer vision enthusiasts.

---

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Enhancements](#suggesting-enhancements)
  - [Pull Requests](#pull-requests)
- [Development Setup](#development-setup)
- [Code Style & Guidelines](#code-style--guidelines)
- [Testing Changes](#testing-changes)

---

## 📜 Code of Conduct

Please maintain a respectful, inclusive, and professional environment. Treat all contributors and community members with courtesy and respect.

---

## 🛠️ How Can I Contribute?

### Reporting Bugs
If you find a bug:
1. Check the [Issues](https://github.com/Sameer-Abbas001/HARIS-face_and_qr_recognition/issues) tab to verify if it has already been reported.
2. Open a new issue with a clear title and description.
3. Include your OS version, Python version, camera hardware, and the exact error traceback.

### Suggesting Enhancements
Feature requests and ideas are encouraged! When submitting an enhancement proposal:
- Clearly explain the problem the enhancement solves.
- Describe the proposed solution and user experience.
- Detail any alternative approaches considered.

### Pull Requests
1. **Fork** the repository.
2. Create a descriptive feature branch:
   ```bash
   git checkout -b feature/enhanced-liveness-check
   ```
3. Commit your changes with clear, concise commit messages:
   ```bash
   git commit -m "feat: add anti-spoofing liveness detection to Detector.py"
   ```
4. Push to your branch:
   ```bash
   git push origin feature/enhanced-liveness-check
   ```
5. Open a **Pull Request** against the `main` branch.

---

## 💻 Development Setup

1. Clone your fork:
   ```bash
   git clone https://github.com/<your-username>/HARIS-face_and_qr_recognition.git
   cd HARIS-face_and_qr_recognition
   ```
2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/macOS
   .\venv\Scripts\activate    # Windows
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## 📐 Code Style & Guidelines

- **PEP 8 Compliance**: Follow standard Python conventions (snake_case functions, PascalCase classes, 4-space indentation).
- **Docstrings & Comments**: Provide clear docstrings for public functions and explain complex OpenCV matrix manipulation logic.
- **Resource Management**: Always release video capture handles (`cap.release()`) and destroy OpenCV windows (`cv2.destroyAllWindows()`) in `finally` blocks or upon exiting loops.

---

## 🧪 Testing Changes

Before opening a PR, verify:
- [ ] `python app-gui.py` launches cleanly with no Tkinter errors.
- [ ] Face dataset capture captures exactly the target number of frames.
- [ ] Classifier training generates a valid `.xml` file without crashing.
- [ ] Photo-QR and ID badges render cleanly in `data/qrcodes/`.
- [ ] Real-time detector correctly detects faces and QR codes without memory leaks.
