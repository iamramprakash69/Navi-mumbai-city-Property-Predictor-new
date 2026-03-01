from typing import Any, Dict, Literal

from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    model: str = Field(default="dummy", description="Model key to use")
    features: Dict[str, Any] = Field(default_factory=dict)


class PredictionResponse(BaseModel):
    model: str
    prediction: Any
    details: Dict[str, Any] = Field(default_factory=dict)


# Real Estate specific schemas
class RealEstatePredictionRequest(BaseModel):
    """Request schema for Navi Mumbai real estate price prediction."""
    
    location: Literal["airoli", "belapur", "cbd belapur", "ghansoli", "kharghar", "nerul", "panvel", "ulwe", "vashi"] = Field(
        ..., 
        description="Property location in Navi Mumbai"
    )
    area_sqft: float = Field(..., gt=0)
    bhk: int = Field(..., ge=1, le=10)
    bathrooms: int = Field(..., ge=1, le=10)
    floor: int = Field(..., ge=0)
    total_floors: int = Field(..., ge=1)
    age_of_property: int = Field(..., ge=0)
    parking: bool = Field(...)
    lift: bool = Field(...)


class RealEstatePredictionResponse(BaseModel):
    """Response schema for real estate price prediction."""
    
    predicted_price: float = Field(
        ..., 
        description="Predicted property price in INR"
    )
    price_per_sqft: float = Field(
        ..., 
        description="Predicted price per square foot in INR"
    )
    market_status: str = Field(
        ..., 
        description="Market comparison: Below Market, Average, or Above Market"
    )
