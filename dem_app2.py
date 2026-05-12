import streamlit as st
import numpy as np
import pandas as pd
import rasterio
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Comparacion entre DEMs")

# -----------------------------
# Helper Functions
# -----------------------------
def read_raster(uploaded_file):
    with rasterio.open(uploaded_file) as src:
        data = src.read(1).astype(float)
        data[data == src.nodata] = np.nan
    return data

def compute_stats(arr, name):
    arr_flat = arr[~np.isnan(arr)]
    stats = {
        "Dataset": name,
        "Min": np.min(arr_flat),
        "Max": np.max(arr_flat),
        "Mean": np.mean(arr_flat),
        "Std Dev": np.std(arr_flat),
        "Median": np.median(arr_flat)
    }
    return stats, arr_flat

def plot_image(arr, title):
    fig, ax = plt.subplots()
    im = ax.imshow(arr, cmap="terrain")
    ax.set_title(title)
    plt.colorbar(im, ax=ax)
    st.pyplot(fig)

def plot_histogram(arr_flat, name):
    fig = px.histogram(arr_flat, nbins=50, title=f"Histograma - {name}")
    st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# File Upload
# -----------------------------
st.sidebar.header("Cargue los archivos DEM")

dem_file = st.sidebar.file_uploader("Cargar ASTER-DEM", type=["tif"])
dsm_file = st.sidebar.file_uploader("Cargar SRTM-DEM", type=["tif"])
dtm_file = st.sidebar.file_uploader("Cargar ALOS-DEM", type=["tif"])

if dem_file and dsm_file and dtm_file:

    dem = read_raster(dem_file)
    dsm = read_raster(dsm_file)
    dtm = read_raster(dtm_file)

    # -----------------------------
    # Visualization
    # -----------------------------
    st.header("Visualizacion")

    col1, col2, col3 = st.columns(3)
    with col1:
        plot_image(dem, "ASTER")
    with col2:
        plot_image(dsm, "SRTM")
    with col3:
        plot_image(dtm, "ALOS")

    # -----------------------------
    # Statistics
    # -----------------------------
    st.header("Estadisticas descriptivas")

    dem_stats, dem_flat = compute_stats(dem, "ASTER")
    dsm_stats, dsm_flat = compute_stats(dsm, "SRTM")
    dtm_stats, dtm_flat = compute_stats(dtm, "ALOS")

    stats_df = pd.DataFrame([dem_stats, dsm_stats, dtm_stats])
    st.dataframe(stats_df, use_container_width=True)

    # -----------------------------
    # Histograms
    # -----------------------------
    st.header("Histogramas")

    col1, col2, col3 = st.columns(3)
    with col1:
        plot_histogram(dem_flat, "ASTER")
    with col2:
        plot_histogram(dsm_flat, "SRTM")
    with col3:
        plot_histogram(dtm_flat, "ALOS")

    # -----------------------------
    # Difference Analysis
    # -----------------------------
    st.header("Diferencias de Elevacion")

    if dem.shape == dsm.shape == dtm.shape:

        canopy_height = dsm - dtm
        terrain_diff = dem - dtm

        col1, col2 = st.columns(2)
        with col1:
            plot_image(canopy_height, "SRTM - ASTER (m)")
        with col2:
            plot_image(terrain_diff, "SRTM - ALOS (m)")

        # Stats for differences
        ch_stats, ch_flat = compute_stats(canopy_height, "SRTM - ASTER")
        td_stats, td_flat = compute_stats(terrain_diff, "SRTM - ALOS")

        diff_df = pd.DataFrame([ch_stats, td_stats])
        st.dataframe(diff_df, use_container_width=True)

        # Histograms
        col1, col2 = st.columns(2)
        with col1:
            plot_histogram(ch_flat, "SRTM - ASTER")
        with col2:
            plot_histogram(td_flat, "SRTM - ALOS")

    else:
        st.warning("Deben tener las mismas dimensiones.")

else:
    st.info("Cargue los DEM.")
