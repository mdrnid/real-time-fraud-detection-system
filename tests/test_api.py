import pytest
import numpy as np
from fastapi.testclient import TestClient
from src.main import app

# We use FastAPI's TestClient to test the API locally without a full uvicorn server
client = TestClient(app)

def test_health_check():
    """Verify the health check endpoint works."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "API is Online"

def test_prediction_endpoint():
    """Verify the prediction endpoint returns the correct structure."""
    # Dummy data: 28 features + 1 amount
    payload = {
        "features_v": [0.0] * 28,
        "amount": 100.0
    }
    
    response = client.post("/predict_transaction", json=payload)
    
    # Check status code
    assert response.status_code == 200
    
    # Check JSON structure
    data = response.json()
    assert data["status"] == "success"
    assert "prediction" in data
    assert "confidence_score" in data
    assert "details" in data
    assert data["details"]["raw_amount"] == 100.0

def test_invalid_input():
    """Verify API handles invalid input (wrong number of features) correctly."""
    # Only 10 features instead of 28
    payload = {
        "features_v": [0.0] * 10,
        "amount": 100.0
    }
    
    response = client.post("/predict_transaction", json=payload)
    
    # SHould return 400 Bad Request
    assert response.status_code == 400
    assert "Fitur V harus berjumlah 28" in response.json()["detail"]
