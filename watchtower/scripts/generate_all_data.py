"""Generate all synthetic data types."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from scripts.generate_transactions import generate_transaction_features, generate_detailed_transactions
from scripts.generate_crypto import generate_crypto_transactions
from scripts.generate_kyc import generate_kyc_records
from scripts.generate_merchants import generate_merchant_records
from config import SYNTHETIC_DIR, NUM_SYNTHETIC_TRANSACTIONS, NUM_SYNTHETIC_CRYPTO, NUM_SYNTHETIC_KYC, NUM_SYNTHETIC_MERCHANTS
import pandas as pd

def main():
    """Generate all types of synthetic data."""
    print("=" * 60)
    print("Generating all synthetic data for Watchtower AML Platform")
    print("=" * 60)
    
    # Generate transactions
    print("\n[1/4] Generating transaction data...")
    df_features = generate_transaction_features(NUM_SYNTHETIC_TRANSACTIONS)
    output_path = SYNTHETIC_DIR / "transactions" / "transactions_pca.csv"
    df_features.to_csv(output_path, index=False)
    print(f"Saved {len(df_features)} PCA-style transactions")
    
    df_detailed = generate_detailed_transactions(NUM_SYNTHETIC_TRANSACTIONS)
    output_path_detailed = SYNTHETIC_DIR / "transactions" / "transactions_detailed.csv"
    df_detailed.to_csv(output_path_detailed, index=False)
    print(f"Saved {len(df_detailed)} detailed transactions")
    
    # Generate crypto
    print("\n[2/4] Generating cryptocurrency data...")
    df_crypto = generate_crypto_transactions(NUM_SYNTHETIC_CRYPTO)
    output_path = SYNTHETIC_DIR / "crypto" / "crypto_transactions.csv"
    df_crypto.to_csv(output_path, index=False)
    print(f"Saved {len(df_crypto)} crypto transactions")
    
    # Generate KYC
    print("\n[3/4] Generating KYC data...")
    df_kyc = generate_kyc_records(NUM_SYNTHETIC_KYC)
    output_path = SYNTHETIC_DIR / "kyc" / "kyc_records.csv"
    df_kyc.to_csv(output_path, index=False)
    print(f"Saved {len(df_kyc)} KYC records")
    
    # Generate merchants
    print("\n[4/4] Generating merchant data...")
    df_merchants = generate_merchant_records(NUM_SYNTHETIC_MERCHANTS)
    output_path = SYNTHETIC_DIR / "merchants" / "merchants.csv"
    df_merchants.to_csv(output_path, index=False)
    print(f"Saved {len(df_merchants)} merchant records")
    
    print("\n" + "=" * 60)
    print("All synthetic data generation complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

