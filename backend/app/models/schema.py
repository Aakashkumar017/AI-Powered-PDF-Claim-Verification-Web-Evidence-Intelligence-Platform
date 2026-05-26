from pydantic import BaseModel
from typing import List


class VerificationResponse(BaseModel):
    claim: str
    status: str
    confidence: str
    explanation: str
    correct_fact: str
    sources: List[str] = []