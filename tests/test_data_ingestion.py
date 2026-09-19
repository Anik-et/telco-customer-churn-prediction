import pandas as pd

from src.components.data_ingestion import DataIngestion


def test_load_data(tmp_path):
    """Test that DataIngestion correctly loads a CSV file."""

    # Create a temporary CSV for testing.
    test_file = tmp_path / "sample_telco.csv"

    sample_data = pd.DataFrame(
        {
            "customerID": ["C001", "C002"],
            "tenure": [1, 24],
            "MonthlyCharges": [29.85, 56.95],
            "Churn": ["No", "Yes"],
        }
    )

    sample_data.to_csv(test_file, index=False)

    # Build the configuration expected by DataIngestion.
    config = {
        "data": {
            "raw_data_path": str(test_file)
        }
    }

    # Run the ingestion component.
    ingestion = DataIngestion(config)
    data = ingestion.load_data()

    # Validate the result.
    assert data is not None
    assert not data.empty
    assert data.shape == (2, 4)
    assert "Churn" in data.columns
    assert "customerID" in data.columns