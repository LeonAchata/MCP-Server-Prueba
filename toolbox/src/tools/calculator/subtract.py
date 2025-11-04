"""Subtraction tool."""

from typing import Any
from ..base import MCPTool


class SubtractTool(MCPTool):
    """Tool for subtracting two numbers."""
    
    @property
    def name(self) -> str:
        return "subtract"
    
    @property
    def description(self) -> str:
        return "Subtract two numbers"
    
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
                    "description": "Second number to subtract from the first"
                }
            },
            "required": ["a", "b"]
        }
    
    async def execute(self, a: float, b: float) -> float:
        """
        Subtract two numbers.
        
        Args:
            a: First number
            b: Second number to subtract
            
        Returns:
            Result of a - b
        """
        return a - b
