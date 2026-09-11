# Business Understanding

## 1. Business Problem

Customer churn is a major business challenge for subscription-based companies.

When a customer leaves, the company loses recurring revenue and may also incur additional costs to acquire a replacement customer.

The objective of this project is to build a machine learning model that predicts whether a customer is likely to churn.

The prediction can be used by retention and marketing teams to identify high-risk customers and apply appropriate retention strategies.

---

## 2. Business Objective

The primary objective is:

> Predict the probability that a customer will churn and identify customers who are at higher risk of leaving.

The model should provide a probability rather than only a binary prediction so that the business can prioritize customers based on risk.

---

## 3. Business Use Case

The predicted churn probability can support targeted retention actions such as:

- Promotional offers
- Discounts
- Loyalty benefits
- Personalized communication
- Service improvements
- Customer support interventions

The goal is not to contact every customer.

Instead, the model helps the business prioritize customers where retention efforts are more likely to be valuable.

---

## 4. Stakeholders

Potential stakeholders include:

- CEO / Business Leadership
- Marketing Team
- Customer Success / Retention Team
- Finance Team
- Product Team

Different stakeholders may use the model output for different decisions.

For example:

- Marketing may use churn probability for targeted campaigns.
- Customer Success may prioritize high-risk customers.
- Finance may estimate potential revenue at risk.
- Product teams may investigate services associated with higher churn.

---

## 5. Machine Learning Problem

This is a supervised binary classification problem.

### Target Variable

`Churn`

Possible values:

- `Yes`
- `No`

The target is converted into a binary representation for machine learning:

- `Yes` → `1`
- `No` → `0`

---

## 6. Evaluation Strategy

Accuracy alone is not sufficient for this problem because the target classes are imbalanced.

The primary evaluation metric used for model selection is:

**ROC-AUC**

Additional metrics are:

- Accuracy
- Precision
- Recall
- F1 Score

ROC-AUC was selected as the primary model-selection metric because the model produces churn probabilities and the business may adjust the classification threshold depending on the cost of retention actions and missed churners.

---

## 7. Business Interpretation of Predictions

The model produces a churn probability.

For example:

```text
Churn Probability = 0.7631