import os
import pandas as pd
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Reports", layout="wide")

def run_report_page():
    st.title("📊 Reports")

    # إدخال مسار الفولدر
    folder_path = st.text_input("Enter folder path containing TIF files:")

    if folder_path and os.path.isdir(folder_path):
        data = []

        for file in os.listdir(folder_path):
            if file.lower().endswith(".tif"):
                try:
                    # تقسيم الاسم a-b-c
                    name, order, count = file.replace(".tif", "").split("-")
                    order = int(order)
                    count = int(count)

                    # فتح الصورة لاستخراج الطول
                    img_path = os.path.join(folder_path, file)
                    img = Image.open(img_path)

                    dpi = img.info.get("dpi", (300, 300))  # default لو مش موجود
                    dpi_y = dpi[1]

                    height_px = img.height
                    d_meters = (height_px / dpi_y) * 0.0254  # px → inches → meters

                    # P = c * d
                    p_value = count * d_meters

                    data.append([name, order, count, round(d_meters, 3), round(p_value, 3)])

                except Exception as e:
                    st.warning(f"⚠️ Error reading file {file}: {e}")

        if data:
            df = pd.DataFrame(
                data,
                columns=["Client", "Order", "Copies (c)", "Length (d, m)", "c*d"]
            )

            # ملخص لكل عميل
            summary = df.groupby("Client").agg({
                "Order": "max",
                "c*d": "sum"
            }).reset_index()

            summary.rename(columns={
                "Order": "Number of Orders",
                "c*d": "P (Σ c*d)"
            }, inplace=True)

            st.subheader("📌 Summary per Client")
            st.dataframe(summary, use_container_width=True)

            st.subheader("📂 Raw Data")
            st.dataframe(df, use_container_width=True)

        else:
            st.info("No TIF files found in this folder.")
    else:
        st.info("Please enter a valid folder path.")

# 🔥 شغل الصفحة فعلاً
run_report_page()
