import streamlit as st
import numpy as np
import cv2
from PIL import Image
from pyproj import Transformer

st.set_page_config(layout="wide")



st.title("🇨🇴 Proyecciones cartograficas en Colombia")

uploaded_file = st.file_uploader("Cargue una imagen", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file).convert("RGB")
    img = np.array(image)
    h, w = img.shape[:2]

    # --- CRS Options (Colombia) ---
    projections = {
        "MAGNA-SIRGAS / Colombia Bogotá (EPSG:3116)": "EPSG:3116",
        "MAGNA-SIRGAS Origen Nacional (EPSG:9377)": "EPSG:9377",
        "WGS84 Geographic (EPSG:4326)": "EPSG:4326"
    }

    proj_name = st.sidebar.selectbox("Proyeccion", list(projections.keys()))
    target_crs = projections[proj_name]
    


    # Assume input is lat/lon grid (demo purpose)
    lon = np.linspace(-80, -66, w)
    lat = np.linspace(-4, 13, h)
    lon_grid, lat_grid = np.meshgrid(lon, lat)

    transformer = Transformer.from_crs("EPSG:4326", target_crs, always_xy=True)

    # Transform coordinates
    x, y = transformer.transform(lon_grid, lat_grid)

    # Normalize to image grid
    x_norm = (x - x.min()) / (x.max() - x.min()) * (w - 1)
    y_norm = (y - y.min()) / (y.max() - y.min()) * (h - 1)

    map_x = x_norm.astype(np.float32)
    map_y = y_norm.astype(np.float32)

    warped = cv2.remap(img, map_x, map_y, interpolation=cv2.INTER_LINEAR)

    # --- Grid overlay ---
    def add_grid(image, step=50):
        img_copy = image.copy()
        for i in range(0, img_copy.shape[0], step):
            cv2.line(img_copy, (0, i), (img_copy.shape[1], i), (255, 255, 255), 1)
        for j in range(0, img_copy.shape[1], step):
            cv2.line(img_copy, (j, 0), (j, img_copy.shape[0]), (255, 255, 255), 1)
        return img_copy

    show_grid = st.sidebar.checkbox("Reticula", True)
    
    # --- USER INPUT SECTION ---

    #st.sidebar.title("👤 Concepto")

    user_name = st.sidebar.text_input("Ingrese su nombre", "")
    user_goal = st.sidebar.text_area("Indique las diferencias (visuales y numericas) entre las diferentes proyecciones", "")

    img_display = add_grid(img) if show_grid else img
    warped_display = add_grid(warped) if show_grid else warped

    # --- Distortion Metrics ---
    dx = np.gradient(x, axis=1)
    dy = np.gradient(y, axis=0)

    area_dist = np.mean(np.abs(dx * dy))/1000000
    angle_dist = np.mean(np.abs(np.gradient(dx, axis=0) - np.gradient(dy, axis=1)))

    # --- Layout ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original (WGS84)")
        st.image(img_display)

    with col2:
        st.subheader(proj_name)
        st.image(warped_display)

    # --- Slider ---
    st.subheader("Comparacion")
    alpha = st.slider("Blend", 0.0, 1.0, 0.5)
    blend = (img * (1 - alpha) + warped * alpha).astype(np.uint8)
    st.image(blend)

    # --- Metrics ---
    st.subheader("Metricas de la distorsion")
    st.metric("Distorsion en area", f"{area_dist:.4f} Km2")
    st.metric("Distorsion Angular", f"{angle_dist:.4f} grados")