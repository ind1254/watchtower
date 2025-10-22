"""
Watchtower package initialization.
"""

__version__ = "1.0.0"
__author__ = "Watchtower Team"
__description__ = "Risk Coverage & Drift Monitor for Financial-Crime Models"

# Import main components
from .config import settings
from .monitoring import coverage, drift, alert_kpis
from .models import train_detector, serve
from .api import main as api_main

__all__ = [
    "settings",
    "coverage",
    "drift", 
    "alert_kpis",
    "train_detector",
    "serve",
    "api_main"
]
