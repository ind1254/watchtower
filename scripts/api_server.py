"""FastAPI server for Watchtower AML Platform."""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from pathlib import Path
import sys
from typing import List, Optional

sys.path.append(str(Path(__file__).parent.parent))
from config import MODEL_PATH, API_TITLE, API_VERSION

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

# Load model
try:
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded from {MODEL_PATH}")
except FileNotFoundError:
    print(f"Warning: Model not found at {MODEL_PATH}. Please train the model first.")
    model = None

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

@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Watchtower AML API",
        "version": API_VERSION,
        "status": "online",
        "model_loaded": model is not None
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=TransactionResponse)
async def predict_transaction(transaction: TransactionRequest):
    """Predict if a single transaction is fraudulent."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the model first.")
    
    try:
        # Prepare feature vector
        features = np.array([[
            transaction.Time,
            transaction.V1, transaction.V2, transaction.V3, transaction.V4,
            transaction.V5, transaction.V6, transaction.V7, transaction.V8,
            transaction.V9, transaction.V10, transaction.V11, transaction.V12,
            transaction.V13, transaction.V14, transaction.V15, transaction.V16,
            transaction.V17, transaction.V18, transaction.V19, transaction.V20,
            transaction.V21, transaction.V22, transaction.V23, transaction.V24,
            transaction.V25, transaction.V26, transaction.V27, transaction.V28,
            transaction.Amount
        ]])
        
        # Predict
        fraud_probability = model.predict_proba(features)[0, 1]
        is_fraud = fraud_probability > 0.5
        risk_score = fraud_probability * 100
        
        return TransactionResponse(
            is_fraud=bool(is_fraud),
            fraud_probability=round(float(fraud_probability), 4),
            risk_score=round(float(risk_score), 2)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Prediction error: {str(e)}")

@app.post("/predict/batch", response_model=BatchTransactionResponse)
async def predict_batch_transactions(file: UploadFile = File(...)):
    """Predict fraud for a batch of transactions from CSV file."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded. Please train the model first.")
    
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
        
        # Predict
        fraud_probabilities = model.predict_proba(features)[:, 1]
        predictions = [
            TransactionResponse(
                is_fraud=prob > 0.5,
                fraud_probability=round(float(prob), 4),
                risk_score=round(float(prob * 100), 2)
            )
            for prob in fraud_probabilities
        ]
        
        fraud_count = sum(1 for p in predictions if p.is_fraud)
        
        return BatchTransactionResponse(
            predictions=predictions,
            total_transactions=len(predictions),
            fraud_count=fraud_count,
            fraud_rate=round(fraud_count / len(predictions) * 100, 2)
        )
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="CSV file is empty")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Batch prediction error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    from config import API_HOST, API_PORT
    
    uvicorn.run(app, host=API_HOST, port=API_PORT)

