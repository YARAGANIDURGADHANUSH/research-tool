import pdfplumber
import pytesseract
from pdf2image import convert_from_path
from PIL import Image


def extract_text_from_pdf(pdf_path: str, output_path: str) -> int:
    text = ""

    # -------- TRY NORMAL PDF TEXT --------
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print("pdfplumber failed:", e)

    # -------- OCR FALLBACK --------
    if not text.strip():
        try:
            images = convert_from_path(pdf_path)

            for img in images:
                text += pytesseract.image_to_string(img)
        except Exception as e:
            print("OCR failed:", e)

    # -------- SAVE OUTPUT --------
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return len(text)