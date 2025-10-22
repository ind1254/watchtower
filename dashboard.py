"""
Streamlit dashboard for Watchtower monitoring system.
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests
from typing import Dict, List, Any
import json

from config import settings

# Page configuration
st.set_page_config(
    page_title="Watchtower Dashboard",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# API base URL
API_BASE_URL = f"http://localhost:{settings.api_port}"

def fetch_data(endpoint: str, params: Dict[str, Any] = None) -> List[Dict[str, Any]]:
    """Fetch data from API endpoint."""
    try:
        response = requests.get(f"{API_BASE_URL}/{endpoint}", params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from {endpoint}: {e}")
        return []

def create_kpi_chart(data: List[Dict[str, Any]]) -> go.Figure:
    """Create KPI metrics chart."""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    fig = go.Figure()
    
    for metric in df['metric_name'].unique():
        metric_data = df[df['metric_name'] == metric]
        fig.add_trace(go.Scatter(
            x=metric_data['timestamp'],
            y=metric_data['metric_value'],
            mode='lines+markers',
            name=metric,
            line=dict(width=2)
        ))
    
    fig.update_layout(
        title="KPI Metrics Over Time",
        xaxis_title="Time",
        yaxis_title="Metric Value",
        hovermode='x unified'
    )
    
    return fig

def create_coverage_chart(data: List[Dict[str, Any]]) -> go.Figure:
    """Create coverage chart."""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    fig = px.bar(
        df,
        x='risk_category',
        y='coverage_percentage',
        color='model_name',
        title="Risk Coverage by Category",
        labels={'coverage_percentage': 'Coverage %', 'risk_category': 'Risk Category'}
    )
    
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500
    )
    
    return fig

def create_drift_chart(data: List[Dict[str, Any]]) -> go.Figure:
    """Create drift detection chart."""
    if not data:
        return go.Figure()
    
    df = pd.DataFrame(data)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    
    # Filter for detected drift
    drift_detected = df[df['drift_detected'] == True]
    
    if drift_detected.empty:
        return go.Figure().add_annotation(
            text="No drift detected in the selected time period",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=16)
        )
    
    fig = px.scatter(
        drift_detected,
        x='timestamp',
        y='drift_score',
        color='feature_name',
        size='drift_score',
        hover_data=['drift_type', 'severity', 'p_value'],
        title="Detected Drift Events",
        labels={'drift_score': 'Drift Score', 'timestamp': 'Time'}
    )
    
    return fig

def main():
    """Main Streamlit application."""
    
    st.title("🛡️ Watchtower Dashboard")
    st.markdown("Risk Coverage & Drift Monitor for Financial-Crime Models")
    
    # Sidebar controls
    st.sidebar.header("Controls")
    
    # Time range selector
    time_range = st.sidebar.selectbox(
        "Time Range",
        ["Last 24 hours", "Last 7 days", "Last 30 days"],
        index=0
    )
    
    hours_back = {
        "Last 24 hours": 24,
        "Last 7 days": 168,
        "Last 30 days": 720
    }[time_range]
    
    # Model selector
    model_name = st.sidebar.text_input("Model Name (optional)", placeholder="e.g., fraud_detection_v2")
    
    # Main dashboard
    tab1, tab2, tab3, tab4 = st.tabs(["📊 KPIs", "🎯 Coverage", "📈 Drift", "📋 Playbooks"])
    
    with tab1:
        st.header("Key Performance Indicators")
        
        # Fetch KPI data
        kpi_data = fetch_data("kpis", {"hours_back": hours_back, "model_name": model_name or None})
        
        if kpi_data:
            # KPI metrics chart
            kpi_chart = create_kpi_chart(kpi_data)
            st.plotly_chart(kpi_chart, use_container_width=True)
            
            # KPI summary table
            df_kpi = pd.DataFrame(kpi_data)
            latest_kpis = df_kpi.groupby('metric_name').first().reset_index()
            
            st.subheader("Latest KPI Values")
            st.dataframe(
                latest_kpis[['metric_name', 'metric_value', 'status']],
                use_container_width=True
            )
        else:
            st.info("No KPI data available for the selected time range.")
    
    with tab2:
        st.header("Risk Coverage Analysis")
        
        # Fetch coverage data
        coverage_data = fetch_data("coverage", {"hours_back": hours_back, "model_name": model_name or None})
        
        if coverage_data:
            # Coverage chart
            coverage_chart = create_coverage_chart(coverage_data)
            st.plotly_chart(coverage_chart, use_container_width=True)
            
            # Coverage summary
            df_coverage = pd.DataFrame(coverage_data)
            coverage_summary = df_coverage.groupby('risk_category')['coverage_percentage'].mean().reset_index()
            
            st.subheader("Average Coverage by Risk Category")
            st.dataframe(coverage_summary, use_container_width=True)
            
            # Coverage alerts
            low_coverage = df_coverage[df_coverage['coverage_percentage'] < settings.coverage_threshold * 100]
            if not low_coverage.empty:
                st.warning(f"⚠️ Low coverage detected for {len(low_coverage)} risk categories")
                st.dataframe(low_coverage[['risk_category', 'coverage_percentage', 'model_name']])
        else:
            st.info("No coverage data available for the selected time range.")
    
    with tab3:
        st.header("Drift Detection")
        
        # Fetch drift data
        drift_data = fetch_data("drift", {"hours_back": hours_back, "model_name": model_name or None})
        
        if drift_data:
            # Drift chart
            drift_chart = create_drift_chart(drift_data)
            st.plotly_chart(drift_chart, use_container_width=True)
            
            # Drift summary
            df_drift = pd.DataFrame(drift_data)
            drift_summary = df_drift.groupby(['feature_name', 'drift_detected']).size().reset_index(name='count')
            
            st.subheader("Drift Detection Summary")
            st.dataframe(drift_summary, use_container_width=True)
            
            # High severity drift alerts
            high_severity = df_drift[
                (df_drift['drift_detected'] == True) & 
                (df_drift['severity'] == 'high')
            ]
            if not high_severity.empty:
                st.error(f"🚨 High severity drift detected in {len(high_severity)} features")
                st.dataframe(high_severity[['feature_name', 'drift_score', 'severity', 'timestamp']])
        else:
            st.info("No drift data available for the selected time range.")
    
    with tab4:
        st.header("Playbooks")
        
        # Fetch playbooks
        playbooks = fetch_data("playbooks", {"active_only": True})
        
        if playbooks:
            st.subheader("Active Playbooks")
            
            for playbook in playbooks:
                with st.expander(f"📋 {playbook['name']}"):
                    st.write(f"**Description:** {playbook['description']}")
                    st.write(f"**Active:** {'✅' if playbook['is_active'] else '❌'}")
                    
                    # Show recent executions
                    executions = fetch_data(f"playbooks/{playbook['id']}/executions", {"hours_back": 24})
                    if executions:
                        st.write("**Recent Executions:**")
                        df_exec = pd.DataFrame(executions)
                        st.dataframe(df_exec[['triggered_at', 'status', 'execution_log']], use_container_width=True)
                    else:
                        st.write("No recent executions")
        else:
            st.info("No active playbooks found.")
    
    # Footer
    st.markdown("---")
    st.markdown(f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")

if __name__ == "__main__":
    main()
