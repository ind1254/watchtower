"""
FastAPI main application for Watchtower.
"""

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from datetime import datetime
from loguru import logger

from ..config import settings, setup
from .routes import kpis, health, coverage, drift, playbooks, shap

# Initialize FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description="Risk Coverage & Drift Monitor for Financial-Crime Models",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(kpis.router, prefix="/kpis", tags=["kpis"])
app.include_router(coverage.router, prefix="/coverage", tags=["coverage"])
app.include_router(drift.router, prefix="/drift", tags=["drift"])
app.include_router(playbooks.router, prefix="/playbooks", tags=["playbooks"])
app.include_router(shap.router, prefix="/shap", tags=["shap"])

@app.on_event("startup")
async def startup_event():
    """Initialize application on startup."""
    try:
        # Setup configuration
        setup()
        
        # Initialize model server
        from ..models.serve import initialize_model_server
        model_loaded = initialize_model_server()
        
        if model_loaded:
            logger.info("Model server initialized successfully")
        else:
            logger.warning("Model server initialization failed")
        
        logger.info(f"Watchtower API started on {settings.api_host}:{settings.api_port}")
        
    except Exception as e:
        logger.error(f"Startup failed: {e}")
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown."""
    logger.info("Watchtower API shutting down")

@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Watchtower API",
        "version": settings.api_version,
        "description": "Risk Coverage & Drift Monitor for Financial-Crime Models",
        "endpoints": {
            "health": "/health",
            "kpis": "/kpis",
            "coverage": "/coverage", 
            "drift": "/drift",
            "playbooks": "/playbooks",
            "shap": "/shap",
            "docs": "/docs"
        },
        "timestamp": datetime.now().isoformat()
    }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler."""
    logger.error(f"Unhandled exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": str(exc),
            "timestamp": datetime.now().isoformat()
        }
    )

def main():
    """Main entry point for the API server."""
    uvicorn.run(
        app,
        host=settings.api_host,
        port=settings.api_port,
        log_level=settings.log_level.lower()
    )

if __name__ == "__main__":
    main()
