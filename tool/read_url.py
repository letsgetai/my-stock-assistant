from camel.toolkits import FunctionTool

import requests

def read_url(url: str) -> str:
    """
    读取 URL 内容，可用于读取研报的 PDF。

    Args:
        url (str): The URL to read.

    Returns: 
        str: The content of the URL.
    """
    headers = {
        "X-Return-Format": "markdown"
    }
    url_ = f"https://r.jina.ai/{url}"
    response = requests.get(url_, headers=headers)
    if response.status_code != 200:
        return "Error: {}".format(response.status_code)

    content = response.text

    if len(content)<=12000:
        return content
    
    # 待实现，使用LLM提取或者做RAG检索
    return content[:10000]

read_url_tool = FunctionTool(read_url)

if __name__ == "__main__":
    print(read_url("https://pdf.dfcfw.com/pdf/H3_AP202508181729725661_1.pdf", "贵州茅台"))