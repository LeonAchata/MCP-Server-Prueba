"""Calculator tools for MCP server."""

import logging

logger = logging.getLogger(__name__)


def add(a: float, b: float) -> float:
    """
    Add two numbers.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Sum of a and b
    """
    result = a + b
    logger.info(f"Tool called: add | params: {{'a': {a}, 'b': {b}}} | result: {result}")
    return result


def multiply(a: float, b: float) -> float:
    """
    Multiply two numbers.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Product of a and b
    """
    result = a * b
    logger.info(f"Tool called: multiply | params: {{'a': {a}, 'b': {b}}} | result: {result}")
    return result
