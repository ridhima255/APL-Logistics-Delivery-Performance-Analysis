import streamlit as st
import pandas as pd
import plotly.express as px

# PAGE CONFIGURATION
st.set_page_config(
    page_title="APL Logistics Dashboard",
    page_icon="📦",
    layout="wide"
)

# TITLE
st.title("📦 APL Logistics Dashboard")

st.subheader(
    "Delivery Performance & Delay Risk Analysis"
)

# LOAD DATA
df = pd.read_csv(
    "data/APL_Logistics.csv",
    encoding="latin1"
)

# DATA PREVIEW
st.subheader("Dataset Preview")

st.dataframe(df.head())