from agents import Agent, Runner, function_tool
import asyncio
from system_prompt import sales_agent_picker_instructions_tools, professional_sales_agent_instructions, engaging_sales_agent_instructions, busy_sales_agent_instructions, sales_agent_picker_instructions
from custom_agent_qwen3 import get_model
from pushover import send_pushover_notification

model, model_settings = get_model()
#model = "gpt-4o-mini"  # override the model to use gpt-4o for better performance in sales email generation and selection

sales_agent1 = Agent(
    name="Professional Sales Agent",
    instructions=professional_sales_agent_instructions,
    model=model,
    model_settings=model_settings,
)

sales_agent2 = Agent(
    name="Engaging Sales Agent",
    instructions=engaging_sales_agent_instructions,
    model=model,
    model_settings=model_settings,
)

sales_agent3 = Agent(
    name="Busy Sales Agent",
    instructions=busy_sales_agent_instructions,
    model=model,
    model_settings=model_settings,
)


async def main():
    await automatic_processing_of_sales_agents_via_tools()

async def automatic_processing_of_sales_agents_via_tools():
    sales_agent1.as_tool(tool_name="sales_agent1", tool_description="Generates a professional cold sales email about ComplAI")
    sales_agent2.as_tool(tool_name="sales_agent2", tool_description="Generates an engaging cold sales email about ComplAI")
    sales_agent3.as_tool(tool_name="sales_agent3", tool_description="Generates a busy, concise cold sales email about ComplAI")
    tools = [sales_agent1, sales_agent2, sales_agent3, send_email]
    sales_agent_picker = Agent(
        name="Sales Agent Picker",
        instructions=sales_agent_picker_instructions_tools,
        tools=tools,
        model=model,    
        model_settings=model_settings)
    picker_result = await Runner.run(sales_agent_picker, "Send a cold sales email about ComplAI")
    print("\n-----------------------Best email selected by sales_agent_picker:\n------------------------")
    print(picker_result.final_output)


async def manual_processing_of_sales_agents():
    user_instructions = "send a cold email to a potential customer about ComplAI"

    results = await asyncio.gather(
        Runner.run(sales_agent1, user_instructions),
        Runner.run(sales_agent2, user_instructions),
        Runner.run(sales_agent3, user_instructions),
    )

    sales_agent_picker = Agent(
        name="Sales Agent Picker",
        instructions=sales_agent_picker_instructions,
        model=model,    
        )
    print("\nResults from all three agents received")
    print("now picking the best email using sales_agent_picker...")

    # use sales_agent_picker to pick the best cold email among the three generated emails
    picker_input = f"Here are three cold emails about ComplAI:\n\nEmail 1:\n{results[0].final_output}\n\nEmail 2:\n{results[1].final_output}\n\nEmail 3:\n{results[2].final_output}\n\n"
    picker_result = await Runner.run(sales_agent_picker, picker_input)
    print("\n-----------------------Best email selected by sales_agent_picker:\n------------------------")
    print(picker_result.final_output)
    send_pushover_notification(picker_result.final_output)

@function_tool
def send_email(message):
    """ Send out an email with the given body to all sales prospects """
    send_pushover_notification(message)



if __name__ == "__main__":
    asyncio.run(main())
