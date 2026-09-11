## 1. Objective

The objective of the modeling stage is to build machine learning models that can predict whether a telecom customer is likely to churn.

This is a binary classification problem:

- `0` → Customer does not churn
- `1` → Customer churns

The model should ideally provide both:

1. A predicted churn class.
2. A probability of churn.

The probability is particularly useful from a business perspective because customers can be ranked according to their estimated churn risk.

The prediction pipeline currently uses the following business risk bands:

| Churn Probability | Risk Level |
|---:|---|
| `< 0.40` | Low |
| `0.40 - 0.69` | Medium |
| `>= 0.70` | High |

These thresholds are business rules, not parameters learned by the machine learning model.

---

## 2. Modeling Strategy

The project does not immediately select a single algorithm.

Instead, multiple classification algorithms are trained and compared.

The overall modeling strategy is:

1. Prepare the cleaned dataset.
2. Separate features (`X`) and target (`y`).
3. Split the data into training and test sets.
4. Train multiple candidate models.
5. Evaluate the models using several classification metrics.
6. Investigate model complexity and overfitting.
7. Perform hyperparameter tuning.
8. Compare tuned models with existing configurations.
9. Select the strongest model based primarily on ROC-AUC.
10. Persist the selected model for inference.

The main algorithms considered are:

- Logistic Regression
- Random Forest
- XGBoost

---

## 3. Why Multiple Models?

Different machine learning algorithms make different assumptions and learn different types of patterns.

Using multiple algorithms provides a useful comparison between:

| Model | Main Approach | Main Purpose |
|---|---|---|
| Logistic Regression | Linear classification | Simple and interpretable baseline |
| Random Forest | Bagging-based decision trees | Nonlinear relationships and interactions |
| XGBoost | Gradient-boosted decision trees | Strong performance on tabular data |

The purpose is not to use the most complicated algorithm.

The purpose is to identify a model that provides strong generalization performance while remaining suitable for the business problem.

---

# 4. Train-Test Split

The dataset contains:

- **7,043 customers**
- **21 original columns**
- Binary target: `Churn`

The data is divided into:

- **Training set** → used to learn the model.
- **Test set** → used to evaluate how well the model generalizes to unseen customers.

Conceptually:

    Complete Dataset
           |
           +----------------------+
           |                      |
           v                      v
    Training Set              Test Set
           |                      |
           v                      v
    Model Training          Final Evaluation

The test set represents data that the model has not seen during training.

## Why is this important?

A model can perform extremely well on the training data simply because it has learned the training observations too specifically.

The important question is:

> How well does the model perform on customers it has never seen before?

The test set provides an estimate of this generalization performance.

---

# 5. Target Representation

The original target column is:

    Churn

with two possible values:

    Yes
    No

For machine learning, the target is represented as a binary numerical variable:

    No  -> 0
    Yes -> 1

Therefore:

    0 = Customer did not churn
    1 = Customer churned

The positive class is:

    Churn = Yes

This distinction is important because precision, recall, F1-score and other classification metrics depend on which class is treated as the positive class.

---

# 6. Model 1 - Logistic Regression

## 6.1 What is Logistic Regression?

Logistic Regression is a supervised machine learning algorithm commonly used for binary classification.

It estimates the probability that an observation belongs to the positive class.

First, the model calculates a linear combination of the input features:

    z = β0 + β1x1 + β2x2 + ... + βnxn

This value is then passed through the sigmoid function:

    P(y = 1 | x) = 1 / (1 + e^(-z))

The sigmoid function converts the model output into a value between 0 and 1.

For example:

    0.10 -> Low estimated churn probability
    0.50 -> Moderate estimated churn probability
    0.90 -> High estimated churn probability

The probability is then converted into a class prediction using a classification threshold.

The default classifier threshold is generally:

    0.50

---

## 6.2 Why use Logistic Regression?

Logistic Regression is useful as a baseline because it is:

- Simple
- Fast
- Easy to understand
- Easy to interpret
- Computationally efficient
- Well suited to binary classification

It provides a reference point.

If a complex model does not meaningfully outperform Logistic Regression, then the additional complexity of the complex model may not be justified.

---

## 6.3 Logistic Regression Configuration

The configuration used in the project is:

    logistic_regression:
      max_iter: 1000

The model is also initialized with:

    random_state=42

### `max_iter`

`max_iter` specifies the maximum number of optimization iterations allowed during model fitting.

A sufficiently large value reduces the likelihood of convergence problems, particularly after preprocessing and one-hot encoding.

The project uses:

    max_iter = 1000

---

## 6.4 Limitations of Logistic Regression

Logistic Regression primarily learns a linear relationship between the input variables and the log-odds of the target.

Therefore, it may struggle with highly nonlinear relationships.

For example, churn may depend on combinations such as:

    Short Tenure
          +
    Month-to-Month Contract
          +
    High Monthly Charges
          +
    No Technical Support
          =
    High Churn Risk

A linear model does not automatically capture these complex interactions as effectively as tree-based models.

---

# 7. Model 2 - Random Forest

## 7.1 What is Random Forest?

Random Forest is an ensemble machine learning algorithm based on decision trees.

Instead of creating one decision tree, Random Forest creates many decision trees and combines their predictions.

Conceptually:

    Training Data
          |
    +-----+-----+-----+
    |           |    |
    v           v    v
  Tree 1      Tree 2 Tree 3
    |           |    |
    +-----+-----+----+
          |
          v
    Aggregate Results
          |
          v
    Final Prediction

The basic idea is that combining many different trees can produce a more stable and robust model than relying on one tree.

---

# 8. How Random Forest Creates Diversity

Random Forest introduces randomness mainly through two mechanisms.

## 8.1 Bootstrap Sampling

Each decision tree can be trained on a bootstrap sample of the training data.

Bootstrap sampling means observations are sampled with replacement.

Therefore, each tree can see a somewhat different version of the training dataset.

This helps create diversity among the trees.

---

## 8.2 Random Feature Selection

At each split, Random Forest considers only a subset of the available features.

This means different trees can discover different relationships in the data.

The combination of:

- Different training samples
- Different feature subsets

helps reduce the correlation between individual trees.

---

# 9. Important Random Forest Hyperparameters

## `n_estimators`

`n_estimators` specifies the number of decision trees in the forest.

Example:

    n_estimators=200

More trees can make predictions more stable, although training and prediction become more computationally expensive.

---

## `max_depth`

`max_depth` controls the maximum depth of each decision tree.

A small value produces shallow trees.

A larger value allows trees to learn more complex patterns.

However, very deep trees can overfit the training data.

Conceptually:

    Low max_depth
          |
          v
    Simpler model
          |
          v
    Lower overfitting risk

while:

    High max_depth
          |
          v
    More complex model
          |
          v
    Higher overfitting risk

---

## `max_features`

`max_features` controls the number of features considered when looking for the best split.

The project experimented with values such as:

    sqrt
    log2

Using fewer features at each split increases randomness and diversity between trees.

---

## `min_samples_split`

`min_samples_split` specifies the minimum number of samples required to split an internal node.

Increasing this value makes the tree more conservative.

This can reduce overfitting.

---

## `min_samples_leaf`

`min_samples_leaf` specifies the minimum number of samples that must exist in a leaf node.

A larger value prevents the model from creating extremely small leaves.

This can improve generalization.

---

## `bootstrap`

`bootstrap` determines whether bootstrap samples are used when building the trees.

The project uses:

    bootstrap=True

---

## `random_state`

`random_state` controls the randomness involved in the algorithm.

The project uses:

    random_state=42

This improves reproducibility of experiments.

---

# 10. Random Forest Configuration

An earlier tuned Random Forest configuration used:

    random_forest:
      n_estimators: 100
      max_depth: 8
      max_features: log2
      min_samples_split: 10
      min_samples_leaf: 2
      bootstrap: true

The corresponding tuned parameters were:

    {
        "n_estimators": 100,
        "min_samples_split": 10,
        "min_samples_leaf": 2,
        "max_features": "log2",
        "max_depth": 8,
        "bootstrap": True
    }

The best cross-validation score recorded during that tuning experiment was approximately:

    0.8468

---

# 11. Random Forest Results

The earlier tuned Random Forest achieved the following test performance:

| Metric | Score |
|---|---:|
| Accuracy | 0.8020 |
| Precision | 0.6703 |
| Recall | 0.5000 |
| F1 | 0.5727 |
| ROC-AUC | 0.8419 |

Training accuracy was:

    0.8291

Test accuracy was:

    0.8020

The relatively moderate train-test gap indicates that this tuned configuration was considerably more controlled than a highly unrestricted tree-based model.

---

# 12. Model 3 - XGBoost

## 12.1 What is XGBoost?

XGBoost stands for:

**Extreme Gradient Boosting**

It is a gradient boosting algorithm based on decision trees.

Unlike Random Forest, where trees are generally built independently, XGBoost builds trees sequentially.

Conceptually:

    Initial Model
          |
          v
       Tree 1
          |
          v
    Identify Errors
          |
          v
       Tree 2
          |
          v
    Improve Previous Model
          |
          v
       Tree 3
          |
          v
         ...
          |
          v
    Final Ensemble

Each new tree attempts to improve the existing model.

---

# 13. Gradient Boosting Concept

Suppose the current model makes predictions that are not perfectly aligned with the actual target values.

The next tree is trained to improve the existing predictions.

The new tree does not replace the previous trees.

Instead, it contributes an additional correction.

Conceptually:

    Model 1
       +
    Correction from Tree 2
       +
    Correction from Tree 3
       +
    Correction from Tree 4
       +
    ...
       =
    Final Model

This sequential learning process is the key idea behind gradient boosting.

---

# 14. Why XGBoost?

XGBoost is particularly effective for structured or tabular datasets.

This dataset contains:

- Numerical variables
- One-hot encoded categorical variables
- Nonlinear relationships
- Potential feature interactions

Tree boosting can learn relationships such as:

    Month-to-month contract
            +
    Short tenure
            +
    High monthly charges
            +
    Fiber optic internet
            +
    No online security
            =
    Higher estimated churn probability

The model can learn these interactions without manually creating every possible combination.

---

# 15. Important XGBoost Hyperparameters

## `n_estimators`

The number of boosting trees.

For example:

    n_estimators=500

More trees provide more opportunities for the model to improve its predictions.

However, too many trees can increase computational cost and potentially lead to overfitting.

---

## `max_depth`

Maximum depth of each boosting tree.

Higher depth allows each tree to learn more complex patterns.

However, deeper trees also increase the risk of overfitting.

This parameter was specifically investigated during the project's experiments.

---

## `learning_rate`

The learning rate controls how much each new tree contributes to the final model.

Conceptually:

    F_t(x) = F_(t-1)(x) + ηh_t(x)

where:

- `F_t(x)` = current model
- `F_(t-1)(x)` = previous model
- `h_t(x)` = new tree
- `η` = learning rate

A smaller learning rate means that each individual tree contributes less.

Usually, a lower learning rate requires more trees.

---

## `subsample`

`subsample` specifies the fraction of training observations used for each boosting round.

For example:

    subsample=0.8

means approximately 80% of the training observations are used in each boosting round.

This introduces randomness and can help reduce overfitting.

---

## `min_child_weight`

`min_child_weight` controls the minimum amount of instance weight required in a child node.

Higher values make the model more conservative when creating splits.

This can help reduce overfitting.

---

## `colsample_bytree`

`colsample_bytree` specifies the fraction of features used for each tree.

For example:

    colsample_bytree=0.8

means approximately 80% of the features are sampled for each tree.

This introduces additional randomness and can help improve generalization.

---

## `eval_metric`

The XGBoost model is configured with:

    eval_metric="logloss"

Log loss measures the quality of probabilistic predictions.

For binary classification:

    LogLoss =
    -(1/N) * Σ[
        y_i * log(p_i)
        +
        (1-y_i) * log(1-p_i)
    ]

Lower log loss indicates better probabilistic predictions.

---

# 16. XGBoost Experiments

Several controlled experiments were performed to understand the effect of hyperparameters.

One major experiment investigated:

    max_depth

while keeping the other relevant parameters fixed.

The results were:

| Max Depth | Train Accuracy | Test Accuracy | Precision | Recall | F1 | ROC-AUC |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 0.8209 | 0.8048 | 0.6623 | 0.5401 | 0.5950 | 0.8425 |
| 3 | 0.8395 | 0.7892 | 0.6262 | 0.5107 | 0.5626 | 0.8357 |
| 4 | 0.8685 | 0.7857 | 0.6139 | 0.5187 | 0.5623 | 0.8292 |
| 5 | 0.9104 | 0.7828 | 0.6104 | 0.5027 | 0.5513 | 0.8249 |
| 6 | 0.9381 | 0.7850 | 0.6060 | 0.5428 | 0.5726 | 0.8254 |
| 8 | 0.9831 | 0.7771 | 0.5882 | 0.5348 | 0.5602 | 0.8119 |
| 10 | 0.9933 | 0.7708 | 0.5780 | 0.5053 | 0.5392 | 0.8051 |

---

# 17. Interpretation of the Max Depth Experiment

This experiment provides strong evidence about model complexity.

As `max_depth` increases, training accuracy increases significantly.

For example:

    max_depth = 2
    Train Accuracy ≈ 0.821

while:

    max_depth = 10
    Train Accuracy ≈ 0.993

However, test performance moves in the opposite direction.

The ROC-AUC values were approximately:

    max_depth = 2
    ROC-AUC ≈ 0.8425

and:

    max_depth = 10
    ROC-AUC ≈ 0.8051

This indicates that deeper trees increasingly fit the training data but generalize worse to unseen customers.

This is a classic example of overfitting.

The experiment demonstrates:

> Increasing model complexity does not automatically improve model performance.

---

# 18. Learning Rate and Number of Trees Experiment

Another experiment investigated the relationship between:

- Learning rate
- Number of trees

The results were:

| Learning Rate | Trees | Train Accuracy | Test Accuracy | Precision | Recall | F1 | ROC-AUC |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.30 | 100 | 0.8209 | 0.8048 | 0.6623 | 0.5401 | 0.5950 | 0.8425 |
| 0.20 | 150 | 0.8193 | 0.8034 | 0.6655 | 0.5214 | 0.5847 | 0.8433 |
| 0.10 | 300 | 0.8200 | 0.8034 | 0.6644 | 0.5241 | 0.5859 | 0.8435 |
| 0.05 | 500 | 0.8188 | 0.8013 | 0.6610 | 0.5160 | 0.5796 | 0.8437 |
| 0.01 | 1000 | 0.8154 | 0.8020 | 0.6667 | 0.5080 | 0.5766 | 0.8454 |

---

# 19. Interpretation of Learning Rate Experiment

The experiment demonstrates the trade-off between:

    Learning Rate
          and
    Number of Trees

A high learning rate means each tree makes a larger contribution.

A low learning rate means each tree makes a smaller contribution, so more trees are generally required.

For example:

    learning_rate = 0.30
    n_estimators = 100

compared with:

    learning_rate = 0.01
    n_estimators = 1000

The lower learning rate configuration achieved the highest ROC-AUC in this specific experiment:

    ROC-AUC ≈ 0.8454

However, the difference was relatively small.

This demonstrates why systematic experimentation is preferable to selecting hyperparameters purely based on intuition.

---

# 20. Model Comparison

The production-style model comparison produced the following results:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8055 | 0.6572 | 0.5588 | 0.6040 | 0.8419 |
| Random Forest | 0.8020 | 0.6766 | 0.4866 | 0.5661 | 0.8425 |
| XGBoost | 0.8084 | 0.6757 | 0.5348 | 0.5970 | 0.8490 |

Among these evaluated configurations, XGBoost achieved the highest ROC-AUC:

    ROC-AUC = 0.848963

---

# 21. Why ROC-AUC is Important

Accuracy alone is not sufficient for this project.

The churn classes are imbalanced, and the business is interested in identifying customers who are likely to churn.

A model could achieve reasonable accuracy while still missing a large number of churners.

ROC-AUC measures how well the model separates positive and negative observations across different classification thresholds.

It can also be interpreted as the probability that a randomly selected positive example receives a higher predicted score than a randomly selected negative example.

A rough interpretation is:

| ROC-AUC | General Interpretation |
|---:|---|
| 0.50 | Random discrimination |
| 0.60 - 0.70 | Weak |
| 0.70 - 0.80 | Reasonable |
| 0.80 - 0.90 | Good |
| 0.90+ | Very strong |

The project achieved approximately:

    ROC-AUC = 0.849

which indicates good class-ranking ability.

---

# 22. Hyperparameter Tuning

After the initial model comparisons, hyperparameter tuning was performed for:

- Random Forest
- XGBoost

The objective of tuning is to find a model configuration that generalizes well.

The project uses:

    RandomizedSearchCV

instead of manually testing every possible parameter combination.

---

# 23. Why RandomizedSearchCV?

Suppose we have several hyperparameters and several candidate values for each parameter.

Testing every possible combination can quickly become expensive.

For example:

    Parameter A -> 5 values
    Parameter B -> 4 values
    Parameter C -> 5 values
    Parameter D -> 4 values

A full grid would require:

    5 × 4 × 5 × 4 = 400 combinations

Randomized Search instead samples a specified number of combinations.

This provides a practical trade-off:

    Search Coverage
          vs
    Computational Cost

For this project, RandomizedSearchCV allows a meaningful search without evaluating every possible combination.

---

# 24. Cross-Validation

The hyperparameter tuning process uses:

    5-fold cross-validation

The training data is divided into five folds.

Conceptually:

    Fold 1 | Fold 2 | Fold 3 | Fold 4 | Fold 5

Each fold is used as the validation fold once.

For example:

    Run 1:
    Validation = Fold 1
    Training   = Folds 2, 3, 4, 5

    Run 2:
    Validation = Fold 2
    Training   = Folds 1, 3, 4, 5

    Run 3:
    Validation = Fold 3
    Training   = Folds 1, 2, 4, 5

    Run 4:
    Validation = Fold 4
    Training   = Folds 1, 2, 3, 5

    Run 5:
    Validation = Fold 5
    Training   = Folds 1, 2, 3, 4

The model's performance is averaged across the five validation folds.

This provides a more robust estimate during model selection than relying on a single validation split.

---

# 25. Tuning Search Size

The production-style tuning pipeline used:

## Random Forest

    20 candidate parameter combinations
    5-fold cross-validation

Therefore:

    20 × 5 = 100 model fits

## XGBoost

    25 candidate parameter combinations
    5-fold cross-validation

Therefore:

    25 × 5 = 125 model fits

Total:

    100 + 125 = 225 model fits

This explains why hyperparameter tuning takes significantly longer than training a single model.

---

# 26. Random Forest Tuning Results

The RandomizedSearchCV process identified the following Random Forest configuration:

    {
        "n_estimators": 200,
        "min_samples_split": 2,
        "min_samples_leaf": 1,
        "max_features": "sqrt",
        "max_depth": 6,
        "bootstrap": True
    }

The resulting test performance was:

| Metric | Score |
|---|---:|
| Accuracy | 0.8013 |
| Precision | 0.6780 |
| Recall | 0.4786 |
| F1 | 0.5611 |
| ROC-AUC | 0.8422 |

The tuned Random Forest did not outperform the strongest XGBoost configuration.

---

# 27. XGBoost Tuning Results

The RandomizedSearchCV process identified the following XGBoost configuration:

    {
        "subsample": 0.8,
        "n_estimators": 500,
        "min_child_weight": 7,
        "max_depth": 3,
        "learning_rate": 0.01,
        "colsample_bytree": 0.9
    }

The resulting test performance was:

| Metric | Score |
|---|---:|
| Accuracy | 0.8055 |
| Precision | 0.6748 |
| Recall | 0.5160 |
| F1 | 0.5848 |
| ROC-AUC | 0.8483 |

The resulting ROC-AUC was:

    0.848289

---

# 28. Why Did the Tuned Model Not Win?

An important machine learning principle demonstrated by this project is:

> Hyperparameter tuning does not guarantee better test-set performance.

The stronger existing XGBoost configuration achieved approximately:

    ROC-AUC = 0.848963

while the RandomizedSearchCV-selected XGBoost configuration achieved:

    ROC-AUC = 0.848289

The difference is very small.

Therefore, the tuned configuration did not provide a meaningful improvement over the already strong XGBoost configuration.

This does not mean that tuning failed.

It means that the search did not find a configuration that generalized better on this particular held-out test set.

---

# 29. Cross-Validation Score vs Test Score

It is important to distinguish between cross-validation performance and test performance.

## Cross-validation

Cross-validation is used during:

- Hyperparameter tuning
- Model comparison during development
- Estimating generalization within the training data

It helps answer:

> Which configuration appears to generalize well based on the training data?

## Test set

The test set is used for final evaluation.

It helps answer:

> How well does the selected model perform on unseen data?

Conceptually:

    Training Data
          |
          +----------------------+
          |                      |
          v                      v
    Cross-Validation        Model Training
          |                      |
          v                      |
    Hyperparameter              |
    Selection                   |
          |                      |
          +----------+-----------+
                     |
                     v
                Final Model
                     |
                     v
                  Test Set
                     |
                     v
              Final Performance

Ideally, the test set should remain untouched until final evaluation.

---

# 30. Final Model Selection

Among the evaluated production-style configurations, the strongest ROC-AUC was achieved by XGBoost.

The selected model achieved:

    Accuracy  = 0.8084
    Precision = 0.6757
    Recall    = 0.5348
    F1        = 0.5970
    ROC-AUC   = 0.848963

Therefore:

    Final Model = XGBoost

The trained model is persisted as:

    artifacts/best_model.pkl

---

# 31. Important Configuration Note

There were multiple stages of experimentation during development.

These included:

1. Initial notebook-based model experiments.
2. Manual hyperparameter experiments.
3. Earlier tuned configurations.
4. Production-style RandomizedSearchCV.
5. Final model comparison.

Therefore, the term **baseline** needs to be used carefully.

The current configuration file contains:

    xgboost:
      n_estimators: 800
      max_depth: 3
      learning_rate: 0.01
      subsample: 0.7
      min_child_weight: 5
      colsample_bytree: 0.8

These parameters originated from earlier tuning experiments and should therefore not be described as a pure default XGBoost configuration.

A pure earlier XGBoost baseline experiment produced approximately:

| Metric | Score |
|---|---:|
| Accuracy | 0.7850 |
| Precision | 0.6060 |
| Recall | 0.5428 |
| F1 | 0.5726 |
| ROC-AUC | 0.8254 |

The stronger configured XGBoost model achieved:

    ROC-AUC ≈ 0.8490

This distinction is important when explaining the project.

---

# 32. Overfitting Analysis

Overfitting occurs when a model learns the training data too specifically and does not generalize well to unseen observations.

The XGBoost depth experiment demonstrated this clearly.

For example:

    max_depth = 2
    Train Accuracy = 0.8209
    Test Accuracy  = 0.8048

while:

    max_depth = 10
    Train Accuracy = 0.9933
    Test Accuracy  = 0.7708

The deeper model almost perfectly fits the training data but performs worse on unseen data.

This is strong evidence of overfitting.

---

# 33. Model Complexity vs Generalization

The experiments demonstrate the relationship between model complexity and generalization.

As model complexity increases:

    Model Complexity
           |
           v
    Training Performance Increases
           |
           v
    Overfitting Risk Increases
           |
           v
    Test Performance May Decrease

The goal is therefore not:

    Maximize Training Accuracy

The actual goal is:

    Maximize Generalization Performance

This is why techniques such as:

- Cross-validation
- Regularization
- Tree-depth control
- Sampling
- Minimum-child constraints
- Hyperparameter tuning

are important.

---

# 34. Evaluation Metrics

The project evaluates models using:

- Accuracy
- Precision
- Recall
- F1-score
- ROC-AUC
- Confusion Matrix
- Classification Report

Each metric answers a different business or machine learning question.

---

## 34.1 Accuracy

Accuracy measures the proportion of all predictions that are correct.

    Accuracy =
    (TP + TN) / (TP + TN + FP + FN)

It is useful as a general metric but can be misleading when the target classes are imbalanced.

---

## 34.2 Precision

Precision answers:

> Of the customers predicted to churn, how many actually churned?

    Precision =
    TP / (TP + FP)

High precision means fewer false positives.

In business terms, this can mean fewer customers are incorrectly targeted by retention campaigns.

---

## 34.3 Recall

Recall answers:

> Of all customers who actually churned, how many did the model identify?

    Recall =
    TP / (TP + FN)

High recall means fewer actual churners are missed.

This can be important when the cost of losing a customer is high.

---

## 34.4 F1 Score

F1-score balances precision and recall.

    F1 =
    2 × (Precision × Recall)
    /
    (Precision + Recall)

F1 is useful when both false positives and false negatives matter.

---

## 34.5 ROC-AUC

ROC-AUC evaluates the model's ability to distinguish between positive and negative observations across different thresholds.

It is especially useful when the model's probability ranking is important.

For this project, ROC-AUC is the primary model-selection metric.

---

# 35. Confusion Matrix

A confusion matrix breaks classification results into four categories:

| | Actual No Churn | Actual Churn |
|---|---:|---:|
| Predicted No Churn | TN | FN |
| Predicted Churn | FP | TP |

Where:

- `TN` = True Negative
- `FP` = False Positive
- `FN` = False Negative
- `TP` = True Positive

For churn prediction:

### True Positive

The model predicts churn and the customer actually churns.

### True Negative

The model predicts no churn and the customer actually does not churn.

### False Positive

The model predicts churn but the customer does not churn.

### False Negative

The model predicts no churn but the customer actually churns.

From a business perspective, false negatives can be particularly important because they represent customers who churned but were not identified by the model.

---

# 36. Model Comparison Summary

The key production-style results were:

| Model | Accuracy | Precision | Recall | F1 | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| Logistic Regression | 0.8055 | 0.6572 | 0.5588 | 0.6040 | 0.8419 |
| Random Forest | 0.8020 | 0.6766 | 0.4866 | 0.5661 | 0.8425 |
| XGBoost | **0.8084** | 0.6757 | 0.5348 | 0.5970 | **0.8490** |
| Tuned Random Forest | 0.8013 | **0.6780** | 0.4786 | 0.5611 | 0.8422 |
| Tuned XGBoost | 0.8055 | 0.6748 | 0.5160 | 0.5848 | 0.8483 |

The highest ROC-AUC was:

    XGBoost = 0.848963

Therefore, XGBoost was selected as the final model.

---

# 37. Why Probability Predictions Matter

The model provides a probability rather than only a binary prediction.

For example:

    Customer A
    Churn Probability = 0.82

and:

    Customer B
    Churn Probability = 0.31

The first customer is considerably more likely to churn according to the model.

The business can therefore prioritize Customer A for retention activities.

This allows the system to move from:

    Prediction

to:

    Risk Ranking

---

# 38. Business Interpretation

The model is ultimately intended to support customer retention decisions.

A simplified workflow is:

    Customer Data
          |
          v
    Churn Model
          |
          v
    Churn Probability
          |
          v
    Risk Classification
          |
          +-------------------+
          |                   |
          v                   v
      High Risk          Lower Risk
          |
          v
    Retention Campaign

For example:

    Churn Probability = 0.82
    Risk Level = High

could result in a retention action such as:

- Promotional offer
- Discount
- Service upgrade
- Customer-success intervention
- Targeted communication

The exact action would depend on business rules and customer economics.

---

# 39. Why Probability is More Useful Than Only Yes/No

Suppose two customers are both classified as:

    Churn = Yes

But their predicted probabilities are:

    Customer A = 0.51
    Customer B = 0.91

Treating both customers exactly the same would lose useful information.

The probabilities allow the business to rank customers:

    0.91
    0.87
    0.82
    0.76
    0.68
    0.55
    ...

The retention team can then focus limited resources on the highest-risk customers.

This is particularly valuable because retention interventions have a cost.

---

# 40. Model Persistence

After selecting the final model, it is serialized using `joblib`.

The final model artifact is:

    artifacts/best_model.pkl

The preprocessing pipeline is stored separately:

    artifacts/preprocessor.pkl

The transformed feature names are also persisted:

    artifacts/feature_names.pkl

The model artifacts allow the trained model to be reused without retraining.

---

# 41. Why Save the Preprocessor?

The preprocessing applied during training must be exactly the same during inference.

For example, training may apply:

    Missing-value imputation
            +
    Standard scaling
            +
    One-hot encoding

New customer data must go through the same transformations.

If the preprocessing differs between training and inference, the model may receive data in a representation different from the one it learned.

Therefore:

    Training:
    Raw Data
       |
       v
    Preprocessor
       |
       v
    Transformed Features
       |
       v
    Model

and inference must follow:

    New Customer
       |
       v
    Same Preprocessor
       |
       v
    Same Feature Representation
       |
       v
    Saved Model
       |
       v
    Prediction

This is one of the most important production ML requirements.

---

# 42. Reproducibility

The project uses:

    random_state=42

where supported.

A fixed random state helps make experiments reproducible.

Without a fixed random state, results may change because of randomness in:

- Train/test splitting
- Bootstrap sampling
- Random feature selection
- Randomized hyperparameter search
- Model initialization

Reproducibility makes it easier to:

- Debug the pipeline
- Compare experiments
- Reproduce results
- Track model changes

---

# 43. Overall Modeling Pipeline

The complete modeling workflow is:

    Raw Customer Dataset
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
    Train / Test Split
            |
            +-------------------+
            |          |        |
            v          v        v
       Logistic     Random    XGBoost
       Regression   Forest
            |          |        |
            +----------+--------+
                       |
                       v
                 Model Evaluation
                       |
                       v
              Hyperparameter Tuning
                       |
                       v
                 Model Comparison
                       |
                       v
              Final Model Selection
                       |
                       v
                Save Model Artifact

---

# 44. Limitations

The modeling approach has several limitations.

## 44.1 Dataset Size

The dataset contains approximately 7,000 customers.

This is sufficient for an educational end-to-end project but is relatively small compared with the scale of a real telecom customer base.

A production system would likely have significantly more data.

---

## 44.2 Historical Snapshot

The dataset is primarily a customer-level snapshot.

It does not provide detailed historical sequences such as:

- Daily customer activity
- Monthly usage history
- Billing history
- Customer support interaction sequences
- Contract changes over time
- Historical service changes

A production churn system could benefit from temporal features.

---

## 44.3 Threshold Selection

The current risk thresholds:

    High   >= 0.70
    Medium >= 0.40
    Low    < 0.40

are business rules.

They have not been optimized using an explicit business cost function.

A production implementation should ideally choose intervention thresholds using factors such as:

- Cost of retention campaigns
- Cost of losing a customer
- Customer lifetime value
- Retention capacity
- Expected campaign effectiveness

---

## 44.4 Test Set Reuse During Development

Multiple model experiments were performed during development.

Repeatedly comparing different models on the same test set can introduce indirect test-set overfitting if those results repeatedly influence modeling decisions.

A stricter production methodology would be:

    Training Data
          |
          +--> Cross-Validation
          |
          +--> Model Selection
          |
          v
       Final Model
          |
          v
    Untouched Test Set
          |
          v
    Final Evaluation

For this educational project, the current methodology is acceptable for demonstrating the end-to-end ML workflow, but this limitation should be acknowledged.

---

# 45. Key Modeling Lessons

## Lesson 1 - More complexity is not automatically better

The XGBoost depth experiment showed that deeper trees increased training performance while reducing test performance.

---

## Lesson 2 - Baselines are important

Logistic Regression provides a simple benchmark.

Without a baseline, it is difficult to determine whether a more complex model provides meaningful improvement.

---

## Lesson 3 - Hyperparameter tuning is not guaranteed to improve the test score

The tuned XGBoost configuration achieved a slightly lower test ROC-AUC than the stronger existing XGBoost configuration.

This demonstrates that tuning is a search process, not a guarantee of improvement.

---

## Lesson 4 - Cross-validation provides a better basis for tuning

5-fold cross-validation allows each training observation to participate in validation while keeping the evaluation more robust than a single validation split.

---

## Lesson 5 - Accuracy should not be the only metric

Churn prediction involves class imbalance and business trade-offs.

Precision, recall, F1 and ROC-AUC provide additional information that accuracy alone cannot provide.

---

## Lesson 6 - Probability predictions enable prioritization

A probability score allows customers to be ranked according to estimated churn risk.

This is more useful for many business applications than a simple Yes/No prediction.

---

# 46. Interview Explanation

A concise explanation of the modeling stage would be:

> "I treated churn as a binary classification problem and compared Logistic Regression, Random Forest and XGBoost. I used Logistic Regression as a simple baseline, while Random Forest and XGBoost allowed me to model nonlinear relationships and interactions. I evaluated the models using accuracy, precision, recall, F1 and ROC-AUC, with ROC-AUC as the primary model-selection metric because the churn classes are imbalanced and the business needs good probability-based risk ranking. I also performed controlled experiments on XGBoost tree depth and learning rate. One important finding was that increasing tree depth significantly improved training accuracy but reduced test performance, which indicated overfitting. I then used 5-fold RandomizedSearchCV for Random Forest and XGBoost. The tuned configurations did not materially outperform the stronger existing XGBoost configuration, so I selected XGBoost based on the highest held-out ROC-AUC of approximately 0.849."

---

# 47. Important Interview Questions

## Why did you choose XGBoost?

Because the dataset is structured/tabular and contains nonlinear relationships and feature interactions.

XGBoost performed best among the evaluated configurations based on ROC-AUC.

---

## Why didn't you use accuracy as the primary metric?

Because the churn target is imbalanced.

Accuracy can hide poor performance on the minority class.

The business is particularly interested in identifying customers who are likely to churn, so precision, recall and probability-ranking metrics are important.

---

## Why did you choose ROC-AUC?

ROC-AUC measures how effectively the model ranks positive examples above negative examples across different classification thresholds.

Since the model produces churn probabilities that can be used for customer prioritization, ranking quality is important.

---

## Why did you use Logistic Regression?

It provides a simple, interpretable baseline.

It helps determine whether the more complex tree-based models provide meaningful improvement.

---

## Why did you use Random Forest?

Random Forest can capture nonlinear relationships and interactions while reducing the variance of individual decision trees through ensemble averaging.

---

## What is the difference between Random Forest and XGBoost?

Random Forest is primarily a bagging-based method.

Conceptually:

    Build many trees independently
            |
            v
    Aggregate their predictions

XGBoost is a boosting-based method.

Conceptually:

    Build trees sequentially
            |
            v
    Each new tree improves previous errors
            |
            v
    Combine all trees

Random Forest focuses heavily on reducing variance through randomized trees, while boosting focuses on sequentially improving model errors.

---

## What did you learn from the max-depth experiment?

Increasing tree depth increased training performance but reduced test performance.

For example:

    Depth 2:
    Train Accuracy = 0.8209
    Test Accuracy  = 0.8048

while:

    Depth 10:
    Train Accuracy = 0.9933
    Test Accuracy  = 0.7708

This demonstrated overfitting.

---

## Why did hyperparameter tuning not improve the model?

The existing XGBoost configuration was already strong.

RandomizedSearchCV found another competitive configuration, but its held-out test ROC-AUC was slightly lower.

Tuning optimizes performance based on the cross-validation search objective. It does not guarantee improvement on a particular unseen test set.

---

## What is the relationship between `learning_rate` and `n_estimators`?

`learning_rate` controls how much each tree contributes to the final model.

`n_estimators` controls how many trees are added.

A smaller learning rate usually requires more trees because each individual tree contributes less.

---

## How did you control overfitting?

The project used several approaches:

- Train/test separation
- Cross-validation
- Limiting tree depth
- Random feature sampling
- Row sampling
- Minimum-child constraints
- Minimum leaf/split constraints
- Hyperparameter tuning
- Comparing training and test performance

---

## Why save the preprocessing pipeline?

Because the exact same preprocessing used during training must be applied during inference.

Otherwise, the model could receive features in a different representation from the representation used during training.

---

# 48. Final Modeling Architecture

The final modeling architecture can be summarized as:

    Raw Customer Data
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
    +------+------+------+
    |      |             |
    v      v             v
 Logistic Random       XGBoost
 Regression Forest
    |      |             |
    +------+------+------+
           |
           v
    Model Evaluation
           |
           v
    Hyperparameter Tuning
           |
           v
    Model Comparison
           |
           v
    Select XGBoost
           |
           v
    best_model.pkl

---

# 49. Final Conclusion

The modeling stage evaluated multiple machine learning algorithms instead of assuming that one algorithm would be optimal.

Logistic Regression provided a simple baseline.

Random Forest provided an ensemble-based nonlinear approach.

XGBoost provided a gradient-boosted tree approach and achieved the strongest ROC-AUC among the evaluated configurations.

The experiments demonstrated that:

- Increasing model complexity can cause overfitting.
- Learning rate and number of trees must be considered together.
- Hyperparameter tuning does not guarantee better held-out performance.
- Cross-validation is useful for hyperparameter selection.
- Accuracy alone is not sufficient for churn prediction.
- ROC-AUC is useful for evaluating customer risk ranking.
- Probability predictions allow the business to prioritize customers.
- The preprocessing pipeline must be persisted alongside the model.

The final selected model is:

    XGBoost

with a held-out ROC-AUC of approximately:

    0.849

The final model and supporting artifacts are persisted so that the same preprocessing and prediction logic can be reused during inference.

The next stage is **SHAP Explainability**, where the project will investigate which features influence the model's churn predictions and how individual features contribute to high- or low-risk predictions.
'''
