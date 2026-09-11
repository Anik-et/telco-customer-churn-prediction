# 📊 Telco Customer Churn Prediction

An end-to-end machine learning project that predicts telecom customer churn probability and converts the prediction into actionable business risk levels.

> 🎯 **Goal:** Identify customers who are likely to churn so that retention teams can prioritize customers for targeted interventions.

## 🚀 Live Demo

**Streamlit App:** `https://data-science-lab-tikxuebprgc6bxhvbqjcmk.streamlit.app/`

The application provides an interactive interface where a user can enter customer, service, contract, and billing information and receive:

- Churn prediction
- Churn probability
- Business risk level
- Retention-oriented interpretation

---

## 📌 Project Overview

Customer churn is a major business problem for subscription-based companies. Losing customers affects recurring revenue and customer lifetime value, while acquiring replacement customers can be expensive.

This project builds a complete machine learning workflow to predict whether a telecom customer is likely to churn.

The project goes beyond model training and includes:

- Business understanding
- Data validation
- Exploratory Data Analysis (EDA)
- Data transformation
- Feature engineering
- Multiple model comparison
- Hyperparameter tuning
- Model evaluation
- SHAP explainability
- Reusable prediction pipeline
- Automated testing
- Streamlit deployment
- Production deployment and monitoring design

The final application is publicly deployable through Streamlit Community Cloud.

---

# 🏗️ Project Architecture

```text
                         Raw Customer Data
                                |
                                v
                       +------------------+
                       | Data Ingestion   |
                       +--------+---------+
                                |
                                v
                       +------------------+
                       | Data Validation  |
                       +--------+---------+
                                |
                                v
                       +------------------+
                       | Transformation   |
                       +--------+---------+
                                |
                                v
                       +------------------+
                       | Feature          |
                       | Engineering      |
                       +--------+---------+
                                |
                                v
                       +------------------+
                       | Train / Test     |
                       | Split            |
                       +--------+---------+
                                |
              +-----------------+-----------------+
              |                 |                 |
              v                 v                 v
       Logistic Regression  Random Forest     XGBoost
              |                 |                 |
              +-----------------+-----------------+
                                |
                                v
                       Model Evaluation
                                |
                                v
                       Model Selection
                                |
                       +--------+--------+
                       |                 |
                       v                 v
                 SHAP Analysis    Saved Model
                                         |
                                         v
                                Prediction Pipeline
                                         |
                                         v
                                  Streamlit App
                                         |
                                         v
                              Churn Probability
                                         |
                                         v
                                  Risk Level
```

---

# 🎯 Business Problem

The business wants to identify customers who have a high likelihood of leaving the telecom service.

A retention team has limited time and budget, so it is not practical to treat every customer equally.

The model therefore provides a **risk score** that can be used to prioritize customers.

For example:

```text
Customer
   |
   v
Churn Probability
   |
   +---- < 40% ------> Low Risk
   |
   +---- 40–70% -----> Medium Risk
   |
   +---- >= 70% -----> High Risk
```

These thresholds are business rules defined in `config.yaml`. They are not parameters learned by the model.

A production implementation should optimize these thresholds based on retention cost, customer value, intervention capacity, and the cost of false positives and false negatives.

---

# 📦 Dataset

The project uses the **IBM Telco Customer Churn** dataset distributed through the Kaggle BlastChar dataset.

Dataset source:

`https://www.kaggle.com/datasets/blastchar/telco-customer-churn`

The dataset contains approximately **7,043 customer records** and includes information about:

- Customer demographics
- Account information
- Telecom services
- Contract type
- Payment method
- Monthly charges
- Total charges
- Churn status

### Target Variable

```text
Churn
```

Possible values:

```text
Yes
No
```

The dataset is a customer-level historical snapshot rather than a transaction-level time series.

---

# 🔍 Exploratory Data Analysis

EDA was performed to understand the structure of the dataset and identify patterns associated with churn.

Key areas investigated include:

- Churn distribution
- Customer tenure
- Monthly charges
- Total charges
- Contract type
- Internet service
- Payment method
- Customer demographics
- Service adoption
- Billing characteristics

Important business questions included:

- Are month-to-month customers more likely to churn?
- Does churn vary with customer tenure?
- Are higher monthly charges associated with churn?
- Do customers without additional services have higher churn?
- Does payment method relate to churn behavior?

EDA was used to guide preprocessing, feature engineering, model selection, and business interpretation.

---

# 🧹 Data Quality and Transformation

One important data-quality issue was identified in the `TotalCharges` feature.

Although `TotalCharges` is conceptually numerical, some records contain blank values.

The transformation layer converts the column using:

```python
pd.to_numeric(
    data["TotalCharges"],
    errors="coerce"
)
```

Invalid numeric values are converted to missing values and subsequently handled by the preprocessing pipeline.

The `customerID` column is removed because it is an identifier rather than a useful predictive feature.

---

# ⚙️ Feature Engineering and Preprocessing

The preprocessing pipeline treats numerical and categorical variables separately.

## Numerical Features

```text
Missing values
      ↓
Median Imputation
      ↓
StandardScaler
```

## Categorical Features

```text
Missing values
      ↓
Most-Frequent Imputation
      ↓
One-Hot Encoding
```

The categorical encoder uses:

```python
handle_unknown="ignore"
```

This allows the prediction pipeline to handle previously unseen categorical values without failing during inference.

---

# 🔒 Data Leakage Prevention

The preprocessing pipeline is fitted only on the training data.

```text
Training Data
     |
     v
Fit Preprocessor
     |
     v
Transform Training Data
```

The test data is transformed using the already-fitted preprocessing object.

This prevents information from the test set from influencing learned preprocessing parameters such as imputation statistics, scaling parameters, and categorical encoding mappings.

---

# 🤖 Models Evaluated

Three classification algorithms were evaluated:

### 1. Logistic Regression

Used as an interpretable linear baseline.

### 2. Random Forest

Used to capture nonlinear relationships and feature interactions.

### 3. XGBoost

Used as a gradient-boosted tree model well suited to structured/tabular data.

The objective was to compare different modeling approaches rather than assume that the most complex algorithm would automatically perform best.

---

# 📈 Model Performance

The following results are from the held-out test set used during the project evaluation.

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 80.55% | 65.72% | 55.88% | 60.40% | 84.19% |
| Random Forest | 80.20% | 67.66% | 48.66% | 56.61% | 84.25% |
| XGBoost | **80.84%** | **67.57%** | 53.48% | 59.70% | **84.90%** |

### Selected Model

**Configured XGBoost**

Test ROC-AUC:

```text
0.848963
```

XGBoost achieved the strongest ROC-AUC among the evaluated configurations.

---

# 🧠 Why ROC-AUC?

Accuracy alone is not sufficient for this problem because churn is not evenly distributed across customers.

ROC-AUC evaluates how well the model separates churners from non-churners across different classification thresholds.

This is useful because the business may later choose a threshold based on retention budget, intervention capacity, customer value, cost of contacting customers, and cost of missing actual churners.

The final production threshold should therefore be selected based on business economics rather than model accuracy alone.

---

# 🎛️ XGBoost Configuration

The current production configuration is defined in `config.yaml`:

```yaml
xgboost:
  n_estimators: 800
  max_depth: 3
  learning_rate: 0.01
  subsample: 0.7
  min_child_weight: 5
  colsample_bytree: 0.8
```

The term **configured XGBoost** is used intentionally because the deployed model uses these explicitly configured parameters rather than the untouched library defaults.

---

# 🔬 Hyperparameter Tuning

Randomized hyperparameter search with cross-validation was used to explore Random Forest and XGBoost configurations.

Random Forest parameters explored included:

```text
n_estimators
max_depth
max_features
min_samples_split
min_samples_leaf
bootstrap
```

XGBoost parameters explored included:

```text
n_estimators
max_depth
learning_rate
subsample
min_child_weight
colsample_bytree
```

An important lesson from the experiments was:

> Hyperparameter tuning does not guarantee improvement over an already strong configuration.

Model selection should therefore be evidence-driven.

---

# 🧠 Model Explainability with SHAP

SHAP was used to provide model explainability for the tree-based model.

The analysis helps answer:

> Which features have the strongest influence on the model's churn predictions?

The project generates:

```text
artifacts/shap_summary.png
```

Important predictive features observed during model analysis include variables such as:

- `TotalCharges`
- `tenure`
- `MonthlyCharges`
- Contract type
- Online security
- Payment method
- Technical support
- Internet service

These should be interpreted as **predictive associations**, not causal relationships.

For example:

> A feature having high SHAP importance does not prove that changing that feature will cause churn behavior to change.

---

# 🔮 Prediction Pipeline

The reusable inference pipeline is implemented in:

```text
src/pipeline/predict_pipeline.py
```

The pipeline performs:

```text
Raw Customer Data
       |
       v
Data Transformation
       |
       v
Saved Preprocessor
       |
       v
Saved XGBoost Model
       |
       v
Churn Prediction
       |
       v
Churn Probability
       |
       v
Risk Level
```

Example output:

```python
{
    "churn_prediction": "Yes",
    "churn_probability": 0.7631,
    "risk_level": "High"
}
```

---

# 🌐 Streamlit Application

The interactive application is implemented in:

```text
app.py
```

The application allows users to enter customer information and receive an immediate prediction.

Example:

```text
Churn Probability: 76.31%

Prediction: Likely to Churn

Risk Level: High
```

The application uses the same saved preprocessing and model artifacts as the prediction pipeline.

This avoids duplicating ML logic between the model and the user interface.

---

# 🚦 Risk Classification

Current thresholds:

| Probability | Risk Level | Business Interpretation |
|---:|---|---|
| < 40% | Low | No immediate intervention indicated |
| 40% – <70% | Medium | Consider targeted engagement |
| ≥ 70% | High | Prioritize for retention action |

These thresholds are configured in `config.yaml`:

```yaml
prediction:
  high_risk_threshold: 0.70
  medium_risk_threshold: 0.40
```

The thresholds are business rules and should eventually be optimized using business cost/benefit analysis.

---

# 🧪 Testing

The project includes automated tests for the main reusable components.

Current test coverage includes:

- Data validation
- Data transformation
- Feature engineering
- Prediction pipeline

Tests are executed using:

```bash
python -m pytest
```

Current result:

```text
4 passed, 0 warnings
```

Testing verifies that the core components continue to behave correctly as the project evolves.

---

# 📁 Project Structure

```text
02_Churn_Prediction/
│
├── app.py
├── config.yaml
├── requirements.txt
├── README.md
│
├── data/
│   ├── raw/
│   └── processed/
│
├── artifacts/
│   ├── best_model.pkl
│   ├── feature_names.pkl
│   └── preprocessor.pkl
│
├── docs/
│   ├── 01_business_understanding.md
│   ├── 02_data_understanding.md
│   ├── 03_eda.md
│   ├── 04_feature_engineering.md
│   ├── 05_modeling.md
│   ├── 06_model_evaluation.md
│   ├── 07_shap_explainability.md
│   ├── 08_model_deployment.md
│   ├── 09_API_deployed_with_FastAPI.md
│   ├── 10_testing_and_containerization.md
│   ├── 11_mlops_and_production_monitoring.md
│   └── 12_project_finalization_and_github.md
│
├── notebooks/
│   └── Customer_Churn_EDA.ipynb
│
├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── feature_engineering.py
│   │   ├── model_trainer.py
│   │   ├── model_evaluator.py
│   │   ├── model_tuner.py
│   │   └── shap_analyzer.py
│   │
│   ├── pipeline/
│   │   ├── train_pipeline.py
│   │   └── predict_pipeline.py
│   │
│   └── utils/
│       └── config.py
│
└── tests/
    ├── test_data_validation.py
    ├── test_data_transformation.py
    ├── test_feature_engineering.py
    └── test_prediction_pipeline.py
```

---

# 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Language | Python |
| Data Processing | Pandas, NumPy |
| Visualization | Matplotlib |
| Machine Learning | Scikit-learn |
| Gradient Boosting | XGBoost |
| Explainability | SHAP |
| Model Persistence | Joblib |
| Configuration | YAML |
| Testing | Pytest |
| Web Application | Streamlit |
| Version Control | Git / GitHub |

---

# ⚙️ Local Setup

## 1. Clone the repository

```bash
git clone https://github.com/Anik-et/Data-Science-Lab.git
```

Move to the churn prediction project:

```bash
cd Data-Science-Lab/projects/02_Churn_Prediction
```

## 2. Create a virtual environment

Windows:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.venv\Scripts\activate
```

## 3. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

## 4. Run tests

```powershell
python -m pytest
```

## 5. Run the Streamlit application

```powershell
python -m streamlit run app.py
```

The application will normally be available at:

```text
http://localhost:8501
```

---

# ▶️ Using the Application

1. Open the Streamlit application.
2. Enter customer information.
3. Enter service and account information.
4. Enter billing information.
5. Click **Predict Churn Risk**.
6. Review:
   - Churn probability
   - Churn prediction
   - Risk level
7. Use the result to understand how the customer would be prioritized by a retention workflow.

---

# ☁️ Deployment

The application is deployed using **Streamlit Community Cloud**.

Deployment architecture:

```text
GitHub Repository
       |
       v
Streamlit Community Cloud
       |
       v
app.py
       |
       v
Prediction Pipeline
       |
       +--------------------+
       |                    |
       v                    v
Preprocessor          XGBoost Model
       |                    |
       +---------+----------+
                 |
                 v
        Prediction Result
                 |
                 v
          Risk Classification
```

The deployed application uses the model artifacts stored with the project.

The deployment environment installs the dependencies defined in `requirements.txt`.

---

# 🔄 Production Deployment Architecture

The current application demonstrates the model through Streamlit.

A more production-oriented architecture could expose the prediction pipeline through an API:

```text
CRM / Internal Application
            |
            v
        REST API
            |
            v
    Prediction Service
            |
      +-----+-----+
      |           |
      v           v
Preprocessor    XGBoost
      |           |
      +-----+-----+
            |
            v
 Churn Probability
            |
            v
     Risk Classification
```

FastAPI and Docker are documented as possible production extensions.

The current project should distinguish between components that are implemented and components that are architectural extensions.

---

# 🔁 CI/CD and Production Monitoring

A production version of this project could add:

### Continuous Integration

```text
Git Push
   |
   v
GitHub Actions
   |
   v
Install Dependencies
   |
   v
Run Tests
   |
   v
Build / Deployment Validation
```

### Monitoring

Monitor:

- API availability
- Request latency
- Error rate
- Prediction distribution
- Input feature distributions
- Missing-value rates
- Data drift
- Prediction drift
- Model performance after labels become available

### Retraining

A mature production workflow could trigger retraining when:

- Data drift becomes significant
- Model performance deteriorates
- Business behavior changes
- Sufficient new labeled data becomes available

---

# ⚠️ Limitations

This is a portfolio/project implementation rather than a production system operating on live telecom infrastructure.

Important limitations include:

### 1. Historical Dataset

The dataset is a historical customer snapshot rather than a continuously updated production data stream.

### 2. No Real-Time Customer Data

The deployed application uses manually entered customer information.

### 3. Business Thresholds

The current 40% and 70% thresholds are demonstration/business rules and have not been optimized using actual retention economics.

### 4. Test Set Reuse During Experimentation

Multiple model experiments were evaluated during development. Repeated experimentation against the same held-out test set can introduce indirect test-set overfitting.

A stricter production experiment would maintain an untouched final test set.

### 5. No Causal Inference

The model identifies predictive relationships. It does not establish that changing a feature will cause churn behavior to change.

### 6. No Production Monitoring

The current project documents monitoring architecture but does not represent a mature production monitoring platform.

---

# 🚀 Future Improvements

Potential improvements include:

1. Optimize prediction thresholds using business costs.
2. Add precision-recall analysis.
3. Perform probability calibration.
4. Maintain an untouched final test set.
5. Add experiment tracking.
6. Add model versioning/model registry.
7. Add GitHub Actions CI.
8. Add FastAPI inference service.
9. Add Docker containerization.
10. Deploy the API independently.
11. Add data drift monitoring.
12. Add model performance monitoring.
13. Implement automated retraining.
14. Integrate customer lifetime value.
15. Add retention campaign outcome tracking.

---

# 💼 Business Use Case Extension

A future production workflow could combine churn probability with customer value:

```text
Churn Probability
        +
Customer Lifetime Value
        +
Retention Cost
        |
        v
Expected Retention Value
        |
        v
Prioritized Retention Queue
```

This would be more valuable than simply targeting every customer with a high predicted churn probability.

For example:

```text
High Churn + High Customer Value
        ↓
Highest Priority
```

while:

```text
High Churn + Low Customer Value
        ↓
Potentially Lower Priority
```

The final business decision should depend on the economics of the retention strategy.

---

# 🎤 Summary

### One-minute explanation

> I built an end-to-end telecom customer churn prediction system to identify customers who are likely to leave and help prioritize retention efforts. I started with business understanding and data validation, handled data-quality issues such as the `TotalCharges` field, built separate preprocessing pipelines for numerical and categorical features, and compared Logistic Regression, Random Forest, and XGBoost. XGBoost achieved the strongest ROC-AUC among the evaluated configurations. I then added SHAP explainability, a reusable prediction pipeline, automated tests, and an interactive Streamlit application deployed publicly. I also documented how the system could be extended with CI/CD, FastAPI, Docker, and production monitoring.

### Key technical topics demonstrated

```text
Python
Pandas
Scikit-learn
XGBoost
Feature Engineering
Cross-validation
Hyperparameter Tuning
ROC-AUC
SHAP
Model Serialization
Prediction Pipelines
Streamlit
Pytest
Git/GitHub
Deployment
MLOps Concepts
```

---

# 📚 Project Documentation

Detailed documentation is available in the `docs/` directory.

| Document | Description |
|---|---|
| `01_business_understanding.md` | Business problem, stakeholders, objectives |
| `02_data_understanding.md` | Dataset structure and data quality |
| `03_eda.md` | Exploratory Data Analysis |
| `04_feature_engineering.md` | Transformation and preprocessing |
| `05_modeling.md` | Algorithms and modeling strategy |
| `06_model_evaluation.md` | Metrics and model comparison |
| `07_shap_explainability.md` | SHAP explainability |
| `08_model_deployment.md` | Deployment concepts |
| `09_API_deployed_with_FastAPI.md` | API deployment concepts |
| `10_testing_and_containerization.md` | Testing and containerization |
| `11_mlops_and_production_monitoring.md` | MLOps and monitoring |
| `12_project_finalization_and_github.md` | Finalization and GitHub readiness |

---

# 👤 Author

**Aniket Mali**

Data Science / Machine Learning Portfolio Project

GitHub:

`https://github.com/Anik-et/Data-Science-Lab`

---

# 📄 License

### Project Code

The original source code in this project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for the full license text.

### Dataset

This project uses the **Telco Customer Churn** dataset distributed through the Kaggle BlastChar dataset. The dataset page identifies the data files as © Original Authors. The dataset is therefore treated separately from the project's original source code and documentation.

Dataset source:

[Kaggle — Telco Customer Churn Dataset](https://www.kaggle.com/datasets/blastchar/telco-customer-churn?utm_source=chatgpt.com)

The dataset's original licensing and usage terms should be followed independently when using or redistributing the data.

### Third-Party Dependencies

This project uses open-source Python libraries including Pandas, NumPy, Scikit-learn, XGBoost, SHAP, Streamlit, PyYAML, Joblib, and Pytest. Each dependency remains subject to its respective license.

