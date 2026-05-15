"""
Tests for the Churn Prediction API.
"""

import pytest
from litestar.testing import TestClient

from app.model_utils import predict_churn
from main import app


def test_predict_churn_direct():
    sample_features = {
        "CreditScore": 600,
        "Geography": "France",
        "Gender": "Male",
        "Age": 40,
        "Tenure": 3,
        "Balance": 60000.0,
        "NumOfProducts": 2,
        "HasCrCard": 1,
        "IsActiveMember": 1,
        "EstimatedSalary": 50000.0,
    }

    import pandas as pd
    df = pd.DataFrame([sample_features])

    result = predict_churn(df)

    # ensure valid binary output
    assert result in [0, 1] or result[0] in [0, 1]



def test_predict_endpoint():
    payload = {
        "CreditScore": 600,
        "Geography": "France",
        "Gender": "Male",
        "Age": 40,
        "Tenure": 3,
        "Balance": 60000.0,
        "NumOfProducts": 2,
        "HasCrCard": 1,
        "IsActiveMember": 1,
        "EstimatedSalary": 50000.0,
    }

    with TestClient(app=app) as client:
        response = client.post("/predict", json=payload)

        assert response.status_code in (200, 201)

        body = response.json()
        assert "prediction" in body



def test_health_endpoint():
    with TestClient(app=app) as client:
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


def test_home_endpoint():
    with TestClient(app=app) as client:
        response = client.get("/")

        assert response.status_code == 200
        assert response.json() == {
            "message": "Welcome to the Churn Prediction API"
        }


def test_invalid_input_returns_400():
    bad_payload = {
        "CreditScore": "invalid",  # should be int
        "Geography": "France",
    }

    with TestClient(app=app) as client:
        response = client.post("/predict", json=bad_payload)

        assert response.status_code == 400