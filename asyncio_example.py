import asyncio

async def hello_async():
    return "Hello, Async World!"

async def main():
    res = await hello_async()
    print(res)

asyncio.run(main())