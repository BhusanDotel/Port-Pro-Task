from temporalio import activity
from pnct_scrape import scrape_container_details

@activity.defn
async def scrape_pnct_activity(container_id: str) -> dict:
    """Activity that scrapes PNCT.net"""
    return scrape_container_details(container_id)
