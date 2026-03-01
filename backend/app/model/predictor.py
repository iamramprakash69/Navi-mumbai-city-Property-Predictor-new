"""
Predictor Module - Handles ML model predictions for Navi Mumbai House Prices.
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
        if not MODEL_PATH.exists():
            # Fallback to model.pkl if model_v2.pkl doesn't exist yet
            alt_path = MODEL_DIR / "model.pkl"
            if not alt_path.exists():
                raise FileNotFoundError(
                    f"Model file not found at {MODEL_PATH}. "
                    "Please run train_model_v2.py first."
                )
            MODEL_PATH_TO_USE = alt_path
        else:
            MODEL_PATH_TO_USE = MODEL_PATH
            
        with open(MODEL_PATH_TO_USE, 'rb') as f:
            _model_artifacts = pickle.load(f)
        
        print(f"✓ Model loaded successfully from {MODEL_PATH_TO_USE}!")
    
    return _model_artifacts


def real_estate_predict(features: Dict[str, Any]) -> Dict[str, Any]:
    """
    Predict real estate price for Navi Mumbai properties.
    """
    artifacts = load_model_artifacts()
    model = artifacts['model']
    scaler = artifacts['scaler']
    feature_columns = artifacts['feature_columns']
    location_columns = artifacts['location_columns']
    market_stats = artifacts['market_stats']
    
    # Create input dictionary reflecting the trained model's feature order
    # Note: feature_columns contains both numeric and one-hot encoded location columns
    
    input_data = {}
    
    # Numeric features
    # Map from request schema to model feature names if they differ
    input_data['area_sqft'] = [float(features.get('area_sqft', 0))]
    input_data['bhk'] = [int(features.get('bhk', 0))]
    input_data['bathrooms'] = [int(features.get('bathrooms', 0))]
    input_data['floor'] = [int(features.get('floor', 0))]
    input_data['total_floors'] = [int(features.get('total_floors', 0))]
    input_data['age_of_property'] = [float(features.get('age_of_property', 0))]
    input_data['parking'] = [1 if features.get('parking') else 0]
    input_data['lift'] = [1 if features.get('lift') else 0]
    
    # One-hot encoded location
    location = features.get('location', '').strip()
    for loc_col in location_columns:
        input_data[loc_col] = [1 if loc_col == f"Location_{location}" else 0]
        
    # Create DataFrame and ensure column order matches training
    input_df = pd.DataFrame(input_data)
    input_df = input_df[feature_columns]
    
    # Scale
    input_scaled = scaler.transform(input_df)
    
    # Predict
    predicted_price = model.predict(input_scaled)[0]
    
    # Metrics
    area = input_data['area_sqft'][0]
    price_per_sqft = predicted_price / area if area > 0 else 0
    
    # Market comparison
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
    return {"value": 0, "message": "Dummy prediction enabled."}


class Predictor:
    """Predictor class to manage multiple prediction models."""
    def __init__(self) -> None:
        self._models: Dict[str, Callable[[Dict[str, Any]], Any]] = {}

    def register(self, name: str, fn: Callable[[Dict[str, Any]], Any]) -> None:
        self._models[name] = fn

    def predict(self, name: str, features: Dict[str, Any]) -> Any:
        if name not in self._models:
            raise KeyError(name)
        return self._models[name](features)


# Create global predictor instance and register models
predictor = Predictor()
predictor.register("dummy", dummy_predict)
predictor.register("real_estate", real_estate_predict)
