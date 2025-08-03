
from langchain.agents import initialize_agent, AgentType
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

from app.bailian.common import create_calc_tools, llm, chat_prompt_template


class Output(BaseModel):
    args: str = Field("输入的参数")
    result: str = Field("返回的结果")
    think: str = Field("思考过程")

parser = JsonOutputParser(pydantic_object=Output)
format_instructions = parser.get_format_instructions()

calc_tools = create_calc_tools()
llm_with_tools = llm.bind_tools(calc_tools)

# 智能体初始化
agent = initialize_agent(
    tools=calc_tools,
    llm=llm_with_tools,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

prompt = chat_prompt_template.format_messages(
    role="计算",
    domain="使用工具进行数学计算",
    question=f"""
请阅读下面的问题，并返回一个严格的JSON对象，不要使用Markdown代码块包裹
格式要求：
{format_instructions}

问题：
101+102=？
"""
)

resp = agent.invoke(prompt)

print(resp)
print(resp["output"])