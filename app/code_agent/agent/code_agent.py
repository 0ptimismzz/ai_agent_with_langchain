import asyncio

from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt import create_react_agent

from app.code_agent.model.qwen import llm_qwen
from app.code_agent.tools.file_saver import FileSaver
from app.code_agent.tools.file_tools import file_tools
from app.code_agent.tools.shell_tools import get_stdio_shell_tools


# 调用自己写的mcp工具
async def run_agent():

    memory = FileSaver()

    shell_tools = await get_stdio_shell_tools()
    tools = file_tools + shell_tools

    agent = create_react_agent(
        model=llm_qwen,
        tools=tools,
        checkpointer=memory,
        debug=False,
    )

    config = RunnableConfig(configurable={"thread_id":2})

    while True:
        user_input = input("用户：")
        if user_input == "exit":
            break
        res = await agent.ainvoke(input={"messages": user_input}, config=config)

        print("助理：", res["messages"][-1].content)
        print("\n")

asyncio.run(run_agent())