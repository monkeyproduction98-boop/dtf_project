import streamlit as st

st.set_page_config(page_title="Main Menu", layout="wide")

st.title("Choose an Option")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        <a href="/dtf_dashboard" target="_self">
            <img src="https://img.freepik.com/free-vector/calculator-floating-cartoon-vector-icon-illustration-finance-business-icon-concept-isolated-flat_138676-9297.jpg" 
            style="width:100%; border-radius:15px;">
        </a>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        """
        <a href="/reports" target="_self">
            <img src="https://holistiquetraining.com/storage/write-a-report.jpg" 
            style="width:100%; border-radius:15px;">
        </a>
        """,
        unsafe_allow_html=True
    )
