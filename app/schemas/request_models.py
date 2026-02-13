from pydantic import BaseModel, HttpUrl

class AnalysisRequest(BaseModel):
    github_url: HttpUrl
    target_role: str
