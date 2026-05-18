import streamlit as st
import rasterio
import numpy as np
import matplotlib.pyplot as plt
from pylandtemp import split_window

st.set_page_config(layout="wide")

st.title("🌍 Temperatura Superficial (LST) - Landsat 8/9")

st.markdown("""
Se calculara:
- NDVI (%)
- LST (°C)
""")

# Upload files
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

with col1:
    red_file = st.file_uploader("Cargar Banda 4 (Red)", type=["tif"])

with col2:
    nir_file = st.file_uploader("Cargar Banda 5 (NIR)", type=["tif"])

with col3:
    thermal_file10 = st.file_uploader("Cargar Banda 10 (SWIR10)", type=["tif"])
    
with col4:
    thermal_file11 = st.file_uploader("Cargar Banda 11 (SWIR11)", type=["tif"])

if red_file and nir_file and thermal_file10 and thermal_file11:

    # Read bands
    with rasterio.open(red_file) as src:
        redImage = src.read(1).astype('f4')

    with rasterio.open(nir_file) as src:
        nirImage = src.read(1).astype('f4')
    
    with rasterio.open(thermal_file10) as src:
        tempImage10 = src.read(1).astype('f4')

    with rasterio.open(thermal_file11) as src:
        tempImage11 = src.read(1).astype('f4')

    st.success("Bandas Roja, Infrarroja, SWIR10 y SWIR11 cargadas bien!")
    
    option = st.selectbox(
    "Escoja un metodo:",
    ('jiminez-munoz', 'kerr','price', 'sobrino-1993'))

    method = option
    lst_image_split_window = split_window(
        tempImage10, 
        tempImage11, 
        redImage, 
        nirImage, 
        lst_method=method, 
        emissivity_method='avdan',
        unit='celcius'
    )
    
    lst_celsius = lst_image_split_window - 273.15
    
    # --- NDVI ---
    ndvi = (nirImage - redImage) / (nirImage + redImage + 1e-6)

    # --- Visualization ---
    st.subheader("Resultados")

    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots()
        im = ax.imshow(ndvi, cmap="RdYlGn")
        ax.set_title("NDVI")
        plt.colorbar(im, ax=ax)
        st.pyplot(fig)

    with col2:
        fig, ax = plt.subplots()
        im = ax.imshow(lst_celsius, cmap='viridis')
        ax.set_title("LST (°C)")
        plt.colorbar(im, ax=ax)
        st.pyplot(fig)        
 
    # --- Stats ---
    st.subheader("Estadisticas descriptivas")

    col1, col2, col3 = st.columns(3)

    col1.metric("Promedio LST (°C)", f"{np.nanmean(lst_celsius):.2f}")
    col2.metric("Minima LST (°C)", f"{np.nanmin(lst_celsius):.2f}")
    col3.metric("Maxima LST (°C)", f"{np.nanmax(lst_celsius):.2f}")

    # --- Histogram ---
    st.subheader("Histograma LST")

    fig, ax = plt.subplots()
    ax.hist(lst_celsius.flatten(), bins=50)
    ax.set_title("Distribucion LST")
    st.pyplot(fig)

else:
    st.info("Please upload all required bands.")
    st.info("Debe cargar todas las bandas requeridas.")
