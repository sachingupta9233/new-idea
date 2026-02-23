"""
SQLAlchemy database models
"""

from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base


class Locality(Base):
    """Model for Navi Mumbai localities"""
    __tablename__ = "localities"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    node_type = Column(String(50))  # e.g., "CBD", "Residential", "Mixed"
    metro_distance_km = Column(Float, nullable=True)
    highway_distance_km = Column(Float, nullable=True)
    avg_price_per_sqft = Column(Float, nullable=True)
    avg_price_updated = Column(DateTime, default=datetime.utcnow)
    transaction_volume_30days = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    properties = relationship("Property", back_populates="locality")
    predictions = relationship("Prediction", back_populates="locality")


class Property(Base):
    """Model for property listings/comparables"""
    __tablename__ = "properties"
    
    id = Column(Integer, primary_key=True, index=True)
    locality_id = Column(Integer, ForeignKey("localities.id"), index=True)
    name = Column(String(200), nullable=True)
    bhk = Column(Integer)  # 1, 2, 3, 4, etc.
    carpet_area_sqft = Column(Float)
    floor_number = Column(Integer, nullable=True)
    total_floors = Column(Integer, nullable=True)
    building_age_years = Column(Integer, nullable=True)
    price = Column(Float, index=True)
    price_per_sqft = Column(Float)
    
    # Amenities (boolean flags)
    lift = Column(Boolean, default=False)
    parking = Column(Boolean, default=False)
    gym = Column(Boolean, default=False)
    swimming_pool = Column(Boolean, default=False)
    gated_society = Column(Boolean, default=False)
    cctv = Column(Boolean, default=False)
    
    # Transaction details
    transaction_date = Column(DateTime, nullable=True)
    source = Column(String(50))  # "rera", "listing", "manual"
    source_id = Column(String(100), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    locality = relationship("Locality", back_populates="properties")


class Prediction(Base):
    """Model for price predictions"""
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    locality_id = Column(Integer, ForeignKey("localities.id"), index=True)
    
    # Input features
    bhk = Column(Integer)
    carpet_area_sqft = Column(Float)
    floor_number = Column(Integer, nullable=True)
    total_floors = Column(Integer, nullable=True)
    building_age_years = Column(Integer, nullable=True)
    
    lift = Column(Boolean, default=False)
    parking = Column(Boolean, default=False)
    gym = Column(Boolean, default=False)
    swimming_pool = Column(Boolean, default=False)
    gated_society = Column(Boolean, default=False)
    cctv = Column(Boolean, default=False)
    
    # Prediction outputs
    predicted_total_price = Column(Float, index=True)
    predicted_price_per_sqft = Column(Float)
    confidence_score = Column(Float)  # 0.0 to 1.0
    
    # Price range (80% CI)
    lower_bound = Column(Float)
    upper_bound = Column(Float)
    
    model_version = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    locality = relationship("Locality", back_populates="predictions")


class User(Base):
    """Model for user accounts"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(100), unique=True, index=True)
    phone = Column(String(20), nullable=True)
    hashed_password = Column(String(200))
    full_name = Column(String(200), nullable=True)
    is_active = Column(Boolean, default=True)
    user_type = Column(String(50), default="buyer")  # "buyer", "seller", "investor", "agent"
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class SavedEstimate(Base):
    """Model for saved property estimates"""
    __tablename__ = "saved_estimates"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    prediction_id = Column(Integer, ForeignKey("predictions.id"))
    name = Column(String(200))
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
