"""FastAPI server for Watchtower AML Platform."""

from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
import torch
from pathlib import Path
import sys
from typing import List, Optional

sys.path.append(str(Path(__file__).parent.parent))
from config import MODEL_PATH, DQN_MODEL_PATH, NORM_PARAMS_PATH, DEFAULT_MODEL_TYPE, API_TITLE, API_VERSION

# Import RL and normalization components
try:
    from scripts.rl_agent import DQNAgent
    from scripts.model_utils import Normalizer, load_normalizer
    RL_AVAILABLE = True
except ImportError as e:
    RL_AVAILABLE = False
    print(f"Warning: RL components not available: {e}")

app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description="AML Intelligence Platform API for fraud detection and risk analysis"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Random Forest model
try:
    rf_model = joblib.load(MODEL_PATH)
    print(f"Random Forest model loaded from {MODEL_PATH}")
except FileNotFoundError:
    print(f"Warning: Random Forest model not found at {MODEL_PATH}. Please train the model first.")
    rf_model = None

# Load DQN model
dqn_agent = None
normalizer = None

if RL_AVAILABLE:
    try:
        dqn_agent = DQNAgent(state_dim=30, action_dim=2)
        dqn_agent.load(str(DQN_MODEL_PATH))
        dqn_agent.q_network.eval()  # Set to evaluation mode (disable dropout)
        dqn_agent.epsilon = 0.0  # Disable exploration for inference
        print(f"DQN model loaded from {DQN_MODEL_PATH}")
    except FileNotFoundError:
        print(f"Warning: DQN model not found at {DQN_MODEL_PATH}. DQN predictions will not be available.")
    except Exception as e:
        print(f"Warning: Error loading DQN model: {e}. DQN predictions will not be available.")
        dqn_agent = None
    
    # Load normalization parameters
    if dqn_agent is not None:
        try:
            normalizer = load_normalizer(NORM_PARAMS_PATH)
            print(f"Normalization parameters loaded")
        except Exception as e:
            print(f"Warning: Could not load normalization parameters: {e}")
            normalizer = None
else:
    print("Warning: RL components not available. DQN predictions will not be available.")

# Request/Response models
class TransactionRequest(BaseModel):
    Time: float
    V1: float
    V2: float
    V3: float
    V4: float
    V5: float
    V6: float
    V7: float
    V8: float
    V9: float
    V10: float
    V11: float
    V12: float
    V13: float
    V14: float
    V15: float
    V16: float
    V17: float
    V18: float
    V19: float
    V20: float
    V21: float
    V22: float
    V23: float
    V24: float
    V25: float
    V26: float
    V27: float
    V28: float
    Amount: float

class TransactionResponse(BaseModel):
    is_fraud: bool
    fraud_probability: float
    risk_score: float

class BatchTransactionResponse(BaseModel):
    predictions: List[TransactionResponse]
    total_transactions: int
    fraud_count: int
    fraud_rate: float


def predict_with_dqn(features: np.ndarray, normalizer: Normalizer) -> dict:
    """
    Predict fraud using DQN model with normalization and Q-value conversion.
    
    Args:
        features: Feature array (can be 1D or 2D, shape: (n_samples, 30) or (30,))
        normalizer: Normalizer instance for feature normalization
        
    Returns:
        Dictionary with 'is_fraud', 'fraud_probability', 'risk_score'
    """
    if dqn_agent is None:
        raise ValueError("DQN model is not loaded")
    if normalizer is None:
        raise ValueError("Normalizer is not loaded")
    
    # Ensure features is 2D
    was_1d = features.ndim == 1
    if was_1d:
        features = features.reshape(1, -1)
    
    # Normalize features
    normalized_features = normalizer.transform(features)
    
    # Get Q-values from DQN
    with torch.no_grad():  # Disable gradient computation for inference
        features_tensor = torch.FloatTensor(normalized_features).to(dqn_agent.device)
        q_values = dqn_agent.q_network(features_tensor)  # Shape: (n_samples, 2)
    
    # Convert Q-values to probabilities using softmax
    q_values_np = q_values.cpu().numpy()
    exp_q = np.exp(q_values_np - np.max(q_values_np, axis=-1, keepdims=True))  # Numerically stable softmax
    probabilities = exp_q / np.sum(exp_q, axis=-1, keepdims=True)
    
    # Extract fraud probability (action 1)
    fraud_probabilities = probabilities[:, 1]
    
    # Determine fraud predictions and create responses
    if was_1d:
        fraud_probability = float(fraud_probabilities[0])
        is_fraud = fraud_probability > 0.5
        risk_score = fraud_probability * 100
        
        return {
            'is_fraud': bool(is_fraud),
            'fraud_probability': round(float(fraud_probability), 4),
            'risk_score': round(float(risk_score), 2)
        }
    else:
        # Return array of results
        return {
            'is_fraud': (fraud_probabilities > 0.5).astype(bool),
            'fraud_probability': fraud_probabilities.round(4),
            'risk_score': (fraud_probabilities * 100).round(2)
        }


def predict_with_rf(features: np.ndarray) -> dict:
    """
    Predict fraud using Random Forest model.
    
    Args:
        features: Feature array (can be 1D or 2D)
        
    Returns:
        Dictionary with 'is_fraud', 'fraud_probability', 'risk_score'
    """
    if rf_model is None:
        raise ValueError("Random Forest model is not loaded")
    
    # Ensure features is 2D
    was_1d = features.ndim == 1
    if was_1d:
        features = features.reshape(1, -1)
    
    # Predict
    fraud_probabilities = rf_model.predict_proba(features)[:, 1]
    
    if was_1d:
        fraud_probability = float(fraud_probabilities[0])
        is_fraud = fraud_probability > 0.5
        risk_score = fraud_probability * 100
        
        return {
            'is_fraud': bool(is_fraud),
            'fraud_probability': round(float(fraud_probability), 4),
            'risk_score': round(float(risk_score), 2)
        }
    else:
        # Return array of results
        return {
            'is_fraud': (fraud_probabilities > 0.5).astype(bool),
            'fraud_probability': fraud_probabilities.round(4),
            'risk_score': (fraud_probabilities * 100).round(2)
        }

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Watchtower AML API",
        "version": API_VERSION,
        "status": "online",
        "models": {
            "random_forest": {
                "loaded": rf_model is not None,
                "available": True
            },
            "dqn": {
                "loaded": dqn_agent is not None and normalizer is not None,
                "available": RL_AVAILABLE
            }
        },
        "default_model": DEFAULT_MODEL_TYPE
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    rf_available = rf_model is not None
    dqn_available = dqn_agent is not None and normalizer is not None
    
    return {
        "status": "healthy" if (rf_available or dqn_available) else "degraded",
        "models": {
            "random_forest": {
                "loaded": rf_available,
                "available": True
            },
            "dqn": {
                "loaded": dqn_available,
                "available": RL_AVAILABLE
            }
        },
        "default_model": DEFAULT_MODEL_TYPE
    }

@app.post("/predict", response_model=TransactionResponse)
async def predict_transaction(
    transaction: TransactionRequest,
    model_type: str = Query(default=DEFAULT_MODEL_TYPE, enum=["dqn", "rf"], description="Model type to use for prediction")
):
    """Predict if a single transaction is fraudulent."""
    try:
        # Prepare feature vector
        features = np.array([
            transaction.Time,
            transaction.V1, transaction.V2, transaction.V3, transaction.V4,
            transaction.V5, transaction.V6, transaction.V7, transaction.V8,
            transaction.V9, transaction.V10, transaction.V11, transaction.V12,
            transaction.V13, transaction.V14, transaction.V15, transaction.V16,
            transaction.V17, transaction.V18, transaction.V19, transaction.V20,
            transaction.V21, transaction.V22, transaction.V23, transaction.V24,
            transaction.V25, transaction.V26, transaction.V27, transaction.V28,
            transaction.Amount
        ])
        
        # Predict using selected model
        if model_type == "dqn":
            if dqn_agent is None or normalizer is None:
                raise HTTPException(
                    status_code=503,
                    detail="DQN model or normalizer not loaded. Please train the DQN model first."
                )
            result = predict_with_dqn(features, normalizer)
        elif model_type == "rf":
            if rf_model is None:
                raise HTTPException(
                    status_code=503,
                    detail="Random Forest model not loaded. Please train the model first."
                )
            result = predict_with_rf(features)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid model type: {model_type}")
        
        return TransactionResponse(
            is_fraud=result['is_fraud'],
            fraud_probability=result['fraud_probability'],
            risk_score=result['risk_score']
        )
    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.post("/predict/batch", response_model=BatchTransactionResponse)
async def predict_batch_transactions(
    file: UploadFile = File(...),
    model_type: str = Query(default=DEFAULT_MODEL_TYPE, enum=["dqn", "rf"], description="Model type to use for prediction")
):
    """Predict fraud for a batch of transactions from CSV file."""
    try:
        # Read CSV
        df = pd.read_csv(file.file)
        
        # Validate columns
        required_cols = ['Time'] + [f'V{i}' for i in range(1, 29)] + ['Amount']
        missing_cols = set(required_cols) - set(df.columns)
        if missing_cols:
            raise HTTPException(
                status_code=400,
                detail=f"Missing required columns: {missing_cols}"
            )
        
        # Prepare features
        features = df[required_cols].values
        
        # Predict using selected model
        if model_type == "dqn":
            if dqn_agent is None or normalizer is None:
                raise HTTPException(
                    status_code=503,
                    detail="DQN model or normalizer not loaded. Please train the DQN model first."
                )
            result = predict_with_dqn(features, normalizer)
        elif model_type == "rf":
            if rf_model is None:
                raise HTTPException(
                    status_code=503,
                    detail="Random Forest model not loaded. Please train the model first."
                )
            result = predict_with_rf(features)
        else:
            raise HTTPException(status_code=400, detail=f"Invalid model type: {model_type}")
        
        # Create predictions list
        predictions = [
            TransactionResponse(
                is_fraud=bool(result['is_fraud'][i]),
                fraud_probability=float(result['fraud_probability'][i]),
                risk_score=float(result['risk_score'][i])
            )
            for i in range(len(result['is_fraud']))
        ]
        
        fraud_count = sum(1 for p in predictions if p.is_fraud)
        
        return BatchTransactionResponse(
            predictions=predictions,
            total_transactions=len(predictions),
            fraud_count=fraud_count,
            fraud_rate=round(fraud_count / len(predictions) * 100, 2)
        )
    except HTTPException:
        raise
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Batch prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT
    
    uvicorn.run(app, host=API_HOST, port=API_PORT)

