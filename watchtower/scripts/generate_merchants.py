"""Generate synthetic merchant monitoring data."""

import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import random
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import SYNTHETIC_DIR, NUM_SYNTHETIC_MERCHANTS

fake = Faker()

def generate_merchant_records(num_merchants):
    """Generate synthetic merchant monitoring records."""
    merchant_types = [
        'Retail', 'Restaurant', 'Gas Station', 'Grocery Store',
        'Online Marketplace', 'Entertainment', 'Travel', 'Healthcare',
        'Education', 'Financial Services', 'Cryptocurrency Exchange',
        'Gambling', 'Adult Services', 'Charity'
    ]
    
    statuses = ['Active', 'Suspended', 'Under Review', 'Terminated']
    risk_levels = ['Low', 'Medium', 'High', 'Critical']
    
    merchants = []
    
    for i in range(num_merchants):
        merchant_type = random.choice(merchant_types)
        
        # Some merchant types are inherently riskier
        if merchant_type in ['Cryptocurrency Exchange', 'Gambling', 'Adult Services']:
            base_risk = random.uniform(40, 90)
        else:
            base_risk = random.uniform(0, 60)
        
        registration_date = datetime.now() - timedelta(days=random.randint(30, 1825))
        
        merchant = {
            'merchant_id': f"MER_{random.randint(10000, 99999)}",
            'merchant_name': fake.company(),
            'legal_name': fake.company(),
            'merchant_type': merchant_type,
            'category': merchant_type,
            'registration_date': registration_date.isoformat(),
            'status': random.choice(statuses),
            'tax_id': fake.bothify(text='##-#######'),
            'business_registration_number': fake.bothify(text='BRN######').upper(),
            'address': fake.address().replace('\n', ', '),
            'city': fake.city(),
            'country': fake.country(),
            'country_code': fake.country_code(),
            'postal_code': fake.postcode(),
            'phone': fake.phone_number(),
            'email': fake.company_email(),
            'website': fake.url(),
            'average_transaction_value': round(random.uniform(10, 1000), 2),
            'monthly_transaction_volume': round(random.uniform(1000, 1000000), 2),
            'total_transactions': random.randint(100, 100000),
            'chargeback_rate': round(random.uniform(0, 5), 2),
            'refund_rate': round(random.uniform(0, 10), 2),
            'risk_level': random.choice(risk_levels),
            'risk_score': round(base_risk, 2),
            'compliance_score': round(random.uniform(0, 100), 2),
            'is_high_risk': 1 if base_risk > 70 else 0,
            'is_monitored': random.choice([0, 0, 0, 1]),  # 25% monitored
            'last_review_date': (datetime.now() - timedelta(days=random.randint(0, 180))).isoformat(),
            'notes': fake.text(max_nb_chars=200) if random.random() < 0.3 else ""
        }
        merchants.append(merchant)
    
    return pd.DataFrame(merchants)

if __name__ == "__main__":
    print("Generating synthetic merchant monitoring data...")
    print(f"Generating {NUM_SYNTHETIC_MERCHANTS} merchant records...")
    
    df = generate_merchant_records(NUM_SYNTHETIC_MERCHANTS)
    output_path = SYNTHETIC_DIR / "merchants" / "merchants.csv"
    df.to_csv(output_path, index=False)
    
    print(f"Saved to {output_path}")
    print(f"Status distribution:")
    print(df['status'].value_counts())
    print(f"High risk rate: {df['is_high_risk'].mean() * 100:.2f}%")
    print(f"Average risk score: {df['risk_score'].mean():.2f}")
    print("Merchant data generation complete!")

