import httpx
from app.config import settings

HEADERS = {
    "Authorization": f"token {settings.GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}

BASE_URL = "https://api.github.com"

async def get_user(username: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/users/{username}",
            headers=HEADERS
        )
        response.raise_for_status()
        return response.json()

async def get_repos(username: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/users/{username}/repos?per_page=100",
            headers=HEADERS
        )
        response.raise_for_status()
        return response.json()

async def get_readme(username: str, repo: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{BASE_URL}/repos/{username}/{repo}/readme",
            headers=HEADERS
        )
        if response.status_code == 404:
            return None
        response.raise_for_status()
        return response.json()
