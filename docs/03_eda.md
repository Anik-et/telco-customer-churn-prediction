# Exploratory Data Analysis

## 1. Objective

The objective of exploratory data analysis (EDA) is to understand:

- Customer churn distribution
- Customer characteristics associated with churn
- Service and contract patterns
- Billing-related patterns
- Tenure-related patterns
- Potential relationships that may help predict churn

EDA is used to understand the business problem and guide feature preparation and model development.

---

## 2. Churn Distribution

The target variable `Churn` contains two classes:

- `Yes` — customer churned
- `No` — customer did not churn

The dataset is imbalanced, with non-churned customers representing the majority of observations.

This is important because a model could achieve relatively high accuracy by favoring the majority class while still performing poorly at identifying customers who actually churn.

Therefore, model evaluation should not rely on accuracy alone.

---

## 3. Tenure and Churn

Customer tenure is an important variable for churn prediction.

Customers with shorter tenure generally represent a higher-risk customer segment compared with customers who have remained with the company for a longer period.

This suggests that early-stage customers may require stronger onboarding, engagement, and retention strategies.

Tenure was also one of the most important predictive features in the Random Forest analysis.

---

## 4. Contract Type and Churn

Contract type is an important business variable.

Customers on month-to-month contracts generally represent a higher churn-risk segment than customers with longer-term contracts.

Longer contracts provide greater customer commitment, while month-to-month customers have fewer contractual barriers to leaving.

This suggests that retention strategies could focus on:

- Encouraging longer-term contracts
- Offering incentives for contract upgrades
- Identifying month-to-month customers with additional risk factors

---

## 5. Monthly Charges and Churn

Monthly charges are relevant to churn prediction.

Customers with higher monthly charges can represent a higher-value customer segment, but higher charges may also increase the likelihood that customers reconsider their subscription.

Monthly charges were among the more important predictive variables in the model.

From a business perspective, high-charge customers with elevated churn probability may deserve priority because losing these customers can have a greater revenue impact.

---

## 6. Total Charges and Churn

`TotalCharges` captures the accumulated charges associated with a customer's tenure.

It is strongly related to both customer tenure and overall customer value.

The model identified `TotalCharges` as one of the important predictive features.

However, this feature should not be interpreted independently because it is naturally related to tenure and monthly charges.

---

## 7. Internet Service and Churn

Internet service type is another important customer characteristic.

Customers using fiber-optic internet represent an important segment for churn analysis.

The model identified:

`InternetService_Fiber optic`

as one of the more influential encoded features.

This does not by itself establish that fiber-optic service causes churn. It indicates that the segment contains information useful for distinguishing churn behavior.

Further business investigation would be required to determine the underlying reason.

---

## 8. Additional Service Features

Several service-related variables contribute to the prediction of churn.

Examples include:

- OnlineSecurity
- TechSupport
- OnlineBackup
- DeviceProtection
- StreamingTV
- StreamingMovies

The absence of services such as online security and technical support can be associated with different churn patterns.

These variables provide the model with information about the customer's relationship with the company's service ecosystem.

---

## 9. Payment Method

Payment method also provides useful information for churn prediction.

`Electronic check` appeared among the important encoded features in the Random Forest feature-importance analysis.

Payment behavior can therefore be considered as one of the customer characteristics useful for identifying churn risk.

---

## 10. Key Business Insights

The EDA and modelling analysis highlight several important areas for retention teams:

### 1. Early-tenure customers

Customers with shorter tenure should receive additional attention because they represent a higher-risk segment.

### 2. Month-to-month customers

Month-to-month customers are an important retention segment because they have greater flexibility to leave.

### 3. High-value customers

Customers with high monthly or accumulated charges and high predicted churn probability may represent significant revenue at risk.

### 4. Service engagement

Customers without additional support or security services may represent opportunities for targeted service adoption and retention campaigns.

### 5. Payment behavior

Payment method can provide additional information for identifying customers with elevated churn risk.

---

## 11. Important EDA Caveat

EDA identifies associations and patterns; it does not establish causation.

For example, if customers with a particular internet service show higher churn, this does not mean that the service itself causes customers to leave.

Business teams should combine these findings with customer research, operational data, and controlled experiments before making causal decisions.

---

## 12. EDA to Machine Learning

The EDA findings informed the modelling approach by highlighting:

- Numerical customer characteristics such as tenure and charges
- Categorical service and contract characteristics
- Potentially important customer segments
- Class imbalance
- The need for probability-based predictions

These observations were incorporated into the subsequent preprocessing, modelling, evaluation, and explainability stages.