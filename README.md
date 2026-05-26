# 🛡️ GEO Fact Checker

### AI-Powered PDF Claim Verification & Web Evidence Intelligence Platform

Modern AI fact-checking platform that extracts factual claims from PDF documents and verifies them against live web evidence using LLM reasoning.

---

## 🚀 Features

* 📄 Upload PDF documents
* 🧠 AI-powered claim extraction
* 🌐 Real-time web evidence search
* ✅ Claim verification with confidence scores
* 🔍 AI reasoning and explanation generation
* 🔗 Source citations and supporting links
* ⚡ FastAPI backend + Streamlit frontend
* 🤖 Groq Llama 3.3 70B integration
* 🌍 Tavily live search intelligence
* 🎨 Modern production-style UI

---

# 🖥️ Demo Workflow

```text
PDF Upload
    ↓
Claim Extraction
    ↓
Web Evidence Search
    ↓
AI Verification
    ↓
Confidence Scoring
    ↓
Evidence + Sources Display
```

---

# 🏗️ Tech Stack

| Layer          | Technology           |
| -------------- | -------------------- |
| Frontend       | Streamlit            |
| Backend        | FastAPI              |
| LLM Engine     | Groq - Llama 3.3 70B |
| Search Engine  | Tavily               |
| PDF Processing | PyMuPDF (fitz)       |
| Validation     | Pydantic             |
| API Server     | Uvicorn              |
| Environment    | Python + dotenv      |

---

# 📂 Project Structure

```bash
GEO PROJECT/
│
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   │
│   │   ├── routes/
│   │   │   └── factcheck.py
│   │   │
│   │   ├── services/
│   │   │   ├── pdf_service.py
│   │   │   ├── llm_service.py
│   │   │   ├── search_service.py
│   │   │   └── verifier_service.py
│   │   │
│   │   └── models/
│   │       └── schema.py
│   │
│   ├── requirements.txt
│   └── .env
│
├── frontend/
│   ├── app.py
│   └── requirements.txt
│
├── run_app.py
├── run.bat
├── requirements.txt
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## 1️⃣ Clone Repository

```bash
git clone https://github.com/Aakashkumar017/AI-Powered-PDF-Claim-Verification-Web-Evidence-Intelligence-Platform.git

cd AI-Powered-PDF-Claim-Verification-Web-Evidence-Intelligence-Platform
```

---

# 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 🔑 Environment Variables

Create:

```bash
backend/.env
```

Add your API keys:

```env
GROQ_API_KEY=your_groq_api_key
TAVILY_API_KEY=your_tavily_api_key
```

---

# ▶️ Run Application

## Recommended

```bash
python run_app.py
```

---

# 🌐 Application URLs

| Service            | URL                                                      |
| ------------------ | -------------------------------------------------------- |
| Streamlit Frontend | [http://localhost:8501](http://localhost:8501)           |
| FastAPI Backend    | [http://127.0.0.1:8000](http://127.0.0.1:8000)           |
| Swagger Docs       | [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) |

---

# 🧠 How It Works

## Step 1 — PDF Extraction

PyMuPDF extracts raw text from uploaded PDF files.

## Step 2 — Claim Detection

Groq Llama 3.3 identifies factual claims, statistics, dates, and technical statements.

## Step 3 — Live Web Search

Tavily searches authoritative web sources related to each claim.

## Step 4 — AI Verification

The AI compares evidence with claims and returns:

* VERIFIED
* REFUTED
* UNCERTAIN

## Step 5 — Evidence Display

Frontend displays:

* Confidence scores
* Correct information
* AI reasoning
* Supporting sources

---

# 📸 Example Output

```text
Claim:
"OpenAI was founded in 2010"

Verdict:
REFUTED

Correct Information:
OpenAI was founded in 2015

Confidence:
100%

Sources:
- Wikipedia
- Britannica
- OpenAI
```

---

# 🔒 Security

* `.env` file excluded using `.gitignore`
* API keys never exposed to GitHub
* Local environment variable loading using `python-dotenv`

---

# 📌 Future Improvements

* Multi-PDF support
* RAG pipeline integration
* Vector database memory
* Source credibility ranking
* Export reports as PDF
* Authentication system
* Cloud deployment
* Async verification pipeline

---

# 👨‍💻 Author

## Aakash Kumar

* Data Science Student
* AI/ML Enthusiast
* Python Developer
* Open Source Contributor

### Connect

* GitHub: [Aakash Kumar GitHub](https://github.com/Aakashkumar017?utm_source=chatgpt.com)
* LinkedIn: [Aakash Kumar LinkedIn](https://www.linkedin.com/in/aakash-kumar-78ba57294?utm_source=chatgpt.com)

---

