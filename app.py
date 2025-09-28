import streamlit as st

st.set_page_config(page_title="Main Menu", layout="wide")

st.title("Choose an Option")

col1, col2 = st.columns(2)

with col1:
    if st.button(""):
        st.switch_page("pages/1_Calculator.py")
    st.markdown(
        """
        <img src="https://img.freepik.com/free-vector/calculator-floating-cartoon-vector-icon-illustration-finance-business-icon-concept-isolated-flat_138676-9297.jpg" 
        style="width:100%; border-radius:15px; cursor:pointer;">
        """,
        unsafe_allow_html=True
    )

with col2:
    if st.button(" "):
        st.switch_page("pages/2_Reports.py")
    st.markdown(
        """
        <img src="https://holistiquetraining.com/storage/write-a-report.jpg" 
        style="width:100%; border-radius:15px; cursor:pointer;">
        """,
        unsafe_allow_html=True
    )
