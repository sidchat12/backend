# Portfolio graph and agent logic
from langgraph.graph import StateGraph
from app.schemas.state_models import PortfolioState
from app.services.github_service import get_user, get_repos, get_readme
from app.services.repo_analyzer import analyze_repo
from app.services.role_service import get_role_expectations
from app.services.readme_service import generate_readme, improve_readme
from app.services.resume_service import extract_resume_skills, match_skills_to_repos
from app.services.tutorial_detector import detect_tutorial_similarity
from app.services.scoring_service import compute_scoring
import base64

async def fetch_github_data(state: PortfolioState):

    username = state["github_url"].split("github.com/")[-1].strip("/")

    profile = await get_user(username)
    repos = await get_repos(username)

    analyzed_repos = []

    for repo in repos:
        readme_raw = await get_readme(username, repo["name"])

        readme_content = None

        if readme_raw:
            readme_content = base64.b64decode(
                readme_raw["content"]
            ).decode("utf-8")

        analyzed = analyze_repo(repo, readme_content)
        analyzed["readme_raw_content"] = readme_content
        analyzed_repos.append(analyzed)

    state["profile_data"] = profile
    state["repo_data"] = analyzed_repos

    return state

async def role_context_node(state: PortfolioState):

    role_expectations = get_role_expectations(state["target_role"])
    state["role_expectations"] = role_expectations

    return state


async def readme_node(state: PortfolioState):

    updated_repos = []

    for repo in state["repo_data"]:

        if not repo["readme_exists"]:
            generated = await generate_readme(repo, state["target_role"])
            repo["readme_generated"] = generated

        else:
            improvements = await improve_readme(
                repo["readme_raw_content"]
            )
            repo["readme_improvements"] = improvements

        updated_repos.append(repo)

    state["repo_data"] = updated_repos

    return state

async def tutorial_node(state: PortfolioState):

    tutorial_reports = []

    for repo in state["repo_data"]:

        combined_text = f"""
        {repo['name']}
        {repo['description']}
        """

        result = detect_tutorial_similarity(combined_text)

        if result["is_low_impact"]:
            repo["tutorial_flag"] = result
            tutorial_reports.append({
                "repo": repo["name"],
                "details": result
            })

    state["tutorial_report"] = tutorial_reports
    return state

async def resume_node(state: PortfolioState):

    if not state.get("resume_text"):
        return state

    resume_skills = await extract_resume_skills(
        state["resume_text"]
    )

    validation = match_skills_to_repos(
        resume_skills,
        state["repo_data"]
    )

    state["resume_skills"] = resume_skills
    state["resume_validation"] = validation

    return state

async def scoring_node(state: PortfolioState):

    scoring = compute_scoring(
        state["repo_data"],
        state["role_expectations"]
    )

    state["scoring"] = scoring

    state["final_report"] = {
        "profile": state["profile_data"]["login"],
        "role": state["target_role"],
        "score": scoring,
        "tutorial_flags": state.get("tutorial_report"),
        "resume_validation": state.get("resume_validation"),
        "repos": state["repo_data"]
    }

    return state

def build_portfolio_graph():

    builder = StateGraph(PortfolioState)

    builder.add_node("fetch_data", fetch_github_data)
    builder.add_node("role_context", role_context_node)
    builder.add_node("readme", readme_node)
    builder.add_node("tutorial", tutorial_node)
    builder.add_node("resume", resume_node)
    builder.add_node("scoring", scoring_node)

    builder.set_entry_point("fetch_data")

    builder.add_edge("fetch_data", "role_context")
    builder.add_edge("role_context", "readme")
    builder.add_edge("readme", "tutorial")
    builder.add_edge("tutorial", "resume")
    builder.add_edge("resume", "scoring")

    return builder.compile()
