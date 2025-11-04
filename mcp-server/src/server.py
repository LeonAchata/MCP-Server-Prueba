"""MCP Toolbox Server - HTTP REST Implementation.

This server exposes MCP tools via HTTP REST endpoints, following the MCP protocol
structure and semantics. It can be deployed as a separate service in Docker/Kubernetes.
"""

import logging
from typing import Any, List, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from tools import add, multiply, uppercase, count_words
from config import setup_logging, settings

logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="MCP Toolbox Server",
    description="Model Context Protocol Toolbox - Exposes tools via HTTP REST",
    version="1.0.0"
)


# ============================================================================
# MCP Data Models (Following MCP Protocol Structure)
# ============================================================================

class MCPToolSchema(BaseModel):
    """MCP Tool definition following the protocol specification."""
    name: str
    description: str
    inputSchema: Dict[str, Any] = Field(alias="inputSchema")
    
    class Config:
        populate_by_name = True


class MCPToolsListResponse(BaseModel):
    """Response for tools/list endpoint."""
    tools: List[MCPToolSchema]


class MCPToolCallRequest(BaseModel):
    """Request for tools/call endpoint."""
    name: str
    arguments: Dict[str, Any]


class MCPToolContent(BaseModel):
    """Tool execution result content."""
    type: str = "text"
    text: str


class MCPToolCallResponse(BaseModel):
    """Response for tools/call endpoint."""
    content: List[MCPToolContent]


# ============================================================================
# MCP Tools Definition
# ============================================================================

MCP_TOOLS = [
    MCPToolSchema(
        name="add",
        description="Add two numbers together",
        inputSchema={
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
    ),
    MCPToolSchema(
        name="multiply",
        description="Multiply two numbers together",
        inputSchema={
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
    ),
    MCPToolSchema(
        name="uppercase",
        description="Convert text to uppercase",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to convert to uppercase"
                }
            },
            "required": ["text"]
        }
    ),
    MCPToolSchema(
        name="count_words",
        description="Count the number of words in a text",
        inputSchema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "Text to count words in"
                }
            },
            "required": ["text"]
        }
    )
]


# ============================================================================
# MCP Protocol Endpoints
# ============================================================================

@app.post("/mcp/tools/list", response_model=MCPToolsListResponse)
async def list_tools():
    """
    MCP Protocol: List available tools.
    
    This endpoint follows the MCP tools/list specification.
    Returns all tools with their schemas in MCP format.
    """
    logger.info(f"MCP tools/list requested - Returning {len(MCP_TOOLS)} tools")
    return MCPToolsListResponse(tools=MCP_TOOLS)


@app.post("/mcp/tools/call", response_model=MCPToolCallResponse)
async def call_tool(request: MCPToolCallRequest):
    """
    MCP Protocol: Execute a tool.
    
    This endpoint follows the MCP tools/call specification.
    Executes the requested tool with provided arguments.
    
    Args:
        request: Tool name and arguments
        
    Returns:
        Tool execution result in MCP content format
    """
    logger.info(f"MCP tools/call: {request.name} | args: {request.arguments}")
    
    try:
        # Execute tool based on name
        if request.name == "add":
            if "a" not in request.arguments or "b" not in request.arguments:
                raise ValueError("Missing required arguments: a, b")
            result = add(request.arguments["a"], request.arguments["b"])
            
        elif request.name == "multiply":
            if "a" not in request.arguments or "b" not in request.arguments:
                raise ValueError("Missing required arguments: a, b")
            result = multiply(request.arguments["a"], request.arguments["b"])
            
        elif request.name == "uppercase":
            if "text" not in request.arguments:
                raise ValueError("Missing required argument: text")
            result = uppercase(request.arguments["text"])
            
        elif request.name == "count_words":
            if "text" not in request.arguments:
                raise ValueError("Missing required argument: text")
            result = count_words(request.arguments["text"])
            
        else:
            logger.error(f"Unknown tool requested: {request.name}")
            raise HTTPException(
                status_code=404,
                detail=f"Tool '{request.name}' not found. Available tools: {[t.name for t in MCP_TOOLS]}"
            )
        
        logger.info(f"Tool {request.name} executed successfully | result: {result}")
        
        # Return result in MCP content format
        return MCPToolCallResponse(
            content=[
                MCPToolContent(type="text", text=str(result))
            ]
        )
        
    except ValueError as e:
        logger.error(f"Invalid arguments for tool {request.name}: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        logger.error(f"Error executing tool {request.name}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Tool execution failed: {str(e)}")


# ============================================================================
# Health & Info Endpoints
# ============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint for Kubernetes liveness/readiness probes."""
    return {
        "status": "healthy",
        "service": "mcp-toolbox",
        "tools_count": len(MCP_TOOLS),
        "protocol": "MCP over HTTP REST"
    }


@app.get("/")
async def root():
    """Root endpoint with service information."""
    return {
        "service": "MCP Toolbox Server",
        "version": "1.0.0",
        "protocol": "Model Context Protocol (MCP) over HTTP REST",
        "endpoints": {
            "list_tools": "POST /mcp/tools/list",
            "call_tool": "POST /mcp/tools/call",
            "health": "GET /health"
        },
        "tools": [t.name for t in MCP_TOOLS]
    }


# ============================================================================
# Startup
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Application startup."""
    setup_logging(settings.log_level)
    logger.info("=" * 60)
    logger.info("MCP Toolbox Server Starting...")
    logger.info(f"Protocol: MCP over HTTP REST")
    logger.info(f"Registered tools: {', '.join([t.name for t in MCP_TOOLS])}")
    logger.info("=" * 60)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port,
        log_level=settings.log_level.lower()
    )
