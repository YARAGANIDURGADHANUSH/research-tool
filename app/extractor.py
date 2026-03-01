import pdfplumber


def extract_text_from_pdf(pdf_path: str, output_path: str) -> int:
    text = ""

    # ---- TEXT EXTRACTION ONLY (LOW MEMORY) ----
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    if not text.strip():
        text = "No extractable text found in PDF."

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return len(text)