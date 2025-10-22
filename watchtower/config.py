"""
Configuration management for Watchtower.
"""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings
from loguru import logger

class Settings(BaseSettings):
    """Watchtower configuration settings."""
    
    # Database
    database_path: str = "data/watchtower.duckdb"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "Watchtower API"
    api_version: str = "1.0.0"
    
    # UI Configuration
    ui_host: str = "0.0.0.0"
    ui_port: int = 8501
    
    # Monitoring Configuration
    drift_threshold: float = 0.1
    coverage_threshold: float = 0.95
    kpi_check_interval: int = 300  # seconds
    
    # Alerting Configuration
    alert_email: Optional[str] = None
    alert_webhook: Optional[str] = None
    alert_retry_attempts: int = 3
    
    # Model Configuration
    model_retrain_threshold: float = 0.15
    model_fallback_enabled: bool = True
    model_version: str = "v1.0"
    
    # Logging Configuration
    log_level: str = "INFO"
    log_file: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"

def setup():
    """Setup Watchtower environment."""
    
    # Create necessary directories
    DATA_DIR.mkdir(exist_ok=True)
    LOGS_DIR.mkdir(exist_ok=True)
    
    # Configure logging
    logger.remove()  # Remove default handler
    
    # Add console handler
    logger.add(
        sink=lambda msg: print(msg, end=""),
        level=settings.log_level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    )
    
    # Add file handler if specified
    if settings.log_file:
        logger.add(
            sink=settings.log_file,
            level=settings.log_level,
            rotation="1 day",
            retention="30 days",
            format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
        )
    
    logger.info("Watchtower configuration loaded")
    logger.info(f"Database path: {settings.database_path}")
    logger.info(f"API endpoint: http://{settings.api_host}:{settings.api_port}")
    logger.info(f"UI endpoint: http://{settings.ui_host}:{settings.ui_port}")

def get_database_path() -> Path:
    """Get the database file path."""
    return PROJECT_ROOT / settings.database_path

def validate_config() -> bool:
    """Validate configuration settings."""
    
    # TODO: Implement comprehensive config validation
    # - Check database connectivity
    # - Validate API endpoints
    # - Verify alerting configuration
    # - Check model file existence
    
    try:
        # Check if database directory exists
        db_path = get_database_path()
        if not db_path.parent.exists():
            logger.error(f"Database directory does not exist: {db_path.parent}")
            return False
        
        # Check API port availability
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((settings.api_host, settings.api_port))
        sock.close()
        
        if result == 0:
            logger.warning(f"API port {settings.api_port} is already in use")
        
        logger.info("Configuration validation passed")
        return True
        
    except Exception as e:
        logger.error(f"Configuration validation failed: {e}")
        return False

if __name__ == "__main__":
    setup()
    validate_config()
