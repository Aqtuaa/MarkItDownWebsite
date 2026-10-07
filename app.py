from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from markitdown import MarkItDown
import os
import uuid
import fitz  # PyMuPDF
from PIL import Image
import io
 
app = Flask(__name__)
CORS(app)
 
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"pdf", "docx", "pptx", "xlsx", "txt", "html", "csv", "json", "xml"}
 
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
 
# --- Auto-detect Tesseract path (Windows + Linux/Mac) ---
try:
    import pytesseract
 
    TESSERACT_PATHS = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Users\{}\AppData\Local\Tesseract-OCR\tesseract.exe".format(os.environ.get("USERNAME", "")),
        "/usr/bin/tesseract",
        "/usr/local/bin/tesseract",
    ]
 
    for p in TESSERACT_PATHS:
        if os.path.exists(p):
            pytesseract.pytesseract.tesseract_cmd = p
            break
 
    pytesseract.get_tesseract_version()
    OCR_AVAILABLE = True
 
except Exception:
    OCR_AVAILABLE = False
 
 
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
 
 
def ocr_pdf(path):
    """Render each PDF page as image, then OCR it using PyMuPDF + Tesseract."""
    import pytesseract
    doc = fitz.open(path)
    pages_text = []
 
    for i, page in enumerate(doc):
        mat = fitz.Matrix(2.0, 2.0)  # 2x scale ~144 dpi
        pix = page.get_pixmap(matrix=mat)
        img = Image.open(io.BytesIO(pix.tobytes("png")))
        text = pytesseract.image_to_string(img, lang="eng")
        if text.strip():
            pages_text.append(f"## Page {i + 1}\n\n{text.strip()}")
 
    doc.close()
    return "\n\n---\n\n".join(pages_text)
 
 
@app.route("/")
def home():
    return send_file("index.html")
 
 
@app.route("/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
 
    file = request.files["file"]
 
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400
 
    if not allowed_file(file.filename):
        ext = file.filename.rsplit(".", 1)[-1].lower() if "." in file.filename else "unknown"
        return jsonify({
            "error": f"File type '.{ext}' is not supported.",
            "supported": sorted(ALLOWED_EXTENSIONS)
        }), 415
 
    unique_filename = f"{uuid.uuid4().hex}_{file.filename}"
    path = os.path.join(UPLOAD_FOLDER, unique_filename)
 
    try:
        file.save(path)
 
        # Step 1: Try MarkItDown first
        md = MarkItDown()
        result = md.convert(path)
        markdown = result.text_content.strip()
 
        # Step 2: If empty AND it's a PDF, try OCR fallback
        if not markdown and path.lower().endswith(".pdf"):
            if not OCR_AVAILABLE:
                return jsonify({
                    "error": (
                        "This PDF appears to be image-based and requires OCR, "
                        "but Tesseract is not installed.\n\n"
                        "Install it from: https://github.com/UB-Mannheim/tesseract/wiki\n"
                        "Then restart app.py."
                    )
                }), 422
 
            markdown = ocr_pdf(path)
            if markdown:
                markdown = (
                    "> ⚠️ PDF is image-based. Text extracted via OCR — may contain errors.\n\n"
                    "---\n\n" + markdown
                )
 
        # Step 3: Still empty
        if not markdown:
            return jsonify({
                "error": "No text could be extracted. The file may be encrypted or corrupted."
            }), 422
 
        return jsonify({"markdown": markdown})
 
    except Exception as e:
        return jsonify({"error": f"Conversion failed: {str(e)}"}), 500
 
    finally:
        if os.path.exists(path):
            os.remove(path)
 
 
if __name__ == "__main__":
    if OCR_AVAILABLE:
        print("[OCR] Tesseract detected — image-based PDF support enabled.")
    else:
        print("[OCR] Tesseract NOT found — image-based PDFs will return an install prompt.")
    app.run(debug=True)