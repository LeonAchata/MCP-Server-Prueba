'''MCP Toolbox Server - Refactored with Tool Registry.

This server exposes MCP tools via HTTP REST endpoints using a clean,
scalable tool registry pattern.
'''

import logging
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from tools import get_all_tools, get_tool, TOOL_REGISTRY
from config import setup_logging, settings

logger = logging.getLogger(__name__)

app = FastAPI(
    title='MCP Toolbox Server',
    description='Model Context Protocol Toolbox - Clean & Scalable Architecture',
    version='2.0.0'
)

class MCPToolCallRequest(BaseModel):
    name: str
    arguments: Dict[str, Any]

class MCPToolContent(BaseModel):
    type: str = 'text'
    text: str

class MCPToolCallResponse(BaseModel):
    content: list

@app.post('/mcp/tools/list')
async def list_tools():
    tools = get_all_tools()
    logger.info(f'MCP tools/list requested - Returning {len(tools)} tools')
    return {'tools': tools}

@app.post('/mcp/tools/call')
async def call_tool(request: MCPToolCallRequest):
    tool_name = request.name
    arguments = request.arguments
    logger.info(f'MCP tools/call: {tool_name} | args: {arguments}')
    
    try:
        tool = get_tool(tool_name)
        result = await tool.execute(**arguments)
        logger.info(f'Tool {tool_name} executed successfully | result: {result}')
        return {'content': [{'type': 'text', 'text': str(result)}]}
    except ValueError as e:
        logger.error(f'Invalid request for tool {tool_name}: {str(e)}')
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f'Error executing tool {tool_name}: {str(e)}', exc_info=True)
        raise HTTPException(status_code=500, detail=f'Tool execution failed: {str(e)}')

@app.get('/health')
async def health_check():
    return {
        'status': 'healthy',
        'service': 'mcp-toolbox',
        'version': '2.0.0',
        'tools_count': len(TOOL_REGISTRY),
        'protocol': 'MCP over HTTP REST',
        'architecture': 'Tool Registry Pattern'
    }

@app.get('/')
async def root():
    return {
        'service': 'MCP Toolbox Server',
        'version': '2.0.0',
        'protocol': 'Model Context Protocol (MCP) over HTTP REST',
        'architecture': 'Tool Registry Pattern - Clean & Scalable',
        'endpoints': {
            'list_tools': 'POST /mcp/tools/list',
            'call_tool': 'POST /mcp/tools/call',
            'health': 'GET /health'
        },
        'tools': list(TOOL_REGISTRY.keys()),
        'tools_count': len(TOOL_REGISTRY)
    }

@app.on_event('startup')
async def startup_event():
    setup_logging(settings.log_level)
    logger.info('=' * 70)
    logger.info('MCP Toolbox Server Starting...')
    logger.info(f'Architecture: Tool Registry Pattern (Refactored)')
    logger.info(f'Protocol: MCP over HTTP REST')
    logger.info(f'Version: 2.0.0')
    tool_names = ', '.join(TOOL_REGISTRY.keys())
    logger.info(f'Registered tools ({len(TOOL_REGISTRY)}): {tool_names}')
    logger.info('=' * 70)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host=settings.host, port=settings.port, log_level=settings.log_level.lower())
