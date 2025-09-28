import streamlit as st
from calculator_page import run_calculator_page
from report_page import run_report_page

st.set_page_config(page_title="DTF Multi-Tool", layout="wide")

st.title("Welcome to DTF Multi-Tool")

option = st.radio(
    "Choose a tool:",
    ["🧮 Cost Calculator", "📊 Reports"]
)

if option == "🧮 Cost Calculator":
    run_dtf_dashboard()
elif option == "📊 Reports":
    run_report_page()

