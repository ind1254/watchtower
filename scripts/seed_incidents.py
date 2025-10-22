"""
Seed incident data for testing alerting and playbook execution.
"""

import duckdb
import pandas as pd
from datetime import datetime, timedelta
import random
from pathlib import Path

def seed_incidents(conn: duckdb.DuckDBPyConnection):
    """Seed incident data for testing."""
    
    # TODO: Implement realistic incident seeding
    # - Various incident types
    # - Different severity levels
    # - Realistic timestamps
    # - Associated transactions
    
    incidents = []
    
    # Generate different types of incidents
    incident_types = [
        'high_drift_detected',
        'low_coverage_alert',
        'model_performance_degradation',
        'suspicious_pattern_detected',
        'threshold_breach'
    ]
    
    severities = ['low', 'medium', 'high', 'critical']
    
    for i in range(50):  # Generate 50 incidents
        incident = {
            'incident_id': f"INC_{i:04d}",
            'incident_type': random.choice(incident_types),
            'severity': random.choice(severities),
            'description': f"Test incident {i}",
            'timestamp': datetime.now() - timedelta(
                hours=random.randint(1, 168)  # Last week
            ),
            'status': random.choice(['open', 'investigating', 'resolved']),
            'assigned_to': f"analyst_{random.randint(1, 5)}",
            'resolution_time': random.randint(1, 24) if random.random() > 0.3 else None
        }
        incidents.append(incident)
    
    # Create incidents table if it doesn't exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            incident_id VARCHAR PRIMARY KEY,
            incident_type VARCHAR,
            severity VARCHAR,
            description TEXT,
            timestamp TIMESTAMP,
            status VARCHAR,
            assigned_to VARCHAR,
            resolution_time INTEGER
        )
    """)
    
    # Insert incidents
    df = pd.DataFrame(incidents)
    conn.execute("INSERT OR REPLACE INTO incidents SELECT * FROM df")
    
    print(f"Seeded {len(incidents)} incidents")

def seed_playbook_executions(conn: duckdb.DuckDBPyConnection):
    """Seed playbook execution data."""
    
    # TODO: Implement playbook execution seeding
    # - Different playbook types
    # - Success/failure rates
    # - Execution times
    # - Associated incidents
    
    executions = []
    
    playbook_types = [
        'enable_fallback_rule',
        'raise_threshold',
        'trigger_retrain',
        'notify_team',
        'pause_model'
    ]
    
    for i in range(30):  # Generate 30 executions
        execution = {
            'execution_id': f"EXEC_{i:04d}",
            'playbook_type': random.choice(playbook_types),
            'triggered_by': f"INC_{random.randint(1, 50):04d}",
            'status': random.choice(['success', 'failed', 'running']),
            'start_time': datetime.now() - timedelta(
                hours=random.randint(1, 72)
            ),
            'end_time': datetime.now() - timedelta(
                hours=random.randint(0, 24)
            ) if random.random() > 0.2 else None,
            'execution_log': f"Execution log for {i}",
            'metadata': '{"test": true}'
        }
        executions.append(execution)
    
    # Create executions table if it doesn't exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS playbook_executions (
            execution_id VARCHAR PRIMARY KEY,
            playbook_type VARCHAR,
            triggered_by VARCHAR,
            status VARCHAR,
            start_time TIMESTAMP,
            end_time TIMESTAMP,
            execution_log TEXT,
            metadata VARCHAR
        )
    """)
    
    # Insert executions
    df = pd.DataFrame(executions)
    conn.execute("INSERT OR REPLACE INTO playbook_executions SELECT * FROM df")
    
    print(f"Seeded {len(executions)} playbook executions")

def seed_alert_history(conn: duckdb.DuckDBPyConnection):
    """Seed alert history data."""
    
    # TODO: Implement alert history seeding
    # - Different alert types
    # - Alert frequencies
    # - Resolution patterns
    # - False positive rates
    
    alerts = []
    
    alert_types = [
        'drift_alert',
        'coverage_alert',
        'performance_alert',
        'threshold_alert',
        'anomaly_alert'
    ]
    
    for i in range(100):  # Generate 100 alerts
        alert = {
            'alert_id': f"ALERT_{i:04d}",
            'alert_type': random.choice(alert_types),
            'severity': random.choice(['low', 'medium', 'high']),
            'message': f"Alert message {i}",
            'timestamp': datetime.now() - timedelta(
                hours=random.randint(1, 168)
            ),
            'acknowledged': random.choice([True, False]),
            'resolved': random.choice([True, False]) if random.random() > 0.3 else False,
            'false_positive': random.choice([True, False]) if random.random() > 0.8 else False
        }
        alerts.append(alert)
    
    # Create alerts table if it doesn't exist
    conn.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            alert_id VARCHAR PRIMARY KEY,
            alert_type VARCHAR,
            severity VARCHAR,
            message TEXT,
            timestamp TIMESTAMP,
            acknowledged BOOLEAN,
            resolved BOOLEAN,
            false_positive BOOLEAN
        )
    """)
    
    # Insert alerts
    df = pd.DataFrame(alerts)
    conn.execute("INSERT OR REPLACE INTO alerts SELECT * FROM df")
    
    print(f"Seeded {len(alerts)} alerts")

def main():
    """Seed all incident and alert data."""
    
    print("Seeding incident data...")
    
    # Connect to database
    db_path = Path("data/watchtower.duckdb")
    if not db_path.exists():
        print("❌ Database not found. Run 'make data' first.")
        return
    
    conn = duckdb.connect(str(db_path))
    
    try:
        # Seed different types of data
        seed_incidents(conn)
        seed_playbook_executions(conn)
        seed_alert_history(conn)
        
        print("✅ Incident seeding complete!")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()
