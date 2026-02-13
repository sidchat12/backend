from typing import TypedDict, List, Dict, Optional

class PortfolioState(TypedDict):
    github_url: str
    target_role: str
    
    profile_data: Dict
    repo_data: List[Dict]
    
    role_expectations: List[str]
    
    readme_insights: List[Dict]
    
    resume_text: Optional[str]
    resume_skills: Optional[Dict]
    resume_validation: Optional[Dict]
    
    tutorial_report: Optional[List[Dict]]
    
    scoring: Optional[Dict]
    
    final_report: Optional[Dict]
