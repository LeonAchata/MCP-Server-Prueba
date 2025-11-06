"""Graph nodes for LangGraph workflow."""

import logging
import json
import re
from datetime import datetime
from typing import Dict, Any
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage, SystemMessage
from langsmith import traceable

logger = logging.getLogger(__name__)


def _detect_model_from_text(text: str) -> str | None:
    """
    Detect model name from user text.
    
    Args:
        text: User input text
        
    Returns:
        Model name if detected, None otherwise
    """
    text_lower = text.lower()
    
    # Check for model keywords - using exact registry names
    if re.search(r'\b(usa|use|utiliza|con)\s+(openai|gpt|gpt-4|gpt4)', text_lower):
        return "gpt-4o"  # Registry name for OpenAI
    elif re.search(r'\b(usa|use|utiliza|con)\s+(gemini|google)', text_lower):
        return "gemini-pro"  # Registry name for Gemini
    elif re.search(r'\b(usa|use|utiliza|con)\s+(bedrock|nova|aws)', text_lower):
        return "bedrock-nova-pro"  # Registry name for Bedrock
    
    return None


@traceable(run_type="chain", name="process_input")
def process_input_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Process user input and initialize state.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state
    """
    logger.info(f"Node: process_input | Initializing state")
    
    user_input = state.get("user_input", "")
    current_model = state.get("model")
    
    # Try to detect model from text if not already specified
    if not current_model:
        detected_model = _detect_model_from_text(user_input)
        if detected_model:
            logger.info(f"Node: process_input | Detected model from text: {detected_model}")
            current_model = detected_model
    
    # Add user message to history
    messages = [HumanMessage(content=user_input)]
    
    # Add step for tracking
    steps = state.get("steps", [])
    step_info = {
        "node": "process_input",
        "timestamp": datetime.now().isoformat(),
        "input": user_input
    }
    if current_model:
        step_info["model_selected"] = current_model
    
    steps.append(step_info)
    
    logger.info(f"Node: process_input | User input: {user_input}")
    
    result = {
        "messages": messages,
        "steps": steps
    }
    
    # Update model in state if detected
    if current_model:
        result["model"] = current_model
    
    return result


@traceable(run_type="chain", name="llm_gateway_routing")
async def llm_node(state: Dict[str, Any], llm_client, mcp_client) -> Dict[str, Any]:
    """
    Call LLM Gateway to process messages and decide next action.
    
    Args:
        state: Current agent state
        llm_client: LLM Gateway client
        mcp_client: MCP client for tools
        
    Returns:
        Updated state
    """
    logger.info("Node: llm | Calling LLM via Gateway")
    
    messages = state.get("messages", [])
    steps = state.get("steps", [])
    model = state.get("model")  # Get model from state (can be None)
    
    # Log metadata for tracing
    logger.info(
        f"Node: llm | component=agent, model_requested={model}, "
        f"messages_count={len(messages)}"
    )
    
    # Get tools from MCP in simple dictionary format
    tools = mcp_client.get_tools_description()
    
    # Create system message with tool information
    tool_descriptions = []
    for tool in tools:
        tool_info = f"- {tool['name']}: {tool.get('description', 'No description')}"
        if 'input_schema' in tool:
            props = tool['input_schema'].get('properties', {})
            if props:
                tool_info += f"\n  Parameters: {json.dumps(props)}"
        tool_descriptions.append(tool_info)
    
    system_prompt = f"""You are a helpful AI assistant with access to the following tools:

{chr(10).join(tool_descriptions)}

When you need to use a tool, respond with a tool call in this exact format:
TOOL_CALL: tool_name
ARGUMENTS: {{"arg1": "value1", "arg2": "value2"}}

If you don't need any tools, just respond normally to help the user."""
    
    # Prepare messages for LLM with system prompt
    llm_messages = [SystemMessage(content=system_prompt)] + messages
    
    logger.info(f"Node: llm | Sending {len(llm_messages)} messages to LLM (1 system + {len(messages)} user)")
    
    # Call LLM via Gateway with optional model parameter (now using await)
    response = await llm_client.generate(
        messages=llm_messages,
        model=model,  # Pass model from state (None uses default)
        temperature=0.7,
        max_tokens=2000
    )
    
    logger.info(f"Node: llm | Used model: {model or llm_client.default_model}")
    
    # Check if response contains tool calls
    response_text = response.content
    has_tool_call = "TOOL_CALL:" in response_text
    
    if has_tool_call:
        # Parse tool call from response
        try:
            lines = response_text.strip().split('\n')
            tool_name = None
            tool_args = {}
            
            for line in lines:
                if line.startswith("TOOL_CALL:"):
                    tool_name = line.replace("TOOL_CALL:", "").strip()
                elif line.startswith("ARGUMENTS:"):
                    args_str = line.replace("ARGUMENTS:", "").strip()
                    tool_args = json.loads(args_str)
            
            if tool_name:
                # Add tool call info to response
                response.additional_kwargs["tool_calls"] = [{
                    "name": tool_name,
                    "args": tool_args,
                    "id": f"call_{datetime.now().timestamp()}"
                }]
                # Store as attribute for compatibility
                response.tool_calls = response.additional_kwargs["tool_calls"]
                logger.info(f"Node: llm | Parsed tool call: {tool_name}")
        except Exception as e:
            logger.error(f"Node: llm | Error parsing tool call: {str(e)}")
            has_tool_call = False
    
    logger.info(f"Node: llm | Response received: has_tool_calls={has_tool_call}")
    
    # Get the actual model used (from response metadata or default)
    model_used = response.additional_kwargs.get("model") or model or llm_client.default_model
    cached = response.additional_kwargs.get("cached", False)
    latency_ms = response.additional_kwargs.get("latency_ms", 0)
    
    # Log detailed response info
    logger.info(
        f"Node: llm | Model used: {model_used}, "
        f"cached={cached}, latency={latency_ms}ms"
    )
    
    # Add step with model information
    steps.append({
        "node": "llm",
        "timestamp": datetime.now().isoformat(),
        "model": model_used,
        "cached": cached,
        "latency_ms": latency_ms,
        "has_tool_calls": bool(hasattr(response, 'tool_calls') and response.tool_calls)
    })
    
    return {
        "messages": [response],
        "steps": steps
    }


@traceable(run_type="tool", name="tool_execution")
async def tool_execution_node(state: Dict[str, Any], mcp_client) -> Dict[str, Any]:
    """
    Execute tools requested by LLM via MCP.
    
    Args:
        state: Current agent state
        mcp_client: MCP client for tools
        
    Returns:
        Updated state
    """
    logger.info("Node: tool_execution | Executing tools via MCP")
    
    messages = state.get("messages", [])
    steps = state.get("steps", [])
    
    # Get last AI message with tool calls
    last_message = messages[-1]
    
    if not hasattr(last_message, 'tool_calls') or not last_message.tool_calls:
        logger.warning("Node: tool_execution | No tool calls found")
        return {"steps": steps}
    
    tool_calls = last_message.tool_calls
    tool_messages = []
    executed_tools = []
    
    logger.info(f"Node: tool_execution | Executing {len(tool_calls)} tools via MCP")
    
    # Execute each tool
    for tool_call in tool_calls:
        tool_name = tool_call.get("name")
        tool_args = tool_call.get("args", {})
        tool_id = tool_call.get("id")
        
        try:
            # Call tool via MCP
            result = await mcp_client.call_tool(tool_name, tool_args)
            
            # Create tool message
            tool_message = ToolMessage(
                content=str(result),
                tool_call_id=tool_id,
                name=tool_name
            )
            tool_messages.append(tool_message)
            
            executed_tools.append({
                "name": tool_name,
                "args": tool_args,
                "result": result
            })
            
        except Exception as e:
            logger.error(f"Node: tool_execution | Error executing {tool_name}: {str(e)}")
            # Create error tool message
            tool_message = ToolMessage(
                content=f"Error: {str(e)}",
                tool_call_id=tool_id,
                name=tool_name
            )
            tool_messages.append(tool_message)
    
    logger.info(f"Node: tool_execution | Tool execution completed")
    
    # Add step
    steps.append({
        "node": "tool_execution",
        "timestamp": datetime.now().isoformat(),
        "tools": executed_tools
    })
    
    return {
        "messages": tool_messages,
        "steps": steps
    }


@traceable(run_type="chain", name="final_answer")
def final_answer_node(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract and format final answer.
    
    Args:
        state: Current agent state
        
    Returns:
        Updated state
    """
    logger.info("Node: final_answer | Formatting response")
    
    messages = state.get("messages", [])
    steps = state.get("steps", [])
    
    # Get last AI message
    last_message = messages[-1]
    
    if isinstance(last_message, AIMessage):
        final_answer = last_message.content
    else:
        final_answer = str(last_message)
    
    logger.info(f"Node: final_answer | Final answer: {final_answer[:100]}...")
    
    # Add step
    steps.append({
        "node": "final_answer",
        "timestamp": datetime.now().isoformat()
    })
    
    return {
        "final_answer": final_answer,
        "steps": steps
    }


@traceable(run_type="chain", name="route_decision")
def route_decision(state: Dict[str, Any]) -> str:
    """
    Decide next node based on LLM response.
    
    Args:
        state: Current agent state
        
    Returns:
        Next node name
    """
    messages = state.get("messages", [])
    last_message = messages[-1]
    
    # If there are tool calls, go to tool execution
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        logger.debug("Route decision: tools")
        return "tools"
    
    # Otherwise, go to final answer
    logger.debug("Route decision: final")
    return "final"
