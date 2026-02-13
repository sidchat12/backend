import asyncio
import os
import sys

# Add backend directory to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.services.llm_service import call_llm_json

async def verify():
    print("Testing Ollama integration...")
    try:
        response = await call_llm_json(
            prompt="Generate a JSON object with a single key 'message' and value 'Hello from Ollama!'",
            max_tokens=50
        )
        print("Success! Response from LLM:")
        print(response)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(verify())
