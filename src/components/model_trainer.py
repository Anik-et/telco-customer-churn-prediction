import joblib

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


class ModelTrainer:

    def __init__(self, config):

        self.config = config

        self.models = {
            "logistic_regression": LogisticRegression(
            max_iter=config["models"]["logistic_regression"]["max_iter"],
            random_state=42
            ),

            "random_forest": RandomForestClassifier(
                n_estimators=config["models"]["random_forest"]["n_estimators"],
                max_depth=config["models"]["random_forest"]["max_depth"],
                max_features=config["models"]["random_forest"]["max_features"],
                min_samples_split=config["models"]["random_forest"]["min_samples_split"],
                min_samples_leaf=config["models"]["random_forest"]["min_samples_leaf"],
                bootstrap=config["models"]["random_forest"]["bootstrap"],
                random_state=42
            ),

            "xgboost": XGBClassifier(
                n_estimators=config["models"]["xgboost"]["n_estimators"],
                max_depth=config["models"]["xgboost"]["max_depth"],
                learning_rate=config["models"]["xgboost"]["learning_rate"],
                subsample=config["models"]["xgboost"]["subsample"],
                min_child_weight=config["models"]["xgboost"]["min_child_weight"],
                colsample_bytree=config["models"]["xgboost"]["colsample_bytree"],
                random_state=42,
                eval_metric="logloss"
            )
        }

        self.trained_models = {}

    def train_model(self, model_name, X_train, y_train):

        model = self.models[model_name]

        model.fit(X_train, y_train)

        self.trained_models[model_name] = model

        return model

    def train_all(self, X_train, y_train):

        for model_name in self.models:

            self.train_model(
                model_name,
                X_train,
                y_train
            )

        return self.trained_models

    def save_model(self, model_name, path):

        if model_name not in self.trained_models:
            raise ValueError(
                f"{model_name} has not been trained yet."
            )

        joblib.dump(
            self.trained_models[model_name],
            path
        )