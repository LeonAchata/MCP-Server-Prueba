"""Uppercase text tool."""

from typing import Any
from ..base import MCPTool


class UppercaseTool(MCPTool):
    """Tool for converting text to uppercase."""
    
    @property
    def name(self) -> str:
        return "uppercase"
    
    @property
    def description(self) -> str:
        return "Convert text to uppercase"
    
    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to convert to uppercase"
                }
            },
            "required": ["text"]
        }
    
    async def execute(self, text: str) -> str:
        """
        Convert text to uppercase.
        
        Args:
            text: Text to convert
            
        Returns:
            Text in uppercase
        """
        return text.upper()
