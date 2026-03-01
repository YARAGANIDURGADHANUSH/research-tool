from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import uuid
import os
import json

from app.extractor import extract_text_from_pdf
from app.analyzer import analyze_text

router = APIRouter()

UPLOAD_DIR = "uploads"
OUTPUT_DIR = "outputs"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# -------------------------
# HEALTH
# -------------------------
@router.get("/health")
def health():
    return {"status": "ok"}


# -------------------------
# UPLOAD
# -------------------------
@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_id = str(uuid.uuid4())
    file_path = f"{UPLOAD_DIR}/{file_id}_{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "message": "Upload successful"
    }


# -------------------------
# EXTRACT TEXT
# -------------------------
@router.post("/extract-text/{file_id}")
def extract_text(file_id: str):

    files = os.listdir(UPLOAD_DIR)
    target_file = None

    for f in files:
        if f.startswith(file_id):
            target_file = f
            break

    if not target_file:
        raise HTTPException(status_code=404, detail="Uploaded file not found")

    input_path = f"{UPLOAD_DIR}/{target_file}"
    output_path = f"{OUTPUT_DIR}/{file_id}.txt"

    char_count = extract_text_from_pdf(input_path, output_path)

    return {
        "message": "Text extracted successfully",
        "output_file": output_path,
        "characters_extracted": char_count
    }


# -------------------------
# ANALYZE
# -------------------------
@router.post("/analyze/{file_id}")
def analyze(file_id: str):

    text_path = f"{OUTPUT_DIR}/{file_id}.txt"

    if not os.path.exists(text_path):
        raise HTTPException(
            status_code=400,
            detail="Run /extract-text first"
        )

    with open(text_path, "r", encoding="utf-8") as f:
        transcript = f.read()

    result = analyze_text(transcript)

    analysis_path = f"{OUTPUT_DIR}/{file_id}_analysis.json"

    with open(analysis_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)

    return {
        "message": "Analysis complete",
        "analysis_file": analysis_path,
        "analysis": result
    }