"""
Database schema and initialization for Watchtower.
"""

import duckdb
from pathlib import Path
from config import settings, DATA_DIR
from loguru import logger


def init_database() -> duckdb.DuckDBPyConnection:
    """Initialize DuckDB database with required schema."""
    
    db_path = DATA_DIR / "watchtower.duckdb"
    conn = duckdb.connect(str(db_path))
    
    # Create tables for risk coverage monitoring
    conn.execute("""
        CREATE TABLE IF NOT EXISTS model_performance (
            id INTEGER PRIMARY KEY,
            model_name VARCHAR(100) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            accuracy FLOAT,
            precision_score FLOAT,
            recall_score FLOAT,
            f1_score FLOAT,
            auc_score FLOAT,
            false_positive_rate FLOAT,
            false_negative_rate FLOAT
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS risk_coverage (
            id INTEGER PRIMARY KEY,
            model_name VARCHAR(100) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            risk_category VARCHAR(50) NOT NULL,
            coverage_percentage FLOAT NOT NULL,
            total_samples INTEGER NOT NULL,
            covered_samples INTEGER NOT NULL,
            threshold_used FLOAT NOT NULL
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS drift_detection (
            id INTEGER PRIMARY KEY,
            model_name VARCHAR(100) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            feature_name VARCHAR(100) NOT NULL,
            drift_score FLOAT NOT NULL,
            p_value FLOAT,
            drift_detected BOOLEAN NOT NULL,
            drift_type VARCHAR(50), -- 'concept', 'data', 'covariate'
            severity VARCHAR(20) -- 'low', 'medium', 'high'
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS playbooks (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            description TEXT,
            trigger_conditions JSON,
            actions JSON,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS playbook_executions (
            id INTEGER PRIMARY KEY,
            playbook_id INTEGER REFERENCES playbooks(id),
            triggered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status VARCHAR(20) NOT NULL, -- 'success', 'failed', 'running'
            execution_log TEXT,
            metadata JSON
        )
    """)
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS kpis (
            id INTEGER PRIMARY KEY,
            model_name VARCHAR(100) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            metric_name VARCHAR(100) NOT NULL,
            metric_value FLOAT NOT NULL,
            threshold_min FLOAT,
            threshold_max FLOAT,
            status VARCHAR(20) NOT NULL -- 'healthy', 'warning', 'critical'
        )
    """)
    
    logger.info(f"Database initialized at {db_path}")
    return conn


def get_connection() -> duckdb.DuckDBPyConnection:
    """Get database connection."""
    db_path = DATA_DIR / "watchtower.duckdb"
    return duckdb.connect(str(db_path))


if __name__ == "__main__":
    # Initialize database when run directly
    conn = init_database()
    conn.close()
