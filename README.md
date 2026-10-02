# 🛡️ CipherScan — Advanced Digital Forensics & Steganography Suite

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/GUI-Tkinter%20%2B%20Pillow-FF6F00?style=for-the-badge&logo=python&logoColor=white" alt="GUI Framework" />
  <img src="https://img.shields.io/badge/Security-Forensics%20%26%20Stego-00FF9D?style=for-the-badge&logo=hackthebox&logoColor=black" alt="Domain" />
  <img src="https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-blue?style=for-the-badge&logo=windows&logoColor=white" alt="Platform" />
  <img src="https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge" alt="License" />
</p>

<p align="center">
  <b>CipherScan</b> is a multi-purpose desktop security and digital forensics suite engineered to inspect, uncover, and sanitize concealed payloads across images, PDF documents, and uncompressed audio files. Featuring a cyber-forensics dashboard, real-time laser scanning animations, non-intrusive toast notifications, and a multi-theme engine.
</p>

---

## ✨ Features at a Glance

### 🖼️ 1. Image Steganography Inspector
* **Bit-Plane Extraction**: Inspect both **Least Significant Bit (LSB)** and **Most Significant Bit (MSB)** pixel channels across RGB image data to uncover embedded plaintext messages.
* **Embedded Metadata Detection**: Scans and parses PNG chunks, EXIF fields, and custom steganographic tags (such as `HiddenData`).
* **Live Thumbnail Preview**: Instant responsive image preview upon file loading.
* **Exportable Reports**: Generate formatted PDF reports of extracted plaintext and forensic findings with a single click.

---

### 📄 2. PDF Forensics & Metadata Sanitizer
* **Header & Metadata Audit**: Dissects PDF metadata dictionaries (Producer, Creator, Author, Creation Date, Modification Timestamps).
* **Covert `/Message` Tag Detection**: Uncovers hidden steganographic payload keys embedded directly inside the PDF structure.
* **Zero-Trace Sanitizer**: Completely scrubs and flushes all tracking records and metadata dictionaries, producing a clean, sanitized PDF file (`*_Sanitized.pdf`).

---

### 🔍 3. High-Pass Watermark & Edge Scanner
* **Pure Python Edge Frequency Analysis**: Employs spatial contrast enhancement and edge-filtering algorithms without requiring heavyweight OpenCV (`cv2`) dependencies.
* **Anomaly Cluster Detection**: Highlights suspected watermark boundaries, covert logos, and spatial stamps with high-contrast indicator boxes.
* **Dual Preview & Export**: Preview the processed edge mask directly in-app or open it instantly in your native OS image viewer.

---

### 🎙️ 4. Audio Steganography Decoder
* **16-bit PCM WAV Stream Parser**: Analyzes uncompressed audio frames to extract LSB-encoded bitstreams.
* **Audio Technical Telemetry**: Displays sample rate (Hz), channel count (mono/stereo), and frame counts.
* **Forensic PDF Export**: Exports decoded audio transcripts directly to PDF documentation.

---

### 🎨 5. Dynamic Multi-Theme Engine
Switch between **6 handcrafted, high-contrast themes** in real time from the header dropdown menu:

| Theme | Preview Description | Dominant Colors |
| :--- | :--- | :--- |
| 🟢 **Cyber Matrix** | Terminal Hacker Aesthetic | Obsidian `#0a0f14` & Neon Emerald `#00ff9d` |
| 🌌 **Deep Space** | Sleek Cyberpunk Cosmic | Navy `#080c14`, Electric Cyan `#38bdf8`, Slate `#334155` |
| 🔮 **Dracula Synth** | Synthwave Violet | Deep Purple `#12101a`, Lavender `#c084fc`, Hot Pink |
| ❄️ **Nordic Frost** | Minimal Arctic Clean | Polar Night `#191e24`, Frost Blue `#88c0d0` |
| 🔥 **Amber Sunset** | Warm Tactical Darkroom | Bronze `#14100c`, Glowing Amber `#f59e0b` |
| ☀️ **Modern Light** | High-Legibility Studio Light | Crisp White `#ffffff`, Slate `#0f172a`, Royal Indigo `#2563eb` |

---

### ⚡ 6. High-Tech Animations & Modern Dialogs
* **Animated Laser Scanner Sweep**: A high-tech radar line sweeps across active results panels whenever an analysis job runs in background threads.
* **Pulsing Engine Status Orb**: Real-time breathing status badge in the header displaying operational readiness.
* **Micro-Hover Interactions**: Reactive buttons with smooth color shifts and cursor indicators.
* **Non-Intrusive Floating Toasts**: Floating notification toasts slide in smoothly from the top-right corner and auto-dismiss after 3.5 seconds.
* **Custom Themed Modals**: Replaces generic OS popups with theme-styled cards featuring copy buttons, category badges, and stack trace expanders.

---

## 🚀 Quick Start Guide

### 📋 Prerequisites
Ensure you have **Python 3.9+** installed:
```bash
python --version
```

### 📥 1. Clone the Repository
```bash
git clone https://github.com/supernova1803/Cipher_Scan.git
cd Cipher_Scan
```

### 📦 2. Install Dependencies
Install the required packages using `pip`:
```bash
pip install -r requirements.txt
```

> **Dependencies:**
> - [`Pillow`](https://pypi.org/project/Pillow/) — Advanced image manipulation & edge filtering
> - [`PyPDF2`](https://pypi.org/project/PyPDF2/) — PDF parsing, metadata extraction & sanitization
> - [`fpdf`](https://pypi.org/project/fpdf/) — PDF report generation

---

## 💻 Running CipherScan

### Option A: Run via Python (Recommended)
Launch the suite directly through the main application script:
```bash
python worktry.py
```
*or via the project launcher:*
```bash
python cipherscan.py
```

### Option B: Standalone Windows Executable
If you are on Windows and prefer running without a Python environment, run the pre-built executable:
```powershell
.\dist\cipherscan.exe
```

---

## 🛠️ Building Standalone Binary (.exe)

You can compile a standalone, single-file Windows executable using [PyInstaller](https://pyinstaller.org/):

```powershell
pip install pyinstaller
pyinstaller --onefile --windowed --name cipherscan worktry.py
```
*(The generated executable will be placed in the `dist/` directory).*

---

## ⌨️ Keyboard Shortcuts

| Shortcut | Action |
| :---: | :--- |
| <kbd>F11</kbd> | Toggle Fullscreen Mode |
| <kbd>Esc</kbd> | Exit Fullscreen Mode |
| <kbd>Ctrl</kbd> + <kbd>Q</kbd> | Exit Application |

---

## 📁 Project Architecture

```
Cipher_Scan/
├── worktry.py            # Core engine, GUI dashboard, animations, and theme manager
├── cipherscan.py         # Application entrypoint launcher
├── requirements.txt      # Project dependencies (fpdf, Pillow, PyPDF2)
├── cipherscan.spec       # PyInstaller build specification
├── dist/                 # Pre-compiled standalone executable (cipherscan.exe)
├── build/                # Build artifacts
└── README.md             # Project documentation
```

---

## 🛡️ Security & Ethical Disclaimer

> **Notice:** **CipherScan** is created for educational, research, and authorized forensic auditing purposes only. Steganography and forensic analysis tools should only be used on files and systems you own or have explicit permission to test and analyze.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome!
1. Fork the Project (`https://github.com/supernova1803/Cipher_Scan/fork`)
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

<p align="center">
  Made with ❤️ for Security Researchers and Digital Forensics Enthusiasts
</p>
