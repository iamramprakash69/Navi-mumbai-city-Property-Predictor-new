"""
Predictor Module - Handles ML model predictions

This module loads the trained model once and provides prediction functions.
The model is loaded at module import time, not per request.
"""

import pickle
from pathlib import Path
from typing import Any, Callable, Dict

import pandas as pd

# Get model path
MODEL_DIR = Path(__file__).parent
MODEL_PATH = MODEL_DIR / "model_v2.pkl"

# Global variable to store loaded model artifacts
_model_artifacts = None


def load_model_artifacts():
    """Load the trained model and preprocessing artifacts once."""
    global _model_artifacts
    
    if _model_artifacts is None:
        path_to_use = MODEL_PATH if MODEL_PATH.exists() else MODEL_DIR / "model.pkl"
        if not path_to_use.exists():
            raise FileNotFoundError(f"Model file not found at {path_to_use}")
        
        with open(path_to_use, 'rb') as f:
            _model_artifacts = pickle.load(f)
        
        print(f"✓ Model loaded successfully from {path_to_use}!")
    
    return _model_artifacts


def real_estate_predict(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict real estate price for Navi Mumbai properties using v2 model.
    """
    artifacts = load_model_artifacts()
    model = artifacts['model']
    scaler = artifacts['scaler']
    feature_columns = artifacts['feature_columns']
    location_columns = artifacts['location_columns']
    market_stats = artifacts['market_stats']
    
    # Create input dictionary with all features
    input_data = {}
    
    # Numeric features matching training columns
    input_data['area_sqft'] = [float(features.get('area_sqft', 0))]
    input_data['bhk'] = [int(features.get('bhk', 0))]
    input_data['bathrooms'] = [int(features.get('bathrooms', 0))]
    input_data['floor'] = [int(features.get('floor', 0))]
    input_data['total_floors'] = [int(features.get('total_floors', 0))]
    input_data['age_of_property'] = [int(features.get('age_of_property', 0))]
    input_data['parking'] = [1 if features.get('parking') else 0]
    input_data['lift'] = [1 if features.get('lift') else 0]
    
    # One-hot encoded location
    location = features.get('location', '').strip().lower()
    for loc_col in location_columns:
        # loc_col looks like "Location_kharghar" or "Location_Kharghar"
        # The training script used df_encoded = pd.get_dummies(df, columns=['location'], prefix='Location')
        # So it depends on the CSV values. In the CSV, locations are likely lowercase or capitalized.
        input_data[loc_col] = [1 if loc_col.lower() == f"location_{location}" else 0]
        
    # Create DataFrame and ensure column order
    input_df = pd.DataFrame(input_data)
    input_df = input_df[feature_columns]
    
    # Scale
    input_scaled = scaler.transform(input_df)
    
    # Predict
    predicted_price = model.predict(input_scaled)[0]
    
    # Metrics
    area = input_data['area_sqft'][0]
    price_per_sqft = predicted_price / area if area > 0 else 0
    
    # Market status
    avg_price_per_sqft = market_stats['avg_price_per_sqft']
    if price_per_sqft < avg_price_per_sqft * 0.90:
        market_status = "Below Market"
    elif price_per_sqft > avg_price_per_sqft * 1.10:
        market_status = "Above Market"
    else:
        market_status = "Average"
        
    return {
        'predicted_price': round(predicted_price, 2),
        'price_per_sqft': round(price_per_sqft, 2),
        'market_status': market_status,
    }


def dummy_predict(features: Dict[str, Any]) -> Dict[str, Any]:
    """Dummy prediction function for testing."""
    numeric_values = [
        value for value in features.values() if isinstance(value, (int, float))
    ]
    if not numeric_values:
        return {"value": 0, "message": "No numeric features provided."}

    score = sum(numeric_values)
    return {
        "value": score,
        "message": "Dummy prediction is the sum of numeric features.",
    }


class Predictor:
    """Predictor class to manage multiple prediction models."""
    
    def __init__(self) -> None:
        self._models: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    def register(self, name: str, fn: Callable[[Dict[str, Any]], Any]) -> None:
        if not name:
            raise ValueError("Model name is required.")
        self._models[name] = fn

    def predict(self, name: str, features: Dict[str, Any]) -> Any:
        if name not in self._models:
            raise KeyError(name)
        return self._models[name](features)


# Create global predictor instance and register models
predictor = Predictor()
predictor.register("dummy", dummy_predict)
predictor.register("real_estate", real_estate_predict)
