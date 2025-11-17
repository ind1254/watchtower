"""Generate synthetic transaction data for training and testing."""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import random
from pathlib import Path
import sys

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))
from config import SYNTHETIC_DIR, NUM_SYNTHETIC_TRANSACTIONS, FRAUD_RATE

fake = Faker()

def generate_transaction_features(num_transactions, fraud_rate=None):
    """
    Generate synthetic transaction features similar to the sample data.
    
    Args:
        num_transactions: Number of transactions to generate
        fraud_rate: Fraud rate (0.0-1.0). If None, uses config.FRAUD_RATE
    """
    if fraud_rate is None:
        fraud_rate = FRAUD_RATE
    
    transactions = []
    
    # Pre-calculate how many fraud cases we need for better balance
    num_fraud = int(num_transactions * fraud_rate)
    num_normal = num_transactions - num_fraud
    
    # Create balanced list of classes
    classes = [1] * num_fraud + [0] * num_normal
    np.random.shuffle(classes)
    
    for i in range(num_transactions):
        is_fraud = classes[i]
        
        # Generate PCA-like features (V1-V28)
        if is_fraud:
            # Fraud transactions: more extreme and suspicious patterns
            features = np.random.randn(28).tolist()
            # Make fraud features more distinguishable
            # Higher variance in key features
            features[0] = np.random.normal(2.5, 1.5)  # V1: often high for fraud
            features[1] = np.random.normal(-2.0, 1.2)  # V2: often negative for fraud
            features[2] = np.random.normal(1.8, 1.0)   # V3: elevated
            features[3] = np.random.normal(-1.5, 1.0)  # V4: negative
            # Add more variation to other features
            for j in range(4, 28):
                if random.random() < 0.4:  # 40% chance of extreme values
                    features[j] = np.random.normal(0, 2.5)
            
            # Fraud amounts: often larger or unusual
            if random.random() < 0.6:  # 60% larger amounts
                amount = np.random.lognormal(mean=4.5, sigma=1.8)
            else:  # 40% small amounts (testing limits)
                amount = np.random.lognormal(mean=2.0, sigma=0.8)
        else:
            # Normal transactions: typical patterns
            features = np.random.randn(28).tolist()
            # Normalize features to be more centered
            features = [f * 0.8 for f in features]  # Slightly reduce variance
            # Normal amounts: typical distribution
            amount = np.random.lognormal(mean=3.0, sigma=1.2)
        
        # Generate time (seconds from first transaction)
        time = i * random.uniform(0, 2)
        
        transaction = {
            'Time': time,
            **{f'V{i+1}': features[i] for i in range(28)},
            'Amount': round(amount, 2),
            'Class': is_fraud
        }
        transactions.append(transaction)
    
    return pd.DataFrame(transactions)

def generate_detailed_transactions(num_transactions):
    """Generate detailed transaction records with merchant info."""
    transactions = []
    
    for i in range(num_transactions):
        transaction = {
            'transaction_id': f"TXN_{fake.uuid4()[:8].upper()}",
            'timestamp': (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
            'merchant_id': f"MER_{random.randint(1000, 9999)}",
            'merchant_name': fake.company(),
            'card_number': f"****{fake.credit_card_number()[-4:]}",
            'amount': round(random.uniform(10, 5000), 2),
            'currency': random.choice(['USD', 'EUR', 'GBP', 'CAD']),
            'category': random.choice([
                'Retail', 'Dining', 'Gas', 'Groceries', 'Entertainment',
                'Travel', 'Online', 'ATM', 'Healthcare', 'Education'
            ]),
            'country': fake.country_code(),
            'city': fake.city(),
            'risk_score': round(random.uniform(0, 100), 2),
            'is_fraud': random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 1])  # 10% fraud
        }
        transactions.append(transaction)
    
    return pd.DataFrame(transactions)

if __name__ == "__main__":
    print("Generating synthetic transaction data...")
    
    # Generate PCA-style transaction features (for model training)
    print(f"Generating {NUM_SYNTHETIC_TRANSACTIONS} PCA-style transactions...")
    df_features = generate_transaction_features(NUM_SYNTHETIC_TRANSACTIONS)
    output_path = SYNTHETIC_DIR / "transactions" / "transactions_pca.csv"
    df_features.to_csv(output_path, index=False)
    print(f"Saved to {output_path}")
    print(f"Fraud rate: {df_features['Class'].mean() * 100:.2f}%")
    
    # Generate detailed transaction records (for analysis)
    print(f"Generating {NUM_SYNTHETIC_TRANSACTIONS} detailed transactions...")
    df_detailed = generate_detailed_transactions(NUM_SYNTHETIC_TRANSACTIONS)
    output_path_detailed = SYNTHETIC_DIR / "transactions" / "transactions_detailed.csv"
    df_detailed.to_csv(output_path_detailed, index=False)
    print(f"Saved to {output_path_detailed}")
    print(f"Fraud rate: {df_detailed['is_fraud'].mean() * 100:.2f}%")
    
    print("Transaction data generation complete!")

