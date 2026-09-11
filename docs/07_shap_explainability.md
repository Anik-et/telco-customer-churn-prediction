# 06 - Model Evaluation

## 1. Objective

The objective of the model evaluation stage is to determine how well the trained machine learning models perform on unseen customer data and whether their predictions are useful for the business problem.

Model evaluation is different from model training.

During training, the model learns patterns from the training data.

During evaluation, the model is tested on data that was not used to fit the model.

The main questions are:

1. How accurately does the model classify customers?
2. How well does it identify customers who actually churn?
3. How many customers are incorrectly identified as churners?
4. How well does the model rank customers by churn probability?
5. Does the model generalize beyond the training data?
6. Which model is most suitable for the business objective?

The project evaluates the models using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion Matrix
- Classification Report
- Train vs test performance

---

# 2. Evaluation Strategy

The evaluation process follows this structure:

    Trained Model
          |
          v
    Unseen Test Data
          |
          v
    Generate Predictions
          |
          +------------------------+
          |                        |
          v                        v
    Class Prediction        Probability Prediction
          |                        |
          v                        v
    Classification             ROC-AUC
       Metrics
          |
          +------------------------+
                       |
                       v
                Model Comparison
                       |
                       v
                Final Selection

The test data is used to estimate how well the model generalizes to unseen customers.

---

# 3. Why Model Evaluation Matters

A model that performs well during training is not necessarily useful in production.

For example:

    Training Accuracy = 99%

does not automatically mean the model is good.

If the model achieves:

    Test Accuracy = 75%

then there may be a generalization problem.

The goal is therefore not simply to maximize training performance.

The goal is to build a model that performs consistently on unseen data.

---

# 4. Confusion Matrix

A confusion matrix provides a detailed breakdown of classification predictions.

For binary classification:

| | Actual Negative | Actual Positive |
|---|---:|---:|
| Predicted Negative | TN | FN |
| Predicted Positive | FP | TP |

Where:

- `TN` = True Negative
- `FP` = False Positive
- `FN` = False Negative
- `TP` = True Positive

For this project:

- Negative = Customer did not churn
- Positive = Customer churned

---

# 5. True Positive

A True Positive occurs when:

    Actual = Churn
    Predicted = Churn

This means the model correctly identified a customer who churned.

Business interpretation:

> The model successfully identified a customer who was actually at risk of churn.

This is generally a valuable prediction for the retention team.

---

# 6. True Negative

A True Negative occurs when:

    Actual = No Churn
    Predicted = No Churn

This means the model correctly identified a customer who did not churn.

Business interpretation:

> The model correctly determined that the customer did not belong to the churn class.

---

# 7. False Positive

A False Positive occurs when:

    Actual = No Churn
    Predicted = Churn

The model incorrectly identifies a customer as a churner.

Business interpretation:

> The company may spend retention resources on a customer who was not actually going to churn.

Potential consequences include:

- Unnecessary discounts
- Unnecessary promotional offers
- Wasted marketing budget
- Unnecessary customer-success effort

Therefore, precision becomes important.

---

# 8. False Negative

A False Negative occurs when:

    Actual = Churn
    Predicted = No Churn

The model fails to identify a customer who actually churns.

Business interpretation:

> The company misses an opportunity to intervene with a customer who was actually going to churn.

Potential consequences include:

- Lost customer
- Lost future revenue
- Missed retention opportunity
- Lower customer lifetime value

This makes recall particularly important for churn prediction.

---

# 9. Accuracy

Accuracy measures the proportion of all predictions that are correct.

The formula is:

    Accuracy =
    (TP + TN) / (TP + TN + FP + FN)

For example, if 800 out of 1,000 predictions are correct:

    Accuracy = 800 / 1000
             = 0.80

or:

    Accuracy = 80%

---

# 10. Why Accuracy Alone is Not Enough

Accuracy can be misleading when the target classes are imbalanced.

Suppose a dataset contains:

    90% No Churn
    10% Churn

A model that predicts:

    No Churn

for every customer would achieve:

    Accuracy = 90%

However, it would identify:

    0% of churners

Therefore, a high accuracy score does not necessarily mean that the model is useful for the business.

For this reason, additional metrics are required.

---

# 11. Precision

Precision measures how many customers predicted as churners actually churned.

The formula is:

    Precision =
    TP / (TP + FP)

Precision answers:

> Of all customers predicted to churn, how many actually churned?

High precision means that the model's positive predictions are reliable.

---

# 12. Business Meaning of Precision

Suppose the retention team targets every customer predicted to churn.

If precision is high:

    More targeted customers
        |
        v
    Actually churn

If precision is low:

    Many targeted customers
        |
        v
    Would not have churned

Therefore, precision is particularly relevant when retention interventions are expensive.

For example, if a company provides a costly discount to every predicted churner, false positives create unnecessary costs.

---

# 13. Recall

Recall measures how many actual churners were successfully identified.

The formula is:

    Recall =
    TP / (TP + FN)

Recall answers:

> Of all customers who actually churned, how many did the model identify?

High recall means fewer actual churners are missed.

---

# 14. Business Meaning of Recall

Suppose a company has a large number of customers who eventually churn.

A model with low recall may fail to identify many of those customers.

For example:

    100 actual churners
          |
          v
    Model identifies 50
          |
          v
    Recall = 50%

The remaining 50 churners were false negatives.

For a retention-focused use case, missing a high-value customer may be significantly more expensive than incorrectly targeting a customer who would have stayed.

Therefore, recall is an important business metric.

---

# 15. Precision vs Recall Trade-off

Precision and recall often have a trade-off.

Increasing the classification threshold generally makes the model more selective about predicting churn.

This can result in:

    Higher Precision
          |
          v
    Fewer Positive Predictions

but potentially:

    Lower Recall
          |
          v
    More Missed Churners

Conversely, lowering the threshold can identify more potential churners but may increase false positives.

Conceptually:

    Lower Threshold
          |
          +--> More customers classified as churn
          |
          +--> Potentially higher recall
          |
          +--> Potentially lower precision

    Higher Threshold
          |
          +--> Fewer customers classified as churn
          |
          +--> Potentially higher precision
          |
          +--> Potentially lower recall

This trade-off is important for business decision-making.

---

# 16. F1 Score

F1-score combines precision and recall into a single metric.

The formula is:

    F1 =
    2 × (Precision × Recall)
    /
    (Precision + Recall)

F1 is useful when both precision and recall are important.

A model with:

    High Precision
    Low Recall

may still have a relatively modest F1-score.

Likewise:

    Low Precision
    High Recall

may also produce a modest F1-score.

The F1-score rewards models that achieve a reasonable balance between both metrics.

---

# 17. ROC Curve

The ROC curve evaluates model performance across different classification thresholds.

ROC stands for:

**Receiver Operating Characteristic**

The curve plots:

    True Positive Rate
    against
    False Positive Rate

where:

    True Positive Rate = Recall

and:

    False Positive Rate =
    FP / (FP + TN)

The threshold is changed across a range of values, and the resulting true-positive and false-positive rates are calculated.

---

# 18. ROC-AUC

AUC stands for:

**Area Under the Curve**

ROC-AUC summarizes the ROC curve into a single value.

The value generally ranges between:

    0 and 1

Interpretation:

| ROC-AUC | General Interpretation |
|---:|---|
| 0.50 | Random discrimination |
| 0.60 - 0.70 | Weak |
| 0.70 - 0.80 | Reasonable |
| 0.80 - 0.90 | Good |
| 0.90+ | Very strong |

A ROC-AUC of approximately:

    0.849

indicates that the model has good ability to distinguish churners from non-churners.

---

# 19. What Does ROC-AUC = 0.849 Mean?

ROC-AUC can be interpreted as the probability that a randomly selected positive example receives a higher predicted score than a randomly selected negative example.

Therefore, approximately:

    ROC-AUC = 0.849

means the model has approximately an 84.9% probability of ranking a randomly selected churner above a randomly selected non-churner.

This interpretation is useful because the business can use the model's probability score to rank customers according to churn risk.

---

# 20. Why ROC-AUC was Selected as the Primary Metric

The project uses ROC-AUC as the primary model-selection metric for several reasons.

### Reason 1 - Class imbalance

The target classes are not perfectly balanced.

Accuracy alone may therefore hide poor churn detection.

### Reason 2 - Probability ranking

The business can prioritize customers based on predicted churn probability.

ROC-AUC evaluates ranking ability across thresholds.

### Reason 3 - Threshold independence

ROC-AUC evaluates performance across many thresholds rather than depending on a single threshold such as `0.50`.

### Reason 4 - Model comparison

ROC-AUC provides a consistent metric for comparing different classification models.

---

# 21. Model Evaluation Results

The production-style model comparison produced the following results:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8055 | 0.6572 | 0.5588 | 0.6040 | 0.8419 |
| Random Forest | 0.8020 | 0.6766 | 0.4866 | 0.5661 | 0.8425 |
| XGBoost | **0.8084** | 0.6757 | 0.5348 | 0.5970 | **0.8490** |

The highest ROC-AUC was achieved by XGBoost:

    ROC-AUC = 0.848963

Therefore, XGBoost was selected as the final model.

---

# 22. Interpreting Logistic Regression Performance

Logistic Regression achieved:

| Metric | Score |
|---|---:|
| Accuracy | 0.8055 |
| Precision | 0.6572 |
| Recall | 0.5588 |
| F1 | 0.6040 |
| ROC-AUC | 0.8419 |

The model provides a strong baseline.

Its ROC-AUC of approximately:

    0.842

shows that even a relatively simple linear model can provide useful churn discrimination after appropriate preprocessing.

This is an important finding because it establishes a reference point for evaluating more complex models.

---

# 23. Interpreting Random Forest Performance

Random Forest achieved:

| Metric | Score |
|---|---:|
| Accuracy | 0.8020 |
| Precision | 0.6766 |
| Recall | 0.4866 |
| F1 | 0.5661 |
| ROC-AUC | 0.8425 |

Random Forest produced slightly higher precision than Logistic Regression:

    0.6766 vs 0.6572

However, its recall was lower:

    0.4866 vs 0.5588

This means Random Forest was more selective about its positive predictions but missed more actual churners.

Its ROC-AUC was:

    0.8425

which was slightly above Logistic Regression but below XGBoost.

---

# 24. Interpreting XGBoost Performance

XGBoost achieved:

| Metric | Score |
|---|---:|
| Accuracy | 0.8084 |
| Precision | 0.6757 |
| Recall | 0.5348 |
| F1 | 0.5970 |
| ROC-AUC | 0.8490 |

XGBoost achieved the highest:

    Accuracy
    ROC-AUC

among the three primary evaluated configurations.

Its ROC-AUC was:

    0.848963

This made XGBoost the strongest model based on the selected evaluation criterion.

---

# 25. Tuned Model Evaluation

The tuned Random Forest achieved:

| Metric | Score |
|---|---:|
| Accuracy | 0.8013 |
| Precision | 0.6780 |
| Recall | 0.4786 |
| F1 | 0.5611 |
| ROC-AUC | 0.8422 |

The tuned XGBoost achieved:

| Metric | Score |
|---|---:|
| Accuracy | 0.8055 |
| Precision | 0.6748 |
| Recall | 0.5160 |
| F1 | 0.5848 |
| ROC-AUC | 0.8483 |

Comparison:

| Model | ROC-AUC |
|---|---:|
| Random Forest | 0.8425 |
| Tuned Random Forest | 0.8422 |
| XGBoost | **0.8490** |
| Tuned XGBoost | 0.8483 |

The tuned models did not improve the strongest existing configurations on the held-out test set.

---

# 26. Train vs Test Performance

Comparing training and test performance helps identify potential overfitting.

For the XGBoost depth experiment:

| Max Depth | Train Accuracy | Test Accuracy |
|---:|---:|---:|
| 2 | 0.8209 | 0.8048 |
| 3 | 0.8395 | 0.7892 |
| 4 | 0.8685 | 0.7857 |
| 5 | 0.9104 | 0.7828 |
| 6 | 0.9381 | 0.7850 |
| 8 | 0.9831 | 0.7771 |
| 10 | 0.9933 | 0.7708 |

The pattern is clear:

    Increasing depth
          |
          v
    Training accuracy increases
          |
          v
    Test accuracy decreases

This indicates increasing overfitting as the trees become deeper.

---

# 27. Overfitting Detection

Overfitting can be identified by comparing training and validation/test performance.

A simplified pattern is:

    Training Performance ↑
    Test Performance ↓

This indicates that the model is learning increasingly specific patterns from the training data that do not generalize.

In this project:

    max_depth = 10

produced:

    Train Accuracy = 0.9933
    Test Accuracy  = 0.7708

This is substantially different from:

    max_depth = 2

which produced:

    Train Accuracy = 0.8209
    Test Accuracy  = 0.8048

The shallower model therefore generalized better.

---

# 28. Evaluation of Model Complexity

The evaluation experiments demonstrate that model complexity needs to be controlled.

A model with extremely high training accuracy is not necessarily desirable.

For example:

    Model A
    Train Accuracy = 99%
    Test Accuracy  = 77%

can be worse than:

    Model B
    Train Accuracy = 82%
    Test Accuracy  = 80%

Model B generalizes better.

The purpose of evaluation is therefore to measure generalization rather than training memorization.

---

# 29. Classification Threshold

Most binary classifiers produce a probability:

    P(Churn = 1)

The probability is converted into a class prediction using a threshold.

A common default is:

    threshold = 0.50

Conceptually:

    If probability >= 0.50:
        Predict Churn

    Otherwise:
        Predict No Churn

However, the optimal threshold depends on the business objective.

---

# 30. Why the Default 0.50 Threshold May Not Be Optimal

The business may not consider false positives and false negatives equally costly.

For example:

### Scenario A

Retention intervention is cheap.

The business may prefer to identify more potential churners.

This favors higher recall.

### Scenario B

Retention intervention is very expensive.

The business may prefer to target only highly likely churners.

This favors higher precision.

Therefore, the optimal threshold may be:

    0.30

or:

    0.60

or:

    0.70

rather than automatically using:

    0.50

---

# 31. Probability Thresholds vs Risk Bands

The project currently separates two concepts.

## Classification threshold

The model's class prediction uses the classifier's prediction behavior.

## Business risk thresholds

The prediction pipeline defines:

    Probability >= 0.70
        -> High Risk

    0.40 <= Probability < 0.70
        -> Medium Risk

    Probability < 0.40
        -> Low Risk

These risk bands are intended for business interpretation.

They should not be confused with the model's internal classification threshold.

---

# 32. Threshold Optimization as a Future Improvement

A production implementation could optimize the threshold using business costs.

For example:

    Cost of False Positive = $10
    Cost of False Negative = $500

In this situation, missing a churner is much more expensive than incorrectly targeting a customer.

The threshold could therefore be lowered to increase recall.

Alternatively, if retention campaigns are extremely expensive, the threshold could be increased to prioritize precision.

A cost-based objective could conceptually be:

    Total Cost =
    (FP × Cost_FP)
    +
    (FN × Cost_FN)

The threshold that minimizes expected business cost could then be selected.

---

# 33. Precision-Recall Trade-off for the Business

The business decision can be summarized as:

| Priority | Metric | Typical Strategy |
|---|---|---|
| Minimize unnecessary interventions | Precision | Higher threshold |
| Catch as many churners as possible | Recall | Lower threshold |
| Balance both | F1 | Threshold selected for balance |
| Rank customers effectively | ROC-AUC | Evaluate probability ordering |

This makes threshold selection a business decision rather than only a technical decision.

---

# 34. Why ROC-AUC and F1 Serve Different Purposes

ROC-AUC and F1-score should not be treated as interchangeable.

### ROC-AUC

Measures ranking/discrimination across many thresholds.

It is useful for evaluating the underlying quality of probability ranking.

### F1

Measures the balance between precision and recall at a specific classification threshold.

Therefore:

    ROC-AUC
        |
        v
    How well can the model rank customers?

while:

    F1
        |
        v
    How well does the model balance precision and recall at this threshold?

Both provide useful but different information.

---

# 35. Final Model Evaluation

The final selected XGBoost model achieved:

| Metric | Result |
|---|---:|
| Accuracy | 0.8084 |
| Precision | 0.6757 |
| Recall | 0.5348 |
| F1 | 0.5970 |
| ROC-AUC | 0.8490 |

The exact ROC-AUC was:

    0.848963

The model therefore provides good discrimination between churners and non-churners.

However, recall of approximately:

    0.535

also indicates that a significant proportion of actual churners are still missed at the current classification threshold.

This is an important business limitation.

---

# 36. Business Interpretation of the Final Model

The final model should not be interpreted as:

> "The model can perfectly predict who will churn."

Instead, it should be interpreted as:

> "The model can rank customers according to their likelihood of churn with reasonably strong discrimination."

The ROC-AUC of approximately 0.849 supports this interpretation.

The model can therefore be used to identify groups of customers who are more likely to churn and prioritize them for retention strategies.

---

# 37. False Positive vs False Negative Business Trade-off

The two major error types have different business consequences.

## False Positive

    Predicted Churn
          +
    Actually No Churn

Potential cost:

    Unnecessary retention intervention

## False Negative

    Predicted No Churn
          +
    Actually Churn

Potential cost:

    Lost customer

If the cost of losing a customer is much greater than the cost of a retention campaign, the business may prefer a model configuration with higher recall.

This is why model evaluation should ultimately connect technical metrics to business costs.

---

# 38. Evaluation Limitations

The current evaluation has several limitations.

## 38.1 Test Set Size

The dataset contains approximately 7,000 customers.

A larger production dataset could provide a more stable estimate of model performance.

---

## 38.2 Historical Snapshot

The data does not provide detailed longitudinal customer behavior.

A production model could potentially perform better by using:

- Historical billing trends
- Usage trends
- Support interactions
- Previous service changes
- Contract history
- Customer engagement history

---

## 38.3 Threshold Not Business-Optimized

The current classification and risk thresholds are not optimized using a formal business cost function.

A future implementation should evaluate threshold performance using expected financial impact.

---

## 38.4 Repeated Test Evaluation

Multiple experiments were performed during development.

If model decisions repeatedly depend on the same test-set results, the test set can gradually become part of the model-development process.

A stricter approach would reserve the final test set for one final evaluation after model selection.

---

# 39. Recommended Future Evaluation Improvements

For a production-quality churn system, evaluation could be extended with:

### 1. Precision-Recall Curve

Useful when the positive class is relatively uncommon.

### 2. Threshold Analysis

Evaluate precision, recall and business cost at multiple probability thresholds.

### 3. Calibration

Check whether predicted probabilities correspond to observed churn frequencies.

For example:

    Predicted probability ≈ 0.70

should ideally correspond to approximately:

    70% observed churn

for a well-calibrated model.

### 4. Business Cost Function

Incorporate:

- Customer lifetime value
- Retention campaign cost
- Cost of false negatives
- Cost of false positives

### 5. Temporal Validation

Train on earlier customer data and evaluate on later data.

This would better simulate production deployment.

---

# 40. Evaluation Workflow in Code

The project's evaluation component follows the basic process:

    Model
      |
      v
    model.predict(X_test)
      |
      v
    Class Predictions

and:

    Model
      |
      v
    model.predict_proba(X_test)
      |
      v
    Churn Probabilities

The resulting predictions are used to calculate:

    Accuracy
    Precision
    Recall
    F1
    ROC-AUC

The evaluation component also provides:

    Confusion Matrix
    Classification Report

This keeps evaluation logic separate from model training.

---

# 41. Separation of Training and Evaluation

Separating model training from evaluation improves the structure of the project.

Conceptually:

    ModelTrainer
         |
         v
    Trained Models
         |
         v
    ModelEvaluator
         |
         v
    Metrics

This follows the single-responsibility principle.

The model trainer is responsible for training.

The evaluator is responsible for measuring performance.

This makes the project easier to test, maintain and extend.

---

# 42. Final Model Selection Logic

The final selection process can be summarized as:

    Train Candidate Models
             |
             v
       Evaluate Models
             |
             v
       Compare ROC-AUC
             |
             v
    Select Highest ROC-AUC
             |
             v
        XGBoost
             |
             v
    Save best_model.pkl

The selected model achieved:

    ROC-AUC = 0.848963

---

# 43. Final Evaluation Summary

| Evaluation Area | Result |
|---|---|
| Problem Type | Binary Classification |
| Positive Class | Churn = Yes |
| Primary Metric | ROC-AUC |
| Final Model | XGBoost |
| Accuracy | 0.8084 |
| Precision | 0.6757 |
| Recall | 0.5348 |
| F1 | 0.5970 |
| ROC-AUC | 0.8490 |
| Model Artifact | `artifacts/best_model.pkl` |

---

# 44. Key Evaluation Lessons

## Lesson 1 - Accuracy is not enough

A high accuracy score can hide poor performance on the churn class.

---

## Lesson 2 - Precision and recall represent different business risks

Precision is related to unnecessary retention interventions.

Recall is related to missed churners.

---

## Lesson 3 - ROC-AUC evaluates ranking ability

This is useful when customers need to be prioritized based on churn probability.

---

## Lesson 4 - Test performance matters more than training performance

The purpose of evaluation is to estimate generalization to unseen data.

---

## Lesson 5 - Model complexity can hurt generalization

The XGBoost depth experiment showed that deeper trees can increase training performance while decreasing test performance.

---

## Lesson 6 - Threshold selection is a business decision

The optimal classification threshold depends on the relative costs of false positives and false negatives.

---

## Lesson 7 - Probability outputs are valuable

A churn probability allows the business to rank customers and assign risk categories.

---

# 45. Interview Explanation

A concise explanation of the evaluation stage would be:

> "I evaluated the models using accuracy, precision, recall, F1 and ROC-AUC, along with the confusion matrix. I used ROC-AUC as the primary model-selection metric because the churn classes are imbalanced and the business is interested in ranking customers by their churn probability. The final XGBoost model achieved about 0.849 ROC-AUC, 0.808 accuracy, 0.676 precision and 0.535 recall. I also compared training and test performance during the depth experiments and observed that deeper trees increased training accuracy substantially while reducing test performance, which indicated overfitting. From a business perspective, precision represents the efficiency of retention targeting, while recall represents how many actual churners we can identify. The current threshold has not yet been optimized against a formal business cost function, which would be an important production improvement."

---

# 46. Important Interview Questions

## Why did you choose ROC-AUC instead of accuracy?

Because accuracy can be misleading with class imbalance.

ROC-AUC measures how well the model separates churners from non-churners across different thresholds and is useful for ranking customers by churn probability.

---

## What does an ROC-AUC of 0.849 mean?

It means that if we randomly select one churner and one non-churner, the model has approximately an 84.9% probability of assigning a higher churn score to the churner.

---

## What is the difference between precision and recall?

Precision answers:

> When the model says a customer will churn, how often is it correct?

Recall answers:

> Of all customers who actually churn, how many did the model identify?

---

## Which is more important: precision or recall?

There is no universal answer.

It depends on the business cost.

If missing a churner is very expensive, recall may be more important.

If retention interventions are very expensive, precision may be more important.

---

## What is a false positive in this project?

A customer predicted to churn who actually does not churn.

The business may unnecessarily spend retention resources on that customer.

---

## What is a false negative?

A customer predicted not to churn who actually churns.

This represents a missed retention opportunity.

---

## Why can accuracy be misleading?

If most customers belong to the non-churn class, a model could achieve high accuracy by mostly predicting non-churn while failing to identify churners.

---

## What is the difference between ROC-AUC and F1?

ROC-AUC evaluates discrimination across different thresholds.

F1 evaluates the balance between precision and recall at a particular threshold.

---

## How would you improve the evaluation in production?

I would:

1. Perform threshold optimization.
2. Use a business cost function.
3. Analyze the precision-recall curve.
4. Check probability calibration.
5. Use temporal validation.
6. Evaluate model performance across customer segments.
7. Monitor performance after deployment.

---

## Why is threshold optimization important?

Because the default threshold may not reflect the business cost of false positives and false negatives.

The business should choose the threshold that provides the best expected outcome.

---

## How would you choose the threshold?

I would evaluate different thresholds and calculate:

- Precision
- Recall
- F1
- Number of customers targeted
- Expected retention cost
- Expected saved revenue

Then I would select the threshold that optimizes the business objective.

---

# 47. Final Conclusion

The evaluation stage confirmed that the XGBoost model provides the strongest overall discrimination among the evaluated model configurations.

The final model achieved:

    Accuracy  = 0.8084
    Precision = 0.6757
    Recall    = 0.5348
    F1        = 0.5970
    ROC-AUC   = 0.8490

The ROC-AUC of approximately 0.849 indicates good ability to distinguish between customers who churn and customers who do not churn.

However, the recall of approximately 0.535 shows that the current classification threshold still misses a meaningful proportion of actual churners.

Therefore, the next production-oriented improvement would be to connect probability thresholds to business costs and determine how aggressively the company wants to intervene.

The model should ultimately be viewed as a **customer risk-ranking system**, rather than a perfect churn oracle.

The next stage is **SHAP Explainability**, which will explain why the model assigns high or low churn risk to customers and identify the features that have the greatest influence on predictions.
'''