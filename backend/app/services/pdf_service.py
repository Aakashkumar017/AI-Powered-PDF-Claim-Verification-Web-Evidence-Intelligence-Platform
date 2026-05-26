import fitz  # PyMuPDF
from fastapi import HTTPException


async def extract_text(file) -> str:
    """
    Read an uploaded PDF file and return the full extracted text.
    Raises HTTP 400 if the file is not a valid PDF or is empty.
    """
    raw = await file.read()

    if not raw:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    try:
        pdf = fitz.open(stream=raw, filetype="pdf")
    except Exception:
        raise HTTPException(
            status_code=400,
            detail="Could not open file as PDF. Please upload a valid PDF document."
        )

    if pdf.page_count == 0:
        raise HTTPException(status_code=400, detail="The PDF has no pages.")

    text_parts = []
    for page in pdf:
        page_text = page.get_text()
        if page_text:
            text_parts.append(page_text)

    pdf.close()

    text = "\n".join(text_parts).strip()

    if not text:
        raise HTTPException(
            status_code=400,
            detail="No readable text found. The PDF may be scanned/image-only."
        )

    return text