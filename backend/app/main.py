from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.factcheck import router

app = FastAPI(
    title="GEO Fact Checker API",
    version="1.0.0",
    description="AI-powered claim extraction and verification from PDF documents."
)

# Allow Streamlit frontend (localhost:8501) to reach the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "GEO Fact Checker API is running."}


app.include_router(router)