# Response models for API endpoints
from pydantic import BaseModel
from typing import List, Dict, Optional, Any

class RepositoryAnalysis(BaseModel):
    name: str
    stars: int
    language: Optional[str]
    updated_at: str
    readme_exists: bool
    readme_length: int

class PortfolioScore(BaseModel):
    overall_score: float
    category_scores: Dict[str, float]
    strengths: List[str]
    improvements: List[str]

class AnalysisResponse(BaseModel):
    user: str
    repositories: List[RepositoryAnalysis]
    portfolio_score: PortfolioScore
    recommendations: List[str]
