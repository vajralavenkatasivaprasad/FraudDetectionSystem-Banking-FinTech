
import streamlit as st
import pandas as pd
import joblib
import numpy as np
import time

st.set_page_config(page_title="Fraud Detection System", layout="wide")

st.title("🏦 Fraud Detection System (Banking / FinTech)")
st.write("Real-Time Transaction Fraud Detection Dashboard")

# Load model safely
@st.cache_resource
def load_model():
    try:
        return joblib.load("fraud_model.pkl")
    except FileNotFoundError:
        st.error("Model file 'fraud_model.pkl' not found.")
        return None

model = load_model()

# Use the model’s actual training columns
columns = list(model.feature_names_in_) if model is not None else []

fraud_count = 0
legit_count = 0

st.subheader("Live Fraud Simulation")

run = st.button("Start Simulation")

if run and model is not None:
    chart_data = pd.DataFrame({"Fraud": [0], "Legit": [0]})
    chart = st.line_chart(chart_data)

    for i in range(20):
        # Generate random transaction with correct number of features
        transaction = np.random.randn(len(columns))
        transaction_df = pd.DataFrame([transaction], columns=columns)

        prediction = model.predict(transaction_df)[0]

        if prediction == 1:
            fraud_count += 1
            st.error(f"Transaction {i+1}: FRAUD")
        else:
            legit_count += 1
            st.success(f"Transaction {i+1}: LEGIT")

        new_data = pd.DataFrame({"Fraud": [fraud_count], "Legit": [legit_count]})
        chart.add_rows(new_data)

        time.sleep(0.5)

st.subheader("Manual Transaction Check")

input_data = []
for col in columns:
    value = st.number_input(f"Feature {col}", value=0.0)
    input_data.append(value)

if st.button("Predict Manual Transaction") and model is not None:
    input_df = pd.DataFrame([input_data], columns=columns)
    prediction = model.predict(input_df)[0]
    if prediction == 1:
        st.error("⚠ Fraud Transaction Detected")
    else:
        st.success("✅ Legit Transaction")


