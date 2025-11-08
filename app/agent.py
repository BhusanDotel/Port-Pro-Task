import json
import os
from pydantic_ai import Agent
from pydantic_ai.models.google import GoogleModel
from pydantic_ai.providers.google import GoogleProvider
from dotenv import load_dotenv

load_dotenv()

MODEL = "gemini-2.5-flash"
API_KEY = os.getenv("GEMINI_API_KEY")

provider = GoogleProvider(api_key=API_KEY)
model = GoogleModel(MODEL, provider=provider)
agent = Agent(model)

class ContainerAgent:

    async def process_query(self, query: str):
            prompt = f"""
        You are an intelligent agent that extracts structured data from container queries.

        Given a query like:
        "{query}"

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

            response = await agent.run(prompt)

            return json.loads(response.output)
    

if __name__ == "__main__":
    import asyncio

    async def main():
        container_agent = ContainerAgent()
        query = "Where is container MSDU123456?"
        result = await container_agent.process_query(query)
        print(result)

    asyncio.run(main())