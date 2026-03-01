# 📊 Research Tool API — Management Commentary Analyzer

## 📌 Overview
An AI-powered Research Tool that extracts and analyzes management commentary from earnings call transcripts, conference calls, and business updates.

This backend API enables users to:
- Upload a transcript (PDF)
- Automatically extract text
- Generate structured investment research insights using AI

---

## 🚀 Features
- ✅ PDF Upload API  
- ✅ Automatic Text Extraction  
- ✅ AI-Based Management Commentary Analysis  
- ✅ Structured Analyst Output  
- ✅ REST API built using FastAPI  
- ✅ Swagger Documentation (`/docs`)  
- ✅ Local LLM support via Ollama (No API cost)

---

## 🧠 Output Generated
The system converts raw transcripts into structured research insights:

- Management Tone & Sentiment
- Key Positives
- Key Risks & Concerns
- Growth Drivers
- Forward Guidance
- Operational Insights
- Analyst Interpretation

### Example Output
```json
{
  "message": "Analysis complete",
  "analysis": {
    "sentiment": "Optimistic",
    "positives": ["Strong growth outlook", "OSAT progress"],
    "concerns": ["Working capital intensity"],
    "outlook": "Positive long-term growth"
  }
}
```

---

## 🏗️ Project Structure
```
research-tool/
│
├── app/
│   ├── main.py
│   ├── routes.py
│   ├── extractor.py
│   ├── analyzer.py
│   └── __init__.py
│
├── uploads/
├── outputs/
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone Project
```bash
git clone <repo-url>
cd research-tool
```

### 2️⃣ Create Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🤖 Install Local AI Model (Ollama)

### Install Ollama
https://ollama.com

### Pull Model
```bash
ollama pull gemma3:4b
```

### Verify Installation
```bash
ollama list
```

---

## ▶️ Run Application
```bash
uvicorn app.main:app --reload
```

### Open API Documentation
```
http://127.0.0.1:8000/docs
```

---

## 📡 API Workflow

### Step 1 — Upload Transcript
```
POST /upload
```

**Response**
```json
{
  "file_id": "uuid"
}
```

---

### Step 2 — Extract Text
```
POST /extract-text/{file_id}
```

Extracts text from uploaded PDF.

---

### Step 3 — Analyze Transcript
```
POST /analyze/{file_id}
```

Generates structured research analysis.

---

## 🔄 End-to-End Pipeline
```
Upload PDF
    ↓
Extract Text
    ↓
AI Analysis
    ↓
Structured Research Output
```

---

## 🧩 Tech Stack
- Python
- FastAPI
- Ollama (Local LLM)
- PyPDF Extraction
- Uvicorn

---

## 📈 Use Cases
- Equity Research Automation
- Earnings Call Analysis
- Financial Document Intelligence
- Research Analyst Productivity Tools

---

## ✅ Assignment Objective
This project demonstrates:
- API Development
- AI Integration
- Document Processing Pipeline
- Structured Financial Insight Generation

---

## 👤 Author
**Durga Dhanush Yaragani**
