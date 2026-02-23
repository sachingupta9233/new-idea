"""
API router for prediction endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import PredictionRequest, PredictionResponse
from services.prediction_service import PredictionService
from config import get_settings
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/predict", response_model=PredictionResponse)
async def predict_property_price(
    request: PredictionRequest,
    db: Session = Depends(get_db)
):
    """
    Predict property price based on input features (F-01, F-02)
    
    Args:
        request: Property details for prediction
        db: Database session
        
    Returns:
        Prediction with estimated price and confidence interval
    """
    try:
        settings = get_settings()
        
        # Validate locality
        if request.locality_name not in settings.SUPPORTED_LOCALITIES:
            raise HTTPException(
                status_code=400,
                detail=f"Locality '{request.locality_name}' not supported. Supported localities: {settings.SUPPORTED_LOCALITIES}"
            )
        
        # Get prediction service
        service = PredictionService(db)
        
        # Make prediction
        prediction = await service.predict(request)
        
        return prediction
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error generating prediction"
        )


@router.get("/history/{locality_name}")
async def get_prediction_history(
    locality_name: str,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """
    Get recent predictions for a specific locality
    
    Args:
        locality_name: Name of the locality
        limit: Number of predictions to return
        db: Database session
        
    Returns:
        List of recent predictions
    """
    try:
        service = PredictionService(db)
        history = await service.get_prediction_history(locality_name, limit)
        return {"predictions": history}
    except Exception as e:
        logger.error(f"Error fetching prediction history: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Error fetching prediction history"
        )
