from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

import uuid
import os
import shutil

from app.schemas import AnalysisResponse
from app.analyzer import analyze_text
from app.extractor import extract_text_from_pdf


# ---------------------------------------------------
# APP INIT
# ---------------------------------------------------
app = FastAPI(title="Research Tool API")

# ✅ CORS (Swagger + browser access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
# HEALTH CHECK (Render requires this)
# ---------------------------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ---------------------------------------------------
# UPLOAD DOCUMENT (memory-safe streaming)
# ---------------------------------------------------
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files allowed")

    file_id = str(uuid.uuid4())
    file_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")

    try:
        # ✅ stream upload (prevents memory crash)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "message": "Upload successful",
        "file_id": file_id
    }


# ---------------------------------------------------
# ANALYZE DOCUMENT
# ---------------------------------------------------
@app.post("/analyze/{file_id}", response_model=AnalysisResponse)
async def analyze(file_id: str):

    pdf_path = os.path.join(UPLOAD_DIR, f"{file_id}.pdf")
    text_path = os.path.join(OUTPUT_DIR, f"{file_id}.txt")

    if not os.path.exists(pdf_path):
        raise HTTPException(
            status_code=404,
            detail="Uploaded file not found"
        )

    try:
        # ---------------------------------
        # STEP 1 — Extract text (cached)
        # ---------------------------------
        if not os.path.exists(text_path):
            char_count = extract_text_from_pdf(pdf_path, text_path)
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

        # ---------------------------------
        # STEP 4 — Save analyst report
        # ---------------------------------
        report_path = os.path.join(
            OUTPUT_DIR,
            f"{file_id}_report.txt"
        )

        with open(report_path, "w", encoding="utf-8") as f:
            f.write("RESEARCH ANALYSIS REPORT\n")
            f.write("=" * 40 + "\n\n")

            for key, value in result.items():
                f.write(f"{key.upper()}:\n")

                if isinstance(value, list):
                    if value:
                        for item in value:
                            f.write(f" - {item}\n")
                    else:
                        f.write(" Not Mentioned\n")
                else:
                    f.write(f" {value}\n")

                f.write("\n")

        # ---------------------------------
        # RESPONSE
        # ---------------------------------
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
    
