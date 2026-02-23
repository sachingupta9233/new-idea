"""
API router for locality endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import LocalityResponse, LocalityDetailResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/", response_model=list[LocalityResponse])
async def get_all_localities(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get all supported localities with price statistics"""
    from models import Locality
    
    localities = db.query(Locality).offset(skip).limit(limit).all()
    return localities


@router.get("/{locality_name}", response_model=LocalityDetailResponse)
async def get_locality_details(
    locality_name: str,
    db: Session = Depends(get_db)
):
    """Get detailed locality information including recent properties (F-03: Locality Heatmap base data)"""
    from models import Locality
    
    locality = db.query(Locality).filter(
        Locality.name.ilike(locality_name)
    ).first()
    
    if not locality:
        raise HTTPException(status_code=404, detail="Locality not found")
    
    return locality


@router.get("/stats/all")
async def get_locality_stats(
    db: Session = Depends(get_db)
):
    """Get statistics for all localities for heatmap visualization"""
    from models import Locality
    
    localities = db.query(Locality).all()
    
    stats = [
        {
            "id": loc.id,
            "name": loc.name,
            "avg_price_per_sqft": loc.avg_price_per_sqft,
            "transaction_volume": loc.transaction_volume_30days,
            "metro_distance": loc.metro_distance_km
        }
        for loc in localities
    ]
    
    return {"localities": stats}
