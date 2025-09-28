import streamlit as st

st.set_page_config(page_title="Main Menu", layout="wide")

st.markdown(
    """
    <h1 style="text-align:center; margin-bottom:40px;">📌 Main Menu</h1>
    """,
    unsafe_allow_html=True
)

# Layout in two columns
col1, col2 = st.columns(2)

with col1:
    st.markdown(
        f"""
        <div style="border:2px solid #ddd; border-radius:15px; padding:20px; text-align:center; box-shadow:2px 2px 8px rgba(0,0,0,0.1);">
            <img src="https://img.freepik.com/free-vector/calculator-floating-cartoon-vector-icon-illustration-finance-business-icon-concept-isolated-flat_138676-9297.jpg" style="border-radius:10px; margin-bottom:15px; max-width:100%; height:auto;">
            <h3>DTF Calculator</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("🚀 Open DTF Calculator", key="btn1"):
        st.switch_page("pages/dtf_dashboard.py")

with col2:
    st.markdown(
        f"""
        <div style="border:2px solid #ddd; border-radius:15px; padding:20px; text-align:center; box-shadow:2px 2px 8px rgba(0,0,0,0.1);">
            <img src="https://holistiquetraining.com/storage/write-a-report.jpg" style="border-radius:10px; margin-bottom:15px; max-width:100%; height:auto;">
            <h3>Reports</h3>
        </div>
        """,
        unsafe_allow_html=True
    )
    if st.button("📊 Open Reports", key="btn2"):
        st.switch_page("pages/report.py")
