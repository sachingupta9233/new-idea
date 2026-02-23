"""
Navi Mumbai House Price Predictor - FastAPI Backend
Main application entry point
"""

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from typing import Optional
from datetime import datetime

# Initialize FastAPI app
app = FastAPI(
    title="Navi Mumbai House Price Predictor API",
    description="ML-powered real estate valuation for Navi Mumbai",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Import routers
from routers import prediction, properties, localities, trends, auth

# Include routers
app.include_router(prediction.router, prefix="/api/v1/prediction", tags=["prediction"])
app.include_router(properties.router, prefix="/api/v1/properties", tags=["properties"])
app.include_router(localities.router, prefix="/api/v1/localities", tags=["localities"])
app.include_router(trends.router, prefix="/api/v1/trends", tags=["trends"])
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Navi Mumbai House Price Predictor"
    }


@app.get("/")
async def root():
    """Root endpoint with API info"""
    return {
        "message": "Welcome to Navi Mumbai House Price Predictor API",
        "version": "1.0.0",
        "docs_url": "/docs",
        "api_prefix": "/api/v1"
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
