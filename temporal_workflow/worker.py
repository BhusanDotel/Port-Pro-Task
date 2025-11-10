import asyncio
from temporalio.client import Client
from temporalio.worker import Worker

from workflows import ScrapePNCTWorkflow
from activities import scrape_pnct_activity

async def main():
    client = await Client.connect("localhost:7233")  # Temporal server address

    worker = Worker(
        client,
        task_queue="pnct-task-queue",
        workflows=[ScrapePNCTWorkflow],
        activities=[scrape_pnct_activity],
    )

    print("🧠 Worker started — waiting for PNCT scrape tasks...")
    await worker.run()

if __name__ == "__main__":
    asyncio.run(main())
