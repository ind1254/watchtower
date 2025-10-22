"""
Main entry point for Watchtower application.
"""

import uvicorn
import subprocess
import sys
from pathlib import Path
from config import settings

def start_api():
    """Start the FastAPI server."""
    print(f"Starting Watchtower API on {settings.api_host}:{settings.api_port}")
    uvicorn.run("api:app", host=settings.api_host, port=settings.api_port, reload=True)

def start_dashboard():
    """Start the Streamlit dashboard."""
    print(f"Starting Watchtower Dashboard on port {settings.streamlit_port}")
    subprocess.run([
        sys.executable, "-m", "streamlit", "run", "dashboard.py",
        "--server.port", str(settings.streamlit_port)
    ])

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Watchtower: Risk Coverage & Drift Monitor")
    parser.add_argument("--mode", choices=["api", "dashboard", "both"], default="both",
                       help="Mode to run: api, dashboard, or both")
    
    args = parser.parse_args()
    
    if args.mode == "api":
        start_api()
    elif args.mode == "dashboard":
        start_dashboard()
    elif args.mode == "both":
        print("Starting both API and Dashboard...")
        print("API will run on port 8000, Dashboard on port 8501")
        print("Press Ctrl+C to stop both services")
        
        # Start API in background
        import threading
        api_thread = threading.Thread(target=start_api)
        api_thread.daemon = True
        api_thread.start()
        
        # Start dashboard in foreground
        start_dashboard()

if __name__ == "__main__":
    main()
