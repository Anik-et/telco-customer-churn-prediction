import pandas as pd
import streamlit as st

from src.pipeline.predict_pipeline import PredictPipeline


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Telco Customer Churn Prediction",
    page_icon="📊",
    layout="wide"
)


# ---------------------------------------------------------
# Load Prediction Pipeline
# ---------------------------------------------------------

@st.cache_resource
def load_pipeline():
    return PredictPipeline()


try:
    pipeline = load_pipeline()
except Exception as e:
    st.error("Unable to load the prediction pipeline.")
    st.exception(e)
    st.stop()


# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.title("📊 Telco Customer Churn Prediction")

st.markdown(
    """
    Predict the likelihood that a telecom customer will churn
    and identify their business risk level.
    """
)

st.divider()


# ---------------------------------------------------------
# Customer Information
# ---------------------------------------------------------

st.subheader("Customer Information")

col1, col2, col3 = st.columns(3)

with col1:
    gender = st.selectbox(
        "Gender",
        ["Female", "Male"]
    )

    senior_citizen = st.selectbox(
        "Senior Citizen",
        [0, 1],
        format_func=lambda x: "Yes" if x == 1 else "No"
    )

    partner = st.selectbox(
        "Partner",
        ["Yes", "No"]
    )

    dependents = st.selectbox(
        "Dependents",
        ["Yes", "No"]
    )

    tenure = st.number_input(
        "Tenure (months)",
        min_value=0,
        max_value=100,
        value=12
    )

with col2:
    phone_service = st.selectbox(
        "Phone Service",
        ["Yes", "No"]
    )

    multiple_lines = st.selectbox(
        "Multiple Lines",
        ["Yes", "No", "No phone service"]
    )

    internet_service = st.selectbox(
        "Internet Service",
        ["DSL", "Fiber optic", "No"]
    )

    online_security = st.selectbox(
        "Online Security",
        ["Yes", "No", "No internet service"]
    )

    online_backup = st.selectbox(
        "Online Backup",
        ["Yes", "No", "No internet service"]
    )

with col3:
    device_protection = st.selectbox(
        "Device Protection",
        ["Yes", "No", "No internet service"]
    )

    tech_support = st.selectbox(
        "Tech Support",
        ["Yes", "No", "No internet service"]
    )

    streaming_tv = st.selectbox(
        "Streaming TV",
        ["Yes", "No", "No internet service"]
    )

    streaming_movies = st.selectbox(
        "Streaming Movies",
        ["Yes", "No", "No internet service"]
    )


# ---------------------------------------------------------
# Account & Billing Information
# ---------------------------------------------------------

st.subheader("Account & Billing Information")

col1, col2, col3 = st.columns(3)

with col1:
    contract = st.selectbox(
        "Contract",
        [
            "Month-to-month",
            "One year",
            "Two year"
        ]
    )

    paperless_billing = st.selectbox(
        "Paperless Billing",
        ["Yes", "No"]
    )

with col2:
    payment_method = st.selectbox(
        "Payment Method",
        [
            "Electronic check",
            "Mailed check",
            "Bank transfer (automatic)",
            "Credit card (automatic)"
        ]
    )

with col3:
    monthly_charges = st.number_input(
        "Monthly Charges",
        min_value=0.0,
        value=70.0,
        step=1.0
    )

    total_charges = st.number_input(
        "Total Charges",
        min_value=0.0,
        value=monthly_charges * tenure,
        step=10.0
    )


# ---------------------------------------------------------
# Prediction
# ---------------------------------------------------------

st.divider()

predict_button = st.button(
    "🔮 Predict Churn Risk",
    type="primary",
    use_container_width=True
)


if predict_button:

    customer_data = pd.DataFrame([
        {
            "customerID": "STREAMLIT_CUSTOMER",
            "gender": gender,
            "SeniorCitizen": senior_citizen,
            "Partner": partner,
            "Dependents": dependents,
            "tenure": tenure,
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless_billing,
            "PaymentMethod": payment_method,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges
        }
    ])

    try:
        result = pipeline.predict(customer_data)

        churn_prediction = result["churn_prediction"]
        churn_probability = result["churn_probability"]
        risk_level = result["risk_level"]

        st.subheader("Prediction Result")

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:
            st.metric(
                "Churn Probability",
                f"{churn_probability:.2%}"
            )

        with result_col2:
            st.metric(
                "Prediction",
                "Likely to Churn"
                if churn_prediction == "Yes"
                else "Likely to Stay"
            )

        with result_col3:
            st.metric(
                "Risk Level",
                risk_level
            )

        st.progress(churn_probability)

        if risk_level == "High":

            st.error(
                "⚠️ High churn risk — this customer should be "
                "prioritized for retention action."
            )

        elif risk_level == "Medium":

            st.warning(
                "⚠️ Medium churn risk — consider targeted "
                "retention engagement."
            )

        else:

            st.success(
                "✅ Low churn risk — no immediate retention "
                "intervention is indicated."
            )

    except Exception as e:

        st.error("Prediction failed.")
        st.exception(e)


# ---------------------------------------------------------
# Model Information
# ---------------------------------------------------------

st.divider()

with st.expander("About this model"):

    st.markdown(
        """
        ### Model

        The application uses an XGBoost-based churn prediction model.

        ### Pipeline

        The same preprocessing pipeline used during training is
        applied during inference.

        **Raw Customer Data → Transformation → Preprocessor →
        XGBoost → Churn Probability → Risk Level**

        ### Risk Thresholds

        - **High:** probability ≥ 70%
        - **Medium:** probability ≥ 40%
        - **Low:** probability < 40%

        These risk thresholds are business rules and are separate
        from the model's learned parameters.
        """
    )