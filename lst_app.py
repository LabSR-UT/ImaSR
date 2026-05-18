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



# Google. cloud image folder
url = 'https://storage.googleapis.com/gcp-public-data-landsat/LC08/01/042/034/LC08_L1TP_042034_20170616_20170629_01_T1/'

# RGB images file names with file extensions
redband = 'LC08_L1TP_042034_20170616_20170629_01_T1_B{}.TIF'.format(4) 
nirband = 'LC08_L1TP_042034_20170616_20170629_01_T1_B{}.TIF'.format(5)
tempband10 = 'LC08_L1TP_042034_20170616_20170629_01_T1_B{}.TIF'.format(10)
tempband11 = 'LC08_L1TP_042034_20170616_20170629_01_T1_B{}.TIF'.format(11)

if redband and nirband and tempband10 and tempband11:

    # Read bands
    with rasterio.open(url+redband) as src:
        redImage = src.read(1).astype('f4')

    with rasterio.open(url+nirband) as src:
        nirImage = src.read(1).astype('f4')
    
    with rasterio.open(url+tempband10) as src:
        tempImage10 = src.read(1).astype('f4')

    with rasterio.open(url+tempband11) as src:
        tempImage11 = src.read(1).astype('f4')

    st.success("Bandas Roja, Infrarroja, SWIR10 y SWIR11 cargadas bien!")
    
    option = st.selectbox(
    "How would you like to be contacted?",
    ('jiminez-munoz', 'kerr','mc-clain','price', 'sobrino-1993'))

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