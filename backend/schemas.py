"""
Pydantic schemas for request/response validation
"""

from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from enum import Enum


class UserType(str, Enum):
    BUYER = "buyer"
    SELLER = "seller"
    INVESTOR = "investor"
    AGENT = "agent"


# ==================== Property Schemas ====================

class PropertyBase(BaseModel):
    bhk: int
    carpet_area_sqft: float
    floor_number: Optional[int] = None
    total_floors: Optional[int] = None
    building_age_years: Optional[int] = None
    lift: bool = False
    parking: bool = False
    gym: bool = False
    swimming_pool: bool = False
    gated_society: bool = False
    cctv: bool = False


class PropertyCreate(PropertyBase):
    locality_id: int
    name: Optional[str] = None
    price: Optional[float] = None
    transaction_date: Optional[datetime] = None
    source: str = "manual"


class PropertyResponse(PropertyBase):
    id: int
    locality_id: int
    name: Optional[str]
    price: Optional[float]
    price_per_sqft: Optional[float]
    source: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== Prediction Schemas ====================

class PredictionRequest(BaseModel):
    locality_name: str
    bhk: int
    carpet_area_sqft: float
    floor_number: Optional[int] = None
    total_floors: Optional[int] = None
    building_age_years: Optional[int] = None
    lift: bool = False
    parking: bool = False
    gym: bool = False
    swimming_pool: bool = False
    gated_society: bool = False
    cctv: bool = False


class PredictionResponse(BaseModel):
    id: int
    locality_name: str
    bhk: int
    carpet_area_sqft: float
    predicted_total_price: float
    predicted_price_per_sqft: float
    confidence_score: float
    lower_bound: float
    upper_bound: float
    model_version: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== Locality Schemas ====================

class LocalityBase(BaseModel):
    name: str
    node_type: Optional[str] = None
    metro_distance_km: Optional[float] = None
    highway_distance_km: Optional[float] = None


class LocalityCreate(LocalityBase):
    pass


class LocalityResponse(LocalityBase):
    id: int
    avg_price_per_sqft: Optional[float]
    transaction_volume_30days: int
    avg_price_updated: datetime
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class LocalityDetailResponse(LocalityResponse):
    properties: List[PropertyResponse] = []


# ==================== User Schemas ====================

class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    phone: Optional[str] = None
    user_type: UserType = UserType.BUYER


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== Auth Schemas ====================

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


class TokenData(BaseModel):
    email: Optional[str] = None


# ==================== Saved Estimate Schemas ====================

class SavedEstimateBase(BaseModel):
    name: str
    notes: Optional[str] = None


class SavedEstimateCreate(SavedEstimateBase):
    prediction_id: int


class SavedEstimateResponse(SavedEstimateBase):
    id: int
    prediction_id: int
    user_id: Optional[int]
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== Trend Schemas ====================

class TrendDataPoint(BaseModel):
    date: datetime
    avg_price_per_sqft: float
    transaction_count: int


class LocalityTrendResponse(BaseModel):
    locality_name: str
    trend_data: List[TrendDataPoint]
    period_days: int = 180
