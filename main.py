from asyncio import run
from json import dumps

# from src.infra.monitor import Monitor


""" async def main():
    from src.infra.monitor import Monitor

    monitor = Monitor()
    await monitor.execute("98600106009522025") """


async def main():
    from src.infra.integrations import Monitor

    monitor = Monitor()
    messages = await monitor.get_messages("98600106009522025")
    print(dumps(messages, indent=4))


run(main())
