import streamlit as st
from PIL import Image
import numpy as np
import tifffile as tiff
import io

def load_rs_image(uploaded_file):
    """
    Reads a TIFF/GeoTIFF using tifffile, handles multi-band scaling, 
    and returns a PIL Image.
    """
    # Read the file into a numpy array
    img_array = tiff.imread(uploaded_file)
    
    # If image is (Bands, Height, Width), transpose to (Height, Width, Bands)
    if img_array.ndim == 3 and img_array.shape[0] < img_array.shape[2]:
        img_array = np.transpose(img_array, (1, 2, 0))
    
    # Take only the first 3 bands (RGB) if it's a multi-spectral stack
    if img_array.ndim == 3 and img_array.shape[2] > 3:
        img_array = img_array[:, :, :3]

    # Normalize to 0-255 (vital for Landsat 16-bit data)
    img_min, img_max = img_array.min(), img_array.max()
    img_array = (img_array - img_min) / (img_max - img_min) * 255
    
    return Image.fromarray(img_array.astype('uint8'))

def compare_images(img1, img2, split_pct):
    if img1.size != img2.size:
        img2 = img2.resize(img1.size)
    
    width, height = img1.size
    split_point = int(width * (split_pct / 100))
    
    left_part = img1.crop((0, 0, split_point, height))
    right_part = img2.crop((split_point, 0, width, height))
    
    combined = Image.new("RGB", (width, height))
    combined.paste(left_part, (0, 0))
    combined.paste(right_part, (split_point, 0))
    return combined

# --- UI ---
st.title("🛰️ Imagenes Opticas (Landsat-8 vs Sentinel-2)")

# 1. Sidebar Inputs for File Upload
l_file = st.sidebar.file_uploader("Escoja una imagen Landsat TIFF", type=['tif', 'tiff'])
s_file = st.sidebar.file_uploader("Escoja una imagen Sentinel TIFF", type=['tif', 'tiff'])

if l_file and s_file:
    # Processing images
    img_l = load_rs_image(l_file)
    img_s = load_rs_image(s_file)
    
    split = st.slider("Comparison Slider", 0, 100, 50)
    st.image(compare_images(img_l, img_s, split), use_container_width=True)

    # --- NEW: User Input Section ---
    st.divider()
    st.subheader("📝 Interpretacion de imagenes")

    # Question 1: Text Input
    location_name = st.text_input("¿A cual zona se le asemeja esta área de estudio??", placeholder="ej. Amazonas")

    # Question 2: Radio Buttons (Categorical)
    land_cover = st.radio(
        "¿Cuál es el tipo de cobertura terrestre dominante visible??",
        ["Bosque", "Urbano", "Agricultura", "Agua", "Arido"]
    )

    # Question 3: Multi-select
    features = st.multiselect(
        "Identificar características específicas detectadas:",
        ["Deforestacion", "Cultivos", "Suelos", "Sedimentos", "Infraestructura", "Otro"]
    )

    # Question 4: Text Area (Long form)
    observations = st.text_area("Describa las diferencias observadas entre Landsat-8 y Sentinel-2:")

    # Action Button to "Save" or Display the answer
    if st.button("Interpretacion"):
        st.success(f"Interpretacion para {location_name} enviada!")
        st.write("**Resumen:**")
        st.json({
            "Ubicacion": location_name,
            "Tipo de cobertura": land_cover,
            "Atributos": features,
            "Notas": observations
        })

else:
    st.info("Escoja las imágenes para habilitar el cuestionario de análisis.")

