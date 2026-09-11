from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier


class ModelTuner:

    def __init__(self):
        self.best_models = {}
        self.best_params = {}
        self.cv_results = {}

    def tune_random_forest(self, X_train, y_train):

        model = RandomForestClassifier(
            random_state=42
        )

        param_distributions = {
            "n_estimators": [100, 200, 300],
            "max_depth": [4, 6, 8, 10, None],
            "max_features": ["sqrt", "log2"],
            "min_samples_split": [2, 5, 10],
            "min_samples_leaf": [1, 2, 4],
            "bootstrap": [True, False]
        }

        search = RandomizedSearchCV(
            estimator=model,
            param_distributions=param_distributions,
            n_iter=20,
            scoring="roc_auc",
            cv=5,
            random_state=42,
            n_jobs=-1,
            verbose=1
        )

        search.fit(X_train, y_train)

        self.best_models["random_forest"] = search.best_estimator_
        self.best_params["random_forest"] = search.best_params_
        self.cv_results["random_forest"] = search.cv_results_

        return search.best_estimator_

    def tune_xgboost(self, X_train, y_train):

        model = XGBClassifier(
            random_state=42,
            eval_metric="logloss"
        )

        param_distributions = {
            "n_estimators": [100, 300, 500, 800],
            "max_depth": [2, 3, 4, 5],
            "learning_rate": [0.01, 0.05, 0.1, 0.2],
            "subsample": [0.7, 0.8, 0.9, 1.0],
            "colsample_bytree": [0.7, 0.8, 0.9, 1.0],
            "min_child_weight": [1, 3, 5, 7]
        }

        search = RandomizedSearchCV(
            estimator=model,
            param_distributions=param_distributions,
            n_iter=25,
            scoring="roc_auc",
            cv=5,
            random_state=42,
            n_jobs=-1,
            verbose=1
        )

        search.fit(X_train, y_train)

        self.best_models["xgboost"] = search.best_estimator_
        self.best_params["xgboost"] = search.best_params_
        self.cv_results["xgboost"] = search.cv_results_

        return search.best_estimator_

    def get_best_parameters(self):

        return self.best_params