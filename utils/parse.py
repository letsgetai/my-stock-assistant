import re
import json
from typing import Optional, Tuple, Dict, Any

# 首先，你需要安装这个库:
# pip install json-repair
try:
    from json_repair import repair_json
except ImportError:
    print("警告: 'json-repair' 库未安装。")
    print("请运行: pip install json-repair")
    # 定义一个假的 repair_json 函数，以便代码在未安装时也能运行（尽管功能受限）
    def repair_json(s, *args, **kwargs):
        return s # 原样返回，解析将会失败

def parse_stock_analyst_output_robust(response: str) -> Tuple[str, Optional[Dict[str, Any]]]:
    """
    解析遵循“股票分析师”提示词规范的 AI 输出。
    
    此版本使用 json-repair 库来尝试修复格式错误的 JSON。

    Args:
        response: AI 模型的原始字符串输出。

    Returns:
        一个元组 (thought, tool_call):
        - thought (str): AI 的自然语言思考与分析部分。
        - tool_call (Optional[Dict]): 包含工具调用的字典，如果没有工具调用则为 None。
    """
    
    # 1. 使用正则表达式查找 <tool_calls> 块
    tool_call_match = re.search(r"<tool_calls>(.*?)</tool_calls>", response, re.DOTALL)

    if not tool_call_match:
        # --- 情况 2: 未找到工具调用 (这是最终答案) ---
        thought = response.strip()
        tool_call = None
        return thought, tool_call

    # --- 情况 1: 找到了工具调用 ---
    
    # 1. 提取“思考”部分
    thought = response[:tool_call_match.start()].strip()
    
    # 2. 提取 JSON 字符串
    json_str = tool_call_match.group(1).strip()
    
    tool_call = None
    
    # 3. 尝试标准解析
    try:
        tool_call = json.loads(json_str)
    except json.JSONDecodeError as e:
        # 3a. 标准解析失败 -> 尝试修复
        print(f"--- 警告: 标准 JSON 解析失败: {e} ---")
        print(f"原始 JSON 字符串:\n{json_str}")
        
        try:
            # 3b. 使用 json-repair 尝试修复
            repaired_json_str = repair_json(json_str)
            print(f"--- 提示: 尝试使用 json-repair 修复... ---")
            print(f"修复后的 JSON 字符串:\n{repaired_json_str}")
            
            # 3c. 再次尝试解析修复后的字符串
            tool_call = json.loads(repaired_json_str)
            
        except Exception as repair_e:
            # 3d. 修复或再次解析均失败
            print(f"--- 错误: 修复或解析修复后的 JSON 失败: {repair_e} ---")
            # 回退，将全部内容视为“思考”，不进行工具调用
            thought = response.strip()
            tool_call = None

    return thought, tool_call