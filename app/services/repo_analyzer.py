from datetime import datetime

def analyze_readme_structure(content: str):

    content_lower = content.lower()

    return {
        "word_count": len(content.split()),
        "has_installation": "install" in content_lower,
        "has_usage": "usage" in content_lower,
        "has_tech_stack": "tech stack" in content_lower,
        "has_architecture": "architecture" in content_lower,
        "has_deployment": "http" in content_lower,
        "has_screenshots": "![" in content,
        "has_badges": "shields.io" in content_lower
    }

def analyze_repo(repo, readme_content):

    last_updated = datetime.strptime(
        repo["updated_at"], "%Y-%m-%dT%H:%M:%SZ"
    )

    days_since_update = (datetime.utcnow() - last_updated).days

    readme_analysis = None
    readme_exists = False

    if readme_content:
        readme_exists = True
        readme_analysis = analyze_readme_structure(readme_content)

    return {
        "name": repo["name"],
        "description": repo["description"],
        "language": repo["language"],
        "stars": repo["stargazers_count"],
        "forks": repo["forks_count"],
        "open_issues": repo["open_issues_count"],
        "days_since_update": days_since_update,
        "readme_exists": readme_exists,
        "readme_analysis": readme_analysis
    }
