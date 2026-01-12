"""
Modèles Pydantic pour l'API
"""
from pydantic import BaseModel, HttpUrl
from typing import Optional, Dict, List


class AnalysisRequest(BaseModel):
    url: HttpUrl
    use_selenium: Optional[bool] = False


class ChatMessage(BaseModel):
    message: str
    context: Optional[Dict] = None


class AnalysisResponse(BaseModel):
    url: str
    status: str
    report_id: Optional[str] = None
    summary: Optional[Dict] = None
    analysis: Optional[Dict] = None
    recommendations: Optional[List[Dict]] = None
