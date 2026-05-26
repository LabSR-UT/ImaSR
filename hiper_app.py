import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Datos Hiperespectrales",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIMULATE HYPERSPECTRAL DATA CUBE ---
@st.cache_data
def generate_hyperspectral_cube():
    """
    Generates a 100x100x50 simulated hyperspectral data cube.
    Dimensions: 100 rows, 100 columns, 50 spectral bands (400nm to 900nm).
    Divided into 4 quadrants representing different materials.
    """
    rows, cols, bands = 100, 100, 50
    wavelengths = np.linspace(400, 900, bands)
    cube = np.zeros((rows, cols, bands))
    
    # 1. Vegetation Spectrum: Green bump (~540nm), Red absorption (~670nm), sharp NIR rise ("Red Edge")
    veg_sig = 0.05 + 0.12 * np.exp(-((wavelengths - 540)/25)**2) + 0.65 / (1 + np.exp(-(wavelengths - 700)/15))
    
    # 2. Clear Water Spectrum: Highest reflection in Blue (~450nm), drops to near 0 in Near-Infrared (NIR)
    water_sig = 0.25 * np.exp(-((wavelengths - 450)/50)**2) + 0.01
    
    # 3. Dry Soil Spectrum: Steady, linear increase from visible to NIR wavelengths
    soil_sig = 0.12 + 0.45 * (wavelengths - 400) / 500
    
    # 4. Concrete/Urban Spectrum: Fairly flat, high baseline albedo across all wavelengths
    concrete_sig = 0.38 + 0.04 * np.sin(wavelengths / 60)
    
    # Assign signatures to image quadrants
    cube[0:50, 0:50, :] = veg_sig[None, None, :]       # Top-Left: Vegetation
    cube[0:50, 50:100, :] = water_sig[None, None, :]    # Top-Right: Water
    cube[50:100, 0:50, :] = soil_sig[None, None, :]     # Bottom-Left: Soil
    cube[50:100, 50:100, :] = concrete_sig[None, None, :] # Bottom-Right: Concrete
    
    # Add minor Gaussian noise to simulate real-world sensor perturbations
    noise = np.random.normal(0, 0.02, size=cube.shape)
    cube = np.clip(cube + noise, 0, 1)
    
    return cube, wavelengths

# Load the simulated HSI dataset
cube, wavelengths = generate_hyperspectral_cube()

# Helper function to extract explicit RGB composites
def get_rgb_composite(cube, r_idx, g_idx, b_idx):
    rgb = np.zeros((cube.shape[0], cube.shape[1], 3))
    rgb[:,:,0] = cube[:,:,r_idx]
    rgb[:,:,1] = cube[:,:,g_idx]
    rgb[:,:,2] = cube[:,:,b_idx]
    # Normalize channels dynamically for clean plotting
    for i in range(3):
        low, high = np.percentile(rgb[:,:,i], (2, 98))
        rgb[:,:,i] = np.clip((rgb[:,:,i] - low) / (high - low + 1e-5), 0, 1)
    return rgb

# --- UI HEADER ---
st.title("🎓 Visor Imagen Hiperespectral")
st.markdown("""
Una fotografía en color estándar registra solo tres bandas anchas de luz (rojo, verde y azul), mientras que los sensores hiperespectrales, en cambio, capturan docenas o cientos de bandas espectrales estrechas y contiguas.
Esto nos permite extraer una firma espectral única para cada píxel, revelando la composición química de los materiales.
---
""")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("🛠️ Controles de visualizacion")

# Pixel Selector (Inputs for extracting the spectral signature)
st.sidebar.subheader("📍 Seleccione el pixel objetivo")
pixel_x = st.sidebar.slider("Pixel (Coordenada X)", 0, 99, 25)
pixel_y = st.sidebar.slider("Pixel (Coordenada Y", 0, 99, 25)

st.sidebar.markdown("---")

# Left View Controls
st.sidebar.subheader("Panel izquierdo")
left_mode = st.sidebar.selectbox("Tipo de imagen", ["Banda espectral simple", "Combinacion RGB (color natural)", "Combinacion CIR (falso color)"],  key=1)
if left_mode == "Banda espectral simple":
    left_band_idx = st.sidebar.slider("Longitud de onda Banda izquierda", 0, len(wavelengths)-1, 10, format="Band %d", key="left_b")
    st.sidebar.caption(f"Longitud de onda Banda izquierda actual: **{wavelengths[left_band_idx]:.0f} nm**")

# Right View Controls
st.sidebar.subheader("Panel derecho")
right_mode = st.sidebar.selectbox("Tipo de imagen", ["Banda espectral simple", "Combinacion RGB (color natural)", "Combinacion CIR (falso color)"], index=0,  key=2)
if right_mode == "Banda espectral simple":
    right_band_idx = st.sidebar.slider("Longitud de onda Banda derecha", 0, len(wavelengths)-1, 45, format="Band %d", key="right_b")
    st.sidebar.caption(f"Longitud de onda Banda derecha actual: **{wavelengths[right_band_idx]:.0f} nm**")


# --- MAIN APP LAYOUT ---

# 1. Side-by-Side Visualization Section
st.header("🖼️ Visualizacion espacial")
col1, col2 = st.columns(2)

# Find closest standard bands indices for composite building
# 450nm ~ Blue (idx 5), 550nm ~ Green (idx 15), 650nm ~ Red (idx 25), 850nm ~ NIR (idx 45)
with col1:
    st.subheader(f"Vista izquierda: {left_mode}")
    fig_l, ax_l = plt.subplots(figsize=(5, 5))
    if left_mode == "Banda espectral simple":
        ax_l.imshow(cube[:, :, left_band_idx], cmap='gray')
    elif left_mode == "Combinacion RGB (color natural)":
        ax_l.imshow(get_rgb_composite(cube, 25, 15, 5))
    else: # False Color Infrared
        ax_l.imshow(get_rgb_composite(cube, 45, 25, 15))
    
    # Draw crosshairs on the current targeted pixel
    ax_l.axhline(pixel_y, color='cyan', linestyle=':', linewidth=1.5)
    ax_l.axvline(pixel_x, color='cyan', linestyle=':', linewidth=1.5)
    ax_l.axis('off')
    st.pyplot(fig_l)

with col2:
    st.subheader(f"Vista derecha: {right_mode}")
    fig_r, ax_r = plt.subplots(figsize=(5, 5))
    if right_mode == "Banda espectral simple":
        ax_r.imshow(cube[:, :, right_band_idx], cmap='gray')
    elif right_mode == "Combinacion RGB (color natural)":
        ax_r.imshow(get_rgb_composite(cube, 25, 15, 5))
    else: # False Color Infrared
        ax_r.imshow(get_rgb_composite(cube, 45, 25, 15))
        
    ax_r.axhline(pixel_y, color='cyan', linestyle=':', linewidth=1.5)
    ax_r.axvline(pixel_x, color='cyan', linestyle=':', linewidth=1.5)
    ax_r.axis('off')
    st.pyplot(fig_r)

# 2. Interactive Spectral Profiler Section
st.markdown("---")
st.header("📈 Perfil espectral")

# Determine material classification based on pixel coordinates
if pixel_x < 50 and pixel_y < 50:
    detected_mat = "Vegetacion (Arriba-Izquierda)"
    explanation = "Observe el distintivo efecto **'Red Edge'**: la reflexión aumenta drásticamente después de los 700 nm debido a que las estructuras celulares de las plantas dispersan fuertemente la luz infrarroja cercana.."
elif pixel_x >= 50 and pixel_y < 50:
    detected_mat = "Agua (Arriba-Derecha)"
    explanation = "Observa cómo el agua absorbe la luz casi por completo en las longitudes de onda infrarrojas más largas. Se ve brillante en la banda azul, pero se vuelve completamente negra en las bandas superiores.."
elif pixel_x < 50 and pixel_y >= 50:
    detected_mat = "Suelo (Abajo-Izquierda)"
    explanation = "El suelo presenta una rampa lineal constante y predecible hacia arriba a medida que se pasa de la luz visible a la región del infrarrojo de onda corta.."
else:
    detected_mat = "Concreto (Abajo-Deerecha)"
    explanation = "Las estructuras artificiales como el hormigón tienden a mantenerse consistentemente brillantes (albedo alto y estable) en todo el espectro con características de absorción química menores.."

st.info(f"📍 **Material objetivo:** {detected_mat}. {explanation}")

# Plotly Interactive Line Chart for the targeted pixel profile
pixel_spectrum = cube[pixel_y, pixel_x, :]

fig_spec = go.Figure()
fig_spec.add_trace(go.Scatter(
    x=wavelengths, 
    y=pixel_spectrum,
    mode='lines+markers',
    name=f'Pixel ({pixel_x}, {pixel_y})',
    line=dict(color='#1f77b4', width=3),
    marker=dict(size=4)
))

fig_spec.update_layout(
    title=f"Huella espectral en las coordenadas (X: {pixel_x}, Y: {pixel_y})",
    xaxis_title="Longitud de onda (nanometros)",
    yaxis_title="Intensidad de la Reflectancia (0.0 - 1.0)",
    yaxis=dict(range=[0, 1.05]),
    xaxis=dict(gridcolor='rgba(200,200,200,0.2)'),
    template="plotly_dark" if st.get_option("theme.base") == "dark" else "plotly_white",
    height=450
)

st.plotly_chart(fig_spec, use_container_width=True)