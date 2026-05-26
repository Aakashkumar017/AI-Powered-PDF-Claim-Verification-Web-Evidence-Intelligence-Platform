import os
from dotenv import load_dotenv

# backend/app/config.py → backend/app → backend → project root
BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)  # backend/
    )
)

# Load backend/.env first
load_dotenv(os.path.join(BASE_DIR, ".env"))

# Fallback: project root .env
load_dotenv(
    os.path.join(os.path.dirname(BASE_DIR), ".env"),
    override=False
)

GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY", "")

if not GROQ_API_KEY:
    print("[WARNING] GROQ_API_KEY not set — LLM calls will fail.")

if not TAVILY_API_KEY:
    print("[WARNING] TAVILY_API_KEY not set — web search will fail.")