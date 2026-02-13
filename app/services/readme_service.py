from app.services.llm_service import call_llm_json


async def generate_readme(repo, target_role):

    prompt = f"""
You are a strict JSON generator.

You must return ONLY valid JSON.
Do NOT return markdown.
Do NOT return explanations.
Do NOT return text outside JSON.

Return this EXACT schema:

{{
  "title": "",
  "overview": "",
  "features": [],
  "tech_stack": [],
  "installation": "",
  "usage": "",
  "future_improvements": []
}}

Repository:
{repo}

Target Role:
{target_role}
"""

    return await call_llm_json(prompt)


async def improve_readme(readme_content):

    prompt = f"""
You are a strict JSON generator.

Return ONLY valid JSON.
No markdown.
No explanations.
No emojis.
No extra text.

Return this EXACT schema:

{{
  "missing_sections": [],
  "weak_sections": [],
  "improvement_suggestions": []
}}

README:
{readme_content}
"""

    return await call_llm_json(prompt)
