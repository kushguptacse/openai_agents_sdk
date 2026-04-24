from pydantic import BaseModel
import asyncio
from agents import Agent, GuardrailFunctionOutput, Runner, input_guardrail, trace
from custom_agent_qwen3 import get_model
from system_prompt import name_check_gaurdrail_instructions
from dotenv import load_dotenv

load_dotenv(override=True) # Load environment variables from .env file, override existing ones if any


model, model_settings = get_model()
#model = "gpt-4o-mini"

class NameCheckOutput(BaseModel):
    is_name_in_message: bool
    name: str


name_parse_agent = Agent(
    name="Name Parse Agent",
    instructions=name_check_gaurdrail_instructions,
    model=model,
    model_settings=model_settings,
    output_type=NameCheckOutput #specifies that the output of this agent should be parsed into a NameCheckOutput object
)


async def main():

    result = await Runner.run(name_parse_agent, "hello from alice")
    print(result.final_output.is_name_in_message)
    print(result.final_output.name)

if __name__ == "__main__":
    asyncio.run(main())