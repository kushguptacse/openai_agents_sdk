from agents import Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent
import asyncio
from system_prompt import professional_sales_agent_instructions, engaging_sales_agent_instructions, busy_sales_agent_instructions, sales_agent_picker_instructions
from custom_agent_qwen3 import get_model
from pushover import send_pushover_notification

model, model_settings = get_model()


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

sales_agent_picker = Agent(
        name="Sales Agent Picker",
        instructions=sales_agent_picker_instructions,
        model=model,    
        model_settings=model_settings)

async def main():
    await manual_processing_of_sales_agents()

async def manual_processing_of_sales_agents():
    user_instructions = "send a cold email to a potential customer about ComplAI"

    results = await asyncio.gather(
        Runner.run(sales_agent1, user_instructions),
        Runner.run(sales_agent2, user_instructions),
        Runner.run(sales_agent3, user_instructions),
    )
    print("\nResults from all three agents received")
    print("now picking the best email using sales_agent_picker...")

    # use sales_agent_picker to pick the best cold email among the three generated emails
    picker_input = f"Here are three cold emails about ComplAI:\n\nEmail 1:\n{results[0].final_output}\n\nEmail 2:\n{results[1].final_output}\n\nEmail 3:\n{results[2].final_output}\n\n"
    picker_result = await Runner.run(sales_agent_picker, picker_input)
    print("\n-----------------------Best email selected by sales_agent_picker:\n------------------------")
    print(picker_result.final_output)
    send_pushover_notification(picker_result.final_output)



if __name__ == "__main__":
    asyncio.run(main())
