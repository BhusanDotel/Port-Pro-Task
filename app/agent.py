import json
import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

MODEL = "gemini-2.5-flash"  
API_KEY=os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=API_KEY)

class ContainerAgent:

    async def process_query(self, text: str):
            prompt = f"""
        You are an intelligent agent that extracts structured data from container queries.

        Given a query like:
        "{text}"

        Return a JSON with exactly two fields:
        1. "intent": one of ["full_container_details", "check_availability", "get_location", "check_holds", "get_last_free_day"]
        2. "container": the container number (e.g., "MSDU123456").

        Example output:
        {{
        "intent": "full_container_details",
        "container": "MSDU123456"
        }}

        Respond **ONLY** with the JSON, no code blocks, no newlines, no other characters, no explanations, nothing else.
        """

            response = client.models.generate_content(
                model=MODEL,
                contents=prompt
            )

            try:
                result = json.loads(response.text)
            except json.JSONDecodeError:
                result = {"intent": None, "container": None}

            return result