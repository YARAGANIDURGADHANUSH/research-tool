from pydantic import BaseModel
from typing import List, Dict, Any


class AnalysisResult(BaseModel):
    management_tone: str | None = None
    confidence_level: str | None = None
    key_positives: List[str] = []
    key_concerns: List[str] = []
    forward_guidance: str | None = None
    capacity_utilization_trends: str | None = None
    new_growth_initiatives: List[str] = []


class AnalysisResponse(BaseModel):
    message: str
    file_id: str
    characters_extracted: int
    analysis: Dict[str, Any]  # flexible LLM output