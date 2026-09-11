import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler


class FeatureEngineer:

    def __init__(self):

        self.preprocessor = None
        self.feature_names = None

    def create_preprocessor(self, X):

        numerical_features = X.select_dtypes(
            include=["int64", "float64"]
        ).columns.tolist()

        categorical_features = X.select_dtypes(
            include=["object", "string"]
        ).columns.tolist()

        numerical_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler())
            ]
        )

        categorical_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                (
                    "onehot",
                    OneHotEncoder(
                        handle_unknown="ignore",
                        sparse_output=False
                    )
                )
            ]
        )

        self.preprocessor = ColumnTransformer(
            transformers=[
                (
                    "num",
                    numerical_pipeline,
                    numerical_features
                ),
                (
                    "cat",
                    categorical_pipeline,
                    categorical_features
                )
            ]
        )

        return self.preprocessor

    def fit_transform(self, X_train):

        if self.preprocessor is None:
            self.create_preprocessor(X_train)

        X_train_transformed = self.preprocessor.fit_transform(
            X_train
        )

        self.feature_names = (
            self.preprocessor.get_feature_names_out()
        )

        return X_train_transformed

    def transform(self, X):

        if self.preprocessor is None:
            raise ValueError(
                "Preprocessor has not been fitted yet."
            )

        return self.preprocessor.transform(X)

    def get_feature_names(self):

        if self.feature_names is None:
            raise ValueError(
                "Feature names are not available yet."
            )

        return self.feature_names