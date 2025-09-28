import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np

# ------- Page config -------
st.set_page_config(page_title="DTF Cost Range Calculator", layout="wide")

# ------- Sidebar inputs (editable) -------
st.sidebar.header("Cost & Consumption Settings (EGP)")

# Film / roll
film_roll_price = st.sidebar.number_input("Film roll price (EGP per roll)", value=1800.0, step=10.0)
roll_length_m = st.sidebar.number_input("Roll length (meters)", value=100.0, step=1.0)
film_cost_per_m = film_roll_price / roll_length_m

# Ink price
ink_price_per_l = st.sidebar.number_input("Ink price (EGP per liter)", value=1350.0, step=10.0)
ink_price_per_ml = ink_price_per_l / 1000.0

# Powder price
powder_price_per_kg = st.sidebar.number_input("Powder price (EGP per kg)", value=450.0, step=5.0)
powder_price_per_g = powder_price_per_kg / 1000.0

st.sidebar.markdown("---")
st.sidebar.subheader("Ink consumption (ml per meter at 60cm width)")
ink_ml_per_m_min = st.sidebar.number_input("Ink min (ml/m)", value=4.0, step=0.5)
ink_ml_per_m_avg = st.sidebar.number_input("Ink avg (ml/m)", value=6.0, step=0.5)
ink_ml_per_m_max = st.sidebar.number_input("Ink max (ml/m)", value=8.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.subheader("Powder consumption (g per meter at 60cm width)")
powder_g_per_m_min = st.sidebar.number_input("Powder min (g/m)", value=8.0, step=0.5)
powder_g_per_m_avg = st.sidebar.number_input("Powder avg (g/m)", value=10.0, step=0.5)
powder_g_per_m_max = st.sidebar.number_input("Powder max (g/m)", value=12.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.subheader("Monthly overhead")
labor_monthly = st.sidebar.number_input("Labor monthly cost (EGP)", value=85000.0, step=1000.0)
electricity_monthly = st.sidebar.number_input("Electricity monthly cost (EGP)", value=15000.0, step=500.0)
monthly_output_m = st.sidebar.number_input("Monthly production (meters)", value=4000.0, step=50.0)

# ------- Main UI -------
st.title("DTF Cost Calculator — Min → Avg → Max for Ink & Powder")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("1) Upload design (optional) or enter length manually")
    uploaded_file = st.file_uploader("Upload design (PNG/TIFF/JPG) — optional (we won't read DPI for length)", type=["png","tif","tiff","jpg","jpeg"])
    st.info("Important: enter the design LENGTH (height) manually below (cm). This ensures correct length even if image DPI is missing/wrong).")

with col2:
    st.subheader("Quick reference")
    st.write(f"Film cost per meter: **{film_cost_per_m:.2f} EGP/m**")
    st.write(f"Ink price per ml: **{ink_price_per_ml:.3f} EGP/ml**")
    st.write(f"Powder price per g: **{powder_price_per_g:.3f} EGP/g**")
    st.write(f"Overhead per meter (approx): **{(labor_monthly+electricity_monthly)/monthly_output_m:.2f} EGP/m**")

st.markdown("---")

# 2) manual inputs
st.subheader("2) Design dimensions & coverage")
design_height_cm = st.number_input("Design length / height (cm)", value=150.0, step=1.0)  # user-controlled
fixed_width_cm = 60.0  # fixed

# If file uploaded, optionally compute auto coverage from alpha channel (show result but let user override)
auto_coverage_pct = None
if uploaded_file:
    img = Image.open(uploaded_file).convert("RGBA")
    arr = np.array(img)
    alpha = arr[:, :, 3]
    auto_coverage_frac = (alpha > 0).sum() / alpha.size
    auto_coverage_pct = float(round(auto_coverage_frac * 100, 1))
    st.write(f"Estimated coverage from image (alpha non-empty pixels): **{auto_coverage_pct:.1f}%**")

# coverage slider (default uses auto estimate if available)
default_coverage = int(auto_coverage_pct) if auto_coverage_pct is not None else 100
coverage_pct = st.slider("Printing coverage (%) — adjust as needed", min_value=0, max_value=100, value=default_coverage)

# convert lengths
length_m = design_height_cm / 100.0
area_m2 = (fixed_width_cm / 100.0) * length_m  # area of the printed stripe in m²

st.write(f"Design length: **{length_m:.3f} m** — Design area (60cm × length): **{area_m2:.3f} m²**")
st.write(f"Coverage (fraction): **{coverage_pct}%** → effective printed area: **{area_m2 * (coverage_pct/100):.3f} m²**")

# ------- Calculations -------
st.markdown("---")
st.subheader("3) Cost calculation (range)")

# Film cost (linear meters)
film_cost_total = film_cost_per_m * length_m  # single value

# Ink totals (min/avg/max)
ink_ml_total_min = ink_ml_per_m_min * (coverage_pct/100.0) * length_m
ink_ml_total_avg = ink_ml_per_m_avg * (coverage_pct/100.0) * length_m
ink_ml_total_max = ink_ml_per_m_max * (coverage_pct/100.0) * length_m

ink_cost_min = ink_ml_total_min * ink_price_per_ml
ink_cost_avg = ink_ml_total_avg * ink_price_per_ml
ink_cost_max = ink_ml_total_max * ink_price_per_ml

# Powder totals
powder_g_total_min = powder_g_per_m_min * (coverage_pct/100.0) * length_m
powder_g_total_avg = powder_g_per_m_avg * (coverage_pct/100.0) * length_m
powder_g_total_max = powder_g_per_m_max * (coverage_pct/100.0) * length_m

powder_cost_min = powder_g_total_min * powder_price_per_g
powder_cost_avg = powder_g_total_avg * powder_price_per_g
powder_cost_max = powder_g_total_max * powder_price_per_g

# Overhead
overhead_per_m = (labor_monthly + electricity_monthly) / monthly_output_m if monthly_output_m > 0 else 0.0
overhead_total = overhead_per_m * length_m

# Totals min/avg/max
total_min = film_cost_total + ink_cost_min + powder_cost_min + overhead_total
total_avg = film_cost_total + ink_cost_avg + powder_cost_avg + overhead_total
total_max = film_cost_total + ink_cost_max + powder_cost_max + overhead_total

# ------- Output table -------
st.subheader("4) Results — cost range for this file (EGP)")

rows = [
    ["Film (EGP)", f"{film_cost_total:.2f}", f"{film_cost_total:.2f}", f"{film_cost_total:.2f}"],
    ["Ink (EGP)", f"{ink_cost_min:.2f}", f"{ink_cost_avg:.2f}", f"{ink_cost_max:.2f}"],
    ["Powder (EGP)", f"{powder_cost_min:.2f}", f"{powder_cost_avg:.2f}", f"{powder_cost_max:.2f}"],
    ["Overhead (EGP)", f"{overhead_total:.2f}", f"{overhead_total:.2f}", f"{overhead_total:.2f}"],
    ["TOTAL (EGP)", f"{total_min:.2f}", f"{total_avg:.2f}", f"{total_max:.2f}"]
]

result_df = pd.DataFrame(rows, columns=["Item", "Min", "Average", "Max"]).set_index("Item")
st.table(result_df)

st.markdown(f"**Printed linear length:** {length_m:.3f} m — **Coverage:** {coverage_pct}% — **Effective printed area:** {area_m2 * (coverage_pct/100):.3f} m²")

# Optional: downloadable CSV
csv = result_df.to_csv().encode("utf-8")
st.download_button("Download cost table (CSV)", csv, "dtf_costs_range.csv", "text/csv")
