def extract_text_from_pdf(pdf_path: str, output_path: str) -> int:
    """
    Ultra-light extraction for cloud free tier.
    Reads only small portion of file safely.
    """

    text = ""

    # ✅ Read raw bytes safely (no heavy parsing)
    with open(pdf_path, "rb") as f:
        raw = f.read(50000)  # first 50 KB only

    try:
        text = raw.decode("latin-1", errors="ignore")
    except Exception:
        text = "Unable to decode PDF text."

    if not text.strip():
        text = "No readable text found."

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    return len(text)