def run_tool(tool_call, tools):
    if tool_call is None:
            return None

    tool_name = tool_call.get("tool_name")
    parameters = tool_call.get("parameters", {})

    for tool in tools:
        if tool.openai_tool_schema['function']['name'] == tool_name:
            try:
                result = tool(**parameters)
                return f"<tool_result>{result}</tool_result>"
            except Exception as e:
                return f"<tool_error>{str(e)}</tool_error>" 
    
    return f"<tool_error>Tool '{tool_name}' not found.</tool_error>"
