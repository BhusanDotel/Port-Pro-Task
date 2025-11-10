import os
from fastmcp import FastMCP
from typing import Dict, Any
from temporalio.client import Client
from dotenv import load_dotenv
from temporal_workflow.workflows import ScrapePNCTWorkflow  

load_dotenv()

mcp = FastMCP(name="Container MCP")

WORKFLOW_URL = os.getenv("WORKFLOW_URL")

@mcp.tool()
async def full_container_details(container: str) -> Dict[str, Any]:
    f"""
    MCP tool that triggers a Temporal workflow to scrape PNCT details to get the container detail for {container}
    """
    try:
        client = await Client.connect(WORKFLOW_URL)

        # Start the Temporal workflow for this container ID
        handle = await client.start_workflow(
            ScrapePNCTWorkflow.run,
            [container],
            id=f"pnct-scrape-{container}",
            task_queue="pnct-task-queue",
        )

        print(f"Temporal workflow started for container: {container}")

        # Wait for workflow result
        result = await handle.result()
        return result
    except:
        return "Error occurred while fetching container details."


if __name__ == "__main__":
    mcp.run()