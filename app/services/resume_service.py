from app.services.llm_service import call_llm_json
import PyPDF2
import io

async def extract_text_from_pdf(file_content: bytes) -> str:
    pdf_reader = PyPDF2.PdfReader(io.BytesIO(file_content))
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    
    if not text.strip():
        raise ValueError("Could not extract text from PDF. It might be empty or an image scan.")
        
    # Truncate to avoid context window issues (approx 10k chars is safe for Mistral)
    return text[:10000]


async def generate_readme(repo, target_role):

    prompt = f"""
    Generate a recruiter-ready README.md in JSON format:

    {{
      "title": "",
      "sections": {{
          "overview": "",
          "problem_statement": "",
          "features": [],
          "tech_stack": [],
          "installation": "",
          "usage": "",
          "future_improvements": []
      }}
    }}

    Repository:
    {repo}

    Target Role:
    {target_role}
    """

    return await call_llm_json(prompt)


async def improve_readme(readme_content):

    prompt = f"""
    Analyze this README and return improvements:

    {{
      "missing_sections": [],
      "weak_sections": [],
      "improvement_suggestions": []
    }}

    README:
    {readme_content}
    """

    return await call_llm_json(prompt)

async def extract_resume_skills(resume_text):
    prompt = f"""
    Extract technical skills from the following resume text.
    Group them by category (e.g., Languages, Frameworks, Tools, Databases).
    Return a JSON object where keys are categories and values are lists of skill names.

    Resume Text:
    {resume_text}
    """
    return await call_llm_json(prompt)

def match_skills_to_repos(resume_skills: dict, repo_data: list):

    all_repo_text = str(repo_data).lower()

    verified = []
    unverified = []

    for category, skills in resume_skills.items():
        for skill in skills:
            if skill.lower() in all_repo_text:
                verified.append(skill)
            else:
                unverified.append(skill)

    return {
        "verified_skills": verified,
        "unverified_skills": unverified
    }
