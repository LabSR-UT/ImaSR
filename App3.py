import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# Page Config
st.set_page_config(page_title="REM & superficies", layout="wide")

st.title("📡 Interacciones de la REM ")
st.markdown("""
La teledetección se basa en la medición de cómo la radiación electromagnética (REM) interactúa con las características terrestres. 
Cuando la REM incide sobre una superficie, ocurren tres cosas: se **absorbe**, se **transmite** o se **refleja**.
""")

# --- Sidebar Controls ---
st.sidebar.header("Parametros de Interaccion")
surface_type = st.sidebar.selectbox(
    "Seleccione el tipo de superficie",
    ["Vegetacion verde", "Agua clara", "Suelo desnudo seco"]
)

# --- Logic for Spectral Signatures (Simplified Data) ---
# Wavelengths in micrometers (μm)
wavelengths = [0.4, 0.5, 0.6, 0.7, 0.8, 1.0, 1.2, 1.6, 2.0, 2.4]

data = {
    "Vegetacion verde": [0.05, 0.10, 0.05, 0.50, 0.70, 0.65, 0.60, 0.40, 0.20, 0.10],
    "Agua clara": [0.08, 0.05, 0.03, 0.01, 0.005, 0, 0, 0, 0, 0],
    "Suelo desnudo seco": [0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.45]
}

reflectance = data[surface_type]

# --- Visualization ---
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader(f"Curva de Reflectancia Espectral: {surface_type}")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=wavelengths, y=reflectance, mode='lines+markers', 
                             name='Reflectancia', line=dict(color='limegreen', width=3)))
    
    fig.update_layout(
        xaxis_title="Longitud de onda (μm) - Visible (VIS) hasta Infrarroja de onda corta (SWIR)",
        yaxis_title="Reflectancia (0.0 - 1.0)",
        template="plotly_white",
        hovermode="x unified"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Tres superficies principales")
    current_refl = reflectance[4] # Index for Near-Infrared approx
    
    st.metric("Reflejada (NIR)", f"{current_refl*100:.0f}%")
    st.write("---")
    
    if surface_type == "Vegetacion verde":
        st.info("**¿Por qué?** La clorofila absorbe la luz azul/roja (energía para la fotosíntesis) pero refleja fuertemente la luz infrarroja cercana para evitar el sobrecalentamiento.")
    elif surface_type == "Agua clara":
        st.info("**¿Por qué?** El agua absorbe casi toda la energía en las longitudes de onda más largas (rojo e infrarrojo), por eso se ve oscura en las imágenes infrarrojas de los satélites.")
    else:
        st.info("**¿Por qué?** La reflectancia del suelo generalmente aumenta de forma constante con la longitud de onda, influenciada por la humedad y la materia orgánica.")

# --- Educational Section ---
st.divider()
st.subheader("Interaccion fisica")


st.markdown("""
1. Reflexión: El rebote que los sensores realmente detectan. Las superficies lisas generan reflexión especular, mientras que las superficies rugosas generan reflexión difusa.
2. Absorción: La energía se convierte en energía interna (calor). Por eso ciertos gases o minerales «desaparecen» en longitudes de onda específicas.
3. Transmisión: La energía se transmite a través del medio (como la luz a través del agua poco profunda).
""")

st.divider()
st.subheader("Consulta")
st.write("Ingrese los valores de longitud de onda donde cada superficie (Agua, Bosque, Suelo) tiene la mayor reflectancia:")
resp = st.text_input(f"Respuesta:")

user_name = st.text_input("Ingrese su nombre:")