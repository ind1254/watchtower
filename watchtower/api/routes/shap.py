"""
SHAP explainability routes for Watchtower API.
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from loguru import logger
import duckdb
import pandas as pd
import numpy as np

from ...config import settings, get_database_path
from ...models.serve import get_model_server

router = APIRouter()

@router.get("/explain/{transaction_id}")
async def explain_transaction(
    transaction_id: str,
    max_features: int = Query(10, description="Maximum number of features to show")
) -> Dict[str, Any]:
    """Explain a specific transaction prediction."""
    
    # TODO: Implement SHAP explanation
    # - Load transaction data
    # - Generate SHAP values
    # - Calculate feature importance
    # - Return explanation data
    
    try:
        # Get transaction data
        conn = duckdb.connect(str(get_database_path()))
        
        query = """
            SELECT 
                t.transaction_id,
                t.amount,
                t.user_id,
                t.merchant_category,
                t.country,
                t.timestamp,
                p.fraud_probability,
                p.prediction
            FROM transactions t
            LEFT JOIN model_predictions p ON t.transaction_id = p.transaction_id
            WHERE t.transaction_id = ?
        """
        
        result = conn.execute(query, [transaction_id]).fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=404, detail=f"Transaction {transaction_id} not found")
        
        # Convert to dict
        transaction_data = {
            'transaction_id': result[0],
            'amount': result[1],
            'user_id': result[2],
            'merchant_category': result[3],
            'country': result[4],
            'timestamp': result[5],
            'fraud_probability': result[6],
            'prediction': result[7]
        }
        
        # Generate SHAP explanation
        explanation = await generate_shap_explanation(transaction_data, max_features)
        
        logger.info(f"Generated explanation for transaction {transaction_id}")
        return explanation
        
    except Exception as e:
        logger.error(f"Failed to explain transaction {transaction_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/explain")
async def explain_transactions(
    transaction_data: Dict[str, Any],
    max_features: int = Query(10, description="Maximum number of features to show")
) -> Dict[str, Any]:
    """Explain a transaction prediction from provided data."""
    
    # TODO: Implement SHAP explanation for custom data
    # - Validate input data
    # - Generate SHAP values
    # - Calculate feature importance
    # - Return explanation data
    
    try:
        # Validate required fields
        required_fields = ['amount', 'user_id', 'merchant_category', 'country']
        for field in required_fields:
            if field not in transaction_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Generate SHAP explanation
        explanation = await generate_shap_explanation(transaction_data, max_features)
        
        logger.info("Generated explanation for custom transaction data")
        return explanation
        
    except Exception as e:
        logger.error(f"Failed to explain custom transaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/feature-importance")
async def get_feature_importance(
    hours_back: int = Query(24, description="Hours of data to analyze"),
    top_features: int = Query(10, description="Number of top features to return")
) -> Dict[str, Any]:
    """Get global feature importance across recent predictions."""
    
    # TODO: Implement global feature importance
    # - Analyze recent predictions
    # - Calculate average importance
    # - Identify key features
    # - Performance optimization
    
    try:
        conn = duckdb.connect(str(get_database_path()))
        
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        # Get recent transactions with predictions
        query = """
            SELECT 
                t.amount,
                t.user_id,
                t.merchant_category,
                t.country,
                t.timestamp,
                p.fraud_probability,
                p.prediction
            FROM transactions t
            JOIN model_predictions p ON t.transaction_id = p.transaction_id
            WHERE t.timestamp >= ?
            ORDER BY t.timestamp DESC
            LIMIT 1000
        """
        
        result = conn.execute(query, [cutoff_time]).fetchall()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="No recent predictions found")
        
        # Convert to DataFrame
        df = pd.DataFrame(result, columns=[
            'amount', 'user_id', 'merchant_category', 'country', 'timestamp', 'fraud_probability', 'prediction'
        ])
        
        # Calculate feature importance (simplified)
        feature_importance = calculate_global_feature_importance(df)
        
        # Get top features
        top_features_data = sorted(
            feature_importance.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:top_features]
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "analysis_window_hours": hours_back,
            "samples_analyzed": len(df),
            "feature_importance": dict(top_features_data),
            "top_features": [f[0] for f in top_features_data]
        }
        
        logger.info(f"Calculated feature importance for {len(df)} samples")
        return result
        
    except Exception as e:
        logger.error(f"Failed to calculate feature importance: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model-insights")
async def get_model_insights(
    hours_back: int = Query(24, description="Hours of data to analyze")
) -> Dict[str, Any]:
    """Get model insights and behavior analysis."""
    
    # TODO: Implement model insights
    # - Analyze prediction patterns
    # - Identify decision boundaries
    # - Calculate model stability
    # - Generate insights
    
    try:
        conn = duckdb.connect(str(get_database_path()))
        
        cutoff_time = datetime.now() - timedelta(hours=hours_back)
        
        # Get prediction statistics
        query = """
            SELECT 
                COUNT(*) as total_predictions,
                AVG(fraud_probability) as avg_probability,
                STDDEV(fraud_probability) as std_probability,
                MIN(fraud_probability) as min_probability,
                MAX(fraud_probability) as max_probability,
                SUM(CASE WHEN prediction = 1 THEN 1 ELSE 0 END) as fraud_predictions,
                SUM(CASE WHEN prediction = 0 THEN 1 ELSE 0 END) as non_fraud_predictions
            FROM model_predictions p
            JOIN transactions t ON p.transaction_id = t.transaction_id
            WHERE t.timestamp >= ?
        """
        
        result = conn.execute(query, [cutoff_time]).fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=404, detail="No recent predictions found")
        
        total_predictions, avg_prob, std_prob, min_prob, max_prob, fraud_preds, non_fraud_preds = result
        
        # Calculate insights
        fraud_rate = fraud_preds / total_predictions if total_predictions > 0 else 0
        confidence_range = max_prob - min_prob
        
        # Model stability (based on probability variance)
        stability_score = 1 - (std_prob / avg_prob) if avg_prob > 0 else 0
        
        result = {
            "timestamp": datetime.now().isoformat(),
            "analysis_window_hours": hours_back,
            "total_predictions": total_predictions,
            "fraud_prediction_rate": round(fraud_rate, 4),
            "average_confidence": round(avg_prob, 4),
            "confidence_range": round(confidence_range, 4),
            "model_stability": round(stability_score, 4),
            "probability_stats": {
                "min": round(min_prob, 4),
                "max": round(max_prob, 4),
                "std": round(std_prob, 4)
            }
        }
        
        logger.info(f"Generated model insights for {total_predictions} predictions")
        return result
        
    except Exception as e:
        logger.error(f"Failed to generate model insights: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def generate_shap_explanation(
    transaction_data: Dict[str, Any], 
    max_features: int
) -> Dict[str, Any]:
    """Generate SHAP explanation for a transaction."""
    
    # TODO: Implement actual SHAP calculation
    # - Load SHAP explainer
    # - Calculate SHAP values
    # - Generate feature contributions
    # - Return explanation data
    
    # Simplified explanation (replace with actual SHAP)
    features = ['amount', 'user_id', 'merchant_category', 'country']
    
    # Mock SHAP values
    shap_values = {}
    for feature in features:
        if feature in transaction_data:
            # Simple heuristic for demonstration
            if feature == 'amount':
                shap_values[feature] = min(transaction_data[feature] / 1000, 0.5)
            elif feature == 'merchant_category':
                shap_values[feature] = 0.3 if transaction_data[feature] == 'online' else 0.1
            elif feature == 'country':
                shap_values[feature] = 0.2 if transaction_data[feature] not in ['US', 'CA'] else 0.05
            else:
                shap_values[feature] = 0.1
    
    # Sort by absolute value
    sorted_features = sorted(
        shap_values.items(), 
        key=lambda x: abs(x[1]), 
        reverse=True
    )[:max_features]
    
    return {
        "transaction_id": transaction_data.get('transaction_id', 'custom'),
        "prediction": transaction_data.get('prediction', 0),
        "fraud_probability": transaction_data.get('fraud_probability', 0.5),
        "feature_contributions": dict(sorted_features),
        "top_contributing_features": [f[0] for f in sorted_features],
        "explanation_method": "simplified_heuristic",
        "timestamp": datetime.now().isoformat()
    }

def calculate_global_feature_importance(df: pd.DataFrame) -> Dict[str, float]:
    """Calculate global feature importance."""
    
    # TODO: Implement actual feature importance calculation
    # - Use SHAP or permutation importance
    # - Calculate across all samples
    # - Return importance scores
    
    # Simplified calculation
    importance = {}
    
    # Amount importance
    importance['amount'] = df['amount'].std() / df['amount'].mean() if df['amount'].mean() > 0 else 0
    
    # Merchant category importance
    category_counts = df['merchant_category'].value_counts()
    importance['merchant_category'] = category_counts.std() / category_counts.mean() if category_counts.mean() > 0 else 0
    
    # Country importance
    country_counts = df['country'].value_counts()
    importance['country'] = country_counts.std() / country_counts.mean() if country_counts.mean() > 0 else 0
    
    # User ID importance (simplified)
    importance['user_id'] = 0.1
    
    return importance
