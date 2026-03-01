import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import os

# Windows-only Tesseract path
if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = \
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"


def extract_text_from_pdf(input_path: str, output_path: str):

    full_text = ""

    # -------------------------------
    # Normal PDF extraction
    # -------------------------------
    with pdfplumber.open(input_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    # -------------------------------
    # OCR fallback (safe)
    # -------------------------------
    if not full_text.strip():
        print("Running OCR fallback...")

        try:
            images = convert_from_path(input_path, dpi=150)

            for img in images:
                full_text += pytesseract.image_to_string(img)

        except Exception:
            print("OCR skipped (Tesseract not available)")

    if not full_text.strip():
        raise ValueError("No readable text detected")

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    return len(full_text)