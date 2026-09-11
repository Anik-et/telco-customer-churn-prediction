import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    classification_report
)


class ModelEvaluator:

    def __init__(self):
        self.results = []

    def evaluate_model(
        self,
        model_name,
        model,
        X_test,
        y_test
    ):

        y_pred = model.predict(X_test)

        y_probability = model.predict_proba(X_test)[:, 1]

        results = {
            "Model": model_name,
            "Accuracy": accuracy_score(y_test, y_pred),
            "Precision": precision_score(y_test, y_pred),
            "Recall": recall_score(y_test, y_pred),
            "F1": f1_score(y_test, y_pred),
            "ROC-AUC": roc_auc_score(
                y_test,
                y_probability
            )
        }

        self.results.append(results)

        return results


    def evaluate_all(
        self,
        models,
        X_test,
        y_test
    ):

        self.results = []

        for model_name, model in models.items():
            self.evaluate_model(
                model_name,
                model,
                X_test,
                y_test
            )

        return pd.DataFrame(self.results)

    def get_confusion_matrix(
        self,
        model,
        X_test,
        y_test
    ):

        y_pred = model.predict(X_test)

        return confusion_matrix(
            y_test,
            y_pred
        )

    def get_classification_report(
        self,
        model,
        X_test,
        y_test
    ):

        y_pred = model.predict(X_test)

        return classification_report(
            y_test,
            y_pred
        )