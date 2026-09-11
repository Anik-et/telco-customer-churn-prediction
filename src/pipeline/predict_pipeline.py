import joblib
import pandas as pd
from pathlib import Path

from src.components.data_transformation import DataTransformation
from src.utils.config import read_yaml


class PredictPipeline:

    def __init__(self, config_path=None):

        # Project root:
        # src/pipeline/predict_pipeline.py
        #       ↑
        # parents[2] = 02_Churn_Prediction
        project_root = Path(__file__).resolve().parents[2]

        if config_path is None:
            config_path = project_root / "config.yaml"

        self.config = read_yaml(config_path)

        self.model_path = project_root / self.config["artifacts"]["best_model"]
        self.preprocessor_path = project_root / self.config["artifacts"]["preprocessor"]

        self.model = joblib.load(self.model_path)
        self.preprocessor = joblib.load(self.preprocessor_path)

        self.data_transformation = DataTransformation()

    def predict(self, input_data):
        """
        Predict churn for new customer data.

        Parameters
        ----------
        input_data : pandas.DataFrame
            Raw customer data.

        Returns
        -------
        dict
            Churn prediction, probability and risk level.
        """

        data = input_data.copy()

        # Apply the same raw-data transformation used during training
        data = self.data_transformation.transform(data)

        # Apply the fitted preprocessing pipeline
        transformed_data = self.preprocessor.transform(data)

        # Generate prediction
        prediction = self.model.predict(transformed_data)[0]

        # Generate churn probability
        probability = self.model.predict_proba(transformed_data)[0][1]

        # Convert prediction into business-friendly output
        prediction_label = "Yes" if prediction == 1 else "No"

        high_risk_threshold = self.config["prediction"]["high_risk_threshold"]
        medium_risk_threshold = self.config["prediction"]["medium_risk_threshold"]

        if probability >= high_risk_threshold:
            risk_level = "High"
        elif probability >= medium_risk_threshold:
            risk_level = "Medium"
        else:
            risk_level = "Low"
       
        return {
            "churn_prediction": prediction_label,
            "churn_probability": round(float(probability), 4),
            "risk_level": risk_level
        }


if __name__ == "__main__":

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

    print("\nPrediction Result:")
    print(f"Churn Prediction : {result['churn_prediction']}")
    print(f"Churn Probability: {result['churn_probability']}")
    print(f"Risk Level       : {result['risk_level']}")