from dotenv import load_dotenv
load_dotenv()
import os
from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.types import ModelPlatformType, ModelType
# from tool.financial_tools import financial_tool_list
from camel.toolkits.openbb_toolkit import OpenBBToolkit
from camel.toolkits import FunctionTool, SearchToolkit
from tool.ak import ak_tools
from tool.read_url import read_url_tool

google_tool = FunctionTool(SearchToolkit().search_tavily)

tools = ak_tools + [google_tool] + [read_url_tool]

# Method 7: Using ModelFactory with string parameters
model = ModelFactory.create(
    model_platform="openai",     # Using string
    model_type=os.environ["OPENAI_MODEL"],    # Using string
    url = os.environ["OPENAI_API_URL"],
    model_config_dict={"max_tokens":32768,
                       "temperature":1,})

system_prompt = """你是一个世界一流的股票分析师 (Stock Analyst Agent)。

# 核心任务
你的任务是深入、客观地分析用户提出的关于特定股票或公司的问题。

# 执行步骤 (HINT)
1.  你**必须**首先使用工具（如 `ak_tools`）来获取股票基本信息和公司信息。
2.  然后，你**必须**使用搜索工具（如 `google_tool`）查找相关的研报链接。
3.  当你获取研报的链接后，你**必须**使用 `read_url` 工具读取至少一篇研报的核心内容。
4.  **最后**，在收集了所有上述信息（基本数据、研报内容）之后，你才能进行深度分析，并总结你的最终结果。

# important: 
    - 严格按照上述步骤执行。
    - 必须使用 `read_url` 至少一次。

记住上面的提示，开始你的调研：
"""


agent = ChatAgent(system_message= system_prompt, model=model, 
                  tools= tools,
                  )

response = agent.step("贵州茅台这个股票可以买嘛?")

print(response.msg.content)