# Data Understanding

## 1. Dataset Overview

The project uses the IBM Telco Customer Churn dataset.

The dataset contains customer-level information related to:

- Demographics
- Account information
- Services subscribed
- Billing information
- Customer tenure
- Churn status

Dataset dimensions:

- Rows: 7,043
- Columns: 21

---

## 2. Target Variable

The target variable is:

`Churn`

It indicates whether a customer has left the company.

Values:

- `Yes` — customer churned
- `No` — customer did not churn

This makes the problem a binary classification task.

---

## 3. Feature Categories

### Customer Demographics

- `gender`
- `SeniorCitizen`
- `Partner`
- `Dependents`

### Customer Account Information

- `customerID`
- `tenure`
- `Contract`
- `PaperlessBilling`
- `PaymentMethod`

### Services

- `PhoneService`
- `MultipleLines`
- `InternetService`
- `OnlineSecurity`
- `OnlineBackup`
- `DeviceProtection`
- `TechSupport`
- `StreamingTV`
- `StreamingMovies`

### Billing

- `MonthlyCharges`
- `TotalCharges`

---

## 4. Data Types

The dataset contains both numerical and categorical features.

### Numerical Features

- `SeniorCitizen`
- `tenure`
- `MonthlyCharges`
- `TotalCharges`

### Categorical Features

The remaining customer attributes are categorical.

The `customerID` column is an identifier rather than a predictive customer characteristic and is removed before modelling.

---

## 5. Initial Data Quality Checks

The data validation component performs the following checks:

- Dataset is not empty
- Required columns are present
- Duplicate rows
- Missing values
- Expected data types

Validation results:

| Check | Result |
|---|---|
| Required columns missing | 0 |
| Duplicate rows | 0 |
| Missing values | 0 |
| Data type issues | `TotalCharges` |

---

## 6. TotalCharges Data Quality Issue

`TotalCharges` was initially detected as a string/object column rather than a numerical column.

The issue occurs because some records contain blank values.

Instead of treating these blank values as valid numerical values, the transformation pipeline converts the column using:

```python
pd.to_numeric(
    data["TotalCharges"],
    errors="coerce"
)