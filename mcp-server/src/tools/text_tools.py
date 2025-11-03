"""Text processing tools for MCP server."""

import logging

logger = logging.getLogger(__name__)


def uppercase(text: str) -> str:
    """
    Convert text to uppercase.
    
    Args:
        text: Text to convert
    
    Returns:
        Text in uppercase
    """
    result = text.upper()
    logger.info(f"Tool called: uppercase | params: {{'text': '{text}'}} | result: '{result}'")
    return result


def count_words(text: str) -> int:
    """
    Count words in text.
    
    Args:
        text: Text to count words in
    
    Returns:
        Number of words
    """
    result = len(text.split())
    logger.info(f"Tool called: count_words | params: {{'text': '{text}'}} | result: {result}")
    return result
