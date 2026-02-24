"""
Configuration settings for the backend application
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings"""
    
    # API Configuration
    API_TITLE: str = "Navi Mumbai House Price Predictor API"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Database Configuration
    DATABASE_URL: str = "postgresql://user:password@localhost:5432/navi_mumbai_house"
    SQLALCHEMY_ECHO: bool = False
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # JWT Configuration
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # ML Configuration
    MODEL_PATH: str = "./models/xgboost_model.pkl"
    SCALER_PATH: str = "./models/scaler.pkl"
    FEATURE_NAMES_PATH: str = "./models/feature_names.pkl"
    
    # API Configuration
    CORS_ORIGINS: list = ["*"]
    
    # Data Configuration
    DATA_REFRESH_INTERVAL_DAYS: int = 30
    CONFIDENCE_THRESHOLD: float = 0.8
    
    # Prediction Configuration
    PREDICTION_TIMEOUT_SECONDS: int = 5
    MAX_PREDICTION_PRICE: float = 50000000  # 5 crore max (realistic for Navi Mumbai)
    MIN_PREDICTION_PRICE: float = 1000000  # 10 lakhs min
    
    # Localities supported
    SUPPORTED_LOCALITIES: list = [
        "Kharghar", "Vashi", "Panvel", "Nerul", 
        "Belapur", "Airoli", "Ulwe", "Dronagiri",
        "CBD Belapur", "Seawoods", "Koparkhairane",
        "Ghansoli", "Kamothe", "Taloje"
    ]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
