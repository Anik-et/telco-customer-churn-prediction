# 12. Project Finalization and GitHub Readiness

## 12.1 Objective

The goal of project finalization is to turn the working churn prediction project into a clean, reproducible, explainable, and interview-ready machine learning repository.

At this stage, the project should communicate three things clearly:

1. **Business value** — why predicting customer churn matters.
2. **Technical quality** — how data moves through validation, transformation, feature engineering, training, evaluation, explainability, and prediction.
3. **Production thinking** — how the model could be packaged, tested, deployed, monitored, and maintained.

The final repository should be understandable to another data scientist or hiring manager without requiring a walkthrough of the development process.

---

# 12.2 Final Project Scope

The project is a binary classification system for predicting whether a telecom customer is likely to churn.

### Business objective

Identify customers who have a high probability of churn so that retention teams can prioritize interventions such as:

- targeted offers
- discounts
- retention campaigns
- personalized communication
- service improvements

The model should therefore be treated as a **decision-support system**, not simply as a classifier that outputs `Yes` or `No`.

---

# 12.3 Final Repository Structure

A clean final structure can look like:

```text
02_Churn_Prediction/
│
├── config.yaml
├── requirements.txt
├── README.md
├── .gitignore
│
├── data/
│   ├── raw/
│   └── processed/
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
│   ├── 09_api_deployment_fastapi.md
│   ├── 10_testing_and_containerization.md
│   ├── 11_mlops_and_production_monitoring.md
│   └── 12_project_finalization_and_github.md
│
├── src/
│   ├── components/
│   │   ├── data_ingestion.py
│   │   ├── data_validation.py
│   │   ├── data_transformation.py
│   │   ├── feature_engineering.py
│   │   ├── model_trainer.py
│   │   ├── model_evaluator.py
│   │   └── shap_analyzer.py
│   │
│   └── utils/
│       └── config.py
│
├── tests/
│   ├── test_data_validation.py
│   ├── test_data_transformation.py
│   ├── test_feature_engineering.py
│   └── test_prediction_pipeline.py
│
├── artifacts/
│   ├── best_model.pkl
│   ├── preprocessor.pkl
│   ├── feature_names.pkl
│   └── shap_summary.png
│
└── predict_pipeline.py
```

The exact structure can evolve as the project grows. The important principle is separation of concerns:

- `data/` → datasets
- `src/` → reusable application/ML code
- `tests/` → automated tests
- `docs/` → technical documentation
- `artifacts/` → generated model outputs
- `config.yaml` → configurable parameters
- `predict_pipeline.py` → inference entry point

---

# 12.4 What Should Be Committed to Git?

The repository should contain the source code and documentation required to reproduce the project.

## Commit

Recommended:

```text
README.md
config.yaml
requirements.txt
.gitignore

src/
tests/
docs/

predict_pipeline.py
```

Depending on repository policy, small example assets or selected screenshots may also be committed.

## Do Not Commit

Avoid committing:

```text
data/raw/
data/processed/

.env
*.env
kaggle.json

__pycache__/
.ipynb_checkpoints/

artifacts/*.pkl
artifacts/*.joblib
artifacts/*.png
```

Generated model files can become large and are usually better handled through model registries or artifact storage in a production environment.

Raw datasets can also have licensing, privacy, or repository-size considerations.

---

# 12.5 Why `.gitignore` Matters

The `.gitignore` file prevents accidental commits of:

- secrets
- credentials
- raw datasets
- Python cache files
- notebook checkpoints
- generated model artifacts
- temporary files

A good `.gitignore` is part of engineering quality rather than merely a Git convenience.

Example:

```gitignore
# Python environments
venv/
.venv/
env/

# Python cache
__pycache__/
*.py[cod]

# Jupyter
.ipynb_checkpoints/

# Data
data/raw/
data/processed/

# Generated model artifacts
artifacts/*.pkl
artifacts/*.joblib
artifacts/*.png

# Secrets
.env
*.env
kaggle.json

# OS
.DS_Store
Thumbs.db
```

---

# 12.6 README Is the Main Project Entry Point

The README should be written for someone who sees the repository for the first time.

A good README should answer:

- What problem does this project solve?
- What data is used?
- What approach was taken?
- Which models were evaluated?
- Which model was selected?
- How well did it perform?
- How can someone run it?
- How can someone make a prediction?
- What are the limitations?
- What would be improved in a production system?

The README should not contain every implementation detail. Detailed explanations belong in `docs/`.

---

# 12.7 Recommended README Structure

Use this structure:

```markdown
# Telco Customer Churn Prediction

## Overview

## Business Problem

## Dataset

## Project Architecture

## EDA Highlights

## Feature Engineering

## Models Evaluated

## Model Results

## Explainability

## Prediction Pipeline

## Testing

## Setup

## Usage

## Limitations

## Future Improvements
```

---

# 12.8 Executive Summary for the README

A concise project summary can be:

> This project develops an end-to-end machine learning pipeline for predicting telecom customer churn. It includes data ingestion and validation, data transformation, feature engineering, model training and evaluation, SHAP-based explainability, automated testing, and a reusable prediction pipeline. Multiple classification algorithms were evaluated, with XGBoost selected based on held-out test ROC-AUC among the evaluated configurations.

This is preferable to saying simply:

> Built a churn prediction model.

The first version demonstrates the complete engineering lifecycle.

---

# 12.9 Business Problem

The README should explain the business problem before the technical solution.

Example:

> Customer churn directly affects recurring revenue and customer lifetime value. A retention team cannot manually investigate every customer, so the objective is to identify customers with a high likelihood of churn and prioritize them for intervention.

Then explain the business action:

```text
Customer Data
     |
     v
Churn Prediction
     |
     v
Churn Probability
     |
     v
Risk Prioritization
     |
     v
Retention Action
```

The important point is that the model supports a business decision.

---

# 12.10 Dataset

The project uses the IBM Telco Customer Churn dataset distributed through the Kaggle BlastChar dataset.

Dataset characteristics:

- customer-level telecom data
- approximately 7,000 customer records
- demographic information
- account information
- service information
- billing information
- churn target

Target:

```text
Churn
```

Values:

```text
Yes
No
```

The dataset is a historical customer-level snapshot rather than a transaction-level time series.

---

# 12.11 EDA Highlights

EDA should be summarized rather than dumping every chart into the README.

Important areas investigated include:

- target distribution
- tenure
- monthly charges
- total charges
- contract type
- internet service
- payment method
- customer demographics
- service adoption
- relationships between customer characteristics and churn

The key purpose of EDA is to identify patterns that can influence modeling and business interpretation.

Examples of useful business questions:

- Do month-to-month customers churn more?
- Does churn differ by tenure?
- Are higher monthly charges associated with greater churn?
- Does service adoption affect churn?
- Are electronic payment customers more likely to churn?

---

# 12.12 Data Quality Handling

The raw dataset contains a data-type issue involving `TotalCharges`.

Although the feature is conceptually numerical, some records contain blank values.

The transformation layer handles this using:

```python
pd.to_numeric(
    data["TotalCharges"],
    errors="coerce"
)
```

Invalid numeric values are converted to missing values and subsequently handled by the preprocessing pipeline.

This is an important example of separating:

```text
Raw data quality handling
        ↓
Transformation
        ↓
Feature preprocessing
        ↓
Model
```

---

# 12.13 Feature Engineering and Preprocessing

The preprocessing pipeline separates numerical and categorical features.

## Numerical features

Numerical variables are handled using:

```text
Median imputation
       ↓
StandardScaler
```

## Categorical features

Categorical variables are handled using:

```text
Most-frequent imputation
       ↓
OneHotEncoder
```

The encoder uses:

```python
handle_unknown="ignore"
```

This is important for inference because a new customer may contain a categorical value that was not present during training.

---

# 12.14 Preventing Train/Test Leakage

The preprocessing object is fitted only using training data.

Conceptually:

```text
Training Data
     |
     v
Fit Preprocessor
     |
     v
Transform Training Data
```

Then:

```text
Test Data
     |
     v
Use Existing Preprocessor
     |
     v
Transform Test Data
```

The test data must not be used to learn:

- scaling parameters
- imputation statistics
- categorical encoding mappings

This prevents information from the test set leaking into training.

---

# 12.15 Models Evaluated

Three classification approaches were evaluated:

1. Logistic Regression
2. Random Forest
3. XGBoost

They represent different modeling assumptions.

### Logistic Regression

Useful as an interpretable linear baseline.

### Random Forest

Useful for nonlinear relationships and feature interactions.

### XGBoost

Useful for structured/tabular data and nonlinear relationships with boosting.

The purpose of evaluating multiple models is not to assume that the most complex algorithm will always win.

---

# 12.16 Model Results

The current evaluation produced the following held-out test results:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8055 | 0.6572 | 0.5588 | 0.6040 | 0.8419 |
| Random Forest | 0.8020 | 0.6766 | 0.4866 | 0.5661 | 0.8425 |
| XGBoost | 0.8084 | 0.6757 | 0.5348 | 0.5970 | **0.8490** |

The XGBoost configuration achieved the strongest ROC-AUC among the evaluated models.

---

# 12.17 Why ROC-AUC Matters

Accuracy alone is not sufficient for this problem.

Churn datasets are commonly imbalanced, so a model could achieve reasonable accuracy while missing many churners.

ROC-AUC measures how well the model separates churners from non-churners across classification thresholds.

This is particularly useful when the business eventually wants to choose a probability threshold based on:

- retention budget
- intervention capacity
- cost of false positives
- cost of missed churners

Therefore, model evaluation should not stop at accuracy.

---

# 12.18 Precision vs Recall

The business interpretation is important.

### High precision

Means that customers predicted as churners are more likely to actually churn.

Useful when retention actions are expensive.

### High recall

Means that the system catches more actual churners.

Useful when missing a potential churner is expensive.

There is no universally correct threshold.

The optimal operating point should be determined using business costs and intervention capacity.

---

# 12.19 Final Model

The current project selects **XGBoost** based on the best held-out test ROC-AUC among the evaluated configurations.

Current test ROC-AUC:

```text
0.848963
```

The model is referred to as **configured XGBoost** because the production model uses the parameters supplied through `config.yaml`.

Current configuration:

```yaml
xgboost:
  n_estimators: 800
  max_depth: 3
  learning_rate: 0.01
  subsample: 0.7
  min_child_weight: 5
  colsample_bytree: 0.8
```

The distinction matters: these are not the untouched library defaults.

---

# 12.20 Important Model Selection Caveat

The project explored multiple configurations while evaluating performance on the same held-out test set.

Strict production methodology would ideally use:

```text
Training Set
     |
     +---- Cross-validation / tuning
     |
Validation Set
     |
     v
Model Selection
     |
     v
Final Model
     |
     v
Untouched Test Set
     |
     v
Final Performance Estimate
```

Repeatedly using the same test set for experimentation can indirectly cause test-set overfitting.

For a portfolio project this is an important limitation to acknowledge.

For a production-grade experiment, maintain a truly untouched final test set.

---

# 12.21 Hyperparameter Tuning

The project also explored Random Forest and XGBoost hyperparameters using cross-validation.

Examples of tuned parameters include:

Random Forest:

```text
n_estimators
max_depth
max_features
min_samples_split
min_samples_leaf
bootstrap
```

XGBoost:

```text
n_estimators
max_depth
learning_rate
subsample
min_child_weight
colsample_bytree
```

The tuning experiments demonstrate that:

> Hyperparameter tuning does not guarantee improvement over a strong existing configuration.

The correct approach is to compare candidates objectively and retain the model that performs best under the chosen evaluation methodology.

---

# 12.22 SHAP Explainability

The project uses SHAP to explain the tree-based model.

SHAP helps answer:

> Which features are driving the model's predictions?

The project generates:

```text
artifacts/shap_summary.png
```

The summary plot provides global feature importance and shows how feature values influence predictions.

Important distinction:

```text
Feature importance
        ≠
Causal relationship
```

A feature having high SHAP importance does not prove that changing that feature will cause churn to increase or decrease.

---

# 12.23 Feature Importance Findings

The Random Forest analysis showed strong contributions from variables such as:

- `TotalCharges`
- `tenure`
- `MonthlyCharges`
- contract type
- online security
- payment method
- technical support
- internet service

These results are useful for business discussion, but they should be interpreted as model associations rather than causal conclusions.

---

# 12.24 Prediction Pipeline

The reusable prediction pipeline is implemented in:

```text
predict_pipeline.py
```

It performs:

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
Saved Model
       |
       v
Prediction Probability
       |
       v
Risk Classification
```

The prediction response contains:

```python
{
    "churn_prediction": "Yes",
    "churn_probability": 0.7631,
    "risk_level": "High"
}
```

---

# 12.25 Risk Segmentation

The prediction pipeline converts model probability into business-friendly risk levels.

Current demonstration thresholds:

```text
Probability >= 0.70 → High
0.40 <= Probability < 0.70 → Medium
Probability < 0.40 → Low
```

These thresholds are business rules rather than outputs learned by the model.

In a real organization, thresholds should be optimized using:

- retention campaign capacity
- customer value
- intervention cost
- expected retained revenue
- false-positive cost
- false-negative cost

---

# 12.26 Deployment Architecture

The current project has a reusable inference pipeline.

A production deployment can expose it through an API layer such as FastAPI.

Conceptual architecture:

```text
Client / CRM / Retention System
              |
              v
        REST API
              |
              v
      Prediction Pipeline
              |
       +------+------+
       |             |
       v             v
 Preprocessor      Model
       |             |
       +------+------+
              |
              v
     Probability / Risk
```

The FastAPI and containerization documentation describes the production architecture and implementation approach.

Do not claim that a production API is implemented unless the corresponding application code actually exists in the repository.

---

# 12.27 Testing

The project includes automated tests covering:

- data validation
- data transformation
- feature engineering
- prediction pipeline

Current test result:

```text
4 passed, 0 warnings
```

Tests were executed with:

```bash
python -m pytest
```

This is important because it demonstrates that the core reusable components are not only written but also verified automatically.

---

# 12.28 Testing Philosophy

Tests should focus on behavior rather than implementation details.

Examples:

### Data validation

Check that:

- required columns are detected
- empty datasets are rejected
- duplicate counts are calculated
- missing values are reported
- data types are checked

### Transformation

Check that:

- `TotalCharges` becomes numeric
- `customerID` is removed

### Feature engineering

Check that:

- preprocessing can be fitted
- transformed features are generated
- feature names are available
- unknown categorical values do not break transformation

### Prediction

Check that:

- a prediction is returned
- probability is within `[0, 1]`
- risk classification is returned

---

# 12.29 Configuration Management

Model parameters and operational thresholds are stored in:

```text
config.yaml
```

This avoids hard-coding every configurable value in Python.

Configuration currently includes:

- data path
- required columns
- expected data types
- model parameters
- artifact paths
- SHAP output path
- risk thresholds

This makes experimentation easier and improves maintainability.

---

# 12.30 Reproducibility

The project should make it possible for another developer to recreate the environment.

Recommended setup:

```bash
python -m venv .venv
```

Activate the environment and install dependencies:

```bash
python -m pip install -r requirements.txt
```

Run tests:

```bash
python -m pytest
```

Run the inference example:

```bash
python predict_pipeline.py
```

The exact commands should be updated in the README to match the final repository entry points.

---

# 12.31 Requirements File

The repository should contain a `requirements.txt` file containing the libraries actually required by the project.

Typical dependencies include:

```text
pandas
numpy
scikit-learn
xgboost
shap
matplotlib
pyyaml
joblib
pytest
```

The exact versions should reflect the environment used for the final project.

Pinning versions improves reproducibility, especially for libraries whose APIs can change between releases.

---

# 12.32 Artifact Management

The project produces artifacts such as:

```text
best_model.pkl
preprocessor.pkl
feature_names.pkl
shap_summary.png
```

These artifacts are useful locally for inference and explainability.

However, production systems should generally use dedicated artifact/model storage rather than relying on manually committed binary files.

Possible production solutions include:

- object storage
- model registries
- experiment tracking platforms
- CI/CD artifact stores

The repository should document where the model artifact comes from and how it is generated.

---

# 12.33 Security Checklist

Before pushing the project publicly, verify:

```text
[ ] No API keys
[ ] No passwords
[ ] No tokens
[ ] No .env files
[ ] No cloud credentials
[ ] No kaggle.json
[ ] No private customer data
[ ] No sensitive logs
[ ] No accidentally committed datasets
```

A public GitHub repository should be treated as fully public.

---

# 12.34 Git Workflow

A clean workflow is:

```text
Create feature branch
        |
        v
Implement change
        |
        v
Run tests
        |
        v
Review git diff
        |
        v
Commit
        |
        v
Push branch
        |
        v
Open Pull Request
        |
        v
Review
        |
        v
Merge
```

Useful commands:

```bash
git status
git diff
git add .
git commit -m "Add churn prediction pipeline"
git push
```

For feature work:

```bash
git checkout -b feature/churn-modeling
```

Use descriptive commit messages.

Examples:

```text
Add churn data validation
Add preprocessing pipeline
Add model evaluation
Add SHAP explainability
Add prediction pipeline
Add automated tests
Update project documentation
```

Do not claim a pull request was merged unless GitHub confirms it.

---

# 12.35 GitHub Repository Quality

A strong GitHub project should make the repository understandable within a few minutes.

The landing page should show:

```text
Project title
     ↓
Business problem
     ↓
Approach
     ↓
Results
     ↓
Architecture
     ↓
How to run
     ↓
Limitations
     ↓
Future work
```

The repository should look intentional rather than like a collection of notebook experiments.

---

# 12.36 Portfolio Presentation

When presenting this project in an interview or portfolio, emphasize the complete lifecycle.

Do not start with:

> I trained an XGBoost model.

Instead say:

> I built an end-to-end customer churn prediction pipeline, starting with business understanding and data validation, followed by EDA, preprocessing, feature engineering, model comparison, explainability, testing, and a reusable inference pipeline.

Then explain the business objective.

Then discuss model selection.

Then discuss deployment and monitoring considerations.

This demonstrates engineering maturity.

---

# 12.37 One-Minute Interview Pitch

A concise explanation:

> I built an end-to-end telecom customer churn prediction system to identify customers who are likely to leave and help prioritize retention efforts. I started by understanding the business problem and validating the raw data, including handling the `TotalCharges` data-quality issue. I built separate preprocessing pipelines for numerical and categorical features, evaluated Logistic Regression, Random Forest, and XGBoost, and selected the XGBoost configuration based on held-out ROC-AUC. I also used SHAP for model explainability and built a reusable prediction pipeline that returns churn probability and business-oriented risk levels. Finally, I added automated tests and documented how the solution could be exposed through an API and monitored in production.

This is a much stronger interview answer than focusing only on the algorithm.

---

# 12.38 Two-Minute Technical Explanation

If the interviewer asks for more detail:

```text
Raw CSV
   |
   v
Data Ingestion
   |
   v
Data Validation
   |
   v
Data Transformation
   |
   v
Feature Engineering
   |
   v
Train/Test Split
   |
   +------------------------------+
   |              |               |
   v              v               v
Logistic       Random Forest     XGBoost
Regression
   |              |               |
   +--------------+---------------+
                  |
                  v
            Model Evaluation
                  |
                  v
             Model Selection
                  |
                  v
              SHAP Analysis
                  |
                  v
            Save Model + Pipeline
                  |
                  v
           Prediction Pipeline
                  |
                  v
       Probability + Risk Level
```

Then discuss deployment as the next production layer.

---

# 12.39 Common Interview Questions

## Why did you choose ROC-AUC?

Because the target is imbalanced and the business may operate at different classification thresholds. ROC-AUC evaluates ranking/separation performance across thresholds rather than relying on one fixed threshold.

## Why not accuracy?

Accuracy can hide poor performance on the minority churn class.

## Why compare multiple algorithms?

Different models capture different relationships. A simpler model can sometimes outperform a more complex one, so model choice should be evidence-driven.

## Why XGBoost?

It performed best on the selected evaluation criterion among the evaluated configurations and is well suited to structured/tabular data.

## Why use SHAP?

To understand which features influence predictions and improve model transparency.

## Why save the preprocessor?

The exact preprocessing applied during training must also be applied during inference.

## Why use `handle_unknown="ignore"`?

To prevent inference from failing when new categorical values appear.

## Why use a pipeline?

To make preprocessing and inference reproducible and reduce the risk of applying transformations inconsistently.

## How would you deploy this?

Package the inference code behind an API, containerize it, deploy it to infrastructure, and add monitoring for service health and model/data drift.

## How would you monitor the model?

Monitor:

- request latency
- error rate
- prediction distribution
- feature distributions
- missing-value rates
- drift
- eventual model performance when labels become available

## What would you improve?

Use an untouched final test set, optimize the classification threshold against business costs, add stronger experiment tracking, containerize the service, automate CI/CD, and implement production monitoring.

---

# 12.40 Production Improvements

A production-grade version could add:

### Data pipeline

```text
Scheduled ingestion
        ↓
Data quality checks
        ↓
Feature pipeline
```

### Training pipeline

```text
Validated dataset
        ↓
Train
        ↓
Cross-validation
        ↓
Model selection
        ↓
Model registry
```

### Deployment

```text
Registered model
        ↓
Container
        ↓
API
        ↓
Cloud infrastructure
```

### Monitoring

```text
Application metrics
+
Data drift
+
Prediction drift
+
Model performance
```

---

# 12.41 Future Improvements

Good future improvements include:

1. Business-cost-based threshold optimization.
2. Precision-recall analysis.
3. Calibration analysis.
4. Stratified cross-validation.
5. An untouched final test set.
6. Experiment tracking.
7. Model registry.
8. FastAPI implementation.
9. Docker containerization.
10. CI/CD pipeline.
11. Data drift monitoring.
12. Model performance monitoring.
13. Automated retraining.
14. Cloud deployment.
15. Customer lifetime value integration.

The goal is not to implement every possible technology immediately.

A strong engineering project should evolve incrementally.

---

# 12.42 What Not to Overclaim

Interview credibility is more important than making the project sound artificially advanced.

Do not say:

> The model is production-ready.

unless it actually has production infrastructure, monitoring, security, deployment, and operational ownership.

Prefer:

> The project contains a reusable inference pipeline and documents the architecture required for production deployment.

Similarly, do not say:

> The model proves that month-to-month contracts cause churn.

Instead:

> The model identifies contract type as an important predictive feature.

Do not claim:

> Hyperparameter tuning improved the model.

unless the final selected metric actually improved relative to the relevant baseline.

---

# 12.43 Final Quality Checklist

Before calling the project complete:

## Code

```text
[ ] Code is formatted
[ ] No unnecessary debugging statements
[ ] Functions have clear names
[ ] Classes have clear responsibilities
[ ] No duplicated logic
[ ] Configuration is separated from code
```

## Data

```text
[ ] Raw data is not committed
[ ] Data validation exists
[ ] Missing values are handled
[ ] Data-type issues are handled
```

## ML

```text
[ ] Train/test split is correct
[ ] Preprocessor is fitted only on training data
[ ] Multiple models evaluated
[ ] Appropriate metrics reported
[ ] Final model documented
[ ] Model limitations documented
```

## Explainability

```text
[ ] SHAP analysis generated
[ ] Feature importance interpreted carefully
[ ] No causal claims from feature importance
```

## Testing

```text
[ ] Tests exist
[ ] python -m pytest passes
[ ] Current result: 4 passed, 0 warnings
```

## Deployment

```text
[ ] Prediction pipeline works
[ ] Model artifact can be loaded
[ ] Preprocessor artifact can be loaded
[ ] Deployment architecture documented
```

## GitHub

```text
[ ] README is complete
[ ] .gitignore is correct
[ ] No secrets committed
[ ] No raw data committed
[ ] Commit history is understandable
[ ] Repository structure is clean
```

---

# 12.44 Final Project Definition

At completion, the project can be described as:

> **An end-to-end, explainable customer churn prediction system for structured telecom data, including data validation, preprocessing, feature engineering, model comparison, XGBoost-based prediction, SHAP explainability, automated testing, configurable inference, and production deployment/monitoring design.**

That is the level at which the project should be presented on GitHub and in interviews.

---

# 12.45 Final Takeaway

The most important lesson from this project is not XGBoost itself.

The real learning is the complete ML lifecycle:

```text
Business Problem
      ↓
Data Understanding
      ↓
Data Quality
      ↓
EDA
      ↓
Feature Engineering
      ↓
Modeling
      ↓
Evaluation
      ↓
Explainability
      ↓
Inference
      ↓
Testing
      ↓
Deployment
      ↓
Monitoring
      ↓
Iteration
```

A machine learning model is only one component of a real ML system.

The ability to connect business requirements, data quality, modeling, evaluation, software engineering, deployment, and monitoring is what makes the project valuable for a professional data science or ML engineering role.
