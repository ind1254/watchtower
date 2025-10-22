"""
Model serving module for fraud detection.
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List, Optional, Tuple, Any
from loguru import logger
import joblib
from pathlib import Path

from ..config import settings
from .train_detector import FraudDetectorTrainer

class FraudDetectorServer:
    """Serve fraud detection model for real-time predictions."""
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize model server."""
        self.model_path = model_path or "models/fraud_detector.pkl"
        self.scaler_path = "models/scaler.pkl"
        self.encoder_path = "models/encoders.pkl"
        self.model = None
        self.scaler = None
        self.encoders = {}
        self.is_loaded = False
        self.model_version = settings.model_version
        
        # Performance tracking
        self.prediction_count = 0
        self.total_prediction_time = 0.0
        self.last_prediction_time = None
    
    def load_model(self) -> bool:
        """Load the trained model and preprocessing components."""
        
        # TODO: Implement robust model loading
        # - Load model artifacts
        # - Validate model integrity
        # - Check model version
        # - Handle loading failures
        
        try:
            # Check if model files exist
            if not Path(self.model_path).exists():
                logger.error(f"Model file not found: {self.model_path}")
                return False
            
            # Load model
            self.model = joblib.load(self.model_path)
            
            # Load scaler if exists
            if Path(self.scaler_path).exists():
                self.scaler = joblib.load(self.scaler_path)
            
            # Load encoders if exist
            if Path(self.encoder_path).exists():
                self.encoders = joblib.load(self.encoder_path)
            
            self.is_loaded = True
            logger.info(f"Model loaded successfully: {self.model_path}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            self.is_loaded = False
            return False
    
    def preprocess_input(self, input_data: Dict[str, Any]) -> pd.DataFrame:
        """Preprocess input data for prediction."""
        
        # TODO: Implement comprehensive input preprocessing
        # - Validate input format
        # - Handle missing values
        # - Apply feature transformations
        # - Error handling
        
        # Convert input to DataFrame
        df = pd.DataFrame([input_data])
        
        # Feature engineering
        df['hour'] = pd.to_datetime(df.get('timestamp', datetime.now())).dt.hour
        df['day_of_week'] = pd.to_datetime(df.get('timestamp', datetime.now())).dt.dayofweek
        df['amount_log'] = np.log1p(df.get('amount', 0))
        
        # Ensure all required columns exist
        required_columns = ['amount', 'user_id', 'merchant_category', 'country', 'hour', 'day_of_week', 'amount_log']
        
        for col in required_columns:
            if col not in df.columns:
                df[col] = 0  # Default value
        
        return df[required_columns]
    
    def predict_single(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make prediction on a single transaction."""
        
        # TODO: Implement single prediction
        # - Validate input
        # - Preprocess features
        # - Make prediction
        # - Return structured result
        
        if not self.is_loaded:
            return {
                'error': 'Model not loaded',
                'prediction': None,
                'probability': None,
                'model_version': self.model_version
            }
        
        try:
            start_time = datetime.now()
            
            # Preprocess input
            X = self.preprocess_input(input_data)
            
            # Make prediction
            prediction = self.model.predict(X)[0]
            probability = self.model.predict_proba(X)[0, 1]
            
            # Update performance tracking
            prediction_time = (datetime.now() - start_time).total_seconds()
            self.prediction_count += 1
            self.total_prediction_time += prediction_time
            self.last_prediction_time = datetime.now()
            
            result = {
                'prediction': int(prediction),
                'probability': float(probability),
                'model_version': self.model_version,
                'prediction_time_ms': prediction_time * 1000,
                'timestamp': datetime.now().isoformat()
            }
            
            return result
            
        except Exception as e:
            logger.error(f"Prediction failed: {e}")
            return {
                'error': str(e),
                'prediction': None,
                'probability': None,
                'model_version': self.model_version
            }
    
    def predict_batch(self, input_data: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Make predictions on a batch of transactions."""
        
        # TODO: Implement batch prediction
        # - Process multiple transactions
        # - Optimize for batch processing
        # - Handle batch errors
        # - Return batch results
        
        if not self.is_loaded:
            return [{
                'error': 'Model not loaded',
                'prediction': None,
                'probability': None,
                'model_version': self.model_version
            } for _ in input_data]
        
        try:
            start_time = datetime.now()
            
            # Preprocess batch
            df_list = []
            for data in input_data:
                df = self.preprocess_input(data)
                df_list.append(df)
            
            X_batch = pd.concat(df_list, ignore_index=True)
            
            # Make batch predictions
            predictions = self.model.predict(X_batch)
            probabilities = self.model.predict_proba(X_batch)[:, 1]
            
            # Update performance tracking
            batch_time = (datetime.now() - start_time).total_seconds()
            self.prediction_count += len(input_data)
            self.total_prediction_time += batch_time
            self.last_prediction_time = datetime.now()
            
            # Format results
            results = []
            for i, (pred, prob) in enumerate(zip(predictions, probabilities)):
                result = {
                    'prediction': int(pred),
                    'probability': float(prob),
                    'model_version': self.model_version,
                    'batch_time_ms': batch_time * 1000 / len(input_data),
                    'timestamp': datetime.now().isoformat()
                }
                results.append(result)
            
            return results
            
        except Exception as e:
            logger.error(f"Batch prediction failed: {e}")
            return [{
                'error': str(e),
                'prediction': None,
                'probability': None,
                'model_version': self.model_version
            } for _ in input_data]
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information and performance metrics."""
        
        # TODO: Implement model information
        # - Model metadata
        # - Performance metrics
        # - Health status
        # - Usage statistics
        
        avg_prediction_time = (
            self.total_prediction_time / self.prediction_count 
            if self.prediction_count > 0 else 0
        )
        
        return {
            'model_version': self.model_version,
            'is_loaded': self.is_loaded,
            'model_path': self.model_path,
            'prediction_count': self.prediction_count,
            'avg_prediction_time_ms': avg_prediction_time * 1000,
            'last_prediction_time': self.last_prediction_time.isoformat() if self.last_prediction_time else None,
            'health_status': 'healthy' if self.is_loaded else 'unhealthy'
        }
    
    def health_check(self) -> Dict[str, Any]:
        """Perform health check on the model server."""
        
        # TODO: Implement comprehensive health check
        # - Model availability
        # - Performance metrics
        # - Resource usage
        # - Error rates
        
        health_status = {
            'status': 'healthy' if self.is_loaded else 'unhealthy',
            'model_loaded': self.is_loaded,
            'model_version': self.model_version,
            'prediction_count': self.prediction_count,
            'last_prediction_time': self.last_prediction_time.isoformat() if self.last_prediction_time else None,
            'timestamp': datetime.now().isoformat()
        }
        
        # Add performance warnings
        if self.prediction_count > 0:
            avg_time = self.total_prediction_time / self.prediction_count
            if avg_time > 1.0:  # More than 1 second average
                health_status['warnings'] = ['High prediction latency']
        
        return health_status
    
    def reload_model(self) -> bool:
        """Reload the model from disk."""
        
        # TODO: Implement model reloading
        # - Reload model artifacts
        # - Validate new model
        # - Handle reload failures
        # - Update model version
        
        logger.info("Reloading model...")
        return self.load_model()

# Global model server instance
model_server = FraudDetectorServer()

def get_model_server() -> FraudDetectorServer:
    """Get the global model server instance."""
    return model_server

def initialize_model_server() -> bool:
    """Initialize the model server."""
    return model_server.load_model()

def predict_fraud(transaction_data: Dict[str, Any]) -> Dict[str, Any]:
    """Predict fraud for a single transaction."""
    return model_server.predict_single(transaction_data)

def predict_fraud_batch(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Predict fraud for multiple transactions."""
    return model_server.predict_batch(transactions)

if __name__ == "__main__":
    # Test model serving
    server = FraudDetectorServer()
    
    if server.load_model():
        # Test prediction
        test_data = {
            'amount': 100.0,
            'user_id': 1234,
            'merchant_category': 'online',
            'country': 'US',
            'timestamp': datetime.now()
        }
        
        result = server.predict_single(test_data)
        print(f"Prediction result: {result}")
        
        # Test health check
        health = server.health_check()
        print(f"Health status: {health}")
    else:
        print("Failed to load model")
