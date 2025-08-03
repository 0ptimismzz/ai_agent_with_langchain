from mcp.server.fastmcp import FastMCP
import mcp

mcp = mcp.server.fastmcp.FastMCP("Math Tools")

@mcp.tool()
def add(a:int, b:int):
    """Add two numbers"""
    return a + b

@mcp.tool()
def multiply(a:int, b:int):
    """Multiply two numbers"""
    return a * b

if __name__ == '__main__':
    mcp.run(transport="stdio")