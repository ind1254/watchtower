"""
Watchtower: Risk Coverage & Drift Monitor for Financial-Crime Models

A comprehensive monitoring system for financial crime detection models,
providing coverage analysis, drift detection, and automated playbooks.
"""

from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application configuration settings."""
    
    # Database
    database_path: str = "data/watchtower.duckdb"
    
    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_title: str = "Watchtower API"
    api_version: str = "1.0.0"
    
    # Streamlit
    streamlit_port: int = 8501
    
    # Logging
    log_level: str = "INFO"
    
    # Model monitoring
    drift_threshold: float = 0.1
    coverage_threshold: float = 0.95
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
SRC_DIR = PROJECT_ROOT / "src"
TESTS_DIR = PROJECT_ROOT / "tests"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)
