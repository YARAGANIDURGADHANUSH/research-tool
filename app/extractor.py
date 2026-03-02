import pdfplumber


def extract_text_from_pdf(pdf_path: str, output_path: str) -> int:
    text = ""

    MAX_PAGES = 10   # ✅ memory protection

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages[:MAX_PAGES]:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"

    if not text.strip():
        text = "No extractable text found."

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return len(text)