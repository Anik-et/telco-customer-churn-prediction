import pandas as pd

from src.components.data_transformation import DataTransformation


def test_total_charges_conversion():
    data = pd.DataFrame({
        "customerID": ["1"],
        "TotalCharges": ["100.50"]
    })

    transformer = DataTransformation()
    transformed = transformer.transform(data)

    assert "customerID" not in transformed.columns
    assert transformed["TotalCharges"].dtype == "float64"
    assert transformed["TotalCharges"].iloc[0] == 100.50