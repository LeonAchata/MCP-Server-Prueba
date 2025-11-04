"""Base class for MCP tools.

This module provides the abstract base class that all MCP tools should inherit from.
It defines the interface and common functionality for tools.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class MCPTool(ABC):
    """
    Abstract base class for all MCP tools.
    
    Each tool must implement:
    - name: Unique identifier for the tool
    - description: Human-readable description
    - input_schema: JSON schema for input validation
    - execute: The actual tool logic
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """
        Tool name (unique identifier).
        
        Returns:
            str: Tool name in snake_case
        """
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """
        Human-readable description of what the tool does.
        
        Returns:
            str: Tool description
        """
        pass
    
    @property
    @abstractmethod
    def input_schema(self) -> Dict[str, Any]:
        """
        JSON schema defining the tool's input parameters.
        
        Returns:
            Dict: JSON schema object with type, properties, and required fields
        """
        pass
    
    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """
        Execute the tool with given arguments.
        
        Args:
            **kwargs: Tool-specific arguments matching the input_schema
            
        Returns:
            Any: Tool execution result (will be converted to string)
            
        Raises:
            ValueError: If arguments are invalid
            Exception: If tool execution fails
        """
        pass
    
    def to_mcp_schema(self) -> Dict[str, Any]:
        """
        Convert tool to MCP protocol schema format.
        
        Returns:
            Dict: MCP-compliant tool schema
        """
        return {
            "name": self.name,
            "description": self.description,
            "inputSchema": self.input_schema
        }
    
    def __repr__(self) -> str:
        """String representation of the tool."""
        return f"<MCPTool: {self.name}>"
