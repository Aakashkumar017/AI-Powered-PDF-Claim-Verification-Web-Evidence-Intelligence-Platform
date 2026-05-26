from fastapi import APIRouter, UploadFile, File, HTTPException

from app.services.pdf_service import extract_text
from app.services.llm_service import extract_claims
from app.services.verifier_service import verify_claim

router = APIRouter(tags=["Fact Check"])


@router.post("/fact-check")
async def fact_check(file: UploadFile = File(...)):
    """
    Upload a PDF, extract factual claims, and verify each one against the web.
    """
    # Validate file type by content-type or filename
    filename = file.filename or ""
    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are accepted."
        )

    # Extract text from PDF
    text = await extract_text(file)

    # Extract claims using LLM
    claims = extract_claims(text)

    if not claims:
        return {
            "claims_checked": 0,
            "results": [],
            "message": "No verifiable factual claims were found in the document."
        }

    # Verify each claim — failures are caught inside verify_claim, never crash
    results = []
    for claim in claims:
        verification = verify_claim(claim)
        results.append({
            "claim": claim,
            "status": verification["status"],
            "confidence": verification["confidence"],
            "correct_fact": verification["correct_fact"],
            "explanation": verification["explanation"],
            "sources": verification["sources"],
        })

    return {
        "claims_checked": len(results),
        "results": results,
    }