import json
import os
from dotenv import load_dotenv
from fastmcp import Client
from google import genai

load_dotenv()

MODEL = "gemini-2.5-flash"
API_KEY = os.getenv("GEMINI_API_KEY")


gemini_client = genai.Client()
mcp_client = Client("mcp_client_Server\mcp_server.py")

class ContainerAgent:

    async def process_query(self, query: str):
        try:           
            async with mcp_client:
                response = await gemini_client.aio.models.generate_content(
                            model=MODEL,
                            contents=query,
                            config=genai.types.GenerateContentConfig(
                                temperature=0,
                                tools=[mcp_client.session], 
                            ),
                        )
                return response.text
        except Exception as e:
            return f"An error occurred: {str(e)}"