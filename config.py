"""Configuration file for Watchtower AML Platform."""

import os
from pathlib import Path

# Project paths
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
SAMPLES_DIR = DATA_DIR / "samples"
SYNTHETIC_DIR = DATA_DIR / "synthetic"
MODELS_DIR = PROJECT_ROOT / "models"

# Create directories if they don't exist
DATA_DIR.mkdir(exist_ok=True)
SAMPLES_DIR.mkdir(exist_ok=True)
SYNTHETIC_DIR.mkdir(exist_ok=True)
(SYNTHETIC_DIR / "transactions").mkdir(exist_ok=True)
(SYNTHETIC_DIR / "crypto").mkdir(exist_ok=True)
(SYNTHETIC_DIR / "kyc").mkdir(exist_ok=True)
(SYNTHETIC_DIR / "merchants").mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)

# API Keys (load from environment variables)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

# Model configuration
MODEL_NAME = "rf_model.joblib"
MODEL_PATH = MODELS_DIR / MODEL_NAME

# Data generation settings
NUM_SYNTHETIC_TRANSACTIONS = 10000
NUM_SYNTHETIC_CRYPTO = 5000
NUM_SYNTHETIC_KYC = 3000
NUM_SYNTHETIC_MERCHANTS = 1000

# Fraud detection settings
FRAUD_RATE = 0.08  # 8% fraud rate for better RL training (can be adjusted 0.05-0.10)

# API configuration
API_HOST = "0.0.0.0"
API_PORT = 8000
API_TITLE = "Watchtower AML API"
API_VERSION = "1.0.0"

