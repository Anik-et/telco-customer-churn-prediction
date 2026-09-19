import pandas as pd
from unittest.mock import Mock, patch

from src.pipeline.predict_pipeline import PredictPipeline


@patch("src.pipeline.predict_pipeline.joblib.load")
def test_prediction_pipeline(mock_load):
    """Test prediction pipeline without requiring saved model artifacts."""

    # Mock the trained model.
    mock_model = Mock()
    mock_model.predict.return_value = [1]
    mock_model.predict_proba.return_value = [[0.2, 0.8]]

    # Mock the fitted preprocessor.
    mock_preprocessor = Mock()
    mock_preprocessor.transform.return_value = [[0.0]]

    # PredictPipeline loads model first, then preprocessor.
    mock_load.side_effect = [
        mock_model,
        mock_preprocessor
    ]

    # Create sample customer data.
    input_data = pd.DataFrame(
        {
            "customerID": ["C001"],
            "TotalCharges": ["425"],
        }
    )

    # Run pipeline.
    pipeline = PredictPipeline()
    result = pipeline.predict(input_data)

    # Validate prediction result.
    assert result["churn_prediction"] == "Yes"
    assert result["churn_probability"] == 0.8
    assert result["risk_level"] == "High"