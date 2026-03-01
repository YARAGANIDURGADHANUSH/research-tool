from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import uuid
import os

from app.analyzer import analyze_text
from app.extractor import extract_text_from_pdf

# ---------------------------------------------------
# APP INIT
# ---------------------------------------------------
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
# HEALTH CHECK (important for deployment platforms)
# ---------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------------------------------
# UPLOAD DOCUMENT
# ---------------------------------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

    try:
        contents = await file.read()

        with open(file_path, "wb") as f:
            f.write(contents)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Upload successful",
        "file_id": file_id
    }


# ---------------------------------------------------
# ANALYZE DOCUMENT (FULL PIPELINE)
# ---------------------------------------------------
@app.post("/analyze/{file_id}")
def analyze(file_id: str):

    pdf_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    text_path = os.path.join(OUTPUT_DIR, f"{file_id}.txt")

    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=404,
            detail="Uploaded file not found"
        )

    try:
        # ---------------------------------
        # STEP 1 — Extract text if needed
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

        # ---------------------------------
        # STEP 2 — Load extracted text
        # ---------------------------------
        with open(text_path, "r", encoding="utf-8") as f:
            text = f.read()

        if not text.strip():
            raise HTTPException(
                status_code=400,
                detail="No text extracted from PDF"
            )

        # ---------------------------------
        # STEP 3 — AI Analysis
        # ---------------------------------
        result = analyze_text(text)

        return {
            "message": "Analysis complete",
            "file_id": file_id,
            "characters_extracted": char_count,
            "analysis": result
        }

    except HTTPException:
        raise

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "error": "Analysis failed",
                "details": str(e)
            }
        )