"""MCP Tools Registry.

This module provides a centralized registry for all MCP tools with dynamic
discovery and execution capabilities.
"""

import logging
from typing import Dict, Type, List

from .base import MCPTool
from .calculator.add import AddTool
from .calculator.subtract import SubtractTool
from .calculator.multiply import MultiplyTool
from .calculator.divide import DivideTool
from .text.uppercase import UppercaseTool
from .text.lowercase import LowercaseTool
from .text.count_words import CountWordsTool

logger = logging.getLogger(__name__)

TOOL_REGISTRY: Dict[str, Type[MCPTool]] = {
    "add": AddTool,
    "subtract": SubtractTool,
    "multiply": MultiplyTool,
    "divide": DivideTool,
    "uppercase": UppercaseTool,
    "lowercase": LowercaseTool,
    "count_words": CountWordsTool,
}


def get_all_tools() -> List[Dict]:
    """Get all available tools in MCP format.
    
    Returns:
        List of tool schemas in MCP format
    """
    tools = []
    for tool_class in TOOL_REGISTRY.values():
        tool_instance = tool_class()
        tools.append(tool_instance.to_mcp_schema())
    logger.info(f"Retrieved {len(tools)} tools from registry")
    return tools


def get_tool(name: str) -> MCPTool:
    """Get a tool instance by name.
    
    Args:
        name: The name of the tool to retrieve
        
    Returns:
        An instance of the requested tool
        
    Raises:
        ValueError: If the tool is not found in the registry
    """
    if name not in TOOL_REGISTRY:
        available = ", ".join(TOOL_REGISTRY.keys())
        raise ValueError(f"Tool '{name}' not found. Available tools: {available}")
    
    tool_class = TOOL_REGISTRY[name]
    return tool_class()


def register_tool(name: str, tool_class: Type[MCPTool]) -> None:
    """Register a new tool in the registry.
    
    Args:
        name: The name to register the tool under
        tool_class: The tool class to register
        
    Raises:
        ValueError: If a tool with the same name already exists
    """
    if name in TOOL_REGISTRY:
        raise ValueError(f"Tool '{name}' is already registered")
    
    TOOL_REGISTRY[name] = tool_class
    logger.info(f"Registered new tool: {name}")


__all__ = [
    "MCPTool",
    "TOOL_REGISTRY",
    "get_all_tools",
    "get_tool",
    "register_tool",
    "AddTool",
    "SubtractTool",
    "MultiplyTool",
    "DivideTool",
    "UppercaseTool",
    "LowercaseTool",
    "CountWordsTool",
]
