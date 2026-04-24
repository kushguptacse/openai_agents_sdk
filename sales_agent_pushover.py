#this file covers topics - openai agent sdk usage, agent tool usage, agent handover, and using pushover for notifications instead of email for demonstration purposes. It includes two main functions - one that demonstrates the use of tools by sales agents and a picker agent, and another that demonstrates a more complex workflow with a sales manager agent that uses handover to an email formatting agent that uses tools to format the email before sending it out. The manual_processing_of_sales_agents function demonstrates how to run multiple agents in parallel and then use a picker agent to select the best output among them.
# integration with openai as well as qwen3 is possible, you can switch between them by changing the get_model function in custom_agent_qwen3.py and remove model_settings. The send_email function is decorated with @function_tool which allows it to be used as a tool by the agents. In this example, instead of actually sending an email, it sends a pushover notification for demonstration purposes.

from agents import Agent, Runner, function_tool
import asyncio
from system_prompt import subject_instructions, sales_manager_instructions, html_instructions, email_formatter, sales_agent_picker_instructions_tools, professional_sales_agent_instructions, engaging_sales_agent_instructions, busy_sales_agent_instructions, sales_agent_picker_instructions
from custom_agent_qwen3 import get_model
from pushover import send_pushover_notification

model, model_settings = get_model()
#model = "gpt-4o-mini"

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

async def automatic_processing_of_sales_agents_via_tools():
    sales_agent1_tool = sales_agent1.as_tool(tool_name="sales_agent1", tool_description="Generates a professional cold sales email about ComplAI")
    sales_agent2_tool = sales_agent2.as_tool(tool_name="sales_agent2", tool_description="Generates an engaging cold sales email about ComplAI")
    sales_agent3_tool = sales_agent3.as_tool(tool_name="sales_agent3", tool_description="Generates a busy, concise cold sales email about ComplAI")
    tools = [sales_agent1_tool, sales_agent2_tool, sales_agent3_tool, send_email]
    sales_agent_picker = Agent(
        name="Sales Agent Picker",
        instructions=sales_agent_picker_instructions_tools,
        tools=tools,
        model=model,    
        model_settings=model_settings)
    picker_result = await Runner.run(sales_agent_picker, "Send a cold sales email about ComplAI")
    print("\n-----------------------Best email selected by sales_agent_picker:\n------------------------")
    print(picker_result.final_output)

async def automatic_processing_of_sales_agents_with_handover():
    
    subject_writer = Agent(name="Email subject writer", instructions=subject_instructions, model=model, model_settings=model_settings)
    subject_tool = subject_writer.as_tool(tool_name="subject_writer", tool_description="Write a subject for a cold sales email")

    html_converter = Agent(name="HTML email body converter", instructions=html_instructions, model=model, model_settings=model_settings)
    html_tool = html_converter.as_tool(tool_name="html_converter",tool_description="Convert a text email body to an HTML email body")

    tools = [subject_tool, html_tool, send_email]
    emailer_agent = Agent(name="email manager", instructions=email_formatter, tools=tools, model=model, model_settings=model_settings)


    sales_agent1_tool = sales_agent1.as_tool(tool_name="sales_agent1", tool_description="Generates a professional cold sales email about ComplAI")
    sales_agent2_tool = sales_agent2.as_tool(tool_name="sales_agent2", tool_description="Generates an engaging cold sales email about ComplAI")
    sales_agent3_tool = sales_agent3.as_tool(tool_name="sales_agent3", tool_description="Generates a busy, concise cold sales email about ComplAI")
    sales_cold_mail_tools = [sales_agent1_tool, sales_agent2_tool, sales_agent3_tool]
    handoffs = [emailer_agent]
    sales_manager = Agent(name="Sales Manager", instructions=sales_manager_instructions, tools=sales_cold_mail_tools, handoffs=handoffs, model=model, model_settings=model_settings)

    message = "Send out a cold sales email addressed to Dear CEO from Alice"
    result = await Runner.run(sales_manager, message)
    print("\n-----------------------Best email selected and sent by sales_manager:\n------------------------")
    print(result.final_output)

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
def send_email(message:str) -> dict[str,str]:
    """ Send out an email with the given body to all sales prospects """
    send_pushover_notification(message)
    return {"status": "success"}



if __name__ == "__main__":
    asyncio.run(automatic_processing_of_sales_agents_with_handover())
