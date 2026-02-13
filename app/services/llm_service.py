import json
import re
from mistralai import Mistral
from app.config import settings

client = Mistral(api_key=settings.MISTRAL_API_KEY)


async def call_llm_json(prompt: str):

    response = client.chat.complete(
    model=settings.MISTRAL_MODEL,
    messages=[
        {
            "role": "system",
            "content": "You are a JSON generator. You must return valid JSON only."
        },
        {
            "role": "user",
            "content": prompt
        }
    ],
    temperature=0.2
)


    text = response.choices[0].message.content

    # Remove markdown code fences if present
    text = re.sub(r"```json", "", text)
    text = re.sub(r"```", "", text)

    # Extract JSON block if extra text exists
    json_match = re.search(r"\{.*\}", text, re.DOTALL)

    if json_match:
        text = json_match.group()

    # Try parsing safely
    try:
        return json.loads(text)

    except json.JSONDecodeError:
        # Attempt minor repair (remove trailing commas)
        text = re.sub(r",\s*}", "}", text)
        text = re.sub(r",\s*]", "]", text)

        try:
            return json.loads(text)
        except Exception as e:
            raise ValueError(f"LLM returned invalid JSON:\n{text}\nError: {e}")
