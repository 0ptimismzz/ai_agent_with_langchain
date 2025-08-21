from app.code_agent.utils.mcp import create_mcp_stdio_client


async def get_stdio_browser_tools():
    params = {
        "command":"python",
        "args":[
            "/Users/horizon/Desktop/project/new_agent/app/code_agent/mcp/browser_tools.py",
        ]
    }

    client, tools = await create_mcp_stdio_client("browser_tools", params)
    return tools