import pandas as pd

from src.components.feature_engineering import FeatureEngineer


def test_feature_engineering():
    data = pd.DataFrame({
        "tenure": [1, 10, 20],
        "MonthlyCharges": [50.0, 70.0, 90.0],
        "Contract": [
            "Month-to-month",
            "One year",
            "Two year"
        ]
    })

    engineer = FeatureEngineer()

    transformed = engineer.fit_transform(data)

    assert transformed.shape[0] == 3
    assert transformed.shape[1] > data.shape[1]
    assert len(engineer.get_feature_names()) == transformed.shape[1]