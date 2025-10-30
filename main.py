from dotenv import load_dotenv
load_dotenv()
import os
from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
# from tool.financial_tools import financial_tool_list
from camel.toolkits.openbb_toolkit import OpenBBToolkit
from camel.toolkits import FunctionTool, SearchToolkit, get_openai_function_schema, get_openai_tool_schema
from tool.ak import ak_tools
from tool.read_url import read_url_tool
from prompt.system_prompt import s_p_template
from prompt.planner import planner_prompt
from utils.parse import parse_stock_analyst_output_robust
from utils.run_command import run_tool
from utils.save_to_json import save_to_json
import datetime

search_tavily = FunctionTool(SearchToolkit().search_tavily)

tools = ak_tools + [search_tavily] + [read_url_tool]

# Method 7: Using ModelFactory with string parameters
model = ModelFactory.create(
    model_platform="openai",     # Using string
    model_type=os.environ["OPENAI_MODEL"],    # Using string
    url = os.environ["OPENAI_API_URL"],
    model_config_dict={"max_tokens":32768,
                       "temperature":1,})

tools_description = str([tool.openai_tool_schema for tool in tools])


def reaction_agent(question):
    planner = ChatAgent(system_message= planner_prompt, model=model, 
                    #   tools= tools,
                    )
    response = planner.step(question)
    plan = response.msg.content


    agent = ChatAgent(system_message= s_p_template.format(tools = tools_description, plan = plan), model=model, 
                    #   tools= tools,
                    )

    response = agent.step(question)
    resp = response.msg.content
    while resp.endswith("</tool_calls>"):
        thought, tool_call = parse_stock_analyst_output_robust(resp)
        print(resp)
        tool_result = run_tool(tool_call, tools)
        response = agent.step(tool_result)
        resp = response.msg.content

    save_to_json(agent.chat_history, file_path=f"output/agent/output_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.json")
    print(resp)


reaction_agent("请帮我分析A股股票600519")