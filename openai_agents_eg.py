from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from config import API_URL, CHAT_COMPLETIONS_API_KEY, LLM_MODEL_NAME
from agents import set_tracing_disabled
import asyncio

set_tracing_disabled(True)

qwen3_client = AsyncOpenAI(base_url=API_URL, api_key=CHAT_COMPLETIONS_API_KEY)

model = OpenAIChatCompletionsModel(
    model=LLM_MODEL_NAME, 
    openai_client=qwen3_client
)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model
)


async def main():
    result = await Runner.run(agent, "Tell a joke about Autonomous AI Agents")
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())