# 11 - MLOps and Production Monitoring

## 1. Objective

The objective of this stage is to understand what happens **after an ML model has been trained and deployed**.

A machine learning project does not end when the model reaches production.

A production model must continue to be:

- Monitored
- Evaluated
- Versioned
- Validated
- Maintained
- Retrained when necessary

The overall lifecycle becomes:

    Business Problem
          |
          v
    Data
          |
          v
    Training
          |
          v
    Evaluation
          |
          v
    Deployment
          |
          v
    Monitoring
          |
          v
    New Data
          |
          v
    Retraining
          |
          +------> Evaluation
                         |
                         v
                    Deployment

This continuous lifecycle is a major part of **MLOps**.

---

# 2. What is MLOps?

MLOps stands for:

**Machine Learning Operations**

MLOps combines concepts from:

- Machine learning
- Software engineering
- Data engineering
- DevOps
- Infrastructure
- Monitoring
- Governance

The goal is to reliably build, deploy and maintain machine learning systems.

A useful way to think about MLOps is:

> MLOps is the engineering discipline required to operate machine learning systems reliably throughout their lifecycle.

---

# 3. Why MLOps is Needed

Traditional software generally follows:

    Code
      |
      v
    Build
      |
      v
    Test
      |
      v
    Deploy
      |
      v
    Monitor

Machine learning adds additional moving parts:

    Code
      +
    Data
      +
    Features
      +
    Model
      +
    Model Artifact
      +
    Predictions
      +
    Actual Outcomes

Therefore, ML systems require additional monitoring.

---

# 4. ML System Lifecycle

A simplified ML lifecycle is:

    1. Business Understanding
              |
              v
    2. Data Collection
              |
              v
    3. Data Validation
              |
              v
    4. Feature Engineering
              |
              v
    5. Model Training
              |
              v
    6. Model Evaluation
              |
              v
    7. Model Validation
              |
              v
    8. Deployment
              |
              v
    9. Monitoring
              |
              v
    10. Retraining
              |
              +------> back to Training

The project has already implemented many of these stages.

---

# 5. What Should Be Monitored?

A production ML system should monitor multiple dimensions.

### Data

- Schema
- Missing values
- Invalid values
- Feature distributions
- New categories

### Model

- Prediction quality
- Precision
- Recall
- F1
- ROC-AUC

### Predictions

- Prediction distribution
- Probability distribution
- Risk-band distribution

### Infrastructure

- CPU
- Memory
- Latency
- Throughput
- Error rate

### Business

- Retention success
- Revenue impact
- Campaign conversion
- Customer outcomes

A strong monitoring system combines all of these.

---

# 6. Data Quality Monitoring

Data quality monitoring checks whether incoming data remains valid.

Important checks include:

    Required columns
    Data types
    Missing values
    Numeric ranges
    Categorical values
    Duplicate rates

For example:

    tenure < 0

would indicate invalid data.

Similarly:

    MonthlyCharges = "unknown"

would indicate an invalid numeric value.

---

# 7. Schema Drift

Schema drift occurs when the structure of incoming data changes.

Examples:

### Column removed

    MonthlyCharges

is no longer supplied.

### Column renamed

    MonthlyCharges
        ->
    monthly_charges

### New column

    NewServiceType

appears.

### Data type changed

    tenure
        int
        ->
        string

These changes can break the prediction pipeline.

Therefore, schema validation should happen before inference.

---

# 8. Data Drift

Data drift occurs when the distribution of input features changes.

Suppose the training data had:

    Average MonthlyCharges = $65

but production data later has:

    Average MonthlyCharges = $95

The model is now seeing a different input distribution.

This does not automatically mean the model is wrong, but it is a signal that the production environment has changed.

---

# 9. Example of Data Drift

Historical:

    tenure
    |
    +--> Mostly 12-36 months

Production:

    tenure
    |
    +--> Mostly 1-6 months

This could indicate:

- New customer acquisition strategy
- Product changes
- Different market segment
- Data pipeline changes

The model should be investigated when substantial drift occurs.

---

# 10. Concept Drift

Concept drift occurs when the relationship between features and the target changes.

For example:

Historical:

    Month-to-month contract
            |
            v
       Higher churn

Later:

    Month-to-month contract
            |
            v
       Lower churn

The input distribution might remain similar, but the relationship between the feature and churn has changed.

This can cause model performance to deteriorate.

---

# 11. Data Drift vs Concept Drift

| Type | What Changes? |
|---|---|
| Schema Drift | Data structure |
| Data Drift | Input feature distribution |
| Concept Drift | Relationship between features and target |
| Label Drift | Target distribution |

These concepts should not be treated as interchangeable.

---

# 12. Label Drift

Label drift occurs when the distribution of the target changes.

For example:

Historical:

    Churn = Yes -> 27%

Production:

    Churn = Yes -> 40%

This may indicate a major change in customer behavior or business conditions.

Label drift can also affect evaluation metrics and model assumptions.

---

# 13. Prediction Drift

Prediction drift focuses on changes in model outputs.

Suppose historically:

    High Risk   -> 10%
    Medium Risk -> 30%
    Low Risk    -> 60%

After a deployment:

    High Risk   -> 55%
    Medium Risk -> 30%
    Low Risk    -> 15%

This significant change should trigger investigation.

Possible causes include:

- Data drift
- Model changes
- Customer behavior changes
- Pipeline bugs

---

# 14. Probability Distribution Monitoring

The model produces:

    Churn Probability

rather than only:

    Yes / No

Therefore, monitor the probability distribution.

Useful statistics include:

- Mean probability
- Median probability
- Percentiles
- Minimum
- Maximum
- Distribution over time

For example:

    Average probability:
        0.31 -> 0.48

may indicate a significant shift.

---

# 15. Risk-Band Monitoring

The project uses:

    High Risk   >= 0.70
    Medium Risk >= 0.40
    Low Risk    < 0.40

The proportion of customers in each band can be monitored.

For example:

| Risk Band | Baseline | Current |
|---|---:|---:|
| High | 10% | 12% |
| Medium | 30% | 33% |
| Low | 60% | 55% |

Small changes may be normal.

Large sudden changes should be investigated.

---

# 16. Model Performance Monitoring

Model performance can be measured only after actual outcomes become available.

At prediction time:

    Customer
       |
       v
    Prediction

Later:

    Actual Churn Outcome
       |
       v
    Compare

Then calculate:

    Accuracy
    Precision
    Recall
    F1
    ROC-AUC

This creates a delayed feedback loop.

---

# 17. Why Model Performance is Delayed

At prediction time, we do not immediately know whether a customer will actually churn.

For example:

    January
      |
      v
    Predict churn

Actual behavior may become known:

    February / March
      |
      v
    Customer churned or stayed

Only then can the prediction be compared with reality.

Therefore, model monitoring has both:

    Real-time signals

and:

    Delayed outcome-based signals

---

# 18. Performance Monitoring Window

A business may define an evaluation window.

For example:

    Prediction Date
          |
          v
    Wait for outcome
          |
          v
    30/60/90-day evaluation
          |
          v
    Calculate performance

The appropriate window depends on how quickly churn outcomes become observable.

---

# 19. Monitoring Precision and Recall

Suppose the production model initially has:

    Precision = 0.68
    Recall    = 0.53

Later:

    Precision = 0.52
    Recall    = 0.38

This could indicate model degradation.

However, the reason should be investigated before immediately retraining.

Possible causes include:

- Data drift
- Concept drift
- Data-quality problems
- Incorrect labels
- Pipeline changes
- Business changes

---

# 20. Monitoring ROC-AUC

ROC-AUC can also be monitored over time.

Example:

    Initial:
        ROC-AUC = 0.849

    Later:
        ROC-AUC = 0.82

    Later:
        ROC-AUC = 0.75

A sustained decline suggests that the model is losing discriminatory power.

A threshold for acceptable performance should be defined by the business.

---

# 21. Business Metrics

Technical model metrics are not enough.

The business may ultimately care about:

- Customers retained
- Revenue retained
- Campaign conversion
- Retention cost
- Customer lifetime value
- Return on intervention

For example:

    Model improves recall
          |
          v
    More customers targeted
          |
          v
    Retention cost increases

The model improvement is not automatically valuable if the additional interventions do not generate enough retained revenue.

---

# 22. Business-Level Model Evaluation

A stronger evaluation can calculate:

    Expected Retention Value
        -
    Intervention Cost
        =
    Expected Business Value

For example:

    Predicted churner
          |
          v
    Retention offer
          |
          v
    Customer retained
          |
          v
    Revenue preserved

This connects ML metrics with business outcomes.

---

# 23. Model Monitoring vs Business Monitoring

These are related but different.

### Model Monitoring

Questions:

> Is the model still predicting accurately?

Metrics:

- Precision
- Recall
- F1
- ROC-AUC

### Business Monitoring

Questions:

> Is the model actually improving the business?

Metrics:

- Retention rate
- Revenue
- Campaign ROI
- Customer value

A model can remain technically strong while providing limited business value.

---

# 24. Alerting

Monitoring is useful only when important changes can trigger action.

Examples:

    Missing-value rate > threshold
          |
          v
        Alert

    High-risk percentage changes sharply
          |
          v
        Alert

    ROC-AUC drops below threshold
          |
          v
        Alert

Alerts should be meaningful rather than generated for every small fluctuation.

---

# 25. Alert Severity

A monitoring system can classify alerts.

### Warning

Small or moderate deviation.

### Critical

Severe deviation requiring immediate investigation.

For example:

    Warning:
        High-risk percentage increased by 10%

    Critical:
        Model inference failing

The exact severity rules depend on the production system.

---

# 26. Retraining

Retraining means creating a new model using newer data.

The workflow is:

    New Data
       |
       v
    Data Validation
       |
       v
    Feature Engineering
       |
       v
    Model Training
       |
       v
    Evaluation
       |
       v
    Model Comparison
       |
       v
    Approval
       |
       v
    Deployment

Retraining should not happen blindly.

---

# 27. When Should a Model Be Retrained?

Possible triggers include:

### Performance degradation

    ROC-AUC below threshold

### Data drift

    Significant distribution change

### Concept drift

    Feature-target relationship changes

### Business changes

    New product
    New pricing
    New customer segment

### Scheduled retraining

    Monthly
    Quarterly
    etc.

The correct strategy depends on the business and rate of change.

---

# 28. Scheduled vs Trigger-Based Retraining

## Scheduled

Example:

    Retrain every month

Advantages:

- Simple
- Predictable

Disadvantages:

- May retrain unnecessarily
- May not react quickly enough

## Trigger-Based

Example:

    Retrain when ROC-AUC < 0.80

Advantages:

- Responds to actual degradation

Disadvantages:

- Requires monitoring infrastructure

A hybrid approach is often practical.

---

# 29. Retraining Should Not Automatically Mean Deployment

A critical principle is:

> Retraining creates a candidate model, not automatically a production model.

The candidate should go through:

    Train
      |
      v
    Evaluate
      |
      v
    Compare with production
      |
      v
    Validate
      |
      v
    Approve
      |
      v
    Deploy

This prevents a poorly performing model from replacing a better production model.

---

# 30. Model Versioning

Each model should have an identifiable version.

Example:

    churn-model-v1
    churn-model-v2
    churn-model-v3

A version should ideally record:

- Model algorithm
- Training data version
- Feature version
- Hyperparameters
- Metrics
- Training timestamp
- Dependency versions

---

# 31. Why Model Versioning Matters

Suppose production currently uses:

    v2

A new deployment introduces:

    v3

Performance drops.

Without versioning, rollback becomes difficult.

With versioning:

    v3
     |
     v
    Rollback
     |
     v
    v2

Versioning also makes experiments and production decisions auditable.

---

# 32. Data Versioning

Model versioning alone is not enough.

The training data should also be traceable.

For example:

    Dataset v1
       |
       v
    Model v1

and:

    Dataset v2
       |
       v
    Model v2

This allows the team to understand which data produced a model.

---

# 33. Feature Versioning

Feature definitions can also change.

For example:

    tenure_v1

might later become:

    customer_tenure_months_v2

If feature logic changes, the model should be associated with the correct feature version.

This helps prevent incompatibility between models and feature pipelines.

---

# 34. Model Registry

A model registry stores and tracks model versions.

Conceptually:

    Model Registry
        |
        +--> v1
        |     |
        |     +--> Metrics
        |     +--> Artifact
        |
        +--> v2
        |     |
        |     +--> Metrics
        |     +--> Artifact
        |
        +--> v3
              |
              +--> Metrics
              +--> Artifact

A registry can also track model lifecycle states such as:

    Development
    Staging
    Production
    Archived

The current project does not require a registry, but it is an important production concept.

---

# 35. Model Promotion

A candidate model can move through:

    Development
        |
        v
    Validation
        |
        v
    Staging
        |
        v
    Production

Promotion should happen only after passing predefined acceptance criteria.

---

# 36. Model Rollback

A production system should be able to return to a previous model.

Example:

    v3 deployed
         |
         v
    Performance drops
         |
         v
    Rollback
         |
         v
    v2 restored

Rollback is easier when:

- Models are versioned
- Artifacts are immutable
- Deployments are automated
- Previous versions remain available

---

# 37. CI/CD for Machine Learning

Traditional CI/CD focuses primarily on application code.

ML CI/CD must also consider:

- Data
- Models
- Features
- Metrics

A simplified ML pipeline:

    Code Change
        |
        v
    Tests
        |
        v
    Data Validation
        |
        v
    Train / Evaluate
        |
        v
    Model Quality Gate
        |
        v
    Build
        |
        v
    Deploy

---

# 38. Continuous Integration

Continuous Integration means frequently integrating code changes and automatically validating them.

For this project:

    Git Push
       |
       v
    pytest
       |
       v
    Build Checks

This prevents broken code from progressing.

---

# 39. Continuous Delivery

Continuous Delivery means maintaining the system in a deployable state.

For ML:

    Tested Code
       +
    Approved Model
       |
       v
    Deployable Artifact

The deployment can then be released when approved.

---

# 40. Continuous Deployment

Continuous Deployment automatically releases changes after passing the required gates.

For ML, this should be approached carefully.

A model should not automatically deploy solely because training completed.

A model-quality gate is important.

---

# 41. Model Quality Gates

A candidate model can be required to satisfy:

    ROC-AUC >= 0.84

and perhaps:

    Recall >= 0.50

and:

    Precision >= 0.65

The exact values must be based on actual requirements.

If the candidate fails:

    Candidate
       |
       v
    Quality Gate
       |
       v
      FAIL
       |
       v
    Do Not Deploy

---

# 42. Current Project Quality Baseline

The selected XGBoost configuration achieved approximately:

    Accuracy  = 0.8084
    Precision = 0.6757
    Recall    = 0.5348
    F1        = 0.5970
    ROC-AUC   = 0.8490

This can serve as a reference baseline for future model versions.

A future candidate should be compared against this baseline rather than evaluated in isolation.

---

# 43. Shadow Deployment

A new model can be run alongside the production model without affecting business decisions.

Conceptually:

    Customer
       |
       +----------> Production Model
       |
       +----------> Candidate Model

Only the production model's prediction is used.

The candidate model's predictions are logged for comparison.

This is called:

**Shadow deployment**

It is useful for validating a new model using real production traffic.

---

# 44. A/B Testing

Another approach is to expose different model versions to different groups.

Example:

    90% -> Model v1
    10% -> Model v2

Business outcomes can then be compared.

This can be useful when model changes are expected to affect business decisions.

A/B testing should be designed carefully to avoid biased comparisons.

---

# 45. Canary Deployment

Canary deployment gradually introduces a new model.

Example:

    95% -> v1
     5% -> v2

Monitor:

- Errors
- Latency
- Prediction behavior
- Business outcomes

If the new model performs well:

    75% -> v1
    25% -> v2

and eventually:

    100% -> v2

---

# 46. Blue-Green Deployment

Blue-green deployment maintains two environments.

    Blue
      |
      v
    Current Production
       v1

    Green
      |
      v
    New Version
       v2

Traffic can switch between environments.

If v2 fails:

    Traffic
       |
       v
    Blue / v1

This enables quick rollback.

---

# 47. Monitoring Infrastructure

A production system may use dedicated monitoring systems.

Typical components include:

    Application
        |
        v
    Metrics
        |
        v
    Monitoring System
        |
        v
    Dashboard / Alerts

The exact tools vary by organization.

The important concept is that monitoring should be automated rather than relying on manual inspection.

---

# 48. Monitoring Dashboard

A model monitoring dashboard might contain:

### Data

    Missing-value rate
    Drift score
    New category rate

### Predictions

    Average churn probability
    High-risk percentage

### Model

    Precision
    Recall
    F1
    ROC-AUC

### API

    Latency
    Error rate
    Throughput

### Business

    Retention rate
    Campaign ROI

---

# 49. Monitoring Frequency

Different metrics require different frequencies.

### API health

    Seconds / minutes

### Data drift

    Hourly / daily

### Prediction distributions

    Daily

### Model performance

    Weekly / monthly

### Business outcomes

    Based on outcome availability

The appropriate frequency depends on how quickly the system changes.

---

# 50. Monitoring Baselines

Monitoring requires a baseline.

For example:

    Training Mean MonthlyCharges
        = 65

Current:

    Production Mean MonthlyCharges
        = 66

Likely normal.

But:

    Production Mean MonthlyCharges
        = 120

could indicate significant change.

Baselines should be stored and compared over time.

---

# 51. Statistical Drift Detection

Data drift can be measured using statistical methods.

Examples include:

- Population Stability Index (PSI)
- Kolmogorov-Smirnov test
- Jensen-Shannon divergence
- Distribution distance metrics

The correct method depends on:

- Feature type
- Distribution
- Data volume
- Business requirements

A drift metric should be treated as a signal, not automatically as proof of model failure.

---

# 52. Population Stability Index

PSI is commonly used to compare distributions.

Conceptually:

    PSI
      |
      +--> Low
      |     Similar distributions
      |
      +--> High
            Greater distribution shift

PSI thresholds should not be treated as universal laws.

The business should define appropriate thresholds based on experience and context.

---

# 53. Why Drift Does Not Automatically Mean Retraining

Suppose a feature distribution changes significantly.

That does not automatically mean the model is performing poorly.

For example:

    Data Drift
        |
        v
    Model Performance
        |
        +--> Still strong

In this case, immediate retraining may not be necessary.

The important question is:

> Has the change affected predictive performance or business outcomes?

---

# 54. Monitoring Correlated Features

Some features are naturally related.

In this dataset:

    tenure
    MonthlyCharges
    TotalCharges

may be correlated.

A change in one feature can influence others.

Therefore, drift analysis should consider feature relationships rather than interpreting every individual drift signal independently.

---

# 55. Data Quality vs Data Drift

These are different.

## Data Quality Problem

    MonthlyCharges = "ABC"

The value itself is invalid.

## Data Drift

    MonthlyCharges
    distribution changes
    from historical data

The values may all be valid but their distribution changed.

A system should monitor both.

---

# 56. Prediction Quality vs Prediction Distribution

A model can produce a stable prediction distribution while still being wrong.

For example:

    High Risk = 10%

could remain stable even if actual churn behavior changes.

Therefore:

    Prediction Monitoring
          +
    Outcome Monitoring

are both necessary.

---

# 57. Feedback Loop

A production ML system should create a feedback loop:

    Prediction
       |
       v
    Customer Outcome
       |
       v
    Evaluation
       |
       v
    Monitoring
       |
       v
    Retraining
       |
       v
    New Model
       |
       v
    Deployment

This is the core idea behind continuous ML lifecycle management.

---

# 58. Model Retraining Pipeline

A mature retraining pipeline could be:

    New Data
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
    Train Candidate Models
       |
       v
    Cross-Validation
       |
       v
    Test Evaluation
       |
       v
    Compare with Production
       |
       v
    Quality Gate
       |
       +------ FAIL ------> Reject
       |
       v
     PASS
       |
       v
    Register Model
       |
       v
    Deploy
       |
       v
    Monitor

---

# 59. Why Cross-Validation Matters During Retraining

A candidate model should not be selected based only on one accidental split.

Cross-validation provides multiple validation folds.

For example:

    Fold 1
    Fold 2
    Fold 3
    Fold 4
    Fold 5

This provides a more robust estimate of model performance.

The project already used 5-fold CV during hyperparameter tuning.

---

# 60. Test Set Discipline

A production-quality retraining process should keep a final test set isolated.

The ideal structure is:

    Training Data
        |
        v
    Cross-Validation
        |
        v
    Model Selection
        |
        v
    Final Model
        |
        v
    One-Time Final Test

Repeatedly evaluating many candidate models on the same final test set can gradually overfit decisions to that test set.

This is an important limitation to remember from the current project.

---

# 61. Model Registry Workflow

A model registry workflow can be:

    Candidate Model
          |
          v
    Evaluation
          |
          v
    Register
          |
          v
    Staging
          |
          v
    Validation
          |
          v
    Production

If a model fails after deployment:

    Production
        |
        v
    Rollback
        |
        v
    Previous Version

---

# 62. Reproducibility

A production model should be reproducible.

The system should track:

    Code Version
       +
    Data Version
       +
    Feature Version
       +
    Model Parameters
       +
    Dependency Versions
       |
       v
    Model Artifact

This makes it possible to understand how a specific model was created.

---

# 63. Experiment Tracking

During model development, experiments should record:

- Model type
- Hyperparameters
- Training data
- Validation score
- Test score
- Runtime
- Feature version

For example:

    Experiment 001
        Model = Logistic Regression
        ROC-AUC = 0.842

    Experiment 002
        Model = Random Forest
        ROC-AUC = 0.843

    Experiment 003
        Model = XGBoost
        ROC-AUC = 0.849

This creates a traceable model-development history.

---

# 64. Configuration Management

The project already uses:

    config.yaml

This is useful for managing:

- Model parameters
- Artifact paths
- Validation settings
- Risk thresholds

In production, configuration should be version-controlled where appropriate.

Secrets should not be stored in source-controlled configuration files.

---

# 65. Environment Reproducibility

A model may behave differently if dependencies change.

For example:

    scikit-learn vX
          |
          v
    Model behavior

versus:

    scikit-learn vY
          |
          v
    Potentially different behavior

Therefore, dependency versions should be controlled.

Containers can help create reproducible runtime environments.

---

# 66. Model and Dependency Compatibility

A serialized model may depend on:

- Python version
- scikit-learn version
- XGBoost version
- NumPy version

Therefore, the model artifact should be deployed with compatible dependencies.

This is another reason why model artifacts and environments should be versioned together.

---

# 67. Monitoring the Prediction Pipeline

The inference pipeline itself should be monitored.

Possible stages:

    Request
       |
       v
    Validation
       |
       v
    Transformation
       |
       v
    Preprocessing
       |
       v
    Model
       |
       v
    Response

Each stage can potentially fail.

Monitoring should identify where failures occur.

---

# 68. Logging Strategy

Useful logs include:

    Request received
    Validation success/failure
    Model version
    Prediction completed
    Latency
    Error type

Avoid logging complete customer records unless required.

The logging strategy should follow privacy and security requirements.

---

# 69. Privacy and Governance

Production ML systems may process customer information.

Governance should address:

- Data access
- Data retention
- Model access
- Auditability
- Privacy
- Security
- Regulatory requirements

The model should use only the data necessary for the intended purpose.

---

# 70. Responsible Model Monitoring

Monitoring should also check whether model behavior differs across relevant customer segments.

For example:

    Segment A
        |
        v
    Recall = 0.60

    Segment B
        |
        v
    Recall = 0.35

A large performance difference may require investigation.

The exact segments depend on legitimate business requirements and applicable governance rules.

---

# 71. Model Fairness

Fairness analysis evaluates whether model performance differs substantially across relevant groups.

Possible metrics include:

- Recall by group
- Precision by group
- False-positive rate
- False-negative rate

There is no single universal fairness metric.

The appropriate analysis depends on:

- Business context
- Legal requirements
- Product impact
- Protected characteristics where applicable

---

# 72. Model Explainability Monitoring

SHAP can also be used after deployment.

For example, monitor:

    Top SHAP Features

over time.

If the model's dominant drivers change unexpectedly, investigate.

This can complement:

- Data drift
- Prediction drift
- Performance monitoring

Explainability monitoring should not replace these other methods.

---

# 73. Business Intervention Monitoring

Because this is a churn-retention model, the final business loop is:

    Model
      |
      v
    High-Risk Customer
      |
      v
    Retention Intervention
      |
      v
    Customer Outcome
      |
      v
    Business Value

The system should ideally measure whether the intervention actually helps.

---

# 74. Uplift vs Churn Prediction

A churn model predicts:

> Who is likely to churn?

It does not necessarily predict:

> Who will be saved by a retention intervention?

These are different problems.

A customer may have:

    High churn probability

but:

    Low probability of responding to an offer.

A future advanced system could use uplift modeling to identify customers whose behavior is likely to change because of an intervention.

This is beyond the current project's scope.

---

# 75. Monitoring the Business Objective

The ultimate objective is not:

    Maximize ROC-AUC

The objective is:

    Improve customer retention
          +
    Generate positive business value

Therefore:

    Model Metrics
        +
    Business Metrics

should both be monitored.

---

# 76. Production Monitoring Example

A hypothetical daily dashboard might show:

    Predictions:
        25,000

    High Risk:
        2,900

    Medium Risk:
        7,100

    Low Risk:
        15,000

    Average Churn Probability:
        0.31

    API Error Rate:
        0.1%

    Average Latency:
        35 ms

Later, outcome-based metrics might show:

    Precision:
        0.66

    Recall:
        0.51

    ROC-AUC:
        0.83

This provides a holistic view of system health.

---

# 77. Monitoring Alert Example

Suppose the baseline is:

    ROC-AUC = 0.849

The monitoring system observes:

    ROC-AUC = 0.78

for several evaluation windows.

The response could be:

    Detect degradation
          |
          v
    Investigate data
          |
          v
    Check drift
          |
          v
    Check labels
          |
          v
    Retrain candidate
          |
          v
    Evaluate
          |
          v
    Deploy if approved

Retraining should therefore be part of a controlled workflow.

---

# 78. Incident Response

A production ML system needs an incident-response process.

Example:

    Prediction failures
          |
          v
    Alert
          |
          v
    Investigate
          |
          +--> Data issue
          |
          +--> Infrastructure issue
          |
          +--> Model issue
          |
          v
    Fix / Rollback
          |
          v
    Validate
          |
          v
    Restore service

This is an important operational aspect of ML systems.

---

# 79. Disaster Recovery

Production systems should also consider:

- Artifact backups
- Configuration backups
- Model version retention
- Infrastructure recovery
- Rollback procedures

If a new deployment fails, the organization should be able to restore a known-good version.

---

# 80. Monitoring Data Pipeline Failures

The model can only be as reliable as the data pipeline.

Suppose the source system changes:

    MonthlyCharges
        |
        v
    Null for 80% of records

The model may still technically generate predictions.

That does not mean the predictions are trustworthy.

Data-quality monitoring must therefore happen before model inference.

---

# 81. Monitoring Feature Availability

A production system should track feature availability.

Example:

    Feature                  Availability

    tenure                   99.99%
    MonthlyCharges           99.98%
    TotalCharges             99.95%
    Contract                 99.99%

A sudden drop may indicate a broken upstream data source.

---

# 82. Monitoring Unknown Categories

Because the encoder uses:

    handle_unknown="ignore"

unknown categories will not necessarily crash inference.

However, frequent unknown categories can indicate:

- New product values
- Schema changes
- Upstream pipeline changes
- Data drift

Therefore, the occurrence rate should be monitored.

---

# 83. Monitoring Model Confidence

The model's churn probabilities can be grouped into ranges:

    0.0 - 0.1
    0.1 - 0.2
    ...
    0.9 - 1.0

A sudden increase in extreme probabilities may indicate a change in input data or model behavior.

This is useful as a diagnostic signal.

---

# 84. Probability Calibration Monitoring

The model's predicted probability should ideally correspond reasonably well to observed outcomes.

For example:

    Customers predicted around 0.70

should have an observed churn rate reasonably close to:

    70%

if the model is calibrated.

Calibration can be monitored over time.

This is particularly relevant because the project uses probability-based risk bands.

---

# 85. Monitoring Threshold Effectiveness

The risk thresholds:

    0.40
    0.70

should not be considered permanently optimal.

The business should periodically evaluate:

- Number of customers targeted
- Actual churn rate
- Retention success
- Intervention cost
- Revenue impact

Thresholds can then be adjusted if business conditions change.

---

# 86. Monitoring Feedback Loops

The business process should ideally capture:

    Customer Targeted
        |
        v
    Intervention Type
        |
        v
    Customer Response
        |
        v
    Retained / Churned
        |
        v
    Business Value

This information can eventually improve both model training and decision-making.

---

# 87. MLOps Tooling

Production MLOps can use specialized tools for:

- Experiment tracking
- Data versioning
- Model registry
- Workflow orchestration
- Monitoring
- Deployment

Examples in the wider ecosystem include:

- MLflow
- DVC
- Airflow
- Kubernetes
- Cloud ML platforms

The project does not need all of these tools.

The important objective is to understand the underlying concepts.

---

# 88. Tool vs Concept

An important interview principle is:

> Know what problem a tool solves before discussing the tool itself.

For example:

    Model Registry
        |
        v
    Version and manage models

A specific tool such as MLflow can implement that capability.

Similarly:

    Workflow Orchestration
        |
        v
    Schedule and coordinate pipelines

A tool such as Airflow can implement that capability.

The architectural concept is more important than memorizing tool names.

---

# 89. Practical MLOps Stack for This Project

A reasonable progression could be:

    Git
      |
      v
    pytest
      |
      v
    Docker
      |
      v
    FastAPI
      |
      v
    CI/CD
      |
      v
    Model Registry
      |
      v
    Monitoring

The project does not need to implement the entire stack simultaneously.

---

# 90. Current Project MLOps Maturity

The current project already demonstrates:

- Configuration management
- Component separation
- Automated testing
- Model evaluation
- SHAP explainability
- Model persistence
- Prediction pipeline
- API architecture
- Containerization concepts

Production extensions include:

- Model registry
- Automated CI/CD
- Drift monitoring
- Automated retraining
- Model promotion
- Production alerting

This is a useful distinction when describing the project honestly in an interview.

---

# 91. End-to-End MLOps Architecture

A mature version of this project can be represented as:

    Data Source
        |
        v
    Data Validation
        |
        v
    Feature Pipeline
        |
        v
    Training
        |
        v
    Experiment Tracking
        |
        v
    Model Evaluation
        |
        v
    Model Registry
        |
        v
    Deployment
        |
        v
    FastAPI
        |
        v
    Predictions
        |
        +--------------------+
        |                    |
        v                    v
    Monitoring          Business Outcomes
        |                    |
        +----------+---------+
                   |
                   v
              Retraining
                   |
                   v
               New Model
                   |
                   v
             Model Registry

---

# 92. Recommended Production Workflow

A strong production workflow is:

### Development

    Code
      |
      v
    Tests

### Training

    Data
      |
      v
    Training
      |
      v
    Evaluation

### Validation

    Candidate Model
      |
      v
    Quality Gate

### Deployment

    Approved Model
      |
      v
    API / Container

### Monitoring

    Data
    Predictions
    Performance
    Business

### Improvement

    Drift / Degradation
      |
      v
    Retraining

This creates a continuous ML lifecycle.

---

# 93. Interview Explanation

A concise interview explanation would be:

> "I view MLOps as the operational lifecycle around the model rather than just deployment. After deployment, I would monitor data quality, schema changes, feature drift, prediction distributions, model performance and business outcomes. When actual churn labels become available, I would calculate metrics such as precision, recall, F1 and ROC-AUC and compare them against a baseline. If performance or data quality deteriorates, I would investigate whether the cause is data drift, concept drift or a pipeline issue before triggering retraining. A retrained model would go through validation and model-quality gates before being promoted. I would also version the model, data, features and dependencies so that the deployment is reproducible and rollback is possible."

---

# 94. Common Interview Questions

## What is MLOps?

MLOps is the engineering discipline for reliably developing, deploying, monitoring and maintaining machine learning systems throughout their lifecycle.

---

## What is data drift?

Data drift is a change in the distribution of input features between training and production data.

---

## What is concept drift?

Concept drift is a change in the relationship between input features and the target variable.

---

## What is the difference between data drift and concept drift?

Data drift changes:

    P(X)

Concept drift changes the relationship:

    P(Y | X)

In practical terms:

- Data drift = customer inputs changed.
- Concept drift = what those inputs mean for churn changed.

---

## What is model drift?

Model drift is commonly used to describe degradation in model performance over time, often caused by changes in data or the underlying relationship between inputs and outcomes.

---

## How would you detect model degradation?

I would compare production performance over time against a baseline using metrics such as:

- Precision
- Recall
- F1
- ROC-AUC

and investigate changes alongside data and prediction drift.

---

## When would you retrain the model?

I would retrain based on a defined strategy such as:

- Performance degradation
- Significant drift
- Major business changes
- Scheduled retraining

The retrained model would still need to pass validation before deployment.

---

## Should you automatically retrain when drift occurs?

Not necessarily.

Drift is a signal for investigation.

If performance remains strong, immediate retraining may not be justified.

---

## What is a model registry?

A model registry stores and manages model versions, metadata, metrics and lifecycle states such as staging and production.

---

## Why version models?

To support:

- Reproducibility
- Auditing
- Comparison
- Rollback
- Deployment management

---

## What is a model quality gate?

A predefined set of conditions that a candidate model must satisfy before deployment.

---

## How would you roll back a model?

Keep previous approved model versions available and switch production back to the last known-good version if the new model causes problems.

---

## How would you monitor a churn model?

I would monitor:

    Data quality
    Data drift
    Prediction distribution
    Risk-band distribution
    Precision
    Recall
    F1
    ROC-AUC
    API latency
    Error rate
    Retention outcomes
    Business ROI

---

## What is the difference between monitoring and retraining?

Monitoring detects changes or degradation.

Retraining creates a new candidate model to address those changes.

---

## What is CI/CD in ML?

It is the automation of code testing, model validation, artifact building and deployment while including model-quality checks in addition to traditional software tests.

---

## What is the difference between shadow and canary deployment?

### Shadow

The new model receives production traffic but does not affect decisions.

### Canary

The new model receives a small percentage of real traffic and can influence decisions for that subset.

---

# 95. Final MLOps Checklist

### Data

- [ ] Schema monitored
- [ ] Missing values monitored
- [ ] Feature distributions monitored
- [ ] Unknown categories monitored
- [ ] Data drift monitored

### Model

- [ ] Model version tracked
- [ ] Model metrics tracked
- [ ] Performance baseline defined
- [ ] Quality gates defined
- [ ] Rollback available

### Predictions

- [ ] Probability distribution monitored
- [ ] Risk bands monitored
- [ ] Prediction anomalies detected

### API

- [ ] Latency monitored
- [ ] Error rate monitored
- [ ] Availability monitored
- [ ] Resource usage monitored

### Business

- [ ] Retention outcomes measured
- [ ] Intervention cost measured
- [ ] Revenue impact measured
- [ ] ROI monitored

### Lifecycle

- [ ] Retraining strategy defined
- [ ] Model registry available
- [ ] Data/model versions tracked
- [ ] CI/CD configured
- [ ] Deployment process documented

---

# 96. Final Conclusion

MLOps extends the machine learning project beyond training and deployment.

The key idea is:

> A machine learning model is a living production component whose data, predictions, performance and business impact must be monitored continuously.

For this churn project, the most important production signals are:

    Data Quality
          +
    Data Drift
          +
    Prediction Distribution
          +
    Model Performance
          +
    Business Outcomes

These signals feed into a controlled lifecycle:

    Monitor
       |
       v
    Detect Change
       |
       v
    Investigate
       |
       v
    Retrain if Required
       |
       v
    Evaluate
       |
       v
    Approve
       |
       v
    Deploy
       |
       v
    Monitor Again

The final model's current performance baseline is approximately:

    ROC-AUC = 0.849
    Precision = 0.676
    Recall = 0.535
    F1 = 0.597

Future model versions should be evaluated against this baseline while keeping the final test-set discipline in mind.

The project has now covered the core end-to-end ML lifecycle:

    Business Understanding
            |
            v
    Data Understanding
            |
            v
    EDA
            |
            v
    Feature Engineering
            |
            v
    Model Training
            |
            v
    Model Evaluation
            |
            v
    Explainability
            |
            v
    Deployment
            |
            v
    Testing
            |
            v
    Containerization
            |
            v
    MLOps / Monitoring
            |
            v
    Continuous Improvement

The next stage should focus on **final project packaging, GitHub presentation, README documentation and interview preparation**, rather than adding infrastructure that does not materially improve the learning objective.
'''