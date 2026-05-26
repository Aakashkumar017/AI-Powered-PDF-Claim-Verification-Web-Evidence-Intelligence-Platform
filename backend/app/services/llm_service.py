import json
import re
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0,
)

_EXTRACT_PROMPT = """You are a fact-extraction assistant.

Read the text and extract factual claims that can be verified on the internet.

RULES:
1. Each claim must be a short, clear, positive statement of fact
2. Focus on: numbers, dates, statistics, company facts, scientific facts
3. Do NOT include: opinions, questions, or sentences that say something is wrong
4. Do NOT include sentences like "X is incorrect" or "the real answer is Y"
5. Each claim should be between 10 and 200 characters
6. Return maximum 8 claims
7. No duplicate claims

Return ONLY a JSON array like this example:
["claim one here", "claim two here", "claim three here"]

No extra text, no markdown backticks, just the array.

TEXT TO ANALYZE:
{text}
"""


def _parse_json_array(raw: str) -> list:
    """Extract JSON array from LLM response, handles messy output."""
    # Remove markdown code fences
    raw = raw.strip()
    raw = re.sub(r"```json", "", raw)
    raw = re.sub(r"```", "", raw)
    raw = raw.strip()

    # Try direct parse first
    try:
        result = json.loads(raw)
        if isinstance(result, list):
            return result
    except Exception:
        pass

    # Find [ ... ] block
    start = raw.find("[")
    end = raw.rfind("]")
    if start != -1 and end != -1 and end > start:
        try:
            result = json.loads(raw[start:end + 1])
            if isinstance(result, list):
                return result
        except Exception:
            pass

    return []


def _clean_claims(raw_list: list) -> list:
    """Remove bad claims from the list."""
    bad_phrases = [
        "is incorrect", "is not correct", "is wrong",
        "the correct", "not true", "is untrue",
        "it is argued", "the author claims", "states that",
    ]
    clean = []
    for item in raw_list:
        c = str(item).strip()
        if len(c) < 10 or len(c) > 300:
            continue
        lower = c.lower()
        if any(p in lower for p in bad_phrases):
            continue
        clean.append(c)
    return clean


def _remove_duplicates(claims: list) -> list:
    """Remove near-duplicate claims."""
    seen = []
    for claim in claims:
        words_new = set(claim.lower().split())
        duplicate = False
        for existing in seen:
            words_old = set(existing.lower().split())
            overlap = len(words_new & words_old) / max(len(words_new), 1)
            if overlap > 0.7:
                duplicate = True
                break
        if not duplicate:
            seen.append(claim)
    return seen


def extract_claims(text: str) -> list:
    """Extract factual claims from document text."""
    if not text or not text.strip():
        return []

    # Use first 8000 characters (enough for most documents)
    text_input = text[:8000]

    prompt = _EXTRACT_PROMPT.format(text=text_input)

    try:
        response = llm.invoke(prompt)
        raw_claims = _parse_json_array(response.content)
        cleaned = _clean_claims(raw_claims)
        final = _remove_duplicates(cleaned)
        print(f"[llm_service] Extracted {len(final)} claims")
        return final[:8]
    except Exception as e:
        print(f"[llm_service] Error: {e}")
        return []