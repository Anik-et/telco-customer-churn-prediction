# 08 - Model Deployment

## 1. Objective

The objective of the deployment stage is to make the trained churn model usable for predictions on new customer data.

Up to this point, the project has covered:

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
    SHAP Explainability

Deployment connects the trained machine learning system to real-world usage.

The key goal is:

> Given raw customer information, return a churn prediction, churn probability and business-friendly risk level.

---

# 2. Training vs Deployment

Training and deployment are different stages.

## Training

Training uses historical data to learn patterns.

    Historical Data
          |
          v
    Preprocessing
          |
          v
    Feature Engineering
          |
          v
    Model Training
          |
          v
    Trained Model

## Deployment

Deployment uses the already-trained model.

    New Customer Data
          |
          v
    Same Transformation
          |
          v
    Saved Preprocessor
          |
          v
    Saved Model
          |
          v
    Prediction

The model should not be retrained every time a prediction is requested.

---

# 3. Production Prediction Flow

The project implements a prediction pipeline:

    Raw Customer Input
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
    Prediction Probability
            |
            v
    Risk Classification
            |
            v
    Prediction Response

The prediction response contains:

- Churn prediction
- Churn probability
- Risk level

---

# 4. Why Save the Preprocessor?

The model does not directly consume the original raw customer data.

The data passes through preprocessing such as:

- Numeric imputation
- Standardization
- Categorical imputation
- One-hot encoding

Therefore, the exact fitted preprocessing logic must be preserved.

The project saves:

    artifacts/preprocessor.pkl

Without the fitted preprocessor, new data may not be transformed in exactly the same way as the training data.

---

# 5. Why Save the Model?

The trained model is saved so that it can be loaded later without retraining.

The project saves the best model as:

    artifacts/best_model.pkl

This allows the prediction pipeline to perform inference using the already-trained model.

---

# 6. Model Artifact and Preprocessor Artifact

The deployment system therefore depends on two important artifacts:

    best_model.pkl
            |
            +--> Trained XGBoost model

    preprocessor.pkl
            |
            +--> Fitted preprocessing pipeline

The relationship is:

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
       |
       v
    Prediction

The preprocessor and model must remain compatible.

---

# 7. Why the Training Preprocessor Must Be Reused

A common deployment mistake is to fit a new preprocessor on inference data.

That should not happen.

Incorrect:

    Training Data
        |
        v
    Fit Preprocessor A

    New Customer
        |
        v
    Fit Preprocessor B
        |
        v
    Model

The inference preprocessor can have different:

- Means
- Medians
- Most-frequent categories
- Encoded category mappings
- Feature ordering

Correct:

    Training Data
        |
        v
    Fit Preprocessor
        |
        +----------------------+
        |                      |
        v                      v
    Training Data          New Customer
        |                      |
        v                      v
    Transform              Transform
        |                      |
        +----------+-----------+
                   |
                   v
                 Model

The same fitted preprocessor is reused for inference.

---

# 8. Data Transformation During Prediction

The deployment pipeline uses the same `DataTransformation` component used during training.

One important transformation is:

    TotalCharges

The raw dataset contains values that can be represented as strings, including blank values.

The transformation converts the column using:

    pd.to_numeric(..., errors="coerce")

Invalid values become missing values.

The saved preprocessor can then handle missing numerical values through its imputation step.

---

# 9. Removing the Customer ID

The raw dataset contains:

    customerID

This identifier was removed during transformation.

The reason is that the customer ID is an identifier rather than a useful predictive feature.

During inference, the same transformation is applied:

    customerID
        |
        v
    Removed

This ensures the feature structure remains consistent with training.

---

# 10. Feature Preprocessing During Inference

The saved preprocessing pipeline contains:

## Numerical pipeline

    Numerical Features
          |
          v
    Median Imputation
          |
          v
    StandardScaler
          |
          v
    Transformed Numerical Features

## Categorical pipeline

    Categorical Features
          |
          v
    Most-Frequent Imputation
          |
          v
    One-Hot Encoding
          |
          v
    Transformed Categorical Features

The two outputs are combined through the `ColumnTransformer`.

---

# 11. Handling Unknown Categories

The categorical encoder uses:

    handle_unknown="ignore"

This is important during deployment.

Suppose training data contains:

    Contract:
        Month-to-month
        One year
        Two year

A future input could contain a category that was not present during training.

With:

    handle_unknown="ignore"

the transformer can process the input without failing because of the unseen category.

This improves robustness for production inference.

---

# 12. Prediction Pipeline

The project contains:

    PredictPipeline

This class is responsible for inference.

Its initialization:

1. Loads the YAML configuration.
2. Loads the saved model.
3. Loads the saved preprocessor.
4. Creates the data transformation component.

Conceptually:

    PredictPipeline
          |
          +--> config.yaml
          |
          +--> best_model.pkl
          |
          +--> preprocessor.pkl
          |
          +--> DataTransformation

---

# 13. Prediction Method

The prediction method accepts:

    pandas.DataFrame

containing raw customer information.

The sequence is:

    input_data
        |
        v
    copy data
        |
        v
    DataTransformation.transform()
        |
        v
    preprocessor.transform()
        |
        v
    model.predict()
        |
        v
    model.predict_proba()
        |
        v
    Risk Classification
        |
        v
    Return Dictionary

---

# 14. Why Use a DataFrame for Input?

The input is represented as a pandas DataFrame because the original training data is tabular.

A DataFrame preserves:

- Column names
- Column structure
- Data types
- Multiple records

This makes it suitable for structured customer data.

The same interface can later be extended to:

- CSV input
- JSON input
- API requests
- Batch prediction

---

# 15. Prediction Output

The prediction pipeline returns a dictionary containing:

    {
        "churn_prediction": ...,
        "churn_probability": ...,
        "risk_level": ...
    }

For example:

    Churn Prediction : Yes
    Churn Probability: 0.7631
    Risk Level       : High

This is more useful than returning only a binary label.

---

# 16. Why Return Probability?

A binary prediction only says:

    Yes
    or
    No

A probability provides more information.

For example:

    Customer A -> 0.91
    Customer B -> 0.72
    Customer C -> 0.48
    Customer D -> 0.15

The business can rank customers according to risk.

This supports prioritization rather than a simple yes/no decision.

---

# 17. Risk Level

The project converts churn probability into three business-friendly risk bands.

Current configuration:

    High Risk:
        probability >= 0.70

    Medium Risk:
        0.40 <= probability < 0.70

    Low Risk:
        probability < 0.40

These thresholds are configured in:

    config.yaml

under:

    prediction:
      high_risk_threshold: 0.70
      medium_risk_threshold: 0.40

---

# 18. Risk Thresholds Are Business Rules

The risk thresholds should not be confused with model parameters.

For example:

    max_depth
    learning_rate
    n_estimators

are model parameters.

Whereas:

    0.70 High Risk
    0.40 Medium Risk

are business rules used to translate model probabilities into actionable categories.

They can be changed without retraining the model.

---

# 19. Example Business Workflow

The deployed system can support:

    Customer Data
          |
          v
    Churn Probability
          |
          v
    Risk Level
          |
          v
    Retention Strategy

For example:

### High Risk

Potential actions:

- Customer-success outreach
- Retention offer
- Service review
- Targeted promotion

### Medium Risk

Potential actions:

- Automated communication
- Engagement campaign
- Monitoring

### Low Risk

Potential actions:

- Normal customer lifecycle management
- No immediate intervention

The exact actions should be determined by the business.

---

# 20. Current Inference Test

The prediction pipeline was tested successfully.

Example output:

    Prediction Result:
    Churn Prediction : Yes
    Churn Probability: 0.7631
    Risk Level       : High

This demonstrates that the saved model and preprocessor can be loaded and used to generate a prediction on new input data.

---

# 21. Deployment Architecture

The current project can be viewed as:

    config.yaml
         |
         v
    PredictPipeline
         |
         +---------------------+
         |                     |
         v                     v
    DataTransformation    Saved Preprocessor
         |                     |
         +----------+----------+
                    |
                    v
             Transformed Input
                    |
                    v
             Saved XGBoost Model
                    |
                    v
             Prediction Output
                    |
                    v
          Probability + Risk Level

This is a lightweight inference architecture.

---

# 22. Why Configuration is Externalized

The project uses:

    config.yaml

instead of hard-coding all configuration values inside Python code.

This includes:

- Data path
- Required columns
- Expected data types
- Model parameters
- Artifact paths
- SHAP output path
- Risk thresholds

External configuration makes the system easier to modify without changing application logic.

---

# 23. Example Configuration

The prediction-related configuration is:

    prediction:
      high_risk_threshold: 0.70
      medium_risk_threshold: 0.40

Artifact configuration includes:

    artifacts:
      directory: "artifacts"
      best_model: "artifacts/best_model.pkl"
      preprocessor: "artifacts/preprocessor.pkl"
      feature_names: "artifacts/feature_names.pkl"

This centralizes deployment-related paths and business thresholds.

---

# 24. Deployment Does Not Mean Retraining

A common misunderstanding is:

> "The deployed model should train itself whenever it receives new data."

That is not how the current system works.

Deployment performs:

    Load
      |
      v
    Transform
      |
      v
    Predict

Retraining is a separate workflow.

For example:

    Historical Data
          |
          v
       Retraining
          |
          v
     Model Evaluation
          |
          v
     Model Validation
          |
          v
       New Model
          |
          v
      Deployment

---

# 25. Batch vs Real-Time Prediction

There are two common deployment patterns.

## Batch Prediction

Predictions are generated for many customers at once.

Example:

    100,000 customers
          |
          v
    Batch prediction
          |
          v
    Churn scores
          |
          v
    Retention campaign

This is useful for marketing campaigns.

---

## Real-Time Prediction

A prediction is generated when a customer interacts with the system.

Example:

    Customer interaction
          |
          v
    API request
          |
          v
    Model prediction
          |
          v
    Churn risk

This is useful for:

- Customer support
- Web applications
- Call-center systems
- Real-time personalization

The current project demonstrates the inference logic but does not yet expose it as a web API.

---

# 26. API Deployment as a Future Step

A natural next step would be to expose `PredictPipeline` through an API framework such as:

    FastAPI

A conceptual endpoint could be:

    POST /predict

with customer information in the request.

The flow would be:

    Client
      |
      v
    POST /predict
      |
      v
    API
      |
      v
    PredictPipeline
      |
      v
    Model
      |
      v
    JSON Response

Example response:

    {
      "churn_prediction": "Yes",
      "churn_probability": 0.7631,
      "risk_level": "High"
    }

This would make the model accessible to other applications.

---

# 27. Why FastAPI Would Be Appropriate

For a machine learning inference service, an API framework should provide:

- HTTP endpoints
- Input validation
- JSON responses
- Easy integration
- Good developer experience
- Automatic API documentation

FastAPI is a common choice for this type of Python ML service.

The current project does not yet require an API for the inference pipeline to function.

---

# 28. Deployment Packaging

A production deployment would typically package:

    Source Code
        +
    Dependencies
        +
    Configuration
        +
    Model Artifact
        +
    Preprocessor Artifact

Potential dependency management can use:

    requirements.txt

or a modern Python project configuration such as:

    pyproject.toml

The important goal is reproducibility.

---

# 29. Environment Reproducibility

A model can fail in production if the environment differs significantly from the training environment.

Important dependencies include:

- pandas
- numpy
- scikit-learn
- xgboost
- shap
- joblib
- PyYAML

The project should keep dependency versions controlled for reproducible deployment.

---

# 30. Model Serialization

The project uses:

    joblib

to serialize the trained model and preprocessing artifacts.

Conceptually:

    Trained Object
          |
          v
       joblib.dump()
          |
          v
       .pkl file
          |
          v
       joblib.load()
          |
          v
    Reconstructed Object

This allows the trained objects to be reused without retraining.

---

# 31. Serialization Considerations

Pickle/joblib-based model files should be treated as trusted artifacts.

Loading arbitrary untrusted serialized objects can be unsafe because deserialization mechanisms can execute code.

Therefore:

- Do not load model files from untrusted sources.
- Keep model artifacts controlled.
- Validate artifact provenance.
- Keep model and dependency versions compatible.

This is especially important in production systems.

---

# 32. Input Validation in Production

The current inference pipeline assumes that the input has the expected structure.

A production API should additionally validate:

- Required columns
- Data types
- Allowed categorical values
- Numeric ranges
- Missing values
- Invalid requests

For example:

    tenure < 0

should be rejected.

Similarly:

    MonthlyCharges = "abc"

should not be accepted as valid customer input.

---

# 33. Training-Time vs Inference-Time Validation

The project already contains a data-validation component for dataset validation.

In production, validation should exist at two levels.

## Training Validation

Checks whether the training dataset is valid.

## Inference Validation

Checks whether an individual prediction request is valid.

Conceptually:

    Training Data
         |
         v
    Training Validation

and:

    API Input
         |
         v
    Request Validation

Both protect the model from invalid data.

---

# 34. Data Drift

After deployment, customer behavior may change.

This is known as:

**Data drift**

Examples:

- Pricing changes
- New services
- New contract types
- Changes in customer demographics
- Changes in payment behavior

A model trained on historical data may become less effective when the input distribution changes.

---

# 35. Concept Drift

A more serious situation occurs when the relationship between features and churn changes.

This is commonly referred to as:

**Concept drift**

For example:

    Historical pattern:
    Month-to-month contract -> high churn

After a product change:

    Month-to-month contract -> low churn

The feature distribution may remain similar, but the relationship with the target has changed.

This can reduce model performance.

---

# 36. Model Monitoring

A production deployment should monitor:

### Data quality

- Missing values
- Invalid values
- Unexpected categories
- Schema changes

### Data drift

- Feature distribution changes

### Prediction distribution

- Churn probability distribution
- High/medium/low risk proportions

### Model performance

When actual outcomes become available:

- Accuracy
- Precision
- Recall
- F1
- ROC-AUC

### System health

- API latency
- Error rate
- Throughput
- Resource usage

---

# 37. Retraining Strategy

A deployed churn model should eventually be retrained when its performance deteriorates or the underlying data changes significantly.

A possible workflow is:

    Monitor
       |
       v
    Detect Drift / Performance Drop
       |
       v
    Collect New Data
       |
       v
    Retrain
       |
       v
    Evaluate
       |
       v
    Validate
       |
       v
    Deploy New Model

Retraining frequency should be determined by the business and the rate at which customer behavior changes.

---

# 38. Model Versioning

A production system should track model versions.

For example:

    model_v1
    model_v2
    model_v3

Each version should ideally record:

- Training data version
- Feature definitions
- Model algorithm
- Hyperparameters
- Evaluation metrics
- Training date
- Dependency versions

This makes model changes auditable.

---

# 39. Current Project vs Production System

The current project provides:

- Reusable transformation logic
- Saved preprocessor
- Saved model
- Configuration-driven paths
- Prediction pipeline
- Probability output
- Risk classification
- Unit tests

A full production system would additionally require:

- API service
- Authentication/authorization
- Request validation
- Logging
- Monitoring
- Model versioning
- Deployment infrastructure
- CI/CD
- Drift detection
- Retraining workflow

The current project intentionally demonstrates the core ML deployment architecture without introducing unnecessary infrastructure complexity.

---

# 40. Testing the Prediction Pipeline

The project includes:

    tests/test_prediction_pipeline.py

The prediction pipeline was tested as part of the project's test suite.

The current test suite completed successfully:

    4 passed
    0 warnings

This confirms that the core components and prediction pipeline behave as expected under the implemented tests.

---

# 41. Unit Testing vs Integration Testing

A production ML project should test different layers.

## Unit Tests

Test individual components.

Examples:

    DataValidation
    DataTransformation
    FeatureEngineer
    PredictPipeline

## Integration Tests

Test whether multiple components work together.

For example:

    Raw Input
       |
       v
    Transformation
       |
       v
    Preprocessor
       |
       v
    Model
       |
       v
    Prediction

The current project has basic unit tests and a prediction-pipeline test.

---

# 42. Deployment Failure Scenarios

A production inference service should consider failures such as:

### Missing input column

    customerID missing

### Invalid numeric value

    MonthlyCharges = "unknown"

### Unexpected category

    Contract = "NewContractType"

### Missing model artifact

    best_model.pkl not found

### Missing preprocessor

    preprocessor.pkl not found

### Incompatible artifact

    Model expects a different feature structure

### Configuration error

    Incorrect artifact path

These should result in controlled errors rather than silent incorrect predictions.

---

# 43. Prediction Latency

For real-time systems, latency matters.

The prediction process consists of:

    Input validation
          |
          v
    Transformation
          |
          v
    Preprocessing
          |
          v
    Model inference
          |
          v
    Response

For a tree-based tabular model, inference is generally lightweight compared with model training.

However, production latency should still be measured rather than assumed.

---

# 44. Batch Efficiency

For batch prediction, processing customers individually may be inefficient.

Instead of:

    Customer 1 -> Predict
    Customer 2 -> Predict
    Customer 3 -> Predict
    ...

it is generally preferable to process a DataFrame containing many customers:

    Customers DataFrame
            |
            v
       Transform Once
            |
            v
       Batch Inference
            |
            v
       Prediction DataFrame

This can improve throughput.

---

# 45. Security Considerations

A deployed ML prediction service should also consider security.

Important areas include:

- Input validation
- Authentication
- Authorization
- Rate limiting
- Secure artifact storage
- Dependency security
- Logging without exposing sensitive customer data

The current project is a learning/portfolio implementation and does not implement these production controls.

---

# 46. Privacy Considerations

Customer information can contain sensitive business or personal data.

A production deployment should follow the organization's privacy and data-governance requirements.

Important principles include:

- Minimize data collection
- Avoid logging unnecessary customer information
- Control access to prediction data
- Protect stored artifacts and logs
- Follow applicable privacy regulations

The model itself should not become a reason to expose customer data unnecessarily.

---

# 47. Explainability in Deployment

The deployed prediction system currently returns:

    Prediction
    Probability
    Risk Level

A future version could also return explanation information.

For example:

    {
      "churn_prediction": "Yes",
      "churn_probability": 0.7631,
      "risk_level": "High",
      "top_factors": [...]
    }

This could help customer-success teams understand why a customer was prioritized.

However, explanations should be translated carefully into business language and should not be presented as causal statements.

---

# 48. End-to-End Production Architecture

A more complete future architecture could look like:

    Customer / Application
             |
             v
          API Layer
             |
             v
       Input Validation
             |
             v
       PredictPipeline
             |
       +-----+------+
       |            |
       v            v
    Transform    Preprocessor
       |            |
       +-----+------+
             |
             v
        ML Model
             |
             +----------------+
             |                |
             v                v
        Prediction       Explanation
             |                |
             +-------+--------+
                     |
                     v
                API Response
                     |
                     v
               Monitoring

This is the natural evolution of the current project.

---

# 49. Current Deployment Architecture in the Repository

The important deployment-related components are:

    config.yaml

    src/
        components/
            data_transformation.py
            feature_engineering.py
            model_trainer.py
        predict_pipeline.py
        utils/
            config.py

    artifacts/
        best_model.pkl
        preprocessor.pkl
        feature_names.pkl

The model and preprocessor artifacts are generated by the training workflow and consumed by the prediction workflow.

---

# 50. Why This Design is Reusable

The deployment logic does not need to know how the model was trained.

It only needs:

    Input Data
       +
    Transformation Logic
       +
    Preprocessor
       +
    Model

This separation allows the training and inference workflows to evolve independently.

For example, the model can be retrained with newer data while the inference interface remains conceptually the same.

---

# 51. Important Model-Artifact Compatibility Rule

The model and preprocessor should always be treated as a compatible pair.

For example:

    Model A
    +
    Preprocessor A

is valid.

But:

    Model A
    +
    Preprocessor B

may produce incorrect results if the feature structure differs.

A production system should therefore version or package compatible artifacts together.

---

# 52. Better Production Packaging

A future improvement would be to package the entire preprocessing and model pipeline together.

Conceptually:

    Raw Input
        |
        v
    Full sklearn Pipeline
        |
        +--> Preprocessing
        |
        +--> Model
        |
        v
    Prediction

This can reduce the risk of accidentally loading incompatible preprocessing and model artifacts.

The current project keeps the preprocessor and model as separate artifacts because it explicitly demonstrates the individual pipeline stages.

---

# 53. Deployment Checklist

Before deploying a model, verify:

### Data

- [ ] Required fields are present
- [ ] Data types are valid
- [ ] Numeric ranges are valid
- [ ] Categories are handled
- [ ] Missing values are handled

### Model

- [ ] Correct model artifact loaded
- [ ] Correct preprocessor loaded
- [ ] Feature ordering is compatible
- [ ] Model version is known

### Configuration

- [ ] Artifact paths are correct
- [ ] Risk thresholds are correct
- [ ] Environment configuration is available

### Testing

- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Prediction response is validated

### Operations

- [ ] Logging configured
- [ ] Monitoring configured
- [ ] Errors handled
- [ ] Retraining process defined

### Security

- [ ] Artifacts are trusted
- [ ] Input is validated
- [ ] Access is controlled
- [ ] Sensitive data is protected

---

# 54. Interview Explanation

A concise interview explanation would be:

> "For deployment, I separated the inference workflow from model training. During training, I fitted and saved the preprocessing pipeline and the selected XGBoost model. During inference, the PredictPipeline loads those artifacts, applies the same data transformation and fitted preprocessor to new customer data, and then generates both a churn label and probability. I also convert the probability into configurable high, medium and low risk bands. I deliberately keep the preprocessing used during inference identical to training to avoid feature-order and transformation inconsistencies. For a production deployment, I would expose this pipeline through an API such as FastAPI and add input validation, logging, monitoring, model versioning, drift detection and a retraining workflow."

---

# 55. Common Interview Questions

## Why do you save the preprocessor?

Because the model expects data transformed in exactly the same way as the training data.

The fitted imputation statistics, scaling parameters and one-hot encoding mappings must be reused.

---

## Why can't you fit the preprocessor again on new data?

Because doing so can change the transformation.

For example, scaling statistics or categorical mappings could differ.

This creates training-serving skew.

---

## What is training-serving skew?

It is a mismatch between how data is processed during training and how it is processed during inference.

This can cause the model to receive data in a different representation from what it learned.

---

## What does your prediction pipeline return?

It returns:

- Churn prediction
- Churn probability
- Risk level

---

## Why return probability instead of only the label?

Probability allows the business to rank customers and create different risk segments.

---

## Are the 0.40 and 0.70 thresholds model parameters?

No.

They are business rules used to convert probabilities into risk categories.

They can be changed without retraining the model.

---

## How would you deploy this model as an API?

I would expose the `PredictPipeline` through an API framework such as FastAPI.

A client would send customer data to a prediction endpoint.

The API would validate the request, invoke the pipeline and return a JSON response containing the churn prediction, probability and risk level.

---

## How would you monitor the model after deployment?

I would monitor:

- Input data quality
- Data drift
- Prediction distributions
- Model performance when labels become available
- API latency
- Error rates

---

## How would you know when to retrain?

I would define business and technical triggers such as:

- Significant data drift
- Declining ROC-AUC
- Declining recall or precision
- Changes in customer behavior
- Introduction of new product/service categories

Retraining would then go through the same evaluation and validation process before deployment.

---

## What happens if a new category appears?

The categorical encoder uses:

    handle_unknown="ignore"

so an unseen category does not cause the transformation to fail.

For production, I would also monitor such occurrences because frequent unseen categories may indicate schema or data-distribution changes.

---

## How would you scale this system?

For batch prediction, process customers in batches.

For real-time prediction, deploy the prediction service behind an API and scale service instances horizontally depending on traffic.

Model loading should generally happen when the service starts rather than loading the model for every request.

---

# 56. Current Project Status

At this point, the project has a complete core ML lifecycle:

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
    SHAP Explainability
            |
            v
    Model Persistence
            |
            v
    Prediction Pipeline

The core system can therefore train a model and use the saved artifacts to make predictions on new customer data.

---

# 57. Final Conclusion

The deployment stage converts the trained machine learning model into a reusable inference component.

The most important design principle is consistency:

> The same data transformation and fitted preprocessing logic used during training must be reused during inference.

The current project achieves this by saving:

    artifacts/best_model.pkl

and:

    artifacts/preprocessor.pkl

The `PredictPipeline` then loads these artifacts, transforms new customer data and returns:

    Churn Prediction
    Churn Probability
    Risk Level

The current implementation is intentionally lightweight, but it provides the foundation for a production deployment.

The next logical step is to expose the prediction pipeline through an API, add stronger input validation and introduce production concerns such as logging, monitoring, model versioning and drift detection.
'''
