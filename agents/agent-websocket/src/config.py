"""Configuration for Agent."""

import logging
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Agent settings."""
    
    # MCP Server (for tools)
    mcp_server_url: str = "http://toolbox:8000"
    
    # LLM Gateway (for LLM calls)
    llm_gateway_url: str = "http://llm-gateway:8003"
    default_model: str = "bedrock-nova-pro"
    
    # LangSmith Configuration
    langchain_tracing_v2: bool = True
    langchain_api_key: str = ""
    langchain_project: str = "mcp-agent-websocket"
    langchain_endpoint: str = "https://api.smith.langchain.com"
    
    # Logging
    log_level: str = "DEBUG"
    
    # API
    host: str = "0.0.0.0"
    port: int = 8000
    
    class Config:
        env_file = ".env"
        case_sensitive = False


def setup_logging(log_level: str = "DEBUG"):
    """Setup logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='[%(asctime)s] %(levelname)s [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def setup_langsmith():
    """Setup LangSmith environment variables for tracing."""
    if settings.langchain_api_key:
        os.environ["LANGCHAIN_TRACING_V2"] = str(settings.langchain_tracing_v2).lower()
        os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
        os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
        os.environ["LANGCHAIN_ENDPOINT"] = settings.langchain_endpoint
        logging.info(f"✅ LangSmith tracing enabled - Project: {settings.langchain_project}")
    else:
        logging.warning("⚠️ LangSmith API key not configured - Tracing disabled")


settings = Settings()
