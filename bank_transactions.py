import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px

# Authentication check
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.switch_page("login.py")

st.set_page_config(page_title="Transactions - Fraud Detection", layout="wide")

st.title("💳 Bank Transactions")

# Sidebar
with st.sidebar:
    st.markdown(f"### 👤 {st.session_state.username.upper()}")
    page = st.radio(
        "Navigate:",
        ["🏠 Home", "📊 Dashboard", "💳 Transactions", "🔍 Fraud Analysis", "⚙️ Settings"],
        label_visibility="collapsed"
    )
    
    # Filters
    st.markdown("### Filters")
    status_filter = st.multiselect(
        "Transaction Status",
        ["Completed", "Pending", "Blocked", "Under Review"],
        default=["Completed", "Blocked"]
    )
    
    min_amount = st.slider("Min Amount", 0, 10000, 0)
    max_amount = st.slider("Max Amount", 0, 50000, 50000)
    
    st.divider()
    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.session_state.username = None
        st.switch_page("login.py")

# Generate realistic transaction data
np.random.seed(42)
n_transactions = 100

transaction_data = {
    "Transaction ID": [f"TXN-{100000+i}" for i in range(n_transactions)],
    "Date": pd.date_range(start=datetime.now() - timedelta(days=30), periods=n_transactions, freq="6H"),
    "Amount": np.random.choice(
        np.concatenate([
            np.random.normal(500, 300, int(n_transactions*0.9)),
            np.random.normal(5000, 2000, int(n_transactions*0.1))
        ])
    ).astype(float),
    "Merchant": np.random.choice([
        "Amazon", "Walmart", "Target", "Apple", "Netflix", "Starbucks", 
        "Gas Station", "Hotel Chain", "Restaurant", "Online Gaming"
    ], n_transactions),
    "Status": np.random.choice(["Completed", "Pending", "Blocked", "Under Review"], n_transactions, p=[0.85, 0.05, 0.07, 0.03]),
    "Fraud Probability": np.random.uniform(0, 1, n_transactions),
    "Location": np.random.choice(["New York", "Los Angeles", "Chicago", "Houston", "Miami", "Seattle"], n_transactions),
    "Card Type": np.random.choice(["Debit", "Credit", "Digital Wallet"], n_transactions)
}

df = pd.DataFrame(transaction_data)
df["Amount"] = df["Amount"].abs().round(2)
df["Risk Level"] = df["Fraud Probability"].apply(
    lambda x: "🔴 High" if x > 0.7 else ("🟡 Medium" if x > 0.4 else "🟢 Low")
)
df["Date"] = pd.to_datetime(df["Date"])

# Apply filters
df_filtered = df[
    (df["Status"].isin(status_filter)) &
    (df["Amount"] >= min_amount) &
    (df["Amount"] <= max_amount)
]

# Summary metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Total Transactions",
        len(df_filtered),
        f"{len(df_filtered)} shown"
    )

with col2:
    suspicious = len(df_filtered[df_filtered["Fraud Probability"] > 0.5])
    st.metric(
        "Suspicious Transactions",
        suspicious,
        f"{suspicious/len(df_filtered)*100:.1f}%" if len(df_filtered) > 0 else "0%"
    )

with col3:
    total_volume = df_filtered["Amount"].sum()
    st.metric(
        "Total Volume",
        f"${total_volume:,.2f}",
        f"{len(df_filtered)} txns"
    )

with col4:
    blocked = len(df_filtered[df_filtered["Status"] == "Blocked"])
    st.metric(
        "Blocked",
        blocked,
        f"{blocked} transactions"
    )

st.divider()

# Tabs for different views
tab1, tab2, tab3 = st.tabs(["📋 All Transactions", "📊 Analysis", "🔍 Fraud Details"])

with tab1:
    st.subheader("Transaction List")
    
    # Sort options
    col1, col2 = st.columns([3, 1])
    with col2:
        sort_by = st.selectbox("Sort by", ["Date (Newest)", "Amount (High)", "Amount (Low)", "Risk"])
    
    if sort_by == "Amount (High)":
        df_filtered = df_filtered.sort_values("Amount", ascending=False)
    elif sort_by == "Amount (Low)":
        df_filtered = df_filtered.sort_values("Amount")
    elif sort_by == "Risk":
        df_filtered = df_filtered.sort_values("Fraud Probability", ascending=False)
    
    # Display table
    display_df = df_filtered[["Transaction ID", "Date", "Amount", "Merchant", "Status", "Risk Level", "Location", "Card Type"]].copy()
    display_df["Date"] = display_df["Date"].dt.strftime("%Y-%m-%d %H:%M")
    display_df["Amount"] = display_df["Amount"].apply(lambda x: f"${x:,.2f}")
    
    st.dataframe(display_df, use_container_width=True, hide_index=True)

with tab2:
    st.subheader("Transaction Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Transactions by Merchant**")
        merchant_counts = df_filtered["Merchant"].value_counts().head(10)
        fig = px.bar(x=merchant_counts.index, y=merchant_counts.values,
                     color_discrete_sequence=['#3498db'])
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Transactions by Status**")
        status_counts = df_filtered["Status"].value_counts()
        fig = px.pie(values=status_counts.values, names=status_counts.index,
                     color_discrete_sequence=['#2ecc71', '#f39c12', '#e74c3c', '#95a5a6'])
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Amount Distribution**")
        fig = px.histogram(df_filtered, x="Amount", nbins=30,
                          color_discrete_sequence=['#9b59b6'])
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.write("**Transactions Over Time**")
        daily_txns = df_filtered.groupby(df_filtered["Date"].dt.date).size()
        fig = px.line(x=daily_txns.index, y=daily_txns.values,
                     color_discrete_sequence=['#e74c3c'])
        fig.update_layout(showlegend=False, height=400)
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("Suspicious & Fraudulent Transactions")
    
    fraud_df = df_filtered[df_filtered["Fraud Probability"] > 0.3].sort_values("Fraud Probability", ascending=False)
    
    if len(fraud_df) > 0:
        display_fraud = fraud_df[["Transaction ID", "Date", "Amount", "Merchant", "Status", "Fraud Probability"]].copy()
        display_fraud["Date"] = display_fraud["Date"].dt.strftime("%Y-%m-%d %H:%M")
        display_fraud["Amount"] = display_fraud["Amount"].apply(lambda x: f"${x:,.2f}")
        display_fraud["Fraud Probability"] = display_fraud["Fraud Probability"].apply(lambda x: f"{x*100:.1f}%")
        
        st.warning(f"⚠️ Found {len(fraud_df)} suspicious transactions")
        st.dataframe(display_fraud, use_container_width=True, hide_index=True)
        
        # Download option
        csv = display_fraud.to_csv(index=False)
        st.download_button(
            label="📥 Download Fraud Report",
            data=csv,
            file_name="fraud_transactions.csv",
            mime="text/csv"
        )
    else:
        st.success("✅ No suspicious transactions found in the current filters")