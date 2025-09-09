import streamlit as st
import numpy as np
import plotly.graph_objects as go
import pandas as pd


# Set page title and a brief introduction
st.set_page_config(page_title="Espectro Electromagnetico", layout="wide")

st.title("🌌 Espectro Electromagnetico")
st.markdown("""
Esta herramienta interactiva está diseñada para que estudiantes de pregrado exploren las relaciones fundamentales entre los parámetros de las ondas electromagnéticas (EM): **longitud de onda ($\lambda$)**, **frecuencia ($\nu$)** y **energía (E)**.

Estos parámetros están vinculados por dos ecuaciones clave:
1. **Velocidad de la luz:** $c = \lambda \nu$
2. **Energía del fotón:** $E = h \nu$
Donde $c$ es la velocidad de la luz ($3.0 \times 10^8 \, m/s$) y $h$ es la constante de Planck ($6.626 \times 10^{-34} \, J \cdot s$).
""")
st.markdown("---")

# --- Constants ---
C = 3.0e8  # Speed of light in m/s
H = 6.626e-34  # Planck's constant in J*s

# --- Sidebar for user input ---
st.sidebar.header("Parámetros de onda")
st.sidebar.markdown("Utilice el control deslizante a continuación para cambiar la longitud de onda y ver cómo cambian los demás parámetros.")

# Use a log slider for a wide range of wavelengths
wavelength_log = st.sidebar.slider(
    "Seleccione una longitud de onda (log10 metros)",
    min_value=-15.0,
    max_value=3.0,
    value=0.0,
    step=0.1,
    format="%.1f"
)

wavelength_m = 10**wavelength_log
st.sidebar.metric("Longitud de onda ($\lambda$)", f"{wavelength_m:.2e} m")

# Calculate Frequency and Energy based on the selected wavelength
if wavelength_m > 0:
    frequency = C / wavelength_m
    energy_joules = H * frequency
    energy_ev = energy_joules / 1.602e-19  # Convert Joules to electron-volts

# --- Main App Content ---
st.header("Valores calculados")
col1, col2 = st.columns(2)

with col1:
    st.metric(
        label="Frequencia ($\nu$)",
        value=f"{frequency:.2e} Hz" if 'frequency' in locals() else "N/A"
    )

with col2:
    st.metric(
        label="Energia (E)",
        value=f"{energy_joules:.2e} J" if 'energy_joules' in locals() else "N/A",
        help=f"Energy is also {energy_ev:.2e} eV" if 'energy_ev' in locals() else ""
    )

st.markdown("---")

# --- Interactive Spectrum Visualization ---
st.header("Espectro Electromagnetico")

# Define the boundaries of the EM spectrum regions (in meters)
spectrum_regions = {
    'Ondas de Radio': {'start': 1e-1, 'end': 1e4, 'color': 'rgba(128, 0, 128, 0.4)'},
    'Microondas': {'start': 1e-3, 'end': 1e-1, 'color': 'rgba(255, 165, 0, 0.4)'},
    'Infrarroja': {'start': 7e-7, 'end': 1e-3, 'color': 'rgba(255, 0, 0, 0.4)'},
    'Luz visible': {'start': 4e-7, 'end': 7e-7, 'color': 'rgba(0, 255, 0, 0.4)'},
    'Ultravioleta': {'start': 1e-8, 'end': 4e-7, 'color': 'rgba(0, 0, 255, 0.4)'},
    'Rayos X': {'start': 1e-11, 'end': 1e-8, 'color': 'rgba(128, 128, 128, 0.4)'},
    'Rayos Gamma': {'start': 1e-15, 'end': 1e-11, 'color': 'rgba(255, 255, 0, 0.4)'},
}

# Create a Plotly figure to visualize the spectrum
fig = go.Figure()

for region_name, region_data in spectrum_regions.items():
    # Plotting rectangles for each region of the spectrum
    fig.add_shape(
        type="rect",
        x0=np.log10(region_data['start']),
        y0=0,
        x1=np.log10(region_data['end']),
        y1=1,
        fillcolor=region_data['color'],
        line=dict(width=0),
        layer="below"
    )
    # Add annotation for the region name
    fig.add_annotation(
        x=np.log10(region_data['start']) + (np.log10(region_data['end']) - np.log10(region_data['start'])) / 2,
        y=0.5,
        text=region_name,
        showarrow=False,
        font=dict(size=10, color='black')
    )

# Add a vertical line to show the selected wavelength
fig.add_vline(
    x=wavelength_log,
    line_width=3,
    line_dash="dash",
    line_color="black",
    annotation_text=f"Su seleccion",
    annotation_position="top right"
)

fig.update_layout(
    title="Espectro Electromagnetico",
    xaxis_title="Longitud de onda ($\lambda$) (log10 meters)",
    yaxis_title="Escala relative",
    showlegend=False,
    xaxis_range=[-15, 4],
    yaxis_range=[0, 1],
    height=300,
    margin=dict(l=20, r=20, t=40, b=20)
)
st.plotly_chart(fig, use_container_width=True)

# Explanation of the visible spectrum within the visualization
with st.expander("Explore el espectro visible"):
    st.markdown("""
    La porción de luz visible del espectro es un rango muy pequeño de longitudes de onda, de aproximadamente 400 nm a 700 nm.

    * **Violeta:** ~400-450 nm
    * **Azul:** ~450-495 nm
    * **Verde:** ~495-570 nm
    * **Amarillo:** ~570-590 nm
    * **Naranja:** ~590-620 nm
    * **Rojo:** ~620-700 nm
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

# Initial scorecard dataframe
df = pd.DataFrame({
    'EEM': ['Longitud de onda', 'Frecuencia', 'Energia'],
    'Infrarroja': [0, 0, 0],
    'Microondas': [0, 0, 0]
})

# Getting user input
input_F1 = st.number_input('Valor Frecuencia', key= 1, value=0.0)
input_E1 = st.number_input('Valor Energia', key=2, value=0.0)

input_F2 = st.number_input('Valor Frecuencia', key=3, value=0.0)
input_E2 = st.number_input('Valor Energia', key=4, value=0.0)

# Update dataframe with user input
df.at[0, 'Infrarroja'] = input_F1
df.at[1, 'Infrarroja'] = input_E1
df.at[0, 'Microondas'] = input_F2
df.at[1, 'Microondas'] = input_E2

# Display the updated dataframe
st.table(df.set_index('EEM'))