import streamlit as st
import numpy as np
import rasterio
import rioxarray as rxr
import xarray as xr
import pandas as pd
import plotly.express as px
from scipy.stats import skew, kurtosis
from PIL import Image
import tempfile
import os
import rasterio
from rasterio.io import MemoryFile
from skimage import exposure

st.set_page_config(layout="wide")

st.title("🛰️ Imagenes de Radar (Alos-Palsar)")
st.markdown("Comparar las polarizaciones (HH,VV,HV,VH) de una imagen ALOS PALSAR")


def load_raster(uploaded_file):
    if uploaded_file is None:
        return None

    with MemoryFile(uploaded_file.read()) as memfile:
        with memfile.open() as dataset:
            arr = dataset.read()

    return arr
    
def apply_clahe(arr, clip_limit=0.05):
    arr = arr.astype("float32")

    # Normalize to 0–1
    arr_norm = (arr - np.nanmin(arr)) / (np.nanmax(arr) - np.nanmin(arr) + 1e-8)

    # Apply CLAHE
    clahe = exposure.equalize_adapthist(arr_norm, clip_limit=clip_limit)

    return clahe

# -------------------------------
# 📂 File uploader
# -------------------------------
col1, col2 = st.columns(2)

with col1:
    file1 = st.file_uploader("Cargar Imagen 1", type=["tif", "tiff"])

with col2:
    file2 = st.file_uploader("Cargar Imagen 2", type=["tif", "tiff"])

# -------------------------------
# 📊 Functions
# -------------------------------
def normalize(arr):
    arr = arr.astype("float32")
    return (arr - np.nanmin(arr)) / (np.nanmax(arr) - np.nanmin(arr))

def compute_stats(arr):
    arr = arr.flatten()
    arr = arr[~np.isnan(arr)]
    
    return {
        "Mean": np.mean(arr),
        "Std Dev": np.std(arr),
        "Min": np.min(arr),
        "Max": np.max(arr),
        "Skewness": skew(arr),
        "Kurtosis": kurtosis(arr)
    }

def compute_texture(arr, window=5):
    """Simple local variance texture"""
    from scipy.ndimage import generic_filter
    return generic_filter(arr, np.var, size=window)

# -------------------------------
# 📥 Load data
# -------------------------------
img1 = load_raster(file1).squeeze()
img2 = load_raster(file2).squeeze()

if img1 is not None and img2 is not None:

    # Align shapes (simple crop to smallest)
    min_y = min(img1.shape[0], img2.shape[0])
    min_x = min(img1.shape[1], img2.shape[1])

    img1 = img1[:min_y, :min_x]
    img2 = img2[:min_y, :min_x]

    arr1 = img1
    arr2 = img2

    norm1 = apply_clahe(arr1) #normalize(arr1)
    norm2 = apply_clahe(arr2) #normalize(arr2)

    # -------------------------------
    # 🖼️ Visualization
    # -------------------------------
    st.subheader("🖼️ Comparacion")

    col1, col2 = st.columns(2)

    with col1:
        st.image(norm1, caption="Imagen 1", width='stretch')

    with col2:
        st.image(norm2, caption="Imagen 2", width='stretch')

    # -------------------------------
    # 🔄 Swipe Comparison (fake slider)
    # -------------------------------
    st.subheader("🔄 Deslizador comparativo")

    alpha = st.slider("Deslizador", 0.0, 1.0, 0.5)

    blended = alpha * norm1 + (1 - alpha) * norm2
    st.image(blended, caption="Swipe Blend", width='stretch')

    # -------------------------------
    # 📊 Statistics
    # -------------------------------
    st.subheader("📊 Estadisticas descriptivas")

    stats1 = compute_stats(arr1)
    stats2 = compute_stats(arr2)

    df_stats = pd.DataFrame([stats1, stats2], index=["Imagen 1", "Imagen 2"])
    st.dataframe(df_stats)

    # -------------------------------
    # 📈 Histogram
    # -------------------------------
    st.subheader("📈 Comparacion de Histogramas")

    df_hist = pd.DataFrame({
        "Image 1": arr1.flatten(),
        "Image 2": arr2.flatten()
    })

    df_hist = df_hist.melt(var_name="Image", value_name="Backscatter")

    fig = px.histogram(df_hist, x="Backscatter", color="Image", nbins=100, barmode="overlay")
    st.plotly_chart(fig, width='stretch')

    # -------------------------------
    # 🧠 Texture Analysis
    # -------------------------------
    st.subheader("🧠 Textura (Varianza Local)")

    window = st.slider("Tamaño de Ventana", 3, 7, 5, step=2)

    tex1 = compute_texture(norm1, window)
    tex2 = compute_texture(norm2, window)

    col1, col2 = st.columns(2)

    with col1:
        st.image(normalize(tex1), caption="Textura Imagen 1")

    with col2:
        st.image(normalize(tex2), caption="Textura Imagen 2")

    # -------------------------------
    # 📝 User Comments
    # -------------------------------
    st.subheader("📝 Interpretacion personal")

    comment = st.text_area("Escriba su interpretacion de la comparacion entre las imagenes")

else:
    st.info("Escoja dos imagenes para empezar la comparacion.")