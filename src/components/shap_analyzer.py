import shap
import matplotlib.pyplot as plt


class SHAPAnalyzer:

    def __init__(self):
        self.explainer = None
        self.shap_values = None

    def calculate_shap_values(self, model, X):

        self.explainer = shap.TreeExplainer(model)

        self.shap_values = self.explainer.shap_values(X)

        return self.shap_values

    def plot_summary(
        self,
        X,
        feature_names,
        output_path=None
    ):

        shap_values = self.shap_values

        # Handle binary classification output
        # from SHAP versions returning:
        # (samples, features, classes)
        if len(shap_values.shape) == 3:
            shap_values = shap_values[:, :, 1]

        shap.summary_plot(
            shap_values,
            X,
            feature_names=feature_names,
            show=False
        )

        plt.tight_layout()

        if output_path:
            plt.savefig(
                output_path,
                bbox_inches="tight"
            )

       # plt.show() -- for showing when running the script directly, but not in a pipeline context
        plt.close()