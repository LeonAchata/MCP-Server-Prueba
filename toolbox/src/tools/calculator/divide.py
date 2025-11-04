"""Division tool."""

from typing import Any
from ..base import MCPTool


class DivideTool(MCPTool):
    """Tool for dividing two numbers."""
    
    @property
    def name(self) -> str:
        return "divide"
    
    @property
    def description(self) -> str:
        return "Divide two numbers"
    
    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "a": {
                    "type": "number",
                    "description": "Numerator (number to be divided)"
                },
                "b": {
                    "type": "number",
                    "description": "Denominator (number to divide by, must not be zero)"
                }
            },
            "required": ["a", "b"]
        }
    
    async def execute(self, a: float, b: float) -> float:
        """
        Divide two numbers.
        
        Args:
            a: Numerator
            b: Denominator
            
        Returns:
            Result of a / b
            
        Raises:
            ValueError: If b is zero
        """
        if b == 0:
            raise ValueError("Cannot divide by zero")
        return a / b
