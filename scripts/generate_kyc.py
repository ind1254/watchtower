"""Generate synthetic KYC (Know Your Customer) verification data."""

import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
import random
from pathlib import Path
import sys

sys.path.append(str(Path(__file__).parent.parent))
from config import SYNTHETIC_DIR, NUM_SYNTHETIC_KYC

fake = Faker()

def generate_kyc_records(num_records):
    """Generate synthetic KYC verification records."""
    verification_statuses = ['Verified', 'Pending', 'Rejected', 'Under Review']
    document_types = ['Passport', 'Driver License', 'National ID', 'Government ID']
    risk_levels = ['Low', 'Medium', 'High']
    
    records = []
    
    for i in range(num_records):
        dob = fake.date_of_birth(minimum_age=18, maximum_age=80)
        age = (datetime.now().date() - dob).days // 365
        
        record = {
            'kyc_id': f"KYC_{fake.uuid4()[:8].upper()}",
            'customer_id': f"CUST_{random.randint(100000, 999999)}",
            'first_name': fake.first_name(),
            'last_name': fake.last_name(),
            'email': fake.email(),
            'phone': fake.phone_number(),
            'date_of_birth': dob.isoformat(),
            'age': age,
            'nationality': fake.country(),
            'country_code': fake.country_code(),
            'address': fake.address().replace('\n', ', '),
            'city': fake.city(),
            'postal_code': fake.postcode(),
            'document_type': random.choice(document_types),
            'document_number': fake.bothify(text='??######').upper(),
            'document_issue_date': (dob + timedelta(days=random.randint(0, 18250))).isoformat(),
            'document_expiry_date': (datetime.now().date() + timedelta(days=random.randint(30, 3650))).isoformat(),
            'verification_status': random.choice(verification_statuses),
            'verification_date': (datetime.now() - timedelta(days=random.randint(0, 365))).isoformat(),
            'risk_level': random.choice(risk_levels),
            'risk_score': round(random.uniform(0, 100), 2),
            'is_pep': random.choice([0, 0, 0, 0, 0, 1]),  # 16.7% PEP
            'is_sanctioned': random.choice([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]),  # 9% sanctioned
            'compliance_notes': fake.text(max_nb_chars=200) if random.random() < 0.3 else ""
        }
        records.append(record)
    
    return pd.DataFrame(records)

if __name__ == "__main__":
    print("Generating synthetic KYC verification data...")
    print(f"Generating {NUM_SYNTHETIC_KYC} KYC records...")
    
    df = generate_kyc_records(NUM_SYNTHETIC_KYC)
    output_path = SYNTHETIC_DIR / "kyc" / "kyc_records.csv"
    df.to_csv(output_path, index=False)
    
    print(f"Saved to {output_path}")
    print(f"Verification status distribution:")
    print(df['verification_status'].value_counts())
    print(f"PEP rate: {df['is_pep'].mean() * 100:.2f}%")
    print(f"Sanctioned rate: {df['is_sanctioned'].mean() * 100:.2f}%")
    print("KYC data generation complete!")

