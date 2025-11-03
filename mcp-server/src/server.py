"""MCP Server implementation."""

import logging
import asyncio
from typing import Any
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from tools import add, multiply, uppercase, count_words
from config import setup_logging, settings

logger = logging.getLogger(__name__)

# Initialize MCP server
app = Server("mcp-calculator-text-server")

# Define available tools
TOOLS = [
    Tool(
        name="add",
        description="Add two numbers together",
        inputSchema={
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["a", "b"]
        }
    ),
    Tool(
        name="multiply",
        description="Multiply two numbers together",
        inputSchema={
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "First number"
                },
                "b": {
                    "type": "number",
                    "description": "Second number"
                }
            },
            "required": ["a", "b"]
        }
    ),
    Tool(
        name="uppercase",
        description="Convert text to uppercase",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to convert to uppercase"
                }
            },
            "required": ["text"]
        }
    ),
    Tool(
        name="count_words",
        description="Count the number of words in a text",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to count words in"
                }
            },
            "required": ["text"]
        }
    )
]


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    logger.debug(f"Tools discovery requested. Returning {len(TOOLS)} tools")
    return TOOLS


@app.call_tool()
async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
    """
    Execute a tool by name with given arguments.
    
    Args:
        name: Tool name to execute
        arguments: Tool arguments
    
    Returns:
        Tool execution result
    """
    logger.info(f"Tool call received: {name} | params: {arguments}")
    
    try:
        if name == "add":
            result = add(arguments["a"], arguments["b"])
        elif name == "multiply":
            result = multiply(arguments["a"], arguments["b"])
        elif name == "uppercase":
            result = uppercase(arguments["text"])
        elif name == "count_words":
            result = count_words(arguments["text"])
        else:
            error_msg = f"Unknown tool: {name}"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        logger.info(f"Tool {name} executed successfully | result: {result}")
        return [TextContent(type="text", text=str(result))]
    
    except Exception as e:
        logger.error(f"Error executing tool {name}: {str(e)}")
        raise


async def main():
    """Run MCP server."""
    setup_logging(settings.log_level)
    logger.info(f"Starting MCP Server...")
    logger.info(f"Registered tools: {', '.join([tool.name for tool in TOOLS])}")
    
    async with stdio_server() as (read_stream, write_stream):
        logger.info(f"MCP Server running on stdio transport")
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
