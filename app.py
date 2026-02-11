import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os

# Paths
MODEL_PATH = r'D:\FraudDetectionSystem\ml\fraud_model.pkl'
DATA_PATH = r'D:\FraudDetectionSystem\data\creditcard.csv'

# Load model
model = joblib.load(MODEL_PATH)

st.title("Fraud Detection System (Banking / FinTech)")

# User inputs
st.sidebar.header("Transaction Input")
columns = pd.read_csv(DATA_PATH).drop('Class', axis=1).columns
input_data = {}

for col in columns:
    input_data[col] = st.sidebar.number_input(f"{col}", value=0.0, format="%.5f")

if st.button("Predict Fraud / Legit"):
    X_new = pd.DataFrame([input_data])
    prediction = model.predict(X_new)[0]
    st.success(f"Transaction predicted as: {'Fraud' if prediction==1 else 'Legit'}")
