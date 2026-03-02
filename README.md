# 📊 Research Tool API — Earnings Call Analyzer

AI-powered **FastAPI Research Tool** that converts Earnings Call transcripts into structured analyst-ready insights using Large Language Models (LLMs).

Built as part of an **AI Engineering / Research Tool implementation**, demonstrating end-to-end document analysis and API deployment.

---

## 🚀 Overview

Financial analysts spend significant time reviewing earnings call transcripts manually.  
This tool automates the workflow by transforming unstructured PDFs into structured research insights.

The system provides:

- Management sentiment analysis
- Key positives & risks
- Forward guidance extraction
- Strategic business insights
- Structured JSON output via API

---

## 🧠 Key Features

- 📄 Upload earnings call PDFs
- 🔎 Automatic text extraction
- 🤖 LLM-powered analysis
- 📊 Structured research outputs
- ⚡ FastAPI REST API
- 📘 Auto-generated Swagger documentation
- ☁️ Deployment-ready backend

---

## 🏗️ Tech Stack

| Layer | Technology |
|------|------------|
| Backend | FastAPI |
| Language | Python |
| AI Analysis | LLM (Groq / Local Model) |
| PDF Processing | pdfplumber |
| Server | Uvicorn |
| Deployment | Render |
| Version Control | Git + GitHub |

---

## 📁 Project Structure

```
research-tool/
│
├── app/
│   ├── main.py        # API entry point
│   ├── analyzer.py    # LLM analysis logic
│   ├── pdf_utils.py   # PDF text extraction
│   └── prompts.py     # Prompt templates
│
├── requirements.txt
├── render.yaml
└── .env.example
```

---

## ⚙️ Local Setup

### 1. Clone Repository
```
git clone https://github.com/YARAGANIDURGADHANUSH/research-tool.git
cd research-tool
```

### 2. Create Virtual Environment
```
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate # Mac/Linux
```

### 3. Install Dependencies
```
pip install -r requirements.txt
```

### 4. Add Environment Variable
Create `.env` file:
```
GROQ_API_KEY=your_api_key
```

### 5. Run Server
```
uvicorn app.main:app --reload
```

Open:
```
http://127.0.0.1:8000/docs
```

---

## 📡 API Workflow

1️⃣ Upload Earnings Call PDF  
2️⃣ Text Extraction  
3️⃣ LLM Analysis  
4️⃣ Structured JSON Insights

Example Response:

```json
{
  "summary": "...",
  "key_highlights": [],
  "risks": [],
  "management_outlook": ""
}
```

---

## 🎯 Skills Demonstrated

- FastAPI backend development
- REST API design
- LLM integration
- Prompt engineering
- Document processing pipelines
- AI application architecture
- Cloud deployment workflow

---

## 🔮 Future Improvements

- Multi-document comparison
- RAG integration
- Analyst dashboard
- Authentication & monitoring

---

## 👨‍💻 Author

**Durga Dhanush Yaragani**  
Cloud & AI / ML Engineering Track
