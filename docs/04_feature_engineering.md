# Feature Engineering and Preprocessing

## 1. Objective

Feature engineering and preprocessing convert the raw customer dataset into a numerical representation that can be consumed by machine learning algorithms.

The main objectives are:

- Clean raw feature values.
- Handle invalid and missing values.
- Separate numerical and categorical features.
- Transform categorical variables into numerical representations.
- Scale numerical features where appropriate.
- Maintain a consistent transformation process between training and inference.
- Prevent data leakage.
- Create a reusable preprocessing pipeline.

The preprocessing logic is implemented in:

```text
src/components/data_transformation.py
src/components/feature_engineering.py