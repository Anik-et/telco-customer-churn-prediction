import pandas as pd

from src.components.data_validation import DataValidation


def test_required_columns():
    data = pd.DataFrame({
        "customerID": ["1"],
        "gender": ["Female"],
        "Churn": ["Yes"]
    })

    validator = DataValidation(
        required_columns=["customerID", "gender", "Churn"],
        expected_dtypes={}
    )

    missing_columns = validator.check_required_columns(data)

    assert missing_columns == []