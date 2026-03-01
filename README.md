# Research Tool API — Earnings Call / Management Commentary Analyzer

## Overview

This project implements a **minimal AI-powered research portal** designed as a **structured research tool**, not an open-ended chatbot.

The system allows researchers and analysts to upload earnings call transcripts or management discussion documents and automatically generate **structured analyst-ready insights**.

The tool converts unstructured financial transcripts into clearly organized research outputs such as:

- Management tone and sentiment
- Key positives and risks
- Forward guidance
- Capacity trends
- Growth initiatives

This implementation fulfills the **L2 Research Tool Assignment** requirement of building a working end-to-end research workflow.

---

## Objective

Financial analysts spend hours manually reviewing earnings call transcripts.  
This tool automates the process by transforming transcripts into structured research summaries suitable for investment or business analysis.

The design philosophy:

- ❌ Not a chatbot
- ✅ A focused research tool
- ✅ Deterministic structured output
- ✅ Analyst-usable insights

---

## Key Features

- Upload earnings call transcripts (PDF)
- Automatic PDF text extraction
- AI-powered structured analysis
- Management sentiment classification
- Key positives & concerns extraction
- Forward guidance identification
- Local LLM execution (FREE — no API cost)
- REST API via FastAPI
- Analyst-ready JSON output

---

## System Architecture

```
User Uploads PDF
        ↓
File Storage (uploads/)
        ↓
Text Extraction (PDF → TXT)
        ↓
Local LLM Analysis (Ollama + Gemma3)
        ↓
Structured Research Output (JSON)
        ↓
Saved in outputs/
```

---

## Technology Stack

| Component | Technology |
|-----------|------------|
| Backend API | FastAPI |
| Server | Uvicorn |
| Language | Python 3.12 |
| AI Runtime | Ollama |
| Model | gemma3:4b |
| Document Processing | PDF Text Extraction + OCR |
| API Docs | OpenAPI / Swagger |
| Deployment Ready | Yes |

---

## Why Local LLM (Ollama)?

This project intentionally avoids paid APIs.

Advantages:

- ✅ Completely FREE
- ✅ No OpenAI billing required
- ✅ Runs offline
- ✅ Evaluator-friendly
- ✅ Works without API keys

---

## Project Structure

```
research-tool/
│
├── app/
│   ├── main.py          # FastAPI application entry
│   ├── routes.py        # API endpoints
│   ├── extractor.py     # PDF → text processing
│   └── analyzer.py      # AI analysis using Ollama
│
├── uploads/             # Uploaded PDFs
├── outputs/             # Extracted text + analysis results
├── requirements.txt
└── README.md
```

---

## Installation Guide

### Step 1 — Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/research-tool.git
cd research-tool
```

---

### Step 2 — Create Virtual Environment

Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Mac/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

---

### Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

### Step 4 — Install Ollama

Download from:

https://ollama.com/download

Verify installation:

```bash
ollama list
```

---

### Step 5 — Download AI Model (ONE TIME ONLY)

```bash
ollama pull gemma3:4b
```

Model size ≈ 3GB  
Download time depends on internet speed.

---

### Step 6 — Run Server

```bash
uvicorn app.main:app --reload
```

Server starts at:

```
http://127.0.0.1:8000
```

---

## API Documentation

Open interactive documentation:

```
http://127.0.0.1:8000/docs
```

Swagger UI allows full workflow execution without coding.

---

## End-to-End Workflow

### 1️⃣ Upload Transcript

Endpoint:

```
POST /upload
```

Upload a PDF earnings call transcript.

Example Response:

```json
{
  "file_id": "uuid",
  "message": "Upload successful"
}
```

---

### 2️⃣ Extract Text

Endpoint:

```
POST /extract-text/{file_id}
```

Converts PDF into machine-readable text.

Example Response:

```json
{
  "message": "Text extracted successfully",
  "characters_extracted": 38088
}
```

---

### 3️⃣ Run Research Analysis

Endpoint:

```
POST /analyze/{file_id}
```

Runs AI research analysis using local LLM.

---

## Output Structure (Research Ready)

Example output:

```json
{
  "management_tone": "Optimistic",
  "confidence_level": "High",
  "key_positives": [
    "Strong long-term growth roadmap",
    "Semiconductor value chain expansion",
    "Improved governance processes"
  ],
  "key_concerns": [
    "Working capital pressure",
    "High capex spending"
  ],
  "forward_guidance": "Growth expected with improving operational efficiency.",
  "capacity_utilization_trends": "Increasing utilization with new customers.",
  "growth_initiatives": [
    "OSAT semiconductor initiative",
    "High-end PCB manufacturing expansion"
  ]
}
```

---

## Research Logic Design

### Management Tone Detection

Derived from:

- Executive language patterns
- Risk acknowledgement
- Forward-looking statements
- Confidence indicators

---

### Hallucination Prevention

The model is instructed to:

- Only extract information present in transcript
- Avoid assumptions
- Mark missing information explicitly

---

### Handling Missing Sections

If transcript lacks information:

- Output states **"Not Mentioned"**
- No fabricated content generated

---

## Evaluator Quick Start (2–3 Minutes)

1. Install Ollama
2. Run:

```bash
ollama pull gemma3:4b
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Start API:

```bash
uvicorn app.main:app --reload
```

5. Open:

```
http://127.0.0.1:8000/docs
```

6. Execute:

Upload → Extract → Analyze

---

## Deployment Notes

The project is deployable on:

- Render
- Railway
- VPS
- Local evaluation environment

Free hosting limitations:

- Cold start delays
- Limited compute
- Larger PDFs slower processing

---

## Limitations

- CPU-based inference slower than cloud GPUs
- Large transcripts require more processing time
- Designed for evaluation-scale workloads

---

## Future Improvements

- Multi-document comparison
- Vector database retrieval (RAG)
- Analyst dashboard UI
- Batch processing
- Cloud inference option
- Financial KPI extraction

---

## Assignment Scope Completion

| Requirement | Status |
|-------------|--------|
| Document Upload | ✅ |
| Document Processing | ✅ |
| Research Tool Execution | ✅ |
| Structured Output | ✅ |
| Working API | ✅ |
| Evaluator Usability | ✅ |

Quality and structured output clarity were prioritized over performance as required.

---

## Author

Durga Dhanush Yaragini  
AI / ML Engineering Track  
Research Tool Implementation