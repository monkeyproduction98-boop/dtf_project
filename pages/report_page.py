# pages/report_page.py
import os
import io
import pandas as pd
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Reports", layout="wide")


def _get_dpi(img):
    """
    Try several ways to get DPI (pixels per inch) from the image.
    Fallback to 300 if we can't find a reliable DPI.
    """
    # 1) Pillow info
    dpi_info = img.info.get("dpi")
    if dpi_info:
        try:
            if isinstance(dpi_info, (tuple, list)):
                # (x_dpi, y_dpi)
                dpi = float(dpi_info[1] or dpi_info[0])
            else:
                dpi = float(dpi_info)
            if dpi > 0:
                return dpi
        except Exception:
            pass

    # 2) TIFF tags (common for .tif) using tag_v2
    try:
        tags = getattr(img, "tag_v2", None)
        if tags:
            xres = tags.get(282)  # XResolution
            yres = tags.get(283)  # YResolution
            resunit = tags.get(296)  # ResolutionUnit: 2=inches, 3=cm

            def to_float(v):
                try:
                    return float(v)
                except Exception:
                    # IFDRational or tuple like (num, den)
                    try:
                        if hasattr(v, "numerator") and hasattr(v, "denominator"):
                            return v.numerator / v.denominator
                        if isinstance(v, (tuple, list)) and len(v) >= 2:
                            return float(v[0]) / float(v[1])
                    except Exception:
                        return None
                return None

            val = None
            if yres is not None:
                val = to_float(yres)
            elif xres is not None:
                val = to_float(xres)

            if val:
                # if resolution unit == 3 it's per cm, convert to per inch
                if resunit == 3:
                    val = val * 2.54
                if val > 0:
                    return val
    except Exception:
        pass

    # fallback
    return 300.0


st.title("📊 Reports — TIF folder → client summary")

st.info(
    "You can either (A) upload multiple .tif files directly (works on Streamlit Cloud), "
    "or (B) enter a local folder path (works only when you run this app locally)."
)

# --- Inputs: upload OR folder path ---
uploaded_files = st.file_uploader(
    "Upload TIF files (select multiple) — OR leave empty and use folder path below",
    type=["tif", "tiff"],
    accept_multiple_files=True,
)

folder_path = st.text_input("Or enter folder path (local path, e.g. C:\\\\folder\\tifs):", "")

# collect files to process: tuples of (filename, fileobj_or_path, is_uploaded)
files_to_process = []

if uploaded_files:
    for f in uploaded_files:
        # f is a UploadedFile-like object; PIL can open it directly
        files_to_process.append((f.name, f, True))
elif folder_path:
    if os.path.isdir(folder_path):
        for fname in os.listdir(folder_path):
            if fname.lower().endswith((".tif", ".tiff")):
                files_to_process.append((fname, os.path.join(folder_path, fname), False))
    else:
        st.warning("Folder path is not valid or not accessible from the server. If you're on Streamlit Cloud, use Upload instead.")
        files_to_process = []

if not files_to_process:
    st.info("No files selected yet. Upload TIFs or type a valid local folder path and press Enter.")
    st.stop()

# --- Process files ---
rows = []
errors = []
for fname, source, is_uploaded in files_to_process:
    try:
        name_no_ext = os.path.splitext(fname)[0].strip()
        # split from the right 2 parts so names with dashes in client are OK: a-b-c  (rsplit)
        parts = name_no_ext.rsplit("-", 2)
        if len(parts) != 3:
            errors.append(f"Filename not in a-b-c format: {fname}")
            continue
        client = parts[0].strip()
        order_s = parts[1].strip()
        copies_s = parts[2].strip()
        try:
            order = int(order_s)
            copies = int(copies_s)
        except Exception:
            errors.append(f"Order or copies not integer in file: {fname}")
            continue

        # open image
        if is_uploaded:
            img = Image.open(source)
        else:
            img = Image.open(source)

        # ensure RGBA or at least we can read height
        height_px = getattr(img, "height", img.size[1])

        dpi = _get_dpi(img)
        # calculate length in meters: height_px / dpi (inch) * 0.0254 m/in
        length_m = (height_px / dpi) * 0.0254

        p_val = copies * length_m

        rows.append(
            {
                "Client": client,
                "Order": order,
                "Copies (c)": copies,
                "Length (d, m)": round(length_m, 4),
                "c*d": round(p_val, 4),
                "File": fname,
            }
        )
    except Exception as e:
        errors.append(f"Error processing {fname}: {e}")

# --- Build DataFrames and summary ---
if not rows:
    st.error("No valid TIF files processed. Check filenames and file contents.")
    if errors:
        st.write("Errors:")
        for e in errors:
            st.write("- " + e)
    st.stop()

df = pd.DataFrame(rows)
# summary per client: Number of Orders = max order, P = sum(c*d)
summary = (
    df.groupby("Client", as_index=False)
    .agg({"Order": "max", "c*d": "sum"})
    .rename(columns={"Order": "Number of Orders", "c*d": "P (Σ c*d)"})
)

st.subheader("📌 Summary per Client")
st.dataframe(summary, use_container_width=True)

st.subheader("📂 Raw Files Processed")
st.dataframe(df.sort_values(["Client", "Order"]), use_container_width=True)

# show any errors
if errors:
    st.subheader("⚠️ Warnings / Errors")
    for e in errors:
        st.write("- " + e)

# --- Download CSV ---
csv = summary.to_csv(index=False).encode("utf-8")
st.download_button("Download summary CSV", csv, "report_summary.csv", "text/csv")
