from unittest import result

from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool
from openai.types.responses import ResponseTextDeltaEvent
from typing import Dict
import asyncio

from custom_agent_qwen3 import get_model

model, model_settings = get_model()

instructions1 = "You are a sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write professional, serious cold emails."

instructions2 = "You are a humorous, engaging sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write witty, engaging cold emails that are likely to get a response."

instructions3 = "You are a busy sales agent working for ComplAI, \
a company that provides a SaaS tool for ensuring SOC2 compliance and preparing for audits, powered by AI. \
You write concise, to the point cold emails."

sales_agent1 = Agent(
        name="Professional Sales Agent",
        instructions=instructions1,
        model=model,
        model_settings=model_settings
)

sales_agent2 = Agent(
        name="Engaging Sales Agent",
        instructions=instructions2,
        model=model,
        model_settings=model_settings
)

sales_agent3 = Agent(
        name="Busy Sales Agent",
        instructions=instructions3,
        model=model,
        model_settings=model_settings
)

async def main():
    user_instructions = "send a cold email to a potential customer about ComplAI"

    # invokes sales_agent2 in synchronous mode to write a cold email about ComplAI, and prints the final output
    result = await Runner.run(sales_agent2, user_instructions)
    print(result.final_output)

    # stream the output of sales_agent1 as it writes a cold email about ComplAI, and prints each delta as it is received
    print("------------------Streaming output from sales_agent1-----------------------------------")
    result = Runner.run_streamed(sales_agent1, input=user_instructions)
    async for event in result.stream_events():
      if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
        print(event.data.delta, end="", flush=True)

   # parallel cold email generation: invokes all three sales agents in parallel to write cold emails about ComplAI, and prints the final output of each agent as they complete
    print("\n------------------Parallel generation from all three agents-----------------------------------")
    results  = await asyncio.gather(
       Runner.run(sales_agent1, user_instructions),
       Runner.run(sales_agent2, user_instructions),
       Runner.run(sales_agent3, user_instructions)
    )
    print("\n------------------Professional Sales Agent Output:------------------\n", results[0].final_output)
    print("\n------------------Engaging Sales Agent Output:------------------\n", results[1].final_output)
    print("\n------------------Busy Sales Agent Output:------------------\n", results[2].final_output)     


if __name__ == "__main__":
    asyncio.run(main())