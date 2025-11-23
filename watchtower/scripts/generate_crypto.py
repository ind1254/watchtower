"""Generate synthetic cryptocurrency transaction data."""

import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import random
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import SYNTHETIC_DIR, NUM_SYNTHETIC_CRYPTO

fake = Faker()

def generate_crypto_transactions(num_transactions):
    """Generate synthetic cryptocurrency transactions."""
    crypto_types = ['BTC', 'ETH', 'USDT', 'USDC', 'BNB', 'SOL', 'ADA', 'XRP']
    transaction_types = ['Transfer', 'Exchange', 'Purchase', 'Sale', 'Staking', 'Withdrawal']
    statuses = ['Completed', 'Pending', 'Failed']
    
    transactions = []
    
    for i in range(num_transactions):
        crypto_type = random.choice(crypto_types)
        amount = random.uniform(0.001, 100)
        
        # BTC has higher value
        if crypto_type == 'BTC':
            usd_value = amount * random.uniform(40000, 60000)
        elif crypto_type == 'ETH':
            usd_value = amount * random.uniform(2000, 4000)
        else:
            usd_value = amount * random.uniform(0.5, 2)
        
        transaction = {
            'transaction_id': f"CRYPTO_{fake.sha256()[:16].upper()}",
            'timestamp': (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
            'crypto_type': crypto_type,
            'amount': round(amount, 8),
            'usd_value': round(usd_value, 2),
            'from_address': fake.sha256()[:42],
            'to_address': fake.sha256()[:42],
            'transaction_type': random.choice(transaction_types),
            'network': random.choice(['Mainnet', 'Ethereum', 'BSC', 'Polygon', 'Arbitrum']),
            'fee': round(random.uniform(0.0001, 0.01), 8),
            'block_number': random.randint(1000000, 20000000),
            'confirmations': random.randint(1, 100),
            'status': random.choice(statuses),
            'risk_score': round(random.uniform(0, 100), 2),
            'is_suspicious': random.choice([0, 0, 0, 0, 0, 0, 0, 1])  # 12.5% suspicious
        }
        transactions.append(transaction)
    
    return pd.DataFrame(transactions)

if __name__ == "__main__":
    print("Generating synthetic cryptocurrency transaction data...")
    print(f"Generating {NUM_SYNTHETIC_CRYPTO} crypto transactions...")
    
    df = generate_crypto_transactions(NUM_SYNTHETIC_CRYPTO)
    output_path = SYNTHETIC_DIR / "crypto" / "crypto_transactions.csv"
    df.to_csv(output_path, index=False)
    
    print(f"Saved to {output_path}")
    print(f"Suspicious rate: {df['is_suspicious'].mean() * 100:.2f}%")
    print(f"Total volume (USD): ${df['usd_value'].sum():,.2f}")
    print("Crypto data generation complete!")

