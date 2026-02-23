#!/usr/bin/env python3
"""
Standalone script to train ML model for Navi Mumbai House Price Predictor
"""

import sys
import os

# Add project to path
sys.path.insert(0, '/Users/sachingupta/Desktop/house')

from ml.model_trainer import ModelTrainer

def main():
    # Create models directory
    os.makedirs('/Users/sachingupta/Desktop/house/models', exist_ok=True)
    
    print("\n" + "=" * 70)
    print(" " * 15 + "Navi Mumbai House Price Predictor")
    print(" " * 20 + "Model Training Pipeline")
    print("=" * 70)
    
    # Initialize trainer
    trainer = ModelTrainer()
    
    # Train XGBoost model
    print("\n[1/2] Training XGBoost Model with Synthetic Data...")
    print("-" * 70)
    metrics = trainer.train(model_type="xgboost")
    
    # Save model artifacts
    print("\n[2/2] Saving Model Artifacts...")
    print("-" * 70)
    trainer.save_model()
    
    print("\n" + "=" * 70)
    print("✅ MODEL TRAINING COMPLETE!")
    print("=" * 70)
    print(f"""
Model Artifacts Successfully Created:
  ✓ models/xgboost_model.pkl (trained model)
  ✓ models/scaler.pkl (feature scaler)
  ✓ models/feature_names.pkl (feature names)

Performance Metrics:
  Mean Absolute Error (MAE):    ₹{metrics['mae']:,.0f}
  Root Mean Squared Error:      ₹{metrics['rmse']:,.0f}
  R² Score:                     {metrics['r2']:.4f}
  Mean Absolute Percentage:     {metrics['mape']:.2f}%

Status: Model ready for production! 🚀
""")
    print("=" * 70)

if __name__ == "__main__":
    main()
