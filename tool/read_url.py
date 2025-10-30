from camel.toolkits import FunctionTool
from camel.agents import ChatAgent
import requests
from camel.models import ModelFactory
import os
from dotenv import load_dotenv
load_dotenv()
model = ModelFactory.create(
    model_platform="openai",     # Using string
    model_type=os.environ["OPENAI_MODEL"],    # Using string
    url = os.environ["OPENAI_API_URL"],
    model_config_dict={"max_tokens":32768,
                       "temperature":1,})

read_prompt = """
Please process the following webpage content and user goal to extract relevant information:

## **Webpage Content** 
{webpage_content}


## **Task Guidelines**
1. **Content Scanning for Rational**: Locate the **specific sections/data** directly related to the user's goal within the webpage content
2. **Key Extraction for Evidence**: Identify and extract the **most relevant information** from the content, you never miss any important information, output the **full original context** of the content as far as possible, it can be more than three paragraphs.
3. **Summary Output for Summary**: Organize into a concise paragraph with logical flow, prioritizing clarity and judge the contribution of the information to the goal.

**Final Output Format using JSON format has "rational", "evidence", "summary" feilds**

## **User Goal**
"""

def read_url(url: str, query: str) -> str:
    """
    读取 URL 内容，可用于读取研报的 PDF。

    Args:
        url (str): The URL to read.
        query (str): The query to search.

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

    if len(content)<=5000:
        return content
    
    # 待实现，使用LLM提取或者做RAG检索
    read_agent = ChatAgent(system_message= read_prompt.format(webpage_content = content[:20000]), model=model
                    )
    
    response = read_agent.step(query)

    return response.msg.content

read_url_tool = FunctionTool(read_url)

if __name__ == "__main__":
    print(read_url("https://pdf.dfcfw.com/pdf/H3_AP202508181729725661_1.pdf", "贵州茅台"))