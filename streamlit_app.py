import streamlit as st
import pandas as pd
import joblib
import numpy as np
import time
import random

st.set_page_config(page_title="Fraud Detection System", layout="wide")

st.title("🏦 Fraud Detection System (Banking / FinTech)")
st.write("Real-Time Transaction Fraud Detection Dashboard")

# Load model
@st.cache_resource
def load_model():
    return joblib.load("fraud_model.pkl")

model = load_model()

fraud_count = 0
legit_count = 0

st.subheader("Live Fraud Simulation")

run = st.button("Start Simulation")

if run:
    chart_data = pd.DataFrame({"Fraud": [0], "Legit": [0]})
    chart = st.line_chart(chart_data)

    for i in range(20):
        transaction = np.random.randn(1, 30)

        prediction = model.predict(transaction)[0]

        if prediction == 1:
            fraud_count += 1
            st.error(f"Transaction {i+1}: FRAUD")
        else:
            legit_count += 1
            st.success(f"Transaction {i+1}: LEGIT")

        new_data = pd.DataFrame(
            {"Fraud": [fraud_count], "Legit": [legit_count]}
        )
        chart.add_rows(new_data)

        time.sleep(0.5)

st.subheader("Manual Transaction Check")

input_data = []
for i in range(30):
    value = st.number_input(f"Feature {i+1}", value=0.0)
    input_data.append(value)

if st.button("Predict Manual Transaction"):
    prediction = model.predict([input_data])[0]
    if prediction == 1:
        st.error("⚠ Fraud Transaction Detected")
    else:
        st.success("✅ Legit Transaction")
