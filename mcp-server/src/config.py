"""Configuration for MCP server."""

import logging
import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """MCP Server settings."""
    
    log_level: str = "DEBUG"
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


settings = Settings()
