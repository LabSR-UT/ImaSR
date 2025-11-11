import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Set up the page ---
st.set_page_config(layout="wide")

st.title("Comprensión de los sensores de teledetección 🛰️")
st.write("Explore los principios fundamentales de la teledetección y sumérjase en la tecnología detrás de los diferentes tipos de sensores..")

# --- Interactive CMOS vs. CCD Section ---
st.header("CMOS vs. CCD: El duelo de sensores")
st.write(
    """
    Las cámaras, incluidas las utilizadas en teledetección, se basan en una de dos tecnologías de sensores principales para capturar la luz: **Dispositivo de Carga Acoplada (CCD)** y **Semiconductor Complementario de Óxido Metálico (CMOS)**. Exploremos su funcionamiento y comparemos su rendimiento.
    """
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Cómo funciona el CCD")
    st.write(
        """
        Un sensor CCD tiene un diseño simple donde cada píxel capta luz y la convierte en carga. Una vez que todos los píxeles han captado su carga, esta se transfiere, píxel a píxel, a través de un sistema de "capacitores" hasta un único amplificador de salida. Este diseño ofrece **alta calidad y bajo nivel de ruido**, pero el proceso es más lento y consume más energía.
        """
    )
with col2:
    st.subheader("Cómo funciona CMOS")
    st.write(
        """
        En un sensor CMOS, cada píxel tiene su propio amplificador y circuito. La carga de cada píxel se convierte en voltaje y se lee individualmente. Este diseño permite **mayores velocidades de lectura y menor consumo de energía**, pero los amplificadores individuales pueden introducir más ruido.
        """
    )

st.markdown("---")

# --- Hands-on Exercise ---
st.header("Actividad: Simulación del rendimiento del sensor 📊")
st.write(
    "Utilice los controles deslizantes a continuación para ver cómo las diferentes características del sensor afectan la imagen final. Esta simulación le ayuda a visualizar las compensaciones entre velocidad, ruido y resolución.."
)

# Sliders for user input
pixel_size = st.slider("Tamaño de píxel (para resolución espacial)", min_value=1, max_value=10, value=5)
noise_level = st.slider("Nivel de ruido", min_value=0.0, max_value=1.0, value=0.2, step=0.05)
readout_speed = st.slider("Velocidad de lectura (1 = slow, 10 = fast)", min_value=1, max_value=10, value=5)

# --- Logic to simulate sensor characteristics ---
# A simple function to generate a base image
def generate_base_image(size=100):
    x, y = np.mgrid[0:size, 0:size]
    # Simple checkerboard pattern for visualization
    img = (x // 10 % 2) ^ (y // 10 % 2)
    # Add a gradient
    img = img + np.sin(x / 5) * np.cos(y / 5) * 0.5
    return img

# Create the base image
base_image = generate_base_image()

# --- CCD Simulation ---
# High quality, slow readout
ccd_image = base_image + np.random.randn(*base_image.shape) * (noise_level * 0.5)
ccd_speed = 10 - readout_speed

# --- CMOS Simulation ---
# Faster, potentially noisier
cmos_image = base_image + np.random.randn(*base_image.shape) * (noise_level * 1.5)
cmos_speed = readout_speed

# --- Apply pixelation for spatial resolution ---
def pixelate_image(img, pixel_size):
    h, w = img.shape
    new_h, new_w = h // pixel_size, w // pixel_size
    temp_img = img[:new_h * pixel_size, :new_w * pixel_size]
    pixelated = np.zeros((new_h, new_w))
    for i in range(new_h):
        for j in range(new_w):
            pixelated[i, j] = np.mean(temp_img[i*pixel_size:(i+1)*pixel_size, j*pixel_size:(j+1)*pixel_size])
    return pixelated

pixelated_ccd = pixelate_image(ccd_image, pixel_size)
pixelated_cmos = pixelate_image(cmos_image, pixel_size)

# --- Display the results ---
st.subheader("Salida de sensor simulada")

results_col1, results_col2 = st.columns(2)

with results_col1:
    st.info(f"**Salida del sensor CCD**\n\n- **Velocidad de lectura:** Mas lento ({'🔴' * int(max(1, 10 - readout_speed))})\n- **Nivel de ruido:** Bajo")
    fig, ax = plt.subplots()
    ax.imshow(pixelated_ccd, cmap='gray')
    ax.set_title("Imagen CCD (alta calidad)")
    ax.axis('off')
    st.pyplot(fig)

with results_col2:
    st.info(f"**Salida del sensor CMOS**\n\n- **Velocidad de lectura:** Mas rapido ({'🟢' * int(max(1, readout_speed))})\n- **Nivel de ruido:** Mas alto")
    fig, ax = plt.subplots()
    ax.imshow(pixelated_cmos, cmap='gray')
    ax.set_title("Imagen CMOS (lectura rápida)")
    ax.axis('off')
    st.pyplot(fig)

st.markdown("---")
st.write(
"""
**Interpretación:**
* **Tamaño de píxel:** Un tamaño de píxel mayor (valor más alto en el control deslizante) simula una resolución espacial menor, lo que hace que las imágenes se vean más cuadriculadas.
* **Nivel de ruido:** Al aumentar el ruido, la imagen CMOS se vuelve notablemente más granulada que la imagen CCD, lo que demuestra su característica inherente de ruido.
* **Velocidad de lectura:** Este control deslizante afecta a los indicadores simbólicos. El CCD siempre se considera más lento, mientras que el CMOS es más rápido.
""")

st.markdown("---")

autor = st.text_input("Ingrese su nombre y apellido:")
st.write(f"Realizado por: {autor}")

st.markdown("### Actividad")
st.markdown("""
1. Hacer las consultas requeridas.
2. Ingresar los resultados en la tabla.
3. Enviar por email el resultado.
""")