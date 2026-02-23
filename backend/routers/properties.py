"""
API router for property endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import PropertyCreate, PropertyResponse
import logging

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/", response_model=PropertyResponse)
async def create_property(
    property_data: PropertyCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new property record
    
    Args:
        property_data: Property details
        db: Database session
        
    Returns:
        Created property
    """
    try:
        from models import Property
        
        db_property = Property(**property_data.dict())
        db_property.price_per_sqft = property_data.price / property_data.carpet_area_sqft if property_data.price else None
        
        db.add(db_property)
        db.commit()
        db.refresh(db_property)
        return db_property
    except Exception as e:
        logger.error(f"Error creating property: {str(e)}")
        db.rollback()
        raise HTTPException(status_code=500, detail="Error creating property")


@router.get("/{property_id}", response_model=PropertyResponse)
async def get_property(
    property_id: int,
    db: Session = Depends(get_db)
):
    """Get property by ID"""
    from models import Property
    
    property_obj = db.query(Property).filter(Property.id == property_id).first()
    if not property_obj:
        raise HTTPException(status_code=404, detail="Property not found")
    return property_obj


@router.get("/locality/{locality_id}")
async def get_properties_by_locality(
    locality_id: int,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """Get properties for a specific locality (F-04: Comparable Listings)"""
    from models import Property
    
    properties = db.query(Property).filter(
        Property.locality_id == locality_id
    ).limit(limit).all()
    
    return {"properties": properties, "count": len(properties)}
