"""
Sample data generation and testing utilities for Watchtower.
"""

import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any
import requests
from config import settings

API_BASE_URL = f"http://localhost:{settings.api_port}"

def generate_sample_kpis(model_name: str = "fraud_detection_v2") -> List[Dict[str, Any]]:
    """Generate sample KPI data."""
    
    kpis = []
    base_time = datetime.now() - timedelta(hours=24)
    
    metrics = [
        {"name": "accuracy", "value": 0.95, "min": 0.9, "max": 1.0},
        {"name": "precision", "value": 0.92, "min": 0.85, "max": 1.0},
        {"name": "recall", "value": 0.88, "min": 0.8, "max": 1.0},
        {"name": "f1_score", "value": 0.90, "min": 0.85, "max": 1.0},
        {"name": "auc_score", "value": 0.94, "min": 0.9, "max": 1.0},
        {"name": "false_positive_rate", "value": 0.05, "min": 0.0, "max": 0.1},
        {"name": "false_negative_rate", "value": 0.12, "min": 0.0, "max": 0.2}
    ]
    
    for i in range(24):  # 24 hours of data
        timestamp = base_time + timedelta(hours=i)
        
        for metric in metrics:
            # Add some random variation
            variation = random.uniform(-0.02, 0.02)
            value = max(0, min(1, metric["value"] + variation))
            
            # Determine status
            if value >= metric["min"] and value <= metric["max"]:
                status = "healthy"
            elif value < metric["min"] * 0.95:
                status = "critical"
            else:
                status = "warning"
            
            kpis.append({
                "model_name": model_name,
                "metric_name": metric["name"],
                "metric_value": round(value, 4),
                "threshold_min": metric["min"],
                "threshold_max": metric["max"],
                "status": status
            })
    
    return kpis

def generate_sample_coverage(model_name: str = "fraud_detection_v2") -> List[Dict[str, Any]]:
    """Generate sample coverage data."""
    
    coverage_data = []
    base_time = datetime.now() - timedelta(hours=24)
    
    risk_categories = [
        "money_laundering",
        "terrorist_financing", 
        "sanctions_evasion",
        "fraud",
        "market_manipulation",
        "insider_trading"
    ]
    
    for i in range(6):  # 6 data points over 24 hours
        timestamp = base_time + timedelta(hours=i*4)
        
        for category in risk_categories:
            # Generate realistic coverage percentages
            base_coverage = random.uniform(0.85, 0.98)
            total_samples = random.randint(1000, 10000)
            covered_samples = int(total_samples * base_coverage)
            threshold = random.uniform(0.8, 0.95)
            
            coverage_data.append({
                "model_name": model_name,
                "risk_category": category,
                "coverage_percentage": round(base_coverage * 100, 2),
                "total_samples": total_samples,
                "covered_samples": covered_samples,
                "threshold_used": threshold
            })
    
    return coverage_data

def generate_sample_drift(model_name: str = "fraud_detection_v2") -> List[Dict[str, Any]]:
    """Generate sample drift detection data."""
    
    drift_data = []
    base_time = datetime.now() - timedelta(hours=24)
    
    features = [
        "transaction_amount",
        "transaction_frequency",
        "account_age",
        "geographic_location",
        "time_of_day",
        "merchant_category",
        "payment_method",
        "user_behavior_score"
    ]
    
    drift_types = ["concept", "data", "covariate"]
    severities = ["low", "medium", "high"]
    
    for i in range(12):  # 12 data points over 24 hours
        timestamp = base_time + timedelta(hours=i*2)
        
        for feature in features:
            # 20% chance of drift detection
            drift_detected = random.random() < 0.2
            
            if drift_detected:
                drift_score = random.uniform(0.1, 0.8)
                p_value = random.uniform(0.001, 0.05)
                drift_type = random.choice(drift_types)
                
                # Determine severity based on drift score
                if drift_score > 0.6:
                    severity = "high"
                elif drift_score > 0.3:
                    severity = "medium"
                else:
                    severity = "low"
            else:
                drift_score = random.uniform(0.0, 0.1)
                p_value = random.uniform(0.05, 1.0)
                drift_type = None
                severity = None
            
            drift_data.append({
                "model_name": model_name,
                "feature_name": feature,
                "drift_score": round(drift_score, 4),
                "p_value": round(p_value, 4),
                "drift_detected": drift_detected,
                "drift_type": drift_type,
                "severity": severity
            })
    
    return drift_data

def generate_sample_playbooks() -> List[Dict[str, Any]]:
    """Generate sample playbooks."""
    
    playbooks = [
        {
            "name": "High Drift Alert",
            "description": "Automated response to high-severity drift detection",
            "trigger_conditions": {
                "drift_score": "> 0.6",
                "severity": "high"
            },
            "actions": {
                "notify": ["ml_team@company.com"],
                "retrain_model": True,
                "pause_predictions": False,
                "escalate": True
            },
            "is_active": True
        },
        {
            "name": "Low Coverage Alert",
            "description": "Alert when risk coverage falls below threshold",
            "trigger_conditions": {
                "coverage_percentage": "< 90",
                "risk_category": "money_laundering"
            },
            "actions": {
                "notify": ["risk_team@company.com"],
                "increase_sampling": True,
                "review_model": True
            },
            "is_active": True
        },
        {
            "name": "Critical KPI Alert",
            "description": "Response to critical KPI degradation",
            "trigger_conditions": {
                "status": "critical",
                "metric_name": "accuracy"
            },
            "actions": {
                "notify": ["ml_team@company.com", "management@company.com"],
                "pause_predictions": True,
                "emergency_retrain": True,
                "escalate": True
            },
            "is_active": True
        }
    ]
    
    return playbooks

def populate_sample_data():
    """Populate database with sample data."""
    
    print("Generating sample data...")
    
    # Generate sample data
    kpis = generate_sample_kpis()
    coverage = generate_sample_coverage()
    drift = generate_sample_drift()
    playbooks = generate_sample_playbooks()
    
    print(f"Generated {len(kpis)} KPI records")
    print(f"Generated {len(coverage)} coverage records")
    print(f"Generated {len(drift)} drift records")
    print(f"Generated {len(playbooks)} playbooks")
    
    # Send data to API
    try:
        # Send KPIs
        for kpi in kpis:
            response = requests.post(f"{API_BASE_URL}/kpis", json=kpi)
            if response.status_code != 200:
                print(f"Error sending KPI: {response.text}")
        
        # Send coverage data
        for cov in coverage:
            response = requests.post(f"{API_BASE_URL}/coverage", json=cov)
            if response.status_code != 200:
                print(f"Error sending coverage: {response.text}")
        
        # Send drift data
        for d in drift:
            response = requests.post(f"{API_BASE_URL}/drift", json=d)
            if response.status_code != 200:
                print(f"Error sending drift: {response.text}")
        
        # Send playbooks
        for playbook in playbooks:
            response = requests.post(f"{API_BASE_URL}/playbooks", json=playbook)
            if response.status_code != 200:
                print(f"Error sending playbook: {response.text}")
        
        print("Sample data populated successfully!")
        
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to API: {e}")
        print("Make sure the API server is running on port 8000")

if __name__ == "__main__":
    populate_sample_data()
