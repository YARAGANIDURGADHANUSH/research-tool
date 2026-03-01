import pdfplumber
import pytesseract
from pdf2image import convert_from_path
import os

# ---- FORCE TESSERACT PATH (Windows) ----
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

print("Tesseract path:", pytesseract.pytesseract.tesseract_cmd)
print("Exists:", os.path.exists(pytesseract.pytesseract.tesseract_cmd))


def extract_text_from_pdf(input_path: str, output_path: str):

    full_text = ""

    # -----------------------------------
    # 1️⃣ TRY NORMAL PDF TEXT EXTRACTION
    # -----------------------------------
    with pdfplumber.open(input_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text += text + "\n"

    # -----------------------------------
    # 2️⃣ OCR FALLBACK IF EMPTY
    # -----------------------------------
    if not full_text.strip():
        print("No embedded text detected. Running OCR...")

        images = convert_from_path(input_path)

        for img in images:
            ocr_text = pytesseract.image_to_string(img)
            full_text += ocr_text + "\n"

    # -----------------------------------
    # 3️⃣ FINAL SAFETY CHECK
    # -----------------------------------
    if not full_text.strip():
        raise ValueError("OCR failed — no readable content detected.")

    # save text
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(full_text)

    return len(full_text)