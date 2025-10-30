# === 导入 ===

# 1. 标准库
import os
import datetime

# 2. 第三方库
from dotenv import load_dotenv
from camel.agents import ChatAgent
from camel.models import ModelFactory
from camel.toolkits import FunctionTool, SearchToolkit
# from camel.types import ModelPlatformType, ModelType # 注意：在你的原始代码中未被使用
# from camel.toolkits import get_openai_function_schema, get_openai_tool_schema # 注意：在你的原始代码中未被使用

# 3. 本地应用
from tool.ak import ak_tools
from tool.read_url import read_url_tool
from prompt.system_prompt import s_p_template
from prompt.planner import planner_prompt
from utils.parse import parse_stock_analyst_output_robust
from utils.run_command import run_tool
from utils.save_to_json import save_to_json

# 首先加载环境变量
load_dotenv()

# === 常量和设置 ===

# 定义最终的总结提示模板
FINAL_SUMMARY_PROMPT_TEMPLATE = (
    "基于上述分析结果，给出一个完整的投资建议。"
    "对于一些关键术语请做解释，一些关键结论和数据的使用，请做引用。"
    "你不需要对你的计划做引用，你要面向用户的问题做回答：{question}"
)

# 初始化工具
# search_tavily = FunctionTool(SearchToolkit().search_tavily) # 保持注释状态
TOOLS = ak_tools + [read_url_tool]  # + [search_tavily]
TOOLS_DESCRIPTION = str([tool.openai_tool_schema for tool in TOOLS])

# 初始化模型
MODEL = ModelFactory.create(
    model_platform="openai",
    model_type=os.environ.get("OPENAI_MODEL", "gpt-4-turbo"), # 提供一个默认模型
    url=os.environ.get("OPENAI_API_URL"),
    model_config_dict={
        "max_tokens": 32768,
        "temperature": 0.1,
    }
)

# === 核心功能 ===

def reaction_agent(question: str):
    """
    运行一个两阶段的代理流程：
    1. 规划器(Planner)代理生成一个步骤计划。
    2. 主(Main)代理执行该计划，并根据需要使用工具。
    """
    print(f"--- 开始分析: {question} ---")

    # 1. 规划器代理: 生成计划
    print("--- 规划器(Planner)代理运行中... ---")
    planner = ChatAgent(
        system_message=planner_prompt,
        model=MODEL,
        # tools=TOOLS, # 保持注释状态
    )
    response_planner = planner.step(question)
    plan = response_planner.msg.content
    print(f"--- 📝 生成的计划:\n{plan}\n---")

    # 2. 主执行代理: 遵循计划并使用工具
    print("--- 🛠️ 主(Main)代理运行中... ---")
    agent = ChatAgent(
        system_message=s_p_template.format(tools=TOOLS_DESCRIPTION, plan=plan),
        model=MODEL,
        # tools=TOOLS, # 保持注释状态
    )

    response = agent.step(question)
    resp = response.msg.content

    # 3. 工具使用循环
    while resp.endswith("</tool_calls>"):
        print("--- 🔧 检测到工具调用 ---")
        print(f"代理输出:\n{resp}")
        
        # 解析思想和工具调用
        thought, tool_call = parse_stock_analyst_output_robust(resp)
        # 运行工具
        tool_result = run_tool(tool_call, TOOLS)
        
        print(f"工具结果:\n{tool_result}\n---")
        # 将工具结果反馈给代理
        response = agent.step(tool_result)
        resp = response.msg.content

    # 4. 最终总结步骤
    print("--- 📊 生成最终总结... ---")
    final_prompt = FINAL_SUMMARY_PROMPT_TEMPLATE.format(question=question)
    response = agent.step(final_prompt)
    final_response = response.msg.content
    
    print("--- ✅ 分析完成 ---")
    print(f"最终回复:\n{final_response}")

    # 5. 保存结果
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    history_path = f"output/agent/output_{timestamp}.json"
    memory_path = f"output/agent/memory_{timestamp}.json"
    
    save_to_json(agent.chat_history, file_path=history_path)
    agent.save_memory(path=memory_path)
    
    print("--- 💾 结果已保存 ---")
    print(f"聊天记录: {history_path}")
    print(f"代理内存: {memory_path}")
    
    return final_response

# === 脚本执行 ===

if __name__ == "__main__":
    # 脚本的主入口点
    try:
        reaction_agent("小米这家公司的值得投资吗？")
    except KeyError as e:
        print(f"错误: 缺少环境变量 {e}。请检查你的 .env 文件。")
    except Exception as e:
        print(f"运行中发生错误: {e}")