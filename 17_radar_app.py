import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Set Page Configuration ---
st.set_page_config(
    page_title="Imagenes de Radar",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- App Title and Introduction ---
st.title("📡 Imagenes de Radar")

st.markdown("---")

# --- 2. Interactive Radar Image Manipulation ---
st.header("Actividad: manipulacion de una imagen de radar")
st.markdown(
    """
    Usa los controles de la barra lateral para crear y manipular una imagen de radar simulada.
    Presta atención a cómo los cambios de contraste y ruido afectan la claridad visual y la interpretación de la imagen.
    """
)

# Function to generate a simple simulated radar image
def generate_radar_image(size=200):
    """Generates a simple simulated radar image with different features."""
    img = np.zeros((size, size))

    # Simulate a dark body of water (low backscatter)
    img[int(size*0.6):int(size*0.9), int(size*0.1):int(size*0.4)] = 5
    
    # Simulate a bright urban area (high backscatter due to buildings)
    img[int(size*0.1):int(size*0.3), int(size*0.6):int(size*0.9)] = 200
    
    # Simulate an intermediate forest area (medium backscatter)
    img[int(size*0.4):int(size*0.6), int(size*0.3):int(size*0.7)] = 100
    
    # Add a bright corner reflector
    img[int(size*0.15):int(size*0.18), int(size*0.15):int(size*0.18)] = 255
    
    return img

# Create a sample radar image and a sidebar for controls
radar_size = 200
base_radar_data = generate_radar_image(size=radar_size)

with st.sidebar:
    st.title("Controles")
    st.markdown("Ajuste la visualización de la imagen del radar aquí.")
    
    # Sliders for customization
    contrast = st.slider(
        "Contraste",
        min_value=0.5,
        max_value=2.0,
        value=1.0,
        step=0.1,
        help="Ajusta el contraste de la imagen del radar. Los valores más altos hacen que las áreas brillantes sean más brillantes y las oscuras, más oscuras.."
    )
    
    noise_level = st.slider(
        "Ruido aleatorio",
        min_value=0.0,
        max_value=50.0,
        value=5.0,
        step=1.0,
        help="Simula el ruido o las motas del sensor. Los valores altos hacen que la imagen sea granulada."
    )
    
    colormap_option = st.selectbox(
        "Seleccionar mapa de colores",
        ('gray', 'viridis', 'jet', 'inferno'),
        help="Elija una paleta de colores diferente para la imagen.."
    )

# Apply user settings to the radar data
modified_radar_data = (base_radar_data * contrast) + (np.random.rand(radar_size, radar_size) * noise_level)
modified_radar_data = np.clip(modified_radar_data, 0, 255) # Clip values to stay in valid range

# Create and display the plot
fig, ax = plt.subplots(figsize=(10, 8))
ax.imshow(modified_radar_data, cmap=colormap_option)
ax.set_title("Imagen de radar interactiva", fontsize=16)
ax.set_xlabel("Coordenada X")
ax.set_ylabel("Coordenada Y")
ax.grid(False)
plt.colorbar(ax.imshow(modified_radar_data, cmap=colormap_option), ax=ax, label='Intensidad de retrodispersión')
st.pyplot(fig)

st.markdown("---")

feedback1 = st.text_area("Que pasa cuando se cambia el contraste?")
st.write(feedback1)

feedback2 = st.text_area("Que pasa cuando se el ruido?")
st.write(feedback2)

st.markdown("---")

autor = st.text_input("Ingrese su nombre y apellido:")
st.write(f"Realizado por: {autor}")

st.markdown("### Actividad")
st.markdown("""
1. Interactuar con la aplicacion.
2. Identificar cambios relevantes.
3. Enviar por email el resultado.
""")
