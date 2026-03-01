from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import uuid
import os

from app.analyzer import analyze_text
from app.extractor import extract_text_from_pdf

app = FastAPI(title="Research Tool API")

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ---------------------------------------------------
# ROOT
# ---------------------------------------------------
@app.get("/")
def root():
    return {"message": "Research Tool API running"}


# ---------------------------------------------------
# UPLOAD DOCUMENT
# ---------------------------------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}.pdf"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    return {
        "message": "Upload successful",
        "file_id": file_id
    }


# ---------------------------------------------------
# ANALYZE DOCUMENT (FULL PIPELINE)
# ---------------------------------------------------
@app.post("/analyze/{file_id}")
def analyze(file_id: str):

    pdf_path = f"{UPLOAD_DIR}/{file_id}.pdf"
    text_path = f"{OUTPUT_DIR}/{file_id}.txt"

    if not os.path.exists(pdf_path):
        return JSONResponse(
            status_code=404,
            content={"error": "Uploaded file not found"}
        )

    try:
        # ---------------------------------
        # STEP 1 — Extract only if needed
        # ---------------------------------
        if not os.path.exists(text_path):

            char_count = extract_text_from_pdf(
                pdf_path,
                text_path
            )

        else:
            with open(text_path, "r", encoding="utf-8") as f:
                cached_text = f.read()
                char_count = len(cached_text)

        # load extracted text
        with open(text_path, "r", encoding="utf-8") as f:
            text = f.read()

        if not text.strip():
            return JSONResponse(
                status_code=400,
                content={"error": "No text extracted from PDF"}
            )

        # ---------------------------------
        # STEP 2 — AI Analysis
        # ---------------------------------
        result = analyze_text(text)

        return {
            "message": "Analysis complete",
            "file_id": file_id,
            "characters_extracted": char_count,
            "analysis": result
        }

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Analysis failed",
                "details": str(e)
            }
        )