"""
ML model training pipeline
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
import xgboost as xgb
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error
import joblib
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelTrainer:
    """Train and evaluate house price prediction models"""
    
    def __init__(self, data_path: str = None):
        self.data_path = data_path
        self.model = None
        self.scaler = None
        self.feature_names = None
        self.model_dir = Path("./models")
        self.model_dir.mkdir(exist_ok=True)
    
    def load_data(self, df: pd.DataFrame = None) -> pd.DataFrame:
        """
        Load training data from CSV or use provided dataframe
        
        Expected columns:
        - locality, bhk, carpet_area_sqft, floor_number, total_floors, building_age_years
        - lift, parking, gym, swimming_pool, gated_society, cctv
        - metro_distance_km, highway_distance_km
        - price (target variable)
        """
        if df is not None:
            return df
        
        if self.data_path:
            df = pd.read_csv(self.data_path)
            logger.info(f"Loaded data from {self.data_path}: {df.shape}")
            return df
        
        # Return sample synthetic data for demonstration
        return self._create_sample_data()
    
    def _create_sample_data(self, n_samples: int = 500) -> pd.DataFrame:
        """Create synthetic training data for demonstration"""
        np.random.seed(42)
        
        localities = [
            "Kharghar", "Vashi", "Panvel", "Nerul", 
            "Belapur", "Airoli", "Ulwe", "Dronagiri",
            "CBD Belapur", "Seawoods"
        ]
        
        # More realistic price per sqft ranges for Navi Mumbai localities
        locality_price_ranges = {
            "Seawoods": (140000, 160000),
            "CBD Belapur": (120000, 140000),
            "Vashi": (110000, 130000),
            "Belapur": (100000, 120000),
            "Kharghar": (80000, 100000),
            "Koparkhairane": (90000, 110000),
            "Airoli": (85000, 105000),
            "Ghansoli": (75000, 95000),
            "Kamothe": (65000, 85000),
            "Panvel": (60000, 80000),
            "Ulwe": (50000, 70000),
            "Dronagiri": (45000, 65000),
            "Taloje": (40000, 60000),
        }
        
        data = {
            'locality': np.random.choice(localities, n_samples),
            'bhk': np.random.choice([1, 2, 3, 4], n_samples),
            'carpet_area_sqft': np.random.uniform(500, 4000, n_samples),
            'floor_number': np.random.randint(1, 20, n_samples),
            'total_floors': np.random.randint(5, 40, n_samples),
            'building_age_years': np.random.randint(0, 25, n_samples),
            'lift': np.random.choice([0, 1], n_samples),
            'parking': np.random.choice([0, 1], n_samples),
            'gym': np.random.choice([0, 1], n_samples),
            'swimming_pool': np.random.choice([0, 1], n_samples),
            'gated_society': np.random.choice([0, 1], n_samples),
            'cctv': np.random.choice([0, 1], n_samples),
            'metro_distance_km': np.random.uniform(0.5, 15, n_samples),
            'highway_distance_km': np.random.uniform(1, 10, n_samples),
        }
        
        df = pd.DataFrame(data)
        
        # Generate synthetic price based on realistic patterns
        prices = []
        for idx, row in df.iterrows():
            locality = row['locality']
            base_price_range = locality_price_ranges.get(locality, (80000, 100000))
            base_price_per_sqft = np.random.uniform(base_price_range[0], base_price_range[1])
            
            # Apply feature adjustments
            bhk_multiplier = {1: 0.85, 2: 1.0, 3: 1.15, 4: 1.3}
            bhk_factor = bhk_multiplier.get(int(row['bhk']), 1.0)
            
            # Amenities add value
            amenity_bonus = (row['lift'] * 0.02 + row['parking'] * 0.02 + 
                            row['gym'] * 0.01 + row['swimming_pool'] * 0.02 + 
                            row['gated_society'] * 0.02 + row['cctv'] * 0.01)
            
            # Age factor
            age_factor = 1.0
            if row['building_age_years'] < 5:
                age_factor = 1.08
            elif row['building_age_years'] > 15:
                age_factor = 0.92
            
            # Calculate total price
            adjusted_price_per_sqft = base_price_per_sqft * bhk_factor * (1 + amenity_bonus) * age_factor
            total_price = adjusted_price_per_sqft * row['carpet_area_sqft']
            
            # Add small random variation
            total_price *= np.random.uniform(0.95, 1.05)
            
            prices.append(total_price)
        
        df['price'] = prices
        
        # Realistic bounds for Navi Mumbai
        df['price'] = df['price'].clip(lower=3000000, upper=50000000)
        
        logger.info(f"Created synthetic data: {df.shape}")
        logger.info(f"Price range: ₹{df['price'].min():,.0f} to ₹{df['price'].max():,.0f}")
        return df
    
    def prepare_features(self, df: pd.DataFrame) -> tuple:
        """Prepare features and target for modeling"""
        # Select feature columns
        feature_cols = [
            'bhk', 'carpet_area_sqft', 'floor_number', 'total_floors',
            'building_age_years', 'lift', 'parking', 'gym',
            'swimming_pool', 'gated_society', 'cctv',
            'metro_distance_km', 'highway_distance_km'
        ]
        
        X = df[feature_cols].copy()
        
        # Handle missing values
        X = X.fillna(X.median())
        
        # One-hot encode locality if present
        if 'locality' in df.columns:
            locality_dummies = pd.get_dummies(df['locality'], prefix='loc')
            X = pd.concat([X, locality_dummies], axis=1)
        
        self.feature_names = list(X.columns)
        
        y = df['price']
        
        logger.info(f"Prepared features: {X.shape}, target: {y.shape}")
        return X, y
    
    def train(self, df: pd.DataFrame = None, model_type: str = "xgboost"):
        """
        Train price prediction model
        
        Args:
            df: Training dataframe
            model_type: "xgboost" or "random_forest"
        """
        # Load and prepare data
        df = self.load_data(df)
        X, y = self.prepare_features(df)
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        self.scaler = StandardScaler()
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train model
        if model_type == "xgboost":
            self.model = xgb.XGBRegressor(
                n_estimators=100,
                max_depth=7,
                learning_rate=0.1,
                random_state=42,
                n_jobs=-1
            )
        else:
            self.model = RandomForestRegressor(
                n_estimators=100,
                max_depth=15,
                random_state=42,
                n_jobs=-1
            )
        
        logger.info(f"Training {model_type} model...")
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        mape = np.mean(np.abs((y_test - y_pred) / y_test)) * 100
        
        logger.info("Model Performance:")
        logger.info(f"  MAE: ₹{mae:,.0f}")
        logger.info(f"  RMSE: ₹{rmse:,.0f}")
        logger.info(f"  R² Score: {r2:.4f}")
        logger.info(f"  MAPE: {mape:.2f}%")
        
        # Cross-validation
        cv_scores = cross_val_score(
            self.model, X_train_scaled, y_train,
            cv=5, scoring='r2'
        )
        logger.info(f"  Cross-Val R² (5-fold): {cv_scores.mean():.4f} (+/- {cv_scores.std():.4f})")
        
        return {
            'mae': mae,
            'rmse': rmse,
            'r2': r2,
            'mape': mape,
            'cv_scores': cv_scores
        }
    
    def save_model(self, model_name: str = "xgboost_model"):
        """Save trained model, scaler, and feature names"""
        if self.model is None:
            raise ValueError("Model not trained yet")
        
        model_path = self.model_dir / f"{model_name}.pkl"
        scaler_path = self.model_dir / "scaler.pkl"
        features_path = self.model_dir / "feature_names.pkl"
        
        joblib.dump(self.model, model_path)
        joblib.dump(self.scaler, scaler_path)
        joblib.dump(self.feature_names, features_path)
        
        logger.info(f"Model saved to {model_path}")
        logger.info(f"Scaler saved to {scaler_path}")
        logger.info(f"Features saved to {features_path}")
    
    def load_model(self, model_name: str = "xgboost_model"):
        """Load previously trained model"""
        model_path = self.model_dir / f"{model_name}.pkl"
        scaler_path = self.model_dir / "scaler.pkl"
        features_path = self.model_dir / "feature_names.pkl"
        
        self.model = joblib.load(model_path)
        self.scaler = joblib.load(scaler_path)
        self.feature_names = joblib.load(features_path)
        
        logger.info(f"Model loaded from {model_path}")


if __name__ == "__main__":
    """Example usage"""
    trainer = ModelTrainer()
    
    # Train model
    metrics = trainer.train(model_type="xgboost")
    
    # Save model
    trainer.save_model()
    
    logger.info("Model training complete!")
