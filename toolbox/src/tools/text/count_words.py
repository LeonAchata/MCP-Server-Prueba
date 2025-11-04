"""Count words tool."""

from typing import Any
from ..base import MCPTool


class CountWordsTool(MCPTool):
    """Tool for counting the number of words in text."""
    
    @property
    def name(self) -> str:
        return "count_words"
    
    @property
    def description(self) -> str:
        return "Count the number of words in a text"
    
    @property
    def input_schema(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to count words in"
                }
            },
            "required": ["text"]
        }
    
    async def execute(self, text: str) -> int:
        """
        Count words in text.
        
        Args:
            text: Text to count words in
            
        Returns:
            Number of words in the text
        """
        # Split by whitespace and filter empty strings
        words = [word for word in text.split() if word]
        return len(words)
