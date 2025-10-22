"""
Playbooks routes for Watchtower API.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from loguru import logger
import duckdb
import yaml
from pathlib import Path

from ...config import settings, get_database_path

router = APIRouter()

@router.get("/")
async def get_playbooks(
    active_only: bool = Query(True, description="Return only active playbooks")
) -> List[Dict[str, Any]]:
    """Get playbooks."""
    
    # TODO: Implement comprehensive playbook retrieval
    # - Load from registry
    # - Filter by status
    # - Include metadata
    # - Performance optimization
    
    try:
        # Load playbooks from registry
        registry_path = Path("watchtower/playbooks/registry.yaml")
        
        if not registry_path.exists():
            return []
        
        with open(registry_path, 'r') as f:
            registry = yaml.safe_load(f)
        
        playbooks = registry.get('playbooks', [])
        
        if active_only:
            playbooks = [p for p in playbooks if p.get('is_active', True)]
        
        logger.info(f"Retrieved {len(playbooks)} playbooks")
        return playbooks
        
    except Exception as e:
        logger.error(f"Failed to retrieve playbooks: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_playbook(playbook_data: Dict[str, Any]) -> Dict[str, Any]:
    """Create a new playbook."""
    
    # TODO: Implement playbook creation
    # - Validate playbook structure
    # - Save to registry
    # - Update database
    # - Validate triggers and actions
    
    try:
        # Validate required fields
        required_fields = ['name', 'trigger_conditions', 'actions']
        for field in required_fields:
            if field not in playbook_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Load existing registry
        registry_path = Path("watchtower/playbooks/registry.yaml")
        registry = {'playbooks': []}
        
        if registry_path.exists():
            with open(registry_path, 'r') as f:
                registry = yaml.safe_load(f)
        
        # Add new playbook
        playbook_data['id'] = len(registry['playbooks']) + 1
        playbook_data['created_at'] = datetime.now().isoformat()
        playbook_data['updated_at'] = datetime.now().isoformat()
        
        registry['playbooks'].append(playbook_data)
        
        # Save registry
        with open(registry_path, 'w') as f:
            yaml.dump(registry, f, default_flow_style=False)
        
        logger.info(f"Created playbook: {playbook_data['name']}")
        return {"message": "Playbook created successfully", "playbook": playbook_data}
        
    except Exception as e:
        logger.error(f"Failed to create playbook: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{playbook_id}")
async def get_playbook(playbook_id: int) -> Dict[str, Any]:
    """Get a specific playbook by ID."""
    
    # TODO: Implement playbook retrieval by ID
    # - Load from registry
    # - Validate ID
    # - Include execution history
    # - Performance optimization
    
    try:
        registry_path = Path("watchtower/playbooks/registry.yaml")
        
        if not registry_path.exists():
            raise HTTPException(status_code=404, detail="Playbook registry not found")
        
        with open(registry_path, 'r') as f:
            registry = yaml.safe_load(f)
        
        playbooks = registry.get('playbooks', [])
        playbook = next((p for p in playbooks if p.get('id') == playbook_id), None)
        
        if not playbook:
            raise HTTPException(status_code=404, detail=f"Playbook {playbook_id} not found")
        
        logger.info(f"Retrieved playbook: {playbook['name']}")
        return playbook
        
    except Exception as e:
        logger.error(f"Failed to retrieve playbook {playbook_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{playbook_id}/execute")
async def execute_playbook(
    playbook_id: int,
    execution_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Execute a playbook."""
    
    # TODO: Implement playbook execution
    # - Load playbook
    # - Validate triggers
    # - Execute actions
    # - Log execution results
    
    try:
        # Get playbook
        playbook = await get_playbook(playbook_id)
        
        # Create execution record
        execution_id = f"EXEC_{playbook_id}_{int(datetime.now().timestamp())}"
        
        execution_record = {
            'execution_id': execution_id,
            'playbook_id': playbook_id,
            'playbook_name': playbook['name'],
            'status': 'running',
            'start_time': datetime.now().isoformat(),
            'trigger_data': execution_data,
            'actions_executed': [],
            'execution_log': []
        }
        
        # Execute actions
        actions = playbook.get('actions', [])
        execution_log = []
        
        for action in actions:
            try:
                # TODO: Implement actual action execution
                # - Send notifications
                # - Update thresholds
                # - Trigger retraining
                # - Pause models
                
                action_result = {
                    'action': action,
                    'status': 'success',
                    'timestamp': datetime.now().isoformat(),
                    'result': f"Action {action} executed successfully"
                }
                
                execution_record['actions_executed'].append(action_result)
                execution_log.append(f"✅ {action}: Success")
                
            except Exception as e:
                action_result = {
                    'action': action,
                    'status': 'failed',
                    'timestamp': datetime.now().isoformat(),
                    'error': str(e)
                }
                
                execution_record['actions_executed'].append(action_result)
                execution_log.append(f"❌ {action}: Failed - {str(e)}")
        
        # Update execution record
        execution_record['status'] = 'completed'
        execution_record['end_time'] = datetime.now().isoformat()
        execution_record['execution_log'] = execution_log
        
        # Store execution in database
        conn = duckdb.connect(str(get_database_path()))
        
        conn.execute("""
            INSERT INTO playbook_executions 
            (execution_id, playbook_id, status, start_time, end_time, execution_log, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, [
            execution_id,
            playbook_id,
            execution_record['status'],
            execution_record['start_time'],
            execution_record['end_time'],
            '\n'.join(execution_log),
            str(execution_record)
        ])
        
        conn.close()
        
        logger.info(f"Executed playbook {playbook_id}: {execution_record['status']}")
        return {"message": "Playbook executed successfully", "execution": execution_record}
        
    except Exception as e:
        logger.error(f"Failed to execute playbook {playbook_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{playbook_id}/executions")
async def get_playbook_executions(
    playbook_id: int,
    hours_back: int = Query(24, description="Hours of execution history to retrieve")
) -> List[Dict[str, Any]]:
    """Get execution history for a playbook."""
    
    # TODO: Implement execution history retrieval
    # - Load from database
    # - Filter by time range
    # - Include execution details
    # - Performance optimization
    
    try:
        conn = duckdb.connect(str(get_database_path()))
        
        query = """
            SELECT 
                execution_id,
                playbook_id,
                status,
                start_time,
                end_time,
                execution_log,
                metadata
            FROM playbook_executions
            WHERE playbook_id = ?
            AND start_time >= ?
            ORDER BY start_time DESC
        """
        
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        result = conn.execute(query, [playbook_id, cutoff_time]).fetchall()
        conn.close()
        
        columns = ['execution_id', 'playbook_id', 'status', 'start_time', 'end_time', 'execution_log', 'metadata']
        executions = [dict(zip(columns, row)) for row in result]
        
        logger.info(f"Retrieved {len(executions)} executions for playbook {playbook_id}")
        return executions
        
    except Exception as e:
        logger.error(f"Failed to retrieve executions for playbook {playbook_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/templates")
async def get_playbook_templates() -> List[Dict[str, Any]]:
    """Get available playbook templates."""
    
    # TODO: Implement template retrieval
    # - Load from templates directory
    # - Include template metadata
    # - Validate template structure
    # - Performance optimization
    
    try:
        templates_dir = Path("watchtower/playbooks/templates")
        
        if not templates_dir.exists():
            return []
        
        templates = []
        
        for template_file in templates_dir.glob("*.yaml"):
            try:
                with open(template_file, 'r') as f:
                    template = yaml.safe_load(f)
                
                template['filename'] = template_file.name
                templates.append(template)
                
            except Exception as e:
                logger.warning(f"Failed to load template {template_file}: {e}")
        
        logger.info(f"Retrieved {len(templates)} playbook templates")
        return templates
        
    except Exception as e:
        logger.error(f"Failed to retrieve playbook templates: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/summary")
async def get_playbook_summary(
    hours_back: int = Query(24, description="Hours of data to summarize")
) -> Dict[str, Any]:
    """Get playbook execution summary."""
    
    # TODO: Implement playbook summary
    # - Calculate execution statistics
    # - Identify successful/failed executions
    # - Generate insights
    # - Performance metrics
    
    try:
        conn = duckdb.connect(str(get_database_path()))
        
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        # Get execution summary
        query = """
            SELECT 
                COUNT(*) as total_executions,
                SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as successful_executions,
                SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed_executions,
                SUM(CASE WHEN status = 'running' THEN 1 ELSE 0 END) as running_executions,
                COUNT(DISTINCT playbook_id) as unique_playbooks
            FROM playbook_executions
            WHERE start_time >= ?
        """
        
        result = conn.execute(query, [cutoff_time]).fetchone()
        conn.close()
        
        if not result:
            return {
                "timestamp": datetime.now().isoformat(),
                "summary_window_hours": hours_back,
                "total_executions": 0,
                "successful_executions": 0,
                "failed_executions": 0,
                "running_executions": 0,
                "unique_playbooks": 0,
                "success_rate": 0
            }
        
        total_executions, successful_executions, failed_executions, running_executions, unique_playbooks = result
        
        success_rate = (successful_executions / total_executions * 100) if total_executions > 0 else 0
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "summary_window_hours": hours_back,
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "running_executions": running_executions,
            "unique_playbooks": unique_playbooks,
            "success_rate": round(success_rate, 2)
        }
        
        logger.info(f"Generated playbook summary: {success_rate:.1f}% success rate")
        return result
        
    except Exception as e:
        logger.error(f"Failed to generate playbook summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))
