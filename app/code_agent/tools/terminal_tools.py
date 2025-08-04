from app.code_agent.utils.mcp import create_mcp_stdio_client


async def get_stdio_terminal_tools():
    params = {
        "command":"python",
        "args":[
            "/Users/horizon/Desktop/project/new_agent/app/code_agent/mcp/terminal_tools.py",
        ]
    }

    client, tools = await create_mcp_stdio_client("terminal_tools", params)
    return tools