"""
Main FastAPI application for house price prediction.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .model.predictor import predictor
from .schemas import (
    PredictionRequest,
    PredictionResponse,
    RealEstatePredictionRequest,
    RealEstatePredictionResponse,
)

app = FastAPI(
    title="Navi Mumbai House Price Prediction API",
    description="API for predicting property prices in Navi Mumbai based on historical data.",
    version="1.0.0",
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint to check API status."""
    return {
        "status": "online",
        "message": "Navi Mumbai House Price Prediction API is running.",
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/predict/real-estate", response_model=RealEstatePredictionResponse)
async def predict_real_estate(
    payload: RealEstatePredictionRequest,
) -> RealEstatePredictionResponse:
    """
    Predict real estate prices for Navi Mumbai properties.

    Args:
        payload: The property features for prediction.

    Returns:
        The predicted price and market status.
    """
    try:
        # Convert Pydantic model to dictionary for the predictor
        features = payload.model_dump()
        
        # Get prediction from the real_estate model
        result = predictor.predict("real_estate", features)
        
        return RealEstatePredictionResponse(
            predicted_price=result["predicted_price"],
            price_per_sqft=result["price_per_sqft"],
            market_status=result["market_status"],
        )
        
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(
            status_code=500, detail=f"Prediction failed: {str(exc)}"
        )


@app.post("/predict", response_model=PredictionResponse)
async def predict_general(payload: PredictionRequest) -> PredictionResponse:
    """General prediction endpoint (primarily for testing)."""
    try:
        result = predictor.predict(payload.model, payload.features)
        return PredictionResponse(
            model=payload.model,
            prediction=result,
            details={"input_features": payload.features},
        )
    except KeyError:
        raise HTTPException(
            status_code=400, detail=f"Unknown model '{payload.model}'."
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
