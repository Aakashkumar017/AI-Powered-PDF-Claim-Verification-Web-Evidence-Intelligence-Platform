import json
import re
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY
from app.services.search_service import search_web

llm = ChatGroq(
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.3-70b-versatile",
    temperature=0,
)


def _build_prompt(claim, web_data):
    # String concatenation only — NO .format() — web_data may contain { } which breaks .format()
    return (
        "You are a fact-checking assistant.\n\n"
        "Your job: decide if the CLAIM is true or false using the WEB EVIDENCE.\n\n"
        "CLAIM:\n"
        + claim
        + "\n\nWEB EVIDENCE:\n"
        + web_data
        + "\n\n"
        "Reply with ONLY a raw JSON object. No markdown. No explanation outside JSON.\n"
        "Use exactly this structure:\n"
        '{"status":"VERIFIED","confidence":90,"correct_fact":"","explanation":"reason here"}\n\n'
        "Rules:\n"
        '- status must be one of: VERIFIED  REFUTED  UNCERTAIN\n'
        "- confidence is a number 0 to 100\n"
        "- correct_fact: if REFUTED write the real fact, otherwise empty string\n"
        "- explanation: 1-2 sentences about why\n"
    )


def _parse_confidence(value):
    try:
        v = float(str(value).replace("%", "").strip())
        if v <= 1.0:
            v = v * 100
        return max(0, min(100, int(v)))
    except Exception:
        return 0


def _parse_response(raw):
    raw = raw.strip()

    # Remove markdown fences
    raw = re.sub(r"```json\s*", "", raw)
    raw = re.sub(r"```\s*", "", raw)
    raw = raw.strip()

    print(f"[verifier] Cleaned LLM output: {raw[:400]}")

    # Strategy 1: direct JSON parse
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict) and "status" in obj:
            print("[verifier] Parsed via Strategy 1 (direct)")
            return obj
    except Exception as e:
        print(f"[verifier] Strategy 1 failed: {e}")

    # Strategy 2: extract first { } block
    start = raw.find("{")
    end = raw.rfind("}")
    if start != -1 and end > start:
        try:
            obj = json.loads(raw[start:end + 1])
            if isinstance(obj, dict):
                print("[verifier] Parsed via Strategy 2 (slice)")
                return obj
        except Exception as e:
            print(f"[verifier] Strategy 2 failed: {e}")

    # Strategy 3: regex field extraction
    print("[verifier] Trying Strategy 3 (regex)")
    s_match = re.search(r'"status"\s*:\s*"([^"]+)"', raw, re.IGNORECASE)
    c_match = re.search(r'"confidence"\s*:\s*(\d+)', raw)
    e_match = re.search(r'"explanation"\s*:\s*"(.*?)"(?:\s*[,}])', raw, re.DOTALL)
    f_match = re.search(r'"correct_fact"\s*:\s*"([^"]*)"', raw)

    if s_match:
        print(f"[verifier] Strategy 3 found status: {s_match.group(1)}")
        return {
            "status":       s_match.group(1),
            "confidence":   int(c_match.group(1)) if c_match else 50,
            "explanation":  e_match.group(1).strip() if e_match else "See sources.",
            "correct_fact": f_match.group(1) if f_match else "",
        }

    # Strategy 4: keyword scan
    print("[verifier] Trying Strategy 4 (keyword scan)")
    upper = raw.upper()
    if "REFUTED" in upper:
        status = "REFUTED"
    elif "VERIFIED" in upper:
        status = "VERIFIED"
    else:
        status = "UNCERTAIN"

    nums = re.findall(r'\b(\d{1,3})\b', raw)
    conf = 50
    for n in nums:
        if 0 < int(n) <= 100:
            conf = int(n)
            break

    return {
        "status":       status,
        "confidence":   conf,
        "correct_fact": "",
        "explanation":  raw[:250] if raw else "No explanation.",
    }


def verify_claim(claim):
    print(f"\n[verifier] === Verifying: {claim[:80]} ===")

    # Step 1: Search
    search_results = search_web(claim)
    print(f"[verifier] Got {len(search_results)} search results")

    web_data = ""
    sources = []
    for i, r in enumerate(search_results):
        content = r.get("content", "").strip()
        url = r.get("url", "")
        if content:
            web_data += f"[{i+1}] {content}\n\n"
        if url:
            sources.append(url)

    if not web_data.strip():
        print("[verifier] No web data found")
        return {
            "status": "UNCERTAIN",
            "confidence": 0,
            "correct_fact": "",
            "explanation": "No web evidence was found for this claim.",
            "sources": sources,
        }

    print(f"[verifier] Web data length: {len(web_data)} chars")

    # Step 2: Build prompt using concatenation (NOT .format)
    prompt = _build_prompt(claim, web_data[:5000])

    # Step 3: Call LLM
    try:
        print("[verifier] Calling LLM...")
        response = llm.invoke(prompt)
        raw = response.content
        print(f"[verifier] LLM responded, length: {len(raw)}")
        print(f"[verifier] Raw response:\n{raw[:600]}\n---")

        parsed = _parse_response(raw)

        status = str(parsed.get("status", "UNCERTAIN")).upper().strip()
        if status in {"FALSE", "INACCURATE", "INCORRECT", "WRONG", "FAKE"}:
            status = "REFUTED"
        if status not in {"VERIFIED", "REFUTED", "UNCERTAIN"}:
            status = "UNCERTAIN"

        final = {
            "status":       status,
            "confidence":   _parse_confidence(parsed.get("confidence", 0)),
            "correct_fact": str(parsed.get("correct_fact", "")).strip(),
            "explanation":  str(parsed.get("explanation", "")).strip(),
            "sources":      sources,
        }
        print(f"[verifier] SUCCESS: {final['status']} @ {final['confidence']}%")
        return final

    except Exception as e:
        print(f"[verifier] LLM EXCEPTION TYPE: {type(e).__name__}")
        print(f"[verifier] LLM EXCEPTION: {e}")
        return {
            "status": "UNCERTAIN",
            "confidence": 0,
            "correct_fact": "",
            "explanation": f"Verification error: {str(e)[:200]}",
            "sources": sources,
        }