import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# App Configuration
st.set_page_config(page_title="Simulador de dispersión atmosférica", layout="wide")

st.title("☀️ Dispersión atmosférica")
st.markdown("""
Esta aplicación simula cómo los diferentes tipos de dispersión afectan la intensidad de la luz en todo el espectro visible (de 400 nm a 700 nm).
""")

# --- Sidebar Controls ---
st.sidebar.header("Parámetros de simulación")
particle_size = st.sidebar.slider("Tamaño de partícula (unidades relativas)", 0.1, 10.0, 1.0)
intensity_scale = st.sidebar.slider("Intensidad de la fuente", 1, 100, 50)

# --- Physics Calculations ---
# Visible spectrum in nm
wavelengths = np.linspace(400, 700, 100) 

# 1. Rayleigh: I ~ 1/λ^4
rayleigh = (1 / wavelengths**4) * 1e11 * intensity_scale

# 2. Mie: I ~ 1/λ^p (where p is roughly 1 to 2 depending on size)
# We model the transition as a function of particle size
p_factor = max(0.5, 4 - particle_size) 
mie = (1 / wavelengths**p_factor) * (10**(p_factor+1)) * intensity_scale

# 3. Non-Selective: I is constant across λ
non_selective = np.full_size = np.ones_like(wavelengths) * (intensity_scale * 0.5)

# --- Visualization ---
fig, ax = plt.subplots(figsize=(10, 6))

ax.plot(wavelengths, rayleigh, label='Rayleigh (partículas pequeñas/gases)', color='blue', lw=2)
ax.plot(wavelengths, mie, label='MIE (Aerosoles/Polvo)', color='orange', lw=2)
ax.plot(wavelengths, non_selective, label='No selectivo (gotas grandes)', color='gray', linestyle='--', lw=2)

# Aesthetic mapping for the visible spectrum background
ax.axvspan(400, 450, color='violet', alpha=0.1)
ax.axvspan(450, 495, color='blue', alpha=0.1)
ax.axvspan(495, 570, color='green', alpha=0.1)
ax.axvspan(570, 590, color='yellow', alpha=0.1)
ax.axvspan(590, 620, color='orange', alpha=0.1)
ax.axvspan(620, 700, color='red', alpha=0.1)

ax.set_xlabel("Longitud de onda (nm)")
ax.set_ylabel("Intensidad de dispersión relativa")
ax.set_title(f"Comparación de dispersión (Factor de tamaño de partícula: {particle_size})")
ax.legend()
ax.grid(True, which='both', linestyle='--', alpha=0.5)

st.pyplot(fig)

# --- Educational Breakdown ---
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🔹 Rayleigh")
    st.write("Predomina cuando $d \ll \lambda$. Las longitudes de onda cortas (azul) se dispersan mucho más que las largas (rojo). Por eso el cielo es azul.!")

with col2:
    st.subheader("🔸 MIE")
    st.write("Predomina cuando $d \sim \lambda$ Dispersa todas las longitudes de onda de manera más uniforme que Rayleigh, lo que a menudo resulta en un resplandor 'neblinoso' o blanco/gris..")

with col3:
    st.subheader("⚪ No-selectiva")
    st.write("Predomina cuando $d \gg \lambda$. Todas las longitudes de onda se dispersan por igual. Por eso las nubes densas y la niebla se ven completamente blancas..")
	

# --- Sección de Interacción y Feedback ---
st.divider() # Línea divisoria visual
st.header("📝 Panel de Análisis")

# Pregunta guía para el usuario
st.markdown("""
**Pregunta 1:** Que sucede con la intensidad de la dispersion Rayleigh, cuando se incrementa la intensidad de la fuente?
""")

#R/ Se duplica la intensidad de dispersion relativa

# Cajón de diálogo (Text Area)
user_observation = st.text_area(
    "Respuesta:",
    placeholder="Ejemplo: aumenta, disminuye, no cambia...", key="Q1"
)

# Botón para confirmar o guardar la nota
if st.button("Guardar respuesta", key="R1"):
    if user_observation:
        st.success("¡Respuesta guardada con éxito!")
        st.info(f"**Tu análisis:** {user_observation}")
    else:
        st.warning("No has escrito nada, escribe algo antes de guardar.")

st.markdown("""
**Pregunta 2:** Que sucede con la intensidad de la dispersion MIE, cuando se incrementa el tamaño de particula?
""")

#R/ R/ Se incrementa hasta un 50%

# Cajón de diálogo (Text Area)
user_observation2 = st.text_area(
    "Respuesta:",
    placeholder="Ejemplo: aumenta, disminuye, no cambia...", key="Q2"
)

# Botón para confirmar o guardar la nota
if st.button("Guardar respuesta", key="R2"):
    if user_observation2:
        st.success("¡Respuesta guardada con éxito!")
        st.info(f"**Tu análisis:** {user_observation}")
    else:
        st.warning("No has escrito nada, escribe algo antes de guardar.")

st.markdown("""
**Pregunta 3:** Como se comporta en general la dispersion No-Selectiva?
""")

#R/ Se duplica la intensidad de dispersion relativa

# Cajón de diálogo (Text Area)
user_observation3 = st.text_area(
    "Respuesta:",
    placeholder="Ejemplo: aumenta, disminuye, no cambia...", key="Q3"
)

#R/ Es muy estable, casi no cambia

# Botón para confirmar o guardar la nota
if st.button("Guardar respuesta", key="R3"):
    if user_observation3:
        st.success("¡Respuesta guardada con éxito!")
        st.info(f"**Tu análisis:** {user_observation}")
    else:
        st.warning("No has escrito nada, escribe algo antes de guardar.")

user_input = st.text_input("Ingrese su nombre", None)
st.write(f"Listo!")