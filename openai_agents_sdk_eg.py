import asyncio
from agents import Agent, Runner
from custom_agent_qwen3 import get_model


model, model_settings = get_model()
agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model,
    model_settings=model_settings,
)


async def main():
    result = await Runner.run(agent, "Tell a joke about Autonomous AI Agents")
    print(result.final_output)


if __name__ == "__main__":
    asyncio.run(main())
