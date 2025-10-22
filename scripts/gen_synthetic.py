"""
Synthetic data generation for Watchtower testing and development.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
from pathlib import Path
import json

def generate_synthetic_transactions(n_samples: int = 10000) -> pd.DataFrame:
    """Generate synthetic financial transaction data."""
    
    # TODO: Implement realistic transaction generation
    # - Transaction amounts with realistic distributions
    # - Geographic locations
    # - Time patterns (business hours, weekends)
    # - Merchant categories
    # - User behavior patterns
    
    np.random.seed(42)
    
    data = {
        'transaction_id': [f"TXN_{i:06d}" for i in range(n_samples)],
        'timestamp': pd.date_range(
            start=datetime.now() - timedelta(days=30),
            periods=n_samples,
            freq='1min'
        ),
        'amount': np.random.lognormal(mean=3, sigma=1.5, size=n_samples),
        'user_id': np.random.randint(1000, 9999, n_samples),
        'merchant_category': np.random.choice([
            'retail', 'restaurant', 'gas_station', 'online', 'atm', 'grocery'
        ], n_samples),
        'country': np.random.choice(['US', 'CA', 'MX', 'UK', 'DE'], n_samples),
        'is_fraud': np.random.choice([0, 1], n_samples, p=[0.95, 0.05])
    }
    
    return pd.DataFrame(data)

def generate_model_predictions(transactions: pd.DataFrame) -> pd.DataFrame:
    """Generate synthetic model predictions."""
    
    # TODO: Implement realistic model prediction generation
    # - Add prediction confidence scores
    # - Include feature importance
    # - Model version tracking
    
    predictions = []
    
    for _, tx in transactions.iterrows():
        # Simple rule-based "model" for demo
        fraud_prob = 0.1
        if tx['amount'] > 1000:
            fraud_prob += 0.3
        if tx['merchant_category'] == 'online':
            fraud_prob += 0.2
        if tx['country'] not in ['US', 'CA']:
            fraud_prob += 0.1
            
        predictions.append({
            'transaction_id': tx['transaction_id'],
            'fraud_probability': min(fraud_prob, 0.99),
            'prediction': 1 if fraud_prob > 0.5 else 0,
            'model_version': 'v1.0',
            'prediction_timestamp': tx['timestamp']
        })
    
    return pd.DataFrame(predictions)

def generate_risk_categories() -> dict:
    """Generate risk category definitions."""
    
    # TODO: Implement comprehensive risk categories
    # - Money laundering patterns
    # - Terrorist financing indicators
    # - Sanctions evasion
    # - Market manipulation
    
    return {
        'money_laundering': {
            'description': 'Suspicious patterns indicating money laundering',
            'threshold': 0.7,
            'features': ['amount', 'frequency', 'geographic_patterns']
        },
        'terrorist_financing': {
            'description': 'Indicators of terrorist financing activities',
            'threshold': 0.8,
            'features': ['amount', 'country', 'merchant_category']
        },
        'sanctions_evasion': {
            'description': 'Potential sanctions evasion patterns',
            'threshold': 0.6,
            'features': ['country', 'merchant_category', 'amount']
        },
        'fraud': {
            'description': 'General fraud indicators',
            'threshold': 0.5,
            'features': ['amount', 'merchant_category', 'user_behavior']
        }
    }

def main():
    """Generate all synthetic data."""
    
    print("Generating synthetic data...")
    
    # Create data directory
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Generate transactions
    print("  Generating transactions...")
    transactions = generate_synthetic_transactions(10000)
    transactions.to_csv(data_dir / "synthetic_transactions.csv", index=False)
    
    # Generate predictions
    print("  Generating model predictions...")
    predictions = generate_model_predictions(transactions)
    predictions.to_csv(data_dir / "synthetic_predictions.csv", index=False)
    
    # Generate risk categories
    print("  Generating risk categories...")
    risk_categories = generate_risk_categories()
    with open(data_dir / "synthetic_risk_categories.json", 'w') as f:
        json.dump(risk_categories, f, indent=2)
    
    print("✅ Synthetic data generation complete!")
    print(f"  Generated {len(transactions)} transactions")
    print(f"  Generated {len(predictions)} predictions")
    print(f"  Generated {len(risk_categories)} risk categories")

if __name__ == "__main__":
    main()
