import pandas as pd

from src.pipeline.predict_pipeline import PredictPipeline


def test_prediction_pipeline():

    pipeline = PredictPipeline()

    sample_customer = pd.DataFrame([
        {
            "customerID": "TEST001",
            "gender": "Female",
            "SeniorCitizen": 0,
            "Partner": "Yes",
            "Dependents": "No",
            "tenure": 5,
            "PhoneService": "Yes",
            "MultipleLines": "No",
            "InternetService": "Fiber optic",
            "OnlineSecurity": "No",
            "OnlineBackup": "No",
            "DeviceProtection": "No",
            "TechSupport": "No",
            "StreamingTV": "Yes",
            "StreamingMovies": "Yes",
            "Contract": "Month-to-month",
            "PaperlessBilling": "Yes",
            "PaymentMethod": "Electronic check",
            "MonthlyCharges": 85.0,
            "TotalCharges": 425.0
        }
    ])

    result = pipeline.predict(sample_customer)

    assert "churn_prediction" in result
    assert "churn_probability" in result
    assert "risk_level" in result

    assert result["churn_prediction"] in ["Yes", "No"]
    assert 0 <= result["churn_probability"] <= 1
    assert result["risk_level"] in ["Low", "Medium", "High"]