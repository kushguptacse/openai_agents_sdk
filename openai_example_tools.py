from dotenv import load_dotenv
from agents import Agent, Runner, trace, function_tool
from openai.types.responses import ResponseTextDeltaEvent
from typing import Dict
import os
import asyncio

from pushover import send_pushover_notification


load_dotenv(override=True)

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
    model="gpt-4o-mini",
)

sales_agent2 = Agent(
    name="Engaging Sales Agent",
    instructions=instructions2,
    model="gpt-4o-mini",
)

sales_agent3 = Agent(
    name="Busy Sales Agent",
    instructions=instructions3,
    model="gpt-4o-mini",
)


@function_tool
def send_email(message: str) -> Dict[str, str]:
    """Send out an email with the given body to all sales prospects"""
    send_pushover_notification(message)
    return {"status": "success"}


description = "Write a cold sales email"

tool1 = sales_agent1.as_tool(tool_name="sales_agent1", tool_description=description)
tool2 = sales_agent2.as_tool(tool_name="sales_agent2", tool_description=description)
tool3 = sales_agent3.as_tool(tool_name="sales_agent3", tool_description=description)

tools = [tool1, tool2, tool3, send_email]


async def main():
    # Improved instructions thanks to student Guillermo F.

    instructions = """
    You are a Sales Manager at ComplAI. Your goal is to find the single best cold sales email using the sales_agent tools.

    Follow these steps carefully:
    1. Generate Drafts: Use all three sales_agent tools to generate three different email drafts. Do not proceed until all three drafts are ready.

    2. Evaluate and Select: Review the drafts and choose the single best email using your judgment of which one is most effective.

    3. Use the send_email tool to send the best email (and only the best email) to the user.

    Crucial Rules:
    - You must use the sales agent tools to generate the drafts — do not write them yourself.
    - You must send ONE email using the send_email tool — never more than one.
    """

    sales_manager = Agent(
        name="Sales Manager",
        instructions=instructions,
        tools=tools,
        model="gpt-4o-mini",
    )

    message = "Send a cold sales email addressed to 'Dear CEO'"

    with trace("Sales manager"):
        result = await Runner.run(sales_manager, message)


if __name__ == "__main__":
    asyncio.run(main())
