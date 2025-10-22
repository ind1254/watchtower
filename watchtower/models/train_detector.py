"""
Model training module for fraud detection.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from loguru import logger

from ..config import settings, get_database_path

class FraudDetectorTrainer:
    """Train fraud detection models."""
    
    def __init__(self, model_path: Optional[str] = None):
        """Initialize trainer."""
        self.model_path = model_path or "models/fraud_detector.pkl"
        self.scaler_path = "models/scaler.pkl"
        self.encoder_path = "models/encoders.pkl"
        self.model = None
        self.scaler = None
        self.encoders = {}
        
        # Ensure models directory exists
        Path("models").mkdir(exist_ok=True)
    
    def load_training_data(self) -> Tuple[pd.DataFrame, pd.Series]:
        """Load training data from database."""
        
        # TODO: Implement comprehensive data loading
        # - Load transaction features
        # - Handle missing values
        # - Feature engineering
        # - Data validation
        
        import duckdb
        
        db_path = get_database_path()
        conn = duckdb.connect(str(db_path))
        
        # Load transactions and predictions for training
        query = """
            SELECT 
                t.amount,
                t.user_id,
                t.merchant_category,
                t.country,
                t.timestamp,
                t.is_fraud
            FROM transactions t
            ORDER BY t.timestamp
        """
        
        result = conn.execute(query).fetchall()
        conn.close()
        
        if not result:
            raise ValueError("No training data available")
        
        df = pd.DataFrame(result, columns=[
            'amount', 'user_id', 'merchant_category', 'country', 'timestamp', 'is_fraud'
        ])
        
        # Feature engineering
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        df['day_of_week'] = pd.to_datetime(df['timestamp']).dt.dayofweek
        df['amount_log'] = np.log1p(df['amount'])
        
        # Prepare features and target
        feature_columns = ['amount', 'user_id', 'merchant_category', 'country', 'hour', 'day_of_week', 'amount_log']
        X = df[feature_columns].copy()
        y = df['is_fraud']
        
        return X, y
    
    def preprocess_features(self, X: pd.DataFrame) -> pd.DataFrame:
        """Preprocess features for training."""
        
        # TODO: Implement comprehensive feature preprocessing
        # - Handle categorical variables
        # - Scale numerical features
        # - Handle missing values
        # - Feature selection
        
        X_processed = X.copy()
        
        # Encode categorical variables
        categorical_columns = ['merchant_category', 'country']
        
        for col in categorical_columns:
            if col not in self.encoders:
                self.encoders[col] = LabelEncoder()
                X_processed[col] = self.encoders[col].fit_transform(X_processed[col].astype(str))
            else:
                # Handle unseen categories
                X_processed[col] = X_processed[col].astype(str)
                X_processed[col] = X_processed[col].map(
                    lambda x: self.encoders[col].transform([x])[0] 
                    if x in self.encoders[col].classes_ 
                    else 0
                )
        
        # Scale numerical features
        numerical_columns = ['amount', 'user_id', 'hour', 'day_of_week', 'amount_log']
        
        if self.scaler is None:
            self.scaler = StandardScaler()
            X_processed[numerical_columns] = self.scaler.fit_transform(X_processed[numerical_columns])
        else:
            X_processed[numerical_columns] = self.scaler.transform(X_processed[numerical_columns])
        
        return X_processed
    
    def train_model(self, X: pd.DataFrame, y: pd.Series) -> Dict[str, float]:
        """Train the fraud detection model."""
        
        # TODO: Implement comprehensive model training
        # - Hyperparameter tuning
        # - Cross-validation
        # - Model selection
        # - Performance evaluation
        
        # Preprocess features
        X_processed = self.preprocess_features(X)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X_processed, y, test_size=0.2, random_state=42, stratify=y
        )
        
        # Train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            min_samples_split=5,
            min_samples_leaf=2,
            random_state=42,
            class_weight='balanced'
        )
        
        self.model.fit(X_train, y_train)
        
        # Evaluate model
        train_score = self.model.score(X_train, y_train)
        test_score = self.model.score(X_test, y_test)
        
        # Cross-validation
        cv_scores = cross_val_score(self.model, X_processed, y, cv=5, scoring='f1')
        
        # Generate predictions for detailed metrics
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calculate additional metrics
        from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
        
        precision = precision_score(y_test, y_pred)
        recall = recall_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred)
        auc = roc_auc_score(y_test, y_pred_proba)
        
        metrics = {
            'train_accuracy': train_score,
            'test_accuracy': test_score,
            'precision': precision,
            'recall': recall,
            'f1_score': f1,
            'auc_score': auc,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
        
        logger.info(f"Model training complete. Test accuracy: {test_score:.3f}, F1: {f1:.3f}")
        
        return metrics
    
    def save_model(self):
        """Save trained model and preprocessing components."""
        
        # TODO: Implement model persistence
        # - Save model artifacts
        # - Version control
        # - Model metadata
        # - Backup strategies
        
        if self.model is None:
            raise ValueError("No model to save. Train model first.")
        
        # Save model
        joblib.dump(self.model, self.model_path)
        
        # Save scaler
        if self.scaler is not None:
            joblib.dump(self.scaler, self.scaler_path)
        
        # Save encoders
        if self.encoders:
            joblib.dump(self.encoders, self.encoder_path)
        
        logger.info(f"Model saved to {self.model_path}")
    
    def load_model(self):
        """Load trained model and preprocessing components."""
        
        # TODO: Implement model loading
        # - Load model artifacts
        # - Validate model version
        # - Check model compatibility
        # - Handle loading errors
        
        try:
            self.model = joblib.load(self.model_path)
            logger.info(f"Model loaded from {self.model_path}")
            
            # Load scaler if exists
            scaler_file = Path(self.scaler_path)
            if scaler_file.exists():
                self.scaler = joblib.load(self.scaler_path)
            
            # Load encoders if exist
            encoder_file = Path(self.encoder_path)
            if encoder_file.exists():
                self.encoders = joblib.load(self.encoder_path)
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return False
    
    def predict(self, X: pd.DataFrame) -> Tuple[np.ndarray, np.ndarray]:
        """Make predictions on new data."""
        
        # TODO: Implement prediction pipeline
        # - Preprocess features
        # - Make predictions
        # - Return probabilities
        # - Handle errors
        
        if self.model is None:
            raise ValueError("No model loaded. Load or train model first.")
        
        # Preprocess features
        X_processed = self.preprocess_features(X)
        
        # Make predictions
        predictions = self.model.predict(X_processed)
        probabilities = self.model.predict_proba(X_processed)[:, 1]
        
        return predictions, probabilities

def train_fraud_detector() -> Dict[str, any]:
    """Main training function."""
    
    # TODO: Implement comprehensive training pipeline
    # - Data validation
    # - Model training
    # - Performance evaluation
    # - Model deployment
    
    trainer = FraudDetectorTrainer()
    
    try:
        # Load training data
        logger.info("Loading training data...")
        X, y = trainer.load_training_data()
        
        logger.info(f"Loaded {len(X)} training samples")
        logger.info(f"Fraud rate: {y.mean():.3f}")
        
        # Train model
        logger.info("Training model...")
        metrics = trainer.train_model(X, y)
        
        # Save model
        trainer.save_model()
        
        # Generate summary
        summary = {
            'timestamp': datetime.now(),
            'training_samples': len(X),
            'fraud_rate': y.mean(),
            'metrics': metrics,
            'model_path': trainer.model_path
        }
        
        logger.info("Fraud detector training complete")
        return summary
        
    except Exception as e:
        logger.error(f"Training failed: {e}")
        return {'error': str(e)}

if __name__ == "__main__":
    # Test training
    result = train_fraud_detector()
    print(f"Training result: {result}")
