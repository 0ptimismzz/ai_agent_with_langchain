from app.code_agent.utils.mcp import create_mcp_stdio_client


async def get_stdio_shell_tools():
    params = {
        "command":"python",
        "args":[
            "/Users/horizon/Desktop/project/ai_agent/app/code_agent/mcp/shell_tools.py",
        ]
    }

    client, tools = await create_mcp_stdio_client("shell_tools", params)
    return tools