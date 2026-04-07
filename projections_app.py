import streamlit as st
import numpy as np
from PIL import Image
from pyproj import Transformer
import rasterio
from rasterio.transform import from_bounds
from rasterio.warp import reproject, Resampling

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

    # --- Define fake geographic extent (Colombia approx) ---
    lon_min, lon_max = -80, -66
    lat_min, lat_max = -4, 13

    # Transform for original image
    src_transform = from_bounds(lon_min, lat_min, lon_max, lat_max, w, h)
    src_crs = "EPSG:4326"

    # Destination array
    dst = np.zeros_like(img)

    # Perform reprojection (band by band)
    for i in range(3):  # RGB
        reproject(
            source=img[:, :, i],
            destination=dst[:, :, i],
            src_transform=src_transform,
            src_crs=src_crs,
            dst_crs=target_crs,
            resampling=Resampling.bilinear
        )

    warped = dst

    # --- Grid overlay ---
    def add_grid(image, step=50):
        img_copy = image.copy()
        img_copy[::step, :] = 255
        img_copy[:, ::step] = 255
        return img_copy

    show_grid = st.sidebar.checkbox("Reticula", True)

    # --- USER INPUT ---
    user_name = st.sidebar.text_input("Ingrese su nombre", "")
    user_goal = st.sidebar.text_area(
        "Indique las diferencias (visuales y numericas) entre las diferentes proyecciones", ""
    )

    img_display = add_grid(img) if show_grid else img
    warped_display = add_grid(warped) if show_grid else warped

    # --- Distortion Metrics (igual que antes) ---
    transformer = Transformer.from_crs("EPSG:4326", target_crs, always_xy=True)

    lon = np.linspace(lon_min, lon_max, w)
    lat = np.linspace(lat_min, lat_max, h)
    lon_grid, lat_grid = np.meshgrid(lon, lat)

    x, y = transformer.transform(lon_grid, lat_grid)

    dx = np.gradient(x, axis=1)
    dy = np.gradient(y, axis=0)

    area_dist = np.mean(np.abs(dx * dy)) / 1e6
    angle_dist = np.mean(np.abs(np.gradient(dx, axis=0) - np.gradient(dy, axis=1)))

    # --- Layout ---
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Original (WGS84)")
        st.image(img_display)

    with col2:
        st.subheader(proj_name)
        st.image(warped_display)

    # --- Blend ---
    st.subheader("Comparacion")
    alpha = st.slider("Blend", 0.0, 1.0, 0.5)
    blend = (img * (1 - alpha) + warped * alpha).astype(np.uint8)
    st.image(blend)

    # --- Metrics ---
    st.subheader("Metricas de la distorsion")
    st.metric("Distorsion en area", f"{area_dist:.4f} Km2")
    st.metric("Distorsion Angular", f"{angle_dist:.4f} grados")
