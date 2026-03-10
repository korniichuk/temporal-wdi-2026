import asyncio

from temporalio.client import Client
from temporalio.worker import Worker

from example_workflow import HelloWorld
from example_workflow import nbp


async def main():
    client = await Client.connect("localhost:7233", namespace="default")
    worker = Worker(client,
                    task_queue="example-tasks",
                    workflows=[HelloWorld],
                    activities=[nbp])
    await worker.run()


if __name__ == "__main__":
    asyncio.run(main())
