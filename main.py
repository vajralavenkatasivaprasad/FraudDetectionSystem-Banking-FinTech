import streamlit as st
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Fraud Detection System",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = None

# Custom styling
st.markdown("""
<style>
    [data-testid="stSidebar"] {
        background-color: #1e3a8a;
    }
    
    .main {
        background-color: #f8f9fa;
    }
    
    h1, h2, h3 {
        color: #1f77b4;
    }
    
    .stButton > button {
        background-color: #667eea;
        color: white;
        border-radius: 5px;
    }
    
    .stButton > button:hover {
        background-color: #764ba2;
    }
</style>
""", unsafe_allow_html=True)

# Redirect to login if not authenticated
if not st.session_state.logged_in:
    st.switch_page("login.py")
else:
    # Show home page
    st.switch_page("pages/home.py")