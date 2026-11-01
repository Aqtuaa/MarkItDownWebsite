# MarkItDown Web & Desktop GUI

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Powered by](https://img.shields.io/badge/Powered%20by-Microsoft%20MarkItDown-0078D4.svg)](https://github.com/microsoft/markitdown)
[![Docker Ready](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)

A modern, user-friendly **Web & Desktop GUI** wrapper built on top of [Microsoft MarkItDown](https://github.com/microsoft/markitdown). It easily converts diverse office documents, spreadsheets, slides, and PDFs into clean Markdown text, with built-in **Tesseract OCR fallback** for scanned PDFs.

---

## ✨ Features

- **Multi-Format Document Support**:
  - Documents: `.pdf`, `.docx`, `.txt`, `.html`, `.xml`
  - Presentations: `.pptx`
  - Spreadsheets: `.xlsx`, `.csv`
  - Structured Data: `.json`
- **OCR Fallback for Scanned PDFs**:
  - Automatically detects scanned / image-only PDFs.
  - Falls back to **PyMuPDF + Tesseract OCR** to extract text with page separation.
- **Dual Operating Modes**:
  - 🌐 **Web Application**: Flask API backend serving an interactive drag-and-drop web interface.
  - 💻 **Desktop Application**: Native Windows desktop window powered by `pywebview` (no browser tabs or terminal windows needed).
- **Interactive UI**:
  - Drag-and-drop file upload zone.
  - Side-by-side or live Markdown output preview.
  - One-click **Copy to Clipboard** and **Download `.md`** file.
- **Cloud & Container Ready**:
  - Pre-configured `Dockerfile` with system-level Tesseract OCR and Gunicorn for 1-click cloud deployment (Render, Railway, Fly.io, etc.).

---

## 🛠️ Tech Stack

- **Core Engine**: [Microsoft MarkItDown](https://github.com/microsoft/markitdown)
- **Backend**: Python 3.10+, Flask, Flask-CORS, Gunicorn
- **Desktop Window**: `pywebview` (Microsoft Edge WebView2)
- **OCR & Document Processing**: PyMuPDF (`fitz`), Pillow (`PIL`), `pytesseract`
- **Frontend**: Vanilla HTML5, CSS3, JavaScript
- **Deployment**: Docker & Docker Compose compatible

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10 or newer
- *(Optional for image-based PDFs)*: [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) installed on your system.

### 2. Clone the Repository

```bash
git clone https://github.com/Aqtuaa/MarkItDownWebsite.git
cd MarkItDownWebsite
```

### 3. Setup Virtual Environment & Install Dependencies

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
.\venv\Scripts\activate
# Linux / macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## 🖥️ Running the Application

### Option A: Run as Desktop App (Windows GUI)
Run the desktop GUI window directly:
```bash
python desktop_app.py
```
*(Or simply double-click `Buka MarkItDown.bat` on Windows)*.

### Option B: Run as Local Web Server
```bash
python app.py
```
Open your browser and navigate to: `http://localhost:5000`

---

## 🐳 Docker Deployment

The application includes a production-ready `Dockerfile` with Tesseract OCR pre-installed.

### Build and Run with Docker:

```bash
# Build the Docker image
docker build -t markitdown-app .

# Run the container
docker run -d -p 5000:5000 --name markitdown-container markitdown-app
```
Access the application at `http://localhost:5000`.

### Deploying to Cloud (e.g., Render.com / Railway):
1. Push this repository to GitHub.
2. Link your repository in [Render.com](https://render.com) as a **New Web Service**.
3. Render will auto-detect the `Dockerfile` and build it with full Tesseract OCR capabilities for free.

---

## 📦 Building Standalone Windows Executable (.exe)

You can package the application into a standalone folder with an executable:

```bash
pyinstaller MarkItDown.spec --noconfirm
```
*(Or simply double-click `build_exe.bat` on Windows)*.

The output executable will be generated inside the `dist/MarkItDown/` folder.

---

## 📄 License & Acknowledgments

### Powered by Microsoft MarkItDown
This project utilizes the [MarkItDown](https://github.com/microsoft/markitdown) open-source library developed by **Microsoft Corporation**, which is released under the **MIT License**.

### Project License
This project itself is licensed under the [MIT License](LICENSE). You are free to use, modify, and distribute it in accordance with open-source standards.
