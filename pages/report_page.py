import os
import pandas as pd
import streamlit as st
from PIL import Image

def run_report_page():
    st.title("📊 Reports")

    # اختيار فولدر
    folder_path = st.text_input("Enter folder path containing TIF files:")

    if folder_path and os.path.isdir(folder_path):
        data = []

        for file in os.listdir(folder_path):
            if file.lower().endswith(".tif"):
                try:
                    # Split filename a-b-c
                    name, order, count = file.replace(".tif", "").split("-")
                    order = int(order)
                    count = int(count)

                    # فتح الصورة عشان نجيب الطول بالمتر
                    img_path = os.path.join(folder_path, file)
                    img = Image.open(img_path)

                    dpi = img.info.get("dpi", (300, 300))  # Default DPI لو ناقص
                    dpi_y = dpi[1]

                    height_px = img.height
                    d_meters = (height_px / dpi_y) * 0.0254  # inches → meters

                    # P = c * d
                    p_value = count * d_meters

                    data.append([name, order, count, d_meters, p_value])

                except Exception as e:
                    st.warning(f"⚠️ Error reading file {file}: {e}")

        if data:
            df = pd.DataFrame(data, columns=["Client", "Order", "Copies (c)", "Length (d, m)", "c*d"])

            # تجميع البيانات لكل عميل
            summary = df.groupby("Client").agg({
                "Order": "max",
                "c*d": "sum"
            }).reset_index()

            summary.rename(columns={
                "Order": "Number of Orders",
                "c*d": "P (Σ c*d)"
            }, inplace=True)

            st.subheader("📌 Summary per Client")
            st.dataframe(summary)

            st.subheader("📂 Raw Data")
            st.dataframe(df)
        else:
            st.info("No TIF files found in this folder.")
