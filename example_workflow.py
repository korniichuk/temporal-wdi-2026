from datetime import timedelta

from temporalio import activity
from temporalio import workflow
from temporalio.common import RetryPolicy

from nbp import get_usd_rate

retry_policy = RetryPolicy(
    initial_interval=timedelta(seconds=1),  # first retry after 1s
    backoff_coefficient=2.0,  # double delay after each retry
    maximum_interval=timedelta(seconds=64),  # max delay
    maximum_attempts=0  # unlimited
)


@workflow.defn
class HelloWorld:
    @workflow.run
    async def run(self) -> str:
        num = 2 + 2  # deterministic
        text = await workflow.execute_activity(
            nbp,
            start_to_close_timeout=timedelta(seconds=5),  # max duration
            retry_policy=retry_policy
        )
        return f"num: {num}\n\n{text}"


@activity.defn
async def nbp() -> str:
    text = await get_usd_rate()
    return text
