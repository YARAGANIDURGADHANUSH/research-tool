import pdfplumber


def extract_text_from_pdf(pdf_path: str, output_path: str) -> int:
    text = ""

    MAX_PAGES = 3   # ✅ Free-tier safe limit

    try:
        with pdfplumber.open(pdf_path) as pdf:

            total_pages = min(len(pdf.pages), MAX_PAGES)

            for i in range(total_pages):
                page = pdf.pages[i]

                page_text = page.extract_text() or ""
                text += page_text + "\n"

    except Exception as e:
        # prevents 502 crashes
        text = f"Extraction failed: {str(e)}"

    if not text.strip():
        text = "No extractable text found."

    # save extracted text
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return len(text)