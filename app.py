import asyncio

from example_workflow import HelloWorld
from temporalio.client import Client


async def main():
    client = await Client.connect("localhost:7233")
    handle = await client.start_workflow(
        HelloWorld.run,
        id="example-workflow",
        task_queue="example-tasks",
    )
    result = await handle.result()
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
