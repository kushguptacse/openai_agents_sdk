from agents import Agent, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from config import API_URL, CHAT_COMPLETIONS_API_KEY, LLM_MODEL_NAME
from agents import set_tracing_disabled

set_tracing_disabled(True)

qwen3_client = AsyncOpenAI(base_url=API_URL, api_key=CHAT_COMPLETIONS_API_KEY)

model = OpenAIChatCompletionsModel(model=LLM_MODEL_NAME, openai_client=qwen3_client)

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
    model=model
)

result = Runner.run_sync(agent, "Write a haiku about recursion in programming.")
print(result.final_output)