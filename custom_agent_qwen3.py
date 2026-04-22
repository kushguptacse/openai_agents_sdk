from config import API_URL, CHAT_COMPLETIONS_API_KEY, LLM_MODEL_NAME
from agents import Agent, ModelSettings, Runner, OpenAIChatCompletionsModel, AsyncOpenAI
from agents import set_tracing_disabled

set_tracing_disabled(True)
qwen3_client = AsyncOpenAI(base_url=API_URL, api_key=CHAT_COMPLETIONS_API_KEY)


def get_model():
    return OpenAIChatCompletionsModel(
        model=LLM_MODEL_NAME,
        openai_client=qwen3_client,
    ), ModelSettings(extra_body={"reasoning_effort": "none"})
