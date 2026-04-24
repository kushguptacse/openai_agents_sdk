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


guardrail_agent = Agent(
    name="Name Check Guardrail Agent",
    instructions=name_check_gaurdrail_instructions,
    model=model,
    model_settings=model_settings,
    output_type=NameCheckOutput #specifies that the output of this agent should be parsed into a NameCheckOutput object
)



@input_guardrail
async def guardrail_against_name(ctx, agent, message):
    result = await Runner.run(guardrail_agent, message, context=ctx.context)
    is_name_in_message = result.final_output.is_name_in_message
    return GuardrailFunctionOutput(output_info={"found_name": result.final_output},tripwire_triggered=is_name_in_message)

async def main():

    test_agent = Agent(
        name="Test Agent",
        instructions="You are a test agent that generates a message",
        model=model,
        model_settings=model_settings,
        input_guardrails=[guardrail_against_name] #attach the guardrail to this agent
    )
    result = await Runner.run(test_agent, "Generate a message 'hello' from alice")
    print(f"Generated message: {result}")
    

if __name__ == "__main__":
    asyncio.run(main())