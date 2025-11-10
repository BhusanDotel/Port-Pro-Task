from temporalio import workflow
from activities import scrape_pnct_activity

@workflow.defn
class ScrapePNCTWorkflow:
    @workflow.run
    async def run(self, container_ids: list[str]) -> list[dict]:
        results = []

        for cid in container_ids:
            try:
                result = await workflow.execute_activity(
                    scrape_pnct_activity,
                    cid,
                    schedule_to_close_timeout=60,
                    retry_policy=workflow.RetryPolicy(
                        maximum_attempts=3,
                        backoff_coefficient=2.0,
                    ),
                )
                results.append(result)
            except Exception as e:
                results.append({"container": cid, "error": str(e)})

        return results
