from pydantic import BaseModel, Field

from app.bailian.common import chat_prompt_template, llm
from langchain_core.tools import tool, Tool


class AddInputArgs(BaseModel):
    a:str = Field(description="first number")
    b:str = Field(description="second number")

@tool(
    description="add two numbers",
    args_schema=AddInputArgs,
    return_direct=True,
)
def add(a,b):
    """add two numbers"""
    return a + b

tool_dict = {
    "add": add,
}
# add_tools = Tool.from_function(
#     func=add,
#     name="add",
#     description="add two numbers",
# )

llm_with_tools = llm.bind_tools([add])

chain = chat_prompt_template | llm_with_tools
resp = chain.invoke(input={"role":"计算",
                    "domain":"数学计算",
                    "question":"用工具计算：100+100=?"})
print(resp)

for tool_calls in resp.tool_calls:
    print(tool_calls)
    args = tool_calls['args']
    func_name = tool_calls['name']

    func = tool_dict[func_name]
    tool_content = func.invoke(args)
    print(tool_content)