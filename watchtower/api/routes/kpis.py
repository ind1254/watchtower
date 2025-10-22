"""
KPI routes for Watchtower API.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from loguru import logger
import duckdb

from ...config import settings, get_database_path
from ...monitoring.alert_kpis import KPIMonitor

router = APIRouter()

@router.get("/")
async def get_kpis(
    hours_back: int = Query(24, description="Hours of data to retrieve"),
    metric_name: Optional[str] = Query(None, description="Specific metric to retrieve")
) -> List[Dict[str, Any]]:
    """Get KPI metrics."""
    
    # TODO: Implement comprehensive KPI retrieval
    # - Filter by time range
    # - Filter by metric type
    # - Include trend data
    # - Performance optimization
    
    try:
        conn = duckdb.connect(str(get_database_path()))
        
        query = """
            SELECT 
                id,
                metric_name,
                metric_value,
                threshold_min,
                threshold_max,
                status,
                timestamp
            FROM kpis
            WHERE timestamp >= ?
        """
        params = [datetime.now() - timedelta(hours=hours_back)]
        
        if metric_name:
            query += " AND metric_name = ?"
            params.append(metric_name)
        
        query += " ORDER BY timestamp DESC"
        
        result = conn.execute(query, params).fetchall()
        conn.close()
        
        columns = ['id', 'metric_name', 'metric_value', 'threshold_min', 'threshold_max', 'status', 'timestamp']
        kpis = [dict(zip(columns, row)) for row in result]
        
        logger.info(f"Retrieved {len(kpis)} KPI records")
        return kpis
        
    except Exception as e:
        logger.error(f"Failed to retrieve KPIs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_kpi(kpi_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new KPI metric entry."""
    
    # TODO: Implement KPI creation
    # - Validate input data
    # - Calculate derived metrics
    # - Store in database
    # - Trigger alerts if needed
    
    try:
        conn = duckdb.connect(str(get_database_path()))
        
        # Validate required fields
        required_fields = ['metric_name', 'metric_value']
        for field in required_fields:
            if field not in kpi_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Insert KPI
        conn.execute("""
            INSERT INTO kpis (metric_name, metric_value, threshold_min, threshold_max, status, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """, [
            kpi_data['metric_name'],
            kpi_data['metric_value'],
            kpi_data.get('threshold_min'),
            kpi_data.get('threshold_max'),
            kpi_data.get('status', 'healthy'),
            datetime.now()
        ])
        
        conn.close()
        
        logger.info(f"Created KPI: {kpi_data['metric_name']}")
        return {"message": "KPI created successfully", "kpi": kpi_data}
        
    except Exception as e:
        logger.error(f"Failed to create KPI: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/calculate")
async def calculate_kpis(
    hours_back: int = Query(24, description="Hours of data to analyze")
) -> Dict[str, Any]:
    """Calculate current KPI metrics."""
    
    # TODO: Implement KPI calculation
    # - Calculate all metrics
    # - Check thresholds
    # - Generate alerts
    # - Store results
    
    try:
        monitor = KPIMonitor()
        
        # Calculate KPIs
        kpis = monitor.calculate_kpis(hours_back)
        
        if not kpis:
            raise HTTPException(status_code=404, detail="No data available for KPI calculation")
        
        # Check thresholds and generate alerts
        alerts = monitor.check_kpi_thresholds(kpis)
        
        # Store metrics
        monitor.store_kpi_metrics(kpis)
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "kpis": kpis,
            "alerts": alerts,
            "calculation_window_hours": hours_back
        }
        
        logger.info(f"Calculated {len(kpis)} KPIs, {len(alerts)} alerts generated")
        return result
        
    except Exception as e:
        logger.error(f"Failed to calculate KPIs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/trends/{metric_name}")
async def get_kpi_trends(
    metric_name: str,
    days_back: int = Query(7, description="Days of trend data to retrieve")
) -> Dict[str, Any]:
    """Get KPI trends over time."""
    
    # TODO: Implement trend analysis
    # - Calculate daily trends
    # - Identify patterns
    # - Generate trend reports
    # - Performance optimization
    
    try:
        monitor = KPIMonitor()
        trends_df = monitor.get_kpi_trends(metric_name, days_back)
        
        if trends_df.empty:
            raise HTTPException(status_code=404, detail=f"No trend data found for {metric_name}")
        
        # Convert DataFrame to dict
        trends_data = trends_df.to_dict('records')
        
        result = {
            "metric_name": metric_name,
            "trends": trends_data,
            "days_back": days_back,
            "timestamp": datetime.now().isoformat()
        }
        
        logger.info(f"Retrieved trends for {metric_name}: {len(trends_data)} data points")
        return result
        
    except Exception as e:
        logger.error(f"Failed to get trends for {metric_name}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
async def get_kpi_summary(
    hours_back: int = Query(24, description="Hours of data to summarize")
) -> Dict[str, Any]:
    """Get KPI summary statistics."""
    
    # TODO: Implement KPI summary
    # - Calculate summary statistics
    # - Identify outliers
    # - Generate insights
    # - Performance metrics
    
    try:
        conn = duckdb.connect(str(get_database_path()))
        
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        # Get summary statistics
        query = """
            SELECT 
                metric_name,
                COUNT(*) as measurements,
                AVG(metric_value) as avg_value,
                MIN(metric_value) as min_value,
                MAX(metric_value) as max_value,
                STDDEV(metric_value) as std_value,
                SUM(CASE WHEN status = 'critical' THEN 1 ELSE 0 END) as critical_count,
                SUM(CASE WHEN status = 'warning' THEN 1 ELSE 0 END) as warning_count,
                SUM(CASE WHEN status = 'healthy' THEN 1 ELSE 0 END) as healthy_count
            FROM kpis
            WHERE timestamp >= ?
            GROUP BY metric_name
            ORDER BY metric_name
        """
        
        result = conn.execute(query, [cutoff_time]).fetchall()
        conn.close()
        
        columns = [
            'metric_name', 'measurements', 'avg_value', 'min_value', 
            'max_value', 'std_value', 'critical_count', 'warning_count', 'healthy_count'
        ]
        
        summary_data = [dict(zip(columns, row)) for row in result]
        
        # Calculate overall health
        total_critical = sum(row['critical_count'] for row in summary_data)
        total_warning = sum(row['warning_count'] for row in summary_data)
        total_healthy = sum(row['healthy_count'] for row in summary_data)
        
        overall_health = "healthy"
        if total_critical > 0:
            overall_health = "critical"
        elif total_warning > 0:
            overall_health = "warning"
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "summary_window_hours": hours_back,
            "overall_health": overall_health,
            "total_measurements": sum(row['measurements'] for row in summary_data),
            "critical_alerts": total_critical,
            "warning_alerts": total_warning,
            "healthy_metrics": total_healthy,
            "metrics": summary_data
        }
        
        logger.info(f"Generated KPI summary: {overall_health} health status")
        return result
        
    except Exception as e:
        logger.error(f"Failed to generate KPI summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
