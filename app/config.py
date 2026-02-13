import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN")
    MISTRAL_API_KEY: str = os.getenv("MISTRAL_API_KEY")
    MISTRAL_MODEL: str = os.getenv("MISTRAL_MODEL", "mistral-small")

settings = Settings()

if not settings.GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN not found in environment")

if not settings.MISTRAL_API_KEY:
    raise ValueError("MISTRAL_API_KEY not found in environment")
