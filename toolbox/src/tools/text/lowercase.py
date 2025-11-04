"""Lowercase text tool."""

from typing import Any
from ..base import MCPTool


class LowercaseTool(MCPTool):
    """Tool for converting text to lowercase."""
    
    @property
    def name(self) -> str:
        return "lowercase"
    
    @property
    def description(self) -> str:
        return "Convert text to lowercase"
    
    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to convert to lowercase"
                }
            },
            "required": ["text"]
        }
    
    async def execute(self, text: str) -> str:
        """
        Convert text to lowercase.
        
        Args:
            text: Text to convert
            
        Returns:
            Text in lowercase
        """
        return text.lower()
