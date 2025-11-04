"""Multiplication tool."""

from typing import Any
from ..base import MCPTool


class MultiplyTool(MCPTool):
    """Tool for multiplying two numbers together."""
    
    @property
    def name(self) -> str:
        return "multiply"
    
    @property
    def description(self) -> str:
        return "Multiply two numbers together"
    
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
        Multiply two numbers.
        
        Args:
            a: First number
            b: Second number
            
        Returns:
            Product of a and b
        """
        return a * b
