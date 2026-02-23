"""
API router for price trend endpoints (F-05)
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import LocalityTrendResponse
from datetime import datetime, timedelta
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/{locality_name}/6m", response_model=LocalityTrendResponse)
async def get_6month_trend(
    locality_name: str,
    db: Session = Depends(get_db)
):
    """Get 6-month price trend for a locality (F-05: Price Trend Charts)"""
    from models import Locality, Prediction
    
    locality = db.query(Locality).filter(Locality.name.ilike(locality_name)).first()
    if not locality:
        raise HTTPException(status_code=404, detail="Locality not found")
    
    # Get predictions from last 6 months
    six_months_ago = datetime.utcnow() - timedelta(days=180)
    predictions = db.query(Prediction).filter(
        Prediction.locality_id == locality.id,
        Prediction.created_at >= six_months_ago
    ).order_by(Prediction.created_at).all()
    
    # Aggregate by date
    trend_data = []
    for pred in predictions:
        trend_data.append({
            "date": pred.created_at,
            "avg_price_per_sqft": pred.predicted_price_per_sqft,
            "transaction_count": 1
        })
    
    return LocalityTrendResponse(
        locality_name=locality_name,
        trend_data=trend_data,
        period_days=180
    )


@router.get("/{locality_name}/12m", response_model=LocalityTrendResponse)
async def get_12month_trend(
    locality_name: str,
    db: Session = Depends(get_db)
):
    """Get 12-month price trend for a locality (F-05: Price Trend Charts)"""
    from models import Locality, Prediction
    
    locality = db.query(Locality).filter(Locality.name.ilike(locality_name)).first()
    if not locality:
        raise HTTPException(status_code=404, detail="Locality not found")
    
    # Get predictions from last 12 months
    twelve_months_ago = datetime.utcnow() - timedelta(days=365)
    predictions = db.query(Prediction).filter(
        Prediction.locality_id == locality.id,
        Prediction.created_at >= twelve_months_ago
    ).order_by(Prediction.created_at).all()
    
    # Aggregate by date
    trend_data = []
    for pred in predictions:
        trend_data.append({
            "date": pred.created_at,
            "avg_price_per_sqft": pred.predicted_price_per_sqft,
            "transaction_count": 1
        })
    
    return LocalityTrendResponse(
        locality_name=locality_name,
        trend_data=trend_data,
        period_days=365
    )
