"""
FastAPI backend for Watchtower monitoring system.
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import pandas as pd
from pydantic import BaseModel

from config import settings
from database import get_connection, init_database
from loguru import logger

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="Risk Coverage & Drift Monitor for Financial-Crime Models"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class KPIMetric(BaseModel):
    model_name: str
    metric_name: str
    metric_value: float
    threshold_min: Optional[float] = None
    threshold_max: Optional[float] = None
    status: str

class CoverageData(BaseModel):
    model_name: str
    risk_category: str
    coverage_percentage: float
    total_samples: int
    covered_samples: int
    threshold_used: float

class DriftData(BaseModel):
    model_name: str
    feature_name: str
    drift_score: float
    p_value: Optional[float] = None
    drift_detected: bool
    drift_type: Optional[str] = None
    severity: Optional[str] = None

class Playbook(BaseModel):
    name: str
    description: Optional[str] = None
    trigger_conditions: Dict[str, Any]
    actions: Dict[str, Any]
    is_active: bool = True

class PlaybookExecution(BaseModel):
    playbook_id: int
    status: str
    execution_log: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_database()
    logger.info("Watchtower API started")


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Watchtower API",
        "version": settings.api_version,
        "endpoints": ["/kpis", "/coverage", "/drift", "/playbooks"]
    }


@app.get("/kpis")
async def get_kpis(
    model_name: Optional[str] = None,
    hours_back: int = 24,
    conn: duckdb.DuckDBPyConnection = Depends(get_connection)
) -> List[Dict[str, Any]]:
    """Get KPI metrics for models."""
    
    query = """
        SELECT * FROM kpis 
        WHERE timestamp >= ?
    """
    params = [datetime.now() - timedelta(hours=hours_back)]
    
    if model_name:
        query += " AND model_name = ?"
        params.append(model_name)
    
    query += " ORDER BY timestamp DESC"
    
    result = conn.execute(query, params).fetchall()
    columns = [desc[0] for desc in conn.description]
    
    return [dict(zip(columns, row)) for row in result]


@app.post("/kpis")
async def create_kpi(
    kpi: KPIMetric,
    conn: duckdb.DuckDBPyConnection = Depends(get_connection)
) -> Dict[str, Any]:
    """Create a new KPI metric entry."""
    
    query = """
        INSERT INTO kpis (model_name, metric_name, metric_value, threshold_min, threshold_max, status)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    
    conn.execute(query, [
        kpi.model_name,
        kpi.metric_name,
        kpi.metric_value,
        kpi.threshold_min,
        kpi.threshold_max,
        kpi.status
    ])
    
    return {"message": "KPI created successfully", "kpi": kpi.dict()}


@app.get("/coverage")
async def get_coverage(
    model_name: Optional[str] = None,
    risk_category: Optional[str] = None,
    hours_back: int = 24,
    conn: duckdb.DuckDBPyConnection = Depends(get_connection)
) -> List[Dict[str, Any]]:
    """Get risk coverage data."""
    
    query = """
        SELECT * FROM risk_coverage 
        WHERE timestamp >= ?
    """
    params = [datetime.now() - timedelta(hours=hours_back)]
    
    if model_name:
        query += " AND model_name = ?"
        params.append(model_name)
    
    if risk_category:
        query += " AND risk_category = ?"
        params.append(risk_category)
    
    query += " ORDER BY timestamp DESC"
    
    result = conn.execute(query, params).fetchall()
    columns = [desc[0] for desc in conn.description]
    
    return [dict(zip(columns, row)) for row in result]


@app.post("/coverage")
async def create_coverage_data(
    coverage: CoverageData,
    conn: duckdb.DuckDBPyConnection = Depends(get_connection)
) -> Dict[str, Any]:
    """Create new coverage data entry."""
    
    query = """
        INSERT INTO risk_coverage (model_name, risk_category, coverage_percentage, total_samples, covered_samples, threshold_used)
        VALUES (?, ?, ?, ?, ?, ?)
    """
    
    conn.execute(query, [
        coverage.model_name,
        coverage.risk_category,
        coverage.coverage_percentage,
        coverage.total_samples,
        coverage.covered_samples,
        coverage.threshold_used
    ])
    
    return {"message": "Coverage data created successfully", "coverage": coverage.dict()}


@app.get("/drift")
async def get_drift(
    model_name: Optional[str] = None,
    feature_name: Optional[str] = None,
    hours_back: int = 24,
    conn: duckdb.DuckDBPyConnection = Depends(get_connection)
) -> List[Dict[str, Any]]:
    """Get drift detection data."""
    
    query = """
        SELECT * FROM drift_detection 
        WHERE timestamp >= ?
    """
    params = [datetime.now() - timedelta(hours=hours_back)]
    
    if model_name:
        query += " AND model_name = ?"
        params.append(model_name)
    
    if feature_name:
        query += " AND feature_name = ?"
        params.append(feature_name)
    
    query += " ORDER BY timestamp DESC"
    
    result = conn.execute(query, params).fetchall()
    columns = [desc[0] for desc in conn.description]
    
    return [dict(zip(columns, row)) for row in result]


@app.post("/drift")
async def create_drift_data(
    drift: DriftData,
    conn: duckdb.DuckDBPyConnection = Depends(get_connection)
) -> Dict[str, Any]:
    """Create new drift detection data entry."""
    
    query = """
        INSERT INTO drift_detection (model_name, feature_name, drift_score, p_value, drift_detected, drift_type, severity)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """
    
    conn.execute(query, [
        drift.model_name,
        drift.feature_name,
        drift.drift_score,
        drift.p_value,
        drift.drift_detected,
        drift.drift_type,
        drift.severity
    ])
    
    return {"message": "Drift data created successfully", "drift": drift.dict()}


@app.get("/playbooks")
async def get_playbooks(
    active_only: bool = True,
    conn: duckdb.DuckDBPyConnection = Depends(get_connection)
) -> List[Dict[str, Any]]:
    """Get playbooks."""
    
    query = "SELECT * FROM playbooks"
    params = []
    
    if active_only:
        query += " WHERE is_active = ?"
        params.append(True)
    
    query += " ORDER BY created_at DESC"
    
    result = conn.execute(query, params).fetchall()
    columns = [desc[0] for desc in conn.description]
    
    return [dict(zip(columns, row)) for row in result]


@app.post("/playbooks")
async def create_playbook(
    playbook: Playbook,
    conn: duckdb.DuckDBPyConnection = Depends(get_connection)
) -> Dict[str, Any]:
    """Create a new playbook."""
    
    query = """
        INSERT INTO playbooks (name, description, trigger_conditions, actions, is_active)
        VALUES (?, ?, ?, ?, ?)
    """
    
    conn.execute(query, [
        playbook.name,
        playbook.description,
        str(playbook.trigger_conditions),
        str(playbook.actions),
        playbook.is_active
    ])
    
    return {"message": "Playbook created successfully", "playbook": playbook.dict()}


@app.get("/playbooks/{playbook_id}/executions")
async def get_playbook_executions(
    playbook_id: int,
    hours_back: int = 24,
    conn: duckdb.DuckDBPyConnection = Depends(get_connection)
) -> List[Dict[str, Any]]:
    """Get executions for a specific playbook."""
    
    query = """
        SELECT * FROM playbook_executions 
        WHERE playbook_id = ? AND triggered_at >= ?
        ORDER BY triggered_at DESC
    """
    
    result = conn.execute(query, [playbook_id, datetime.now() - timedelta(hours=hours_back)]).fetchall()
    columns = [desc[0] for desc in conn.description]
    
    return [dict(zip(columns, row)) for row in result]


@app.post("/playbooks/{playbook_id}/execute")
async def execute_playbook(
    playbook_id: int,
    execution: PlaybookExecution,
    conn: duckdb.DuckDBPyConnection = Depends(get_connection)
) -> Dict[str, Any]:
    """Execute a playbook."""
    
    query = """
        INSERT INTO playbook_executions (playbook_id, status, execution_log, metadata)
        VALUES (?, ?, ?, ?)
    """
    
    conn.execute(query, [
        playbook_id,
        execution.status,
        execution.execution_log,
        str(execution.metadata) if execution.metadata else None
    ])
    
    return {"message": "Playbook execution recorded", "execution": execution.dict()}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
