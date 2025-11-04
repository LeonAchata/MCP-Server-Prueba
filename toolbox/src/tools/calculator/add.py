"""Addition tool."""

from typing import Any
from ..base import MCPTool


class AddTool(MCPTool):
    """Tool for adding two numbers together."""
    
    @property
    def name(self) -> str:
        return "add"
    
    @property
    def description(self) -> str:
        return "Add two numbers together"
    
    @property
    def input_schema(self) -> dict:
        return {
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
    
    async def execute(self, a: float, b: float) -> float:
        """
        Add two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Sum of a and b
        """
        return a + b
