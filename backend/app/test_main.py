from fastapi.testclient import TestClient
from backend.app.main import app
import pytest

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "online"

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

def test_predict_real_estate_valid():
    payload = {
        "location": "vashi",
        "area_sqft": 1000,
        "bhk": 2,
        "bathrooms": 2,
        "floor": 5,
        "total_floors": 10,
        "age_of_property": 5,
        "parking": True,
        "lift": True
    }
    response = client.post("/predict/real-estate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "predicted_price" in data
    assert "price_per_sqft" in data
    assert "market_status" in data
    assert data["predicted_price"] > 0

def test_predict_real_estate_invalid_location():
    payload = {
        "location": "mumbai",  # Invalid location
        "area_sqft": 1000,
        "bhk": 2,
        "bathrooms": 2,
        "floor": 5,
        "total_floors": 10,
        "age_of_property": 5,
        "parking": True,
        "lift": True
    }
    response = client.post("/predict/real-estate", json=payload)
    assert response.status_code == 422 # Pydantic validation error

def test_predict_real_estate_negative_area():
    payload = {
        "location": "vashi",
        "area_sqft": -1000, # Invalid area
        "bhk": 2,
        "bathrooms": 2,
        "floor": 5,
        "total_floors": 10,
        "age_of_property": 5,
        "parking": True,
        "lift": True
    }
    response = client.post("/predict/real-estate", json=payload)
    assert response.status_code == 422
