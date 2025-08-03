import asyncio

from langchain.agents import initialize_agent, AgentType
from langchain_mcp_adapters.tools import load_mcp_tools
from mcp import StdioServerParameters, ClientSession
from mcp.client.stdio import stdio_client

from app.mcp.common.llm import llm_qwen


async def create_mcp_stdio_client():
    server_params = StdioServerParameters(
        command="python",
        args=["/Users/horizon/Desktop/project/ai_agent/app/mcp/stdio/mcp_stdio_server.py"],
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:

            await session.initialize()
            tools = await load_mcp_tools(session)
            print(tools)

            agent = initialize_agent(
                llm=llm_qwen,
                tools=tools,
                agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
                verbose=True,
            )

            resp = await agent.ainvoke("1 + 2 * 5 = ?")
            return resp

asyncio.run(create_mcp_stdio_client())

