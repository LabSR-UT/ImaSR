import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Set Page Configuration ---
st.set_page_config(
    page_title="Digital Elevation Model (DEM) App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- App Title ---
st.title("🗺️ The Digital Elevation Model (DEM) Explorer")


# --- Horizontal Line Separator ---
st.markdown("---")

# --- 2. Interactive Visualization Section ---
st.header("Actividad Visualizacion DEM")
st.markdown(
    """
    Esta sección le permite crear y manipular un DEM para ver cómo los diferentes parámetros afectan su representación visual.
    """
)

# Function to generate a simple "mountain" DEM
def generate_dem(size=100, peak_height=1000):
    """Generates a simple, Gaussian-like DEM."""
    x = np.linspace(-1, 1, size)
    y = np.linspace(-1, 1, size)
    X, Y = np.meshgrid(x, y)
    Z = peak_height * np.exp(-(X**2 + Y**2) * 2)
    return Z

# Create a sample DEM and a sidebar for controls
dem_size = 100
dem_data = generate_dem(size=dem_size)

# Sidebar for controls
with st.sidebar:
    st.title("Controles")
    st.markdown("Ajustar la visualizacion aca.")
    
    # Sliders for customization
    height_exaggeration = st.slider(
        "Exageración vertical",
        min_value=1.0,
        max_value=10.0,
        value=3.0,
        step=0.1,
        help="Aumente este valor para que el terreno parezca más espectacular.."
    )
    
    noise_level = st.slider(
        "Añadir ruido aleatorio",
        min_value=0.0,
        max_value=100.0,
        value=0.0,
        step=5.0,
        help="Esto agrega fluctuaciones aleatorias al DEM, simulando imperfecciones en los datos.."
    )
    
    # Color map selection
    cmap_option = st.selectbox(
        "Seleccionar mapa de colores",
        ('terrain', 'viridis', 'plasma', 'cividis', 'jet'),
        help="Elija una paleta de colores diferente para el DEM."
    )

# Apply user settings to the DEM data
modified_dem = dem_data * height_exaggeration + np.random.rand(dem_size, dem_size) * noise_level

# Create and display the plot
fig, ax = plt.subplots(figsize=(10, 8))
ax.imshow(modified_dem, cmap=cmap_option, origin='lower')
ax.set_title("Visualizacion DEM", fontsize=16)
ax.set_xlabel("Coordenada X")
ax.set_ylabel("Coordenada Y")
ax.grid(False)
plt.colorbar(ax.imshow(modified_dem, cmap=cmap_option, origin='lower'), ax=ax, label='Elevacion')
st.pyplot(fig)

st.markdown("---")

# --- 3. Hands-on Exercise Section ---
st.header("Actividad")
st.markdown(
    """
    ¡Pon a prueba tus conocimientos! Responde las preguntas a continuación para demostrar tu comprensión de los conceptos de DEM.
    """
)

# Initialize session state for scoring if it doesn't exist
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'q1_answered' not in st.session_state:
    st.session_state.q1_answered = False
if 'q2_answered' not in st.session_state:
    st.session_state.q2_answered = False

# --- Question 1: DEM Interpretation ---
st.subheader("Pregunta 1: Interpretación del DEM")

# Create a simple DEM image for the question
dem_q1 = np.array([
    [10, 15, 20, 25, 30],
    [15, 20, 25, 30, 35],
    [20, 25, 30, 35, 40],
    [25, 30, 35, 40, 45],
    [30, 35, 40, 45, 50]
])

fig_q1, ax_q1 = plt.subplots(figsize=(6, 5))
im = ax_q1.imshow(dem_q1, cmap='terrain', origin='lower')
ax_q1.set_title("Cuadrícula DEM de muestra")
ax_q1.set_xticks(np.arange(5))
ax_q1.set_yticks(np.arange(5))
ax_q1.set_xticklabels(['A', 'B', 'C', 'D', 'E'])
ax_q1.set_yticklabels(['1', '2', '3', '4', '5'])
plt.colorbar(im, ax=ax_q1, label='Elevacion')

st.pyplot(fig_q1)

q1_answer = st.radio(
    "Basándose en la cuadrícula anterior, ¿qué celda tiene la elevación más alta?",
    ('A5', 'E1', 'C3', 'E5'),
    disabled=st.session_state.q1_answered
)

if st.button("Enviar respuesta 1", disabled=st.session_state.q1_answered):
    st.session_state.q1_answered = True
    if q1_answer == 'E5':
        st.success("¡Correcto! La celda en la coordenada E5 tiene el valor más alto (50), lo que indica la elevación más alta..")
        st.session_state.score += 1
    else:
        st.error("Incorrecto. El valor más alto está en la esquina inferior derecha, que corresponde a la celda E5.")

# --- Question 2: Conceptual Understanding ---
st.subheader("Pregunta 2: Comprensión conceptual")
q2_answer = st.radio(
    "¿Qué tipo de modelo de elevación representa la tierra desnuda, sin edificios ni árboles?",
    ('Modelo digital de superficie (DSM)', 'Modelo digital del terreno (DTM)', 'Modelo ráster', 'Modelo de cuadrícula digital'),
    disabled=st.session_state.q2_answered
)

if st.button("Enviar respuesta 2", disabled=st.session_state.q2_answered):
    st.session_state.q2_answered = True
    if q2_answer == 'Modelo digital del terreno (MDT)':
        st.success("¡Correcto! Un MDT es un modelo de suelo desnudo, útil para el análisis hidrológico y la modelización del flujo natural del agua..")
        st.session_state.score += 1
    else:
        st.error("Incorrecto. Un Modelo Digital de Superficie (MDS) incluye características como edificios y vegetación. La respuesta correcta es MDT.")

st.markdown("---")

autor = st.text_input("Ingrese su nombre y apellido:")
st.write(f"Realizado por: {autor}")

st.markdown("### Actividad")
st.markdown("""
1. Hacer las consultas requeridas.
2. Ingresar los resultados en la tabla.
3. Enviar por email el resultado.
""")