"""
Prediction service for handling ML model predictions
"""

import logging
from sqlalchemy.orm import Session
from schemas import PredictionRequest, PredictionResponse
from models import Prediction, Locality
from datetime import datetime
import joblib
import numpy as np
from config import get_settings

logger = logging.getLogger(__name__)


class PredictionService:
    """Service for handling property price predictions"""
    
    def __init__(self, db: Session):
        self.db = db
        self.settings = get_settings()
        self.model = None
        self.scaler = None
        self.feature_names = None
        self._load_model()
    
    def _load_model(self):
        """Load pre-trained ML model and scaler"""
        try:
            self.model = joblib.load(self.settings.MODEL_PATH)
            self.scaler = joblib.load(self.settings.SCALER_PATH)
            self.feature_names = joblib.load(self.settings.FEATURE_NAMES_PATH)
            logger.info("ML model loaded successfully")
        except Exception as e:
            logger.warning(f"Could not load pre-trained model: {e}. Using fallback model.")
            self.model = None
    
    async def predict(self, request: PredictionRequest) -> PredictionResponse:
        """
        Make a price prediction for a property
        
        Args:
            request: Property details
            
        Returns:
            Prediction with price estimate and confidence interval
        """
        # Get locality information
        locality = self.db.query(Locality).filter(
            Locality.name.ilike(request.locality_name)
        ).first()
        
        if not locality:
            raise ValueError(f"Locality {request.locality_name} not found")
        
        # Prepare features for prediction
        features = self._prepare_features(request, locality)
        
        # Make prediction
        if self.model and self.scaler:
            predicted_price_per_sqft = self._predict_with_ml(features)
        else:
            # Fallback: Use locality average + adjustments
            predicted_price_per_sqft = self._predict_with_fallback(request, locality)
        
        predicted_total_price = predicted_price_per_sqft * request.carpet_area_sqft
        
        # Calculate confidence interval (simplified)
        confidence_score = 0.85  # Default confidence
        margin = predicted_total_price * 0.1  # 10% margin for CI
        lower_bound = predicted_total_price - margin
        upper_bound = predicted_total_price + margin
        
        # Store prediction in database
        db_prediction = Prediction(
            locality_id=locality.id,
            bhk=request.bhk,
            carpet_area_sqft=request.carpet_area_sqft,
            floor_number=request.floor_number,
            total_floors=request.total_floors,
            building_age_years=request.building_age_years,
            lift=request.lift,
            parking=request.parking,
            gym=request.gym,
            swimming_pool=request.swimming_pool,
            gated_society=request.gated_society,
            cctv=request.cctv,
            predicted_total_price=predicted_total_price,
            predicted_price_per_sqft=predicted_price_per_sqft,
            confidence_score=confidence_score,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            model_version="1.0"
        )
        
        self.db.add(db_prediction)
        self.db.commit()
        self.db.refresh(db_prediction)
        
        return PredictionResponse(
            id=db_prediction.id,
            locality_name=request.locality_name,
            bhk=request.bhk,
            carpet_area_sqft=request.carpet_area_sqft,
            predicted_total_price=predicted_total_price,
            predicted_price_per_sqft=predicted_price_per_sqft,
            confidence_score=confidence_score,
            lower_bound=lower_bound,
            upper_bound=upper_bound,
            model_version="1.0",
            created_at=db_prediction.created_at
        )
    
    def _prepare_features(self, request: PredictionRequest, locality: Locality) -> dict:
        """Prepare features for model prediction"""
        features = {
            'bhk': request.bhk,
            'carpet_area_sqft': request.carpet_area_sqft,
            'floor_number': request.floor_number or 1,
            'total_floors': request.total_floors or 5,
            'building_age_years': request.building_age_years or 10,
            'lift': int(request.lift),
            'parking': int(request.parking),
            'gym': int(request.gym),
            'swimming_pool': int(request.swimming_pool),
            'gated_society': int(request.gated_society),
            'cctv': int(request.cctv),
            'metro_distance_km': locality.metro_distance_km or 5.0,
            'highway_distance_km': locality.highway_distance_km or 3.0,
            'avg_price_locality': locality.avg_price_per_sqft or 100000
        }
        return features
    
    def _predict_with_ml(self, features: dict) -> float:
        """Make prediction using trained ML model"""
        try:
            feature_vector = self._features_to_vector(features)
            scaled_features = self.scaler.transform([feature_vector])
            pred = self.model.predict(scaled_features)[0]
            return max(pred, self.settings.MIN_PREDICTION_PRICE)
        except Exception as e:
            logger.error(f"ML prediction error: {e}")
            return self._predict_with_fallback_simple(features)
    
    def _predict_with_fallback(self, request: PredictionRequest, locality: Locality) -> float:
        """Fallback prediction using locality averages and feature adjustments"""
        base_price = locality.avg_price_per_sqft or 100000
        
        # Adjustments based on property features
        adjustment = 1.0
        
        # BHK adjustment
        bhk_multiplier = {1: 0.8, 2: 1.0, 3: 1.15, 4: 1.3, 5: 1.5}
        adjustment *= bhk_multiplier.get(request.bhk, 1.0)
        
        # Amenities adjustment
        amenity_count = sum([
            request.lift, request.parking, request.gym,
            request.swimming_pool, request.gated_society, request.cctv
        ])
        adjustment *= (1.0 + amenity_count * 0.05)
        
        # Floor adjustment (higher floors slightly premium)
        if request.floor_number and request.floor_number > 5:
            adjustment *= 1.05
        
        # Age adjustment
        if request.building_age_years:
            if request.building_age_years < 5:
                adjustment *= 1.1
            elif request.building_age_years > 15:
                adjustment *= 0.9
        
        return base_price * adjustment
    
    def _predict_with_fallback_simple(self, features: dict) -> float:
        """Simple fallback prediction"""
        base_price = features.get('avg_price_locality', 100000)
        adjustment = 1.0 + (features['bhk'] * 0.1)
        return base_price * adjustment
    
    def _features_to_vector(self, features: dict) -> list:
        """Convert feature dict to vector in correct order"""
        ordered_features = [
            features.get(name, 0) for name in self.feature_names
        ]
        return ordered_features
    
    async def get_prediction_history(self, locality_name: str, limit: int = 10):
        """Get recent predictions for a locality"""
        locality = self.db.query(Locality).filter(
            Locality.name.ilike(locality_name)
        ).first()
        
        if not locality:
            raise ValueError(f"Locality {locality_name} not found")
        
        predictions = self.db.query(Prediction).filter(
            Prediction.locality_id == locality.id
        ).order_by(Prediction.created_at.desc()).limit(limit).all()
        
        return [
            PredictionResponse(
                id=p.id,
                locality_name=locality_name,
                bhk=p.bhk,
                carpet_area_sqft=p.carpet_area_sqft,
                predicted_total_price=p.predicted_total_price,
                predicted_price_per_sqft=p.predicted_price_per_sqft,
                confidence_score=p.confidence_score,
                lower_bound=p.lower_bound,
                upper_bound=p.upper_bound,
                model_version=p.model_version,
                created_at=p.created_at
            )
            for p in predictions
        ]
