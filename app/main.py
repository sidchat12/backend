from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.logging_config import setup_logging
from app.schemas.request_models import AnalysisRequest
from app.graph.portfolio_graph import build_portfolio_graph
from app.schemas.state_models import PortfolioState
from app.services.resume_service import extract_text_from_pdf
import tempfile
import logging

setup_logging()
logger = logging.getLogger(__name__)

app = FastAPI(title="GitHub Portfolio Analyzer")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

portfolio_graph = build_portfolio_graph()


def extract_username(url: str):
    if "github.com" not in url:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL")
    return url.split("github.com/")[-1].strip("/")


@app.post("/analyze")
async def analyze_profile(request: AnalysisRequest):

    try:
        username = extract_username(str(request.github_url))

        initial_state: PortfolioState = {
            "github_url": str(request.github_url),
            "target_role": request.target_role,

            "profile_data": {},
            "repo_data": [],
            "role_expectations": [],
            "readme_insights": [],

            "resume_text": None,
            "resume_skills": None,
            "resume_validation": None,

            "tutorial_report": None,
            "scoring": None,
            "final_report": None
        }

        result = await portfolio_graph.ainvoke(initial_state)

        return result["final_report"]

    except Exception as e:
        logger.exception("Error during profile analysis")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analyze-with-resume")
async def analyze_with_resume(
    github_url: str,
    target_role: str,
    file: UploadFile = File(...)
):

    try:
        with tempfile.NamedTemporaryFile(delete=False) as tmp:
            contents = await file.read()
            tmp.write(contents)
            tmp_path = tmp.name

        resume_text = extract_text_from_pdf(tmp_path)

        initial_state: PortfolioState = {
            "github_url": github_url,
            "target_role": target_role,

            "profile_data": {},
            "repo_data": [],
            "role_expectations": [],
            "readme_insights": [],

            "resume_text": resume_text,
            "resume_skills": None,
            "resume_validation": None,

            "tutorial_report": None,
            "scoring": None,
            "final_report": None
        }

        result = await portfolio_graph.ainvoke(initial_state)

        return result["final_report"]

    except Exception as e:
        logger.exception("Error during resume analysis")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
def health_check():
    return {"status": "running"}
