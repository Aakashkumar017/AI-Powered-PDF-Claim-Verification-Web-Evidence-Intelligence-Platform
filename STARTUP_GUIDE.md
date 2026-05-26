# 🚀 GEO PROJECT - Startup Guide

## What is this application?
AI Fact-Checking Web App - A system that extracts claims from PDF documents and verifies them using web search and LLM.

## ✅ Quick Start

### Option 1: Using Python Script (Recommended)
```bash
python run_app.py
```
This will:
1. Install all dependencies automatically
2. Start the backend FastAPI server on port 8000
3. Start the frontend Streamlit app on port 8501

### Option 2: Using Batch File
```bash
run.bat
```

### Option 3: Manual Setup
```bash
# Terminal 1 - Backend
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2 - Frontend
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

## 🌐 Access the Application

- **Frontend (Streamlit)**: http://localhost:8501
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs
- **Alternative API Docs**: http://localhost:8000/redoc

## 📋 How to Use

1. Open http://localhost:8501 in your browser
2. Upload a PDF file using the file uploader
3. The system will:
   - Extract text from the PDF
   - Identify factual claims
   - Search the web for verification
   - Display results with verification status and confidence

## 🔧 Required API Keys

The `.env` file in the backend folder contains:
- **GROQ_API_KEY**: For accessing the LLM (Llama 3)
- **TAVILY_API_KEY**: For web search functionality

These are already configured - no additional setup needed!

## 📁 Project Structure

```
GEO PROJECT/
├── backend/
│   ├── app/
│   │   ├── main.py          (FastAPI app)
│   │   ├── config.py        (Configuration)
│   │   ├── routes/          (API endpoints)
│   │   ├── services/        (Business logic)
│   │   └── models/          (Data models)
│   ├── requirements.txt
│   └── .env
├── frontend/
│   ├── app.py               (Streamlit UI)
│   └── requirements.txt
├── requirements.txt         (root requirement manifest)
├── run_app.py              (Python launcher)
└── run.bat                 (Batch launcher)
```

## 🐛 Troubleshooting

### Port already in use
If port 8000 or 8501 is already in use, modify the commands:
```bash
# Backend on different port
python -m uvicorn app.main:app --reload --port 8001

# Frontend on different port
streamlit run app.py --server.port 8502
```

### Dependency issues
```bash
pip install --upgrade pip
pip install -r requirements.txt --force-reinstall
```

### Backend not responding
Verify the backend is running and check http://localhost:8000/docs

## 📝 Features

- ✅ PDF document upload
- ✅ Automatic claim extraction using LLM
- ✅ Web-based claim verification
- ✅ Confidence scoring
- ✅ Detailed explanations
- ✅ Interactive web interface

Enjoy! 🎉
