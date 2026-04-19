import asyncio

async def hello_async():
    return "Hello, Async World!"

async def main():
    # another way to run the async function. here hello_async is called and 
    #we wait for its result using await. this allows other tasks to run while waiting for the result.
    res = await hello_async()
    print(res)
    
# one way to run the async function. here main is the entry point of the async code. it will run until completion.
asyncio.run(main()) 