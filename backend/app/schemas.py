from typing import Any, Dict, Literal
from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """General prediction request schema."""
    model: str = Field(default="dummy", description="Model key to use")
    features: Dict[str, Any] = Field(default_factory=dict)


class PredictionResponse(BaseModel):
    """General prediction response schema."""
    model: str
    prediction: Any
    details: Dict[str, Any] = Field(default_factory=dict)


class RealEstatePredictionRequest(BaseModel):
    """Request schema for Navi Mumbai real estate price prediction."""

    location: Literal[
        "airoli", "belapur", "cbd belapur", "ghansoli", "kharghar", 
        "nerul", "panvel", "ulwe", "vashi"
    ] = Field(..., description="Property location in Navi Mumbai")
    
    area_sqft: float = Field(
        ..., gt=0, description="Property area in square feet", example=1000
    )
    
    bhk: int = Field(
        ..., ge=1, le=10, description="Number of bedrooms", example=2
    )
    
    bathrooms: int = Field(
        ..., ge=1, le=10, description="Number of bathrooms", example=2
    )
    
    floor: int = Field(
        ..., ge=0, le=50, description="Floor number of the property", example=5
    )
    
    total_floors: int = Field(
        ..., ge=1, le=100, description="Total floors in the building", example=10
    )
    
    age_of_property: float = Field(
        ..., ge=0, le=100, description="Property age in years", example=5
    )
    
    parking: bool = Field(
        ..., description="Whether parking is available", example=True
    )
    
    lift: bool = Field(
        ..., description="Whether lift is available", example=True
    )


class RealEstatePredictionResponse(BaseModel):
    """Response schema for real estate price prediction."""

    predicted_price: float = Field(
        ..., description="Predicted property price in INR"
    )
    price_per_sqft: float = Field(
        ..., description="Predicted price per square foot in INR"
    )
    market_status: str = Field(
        ..., description="Market comparison: Below Market, Average, or Above Market"
    )
