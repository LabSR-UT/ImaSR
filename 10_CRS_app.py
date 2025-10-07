import streamlit as st
import folium
from streamlit_folium import folium_static
from pyproj import Proj, transform
import pandas as pd

# Set the page title and a brief introduction
st.set_page_config(page_title="Sistemas de Referencia de Coordenadas", layout="wide")

st.title("🗺️ Sistemas de Referencia de Coordenadas (CRS)")
st.markdown("""
¡Bienvenido al Explorador de Sistemas de Referencia de Coordenadas (SRC)! Esta aplicación está diseñada para que los estudiantes de teledetección comprendan un concepto fundamental de la ciencia geoespacial: **cómo se definen y representan las ubicaciones en la Tierra**.

Un SRC es un sistema que se utiliza para localizar con precisión una posición en la superficie terrestre. Se compone de un **datum**, un **elipsoide** y una **proyección**.
""")
st.markdown("---")

st.header("1. Sistemas de coordenadas geográficas vs. sistemas de coordenadas proyectadas")
st.markdown("""
* **Sistemas de Coordenadas Geográficas (GCS):** Utilizan una superficie esférica 3D (como un globo terráqueo) para definir ubicaciones. El GCS más común es **WGS84**, que utiliza la latitud y la longitud para localizar una ubicación. Las unidades suelen ser grados.
* **Sistemas de Coordenadas Proyectadas (PCS):** Utilizan una superficie plana 2D para definir ubicaciones. Se utiliza una proyección para transformar los datos 3D del GCS en esta superficie plana. Esto introduce cierta distorsión, pero es esencial para medir distancias y áreas con precisión en un mapa plano. Las unidades suelen ser metros o pies. Un ejemplo común es **UTM**.
""")

# --- Sidebar for user input ---
st.sidebar.header("Ingrese las coordinadas")
st.sidebar.markdown("Ingrese la latitud y longitud para ver la transformacion de coordenadas y la visualizacion en el mapa.")

default_lat, default_lon = 4.4286, -75.2134 # Ibague
lat = st.sidebar.number_input("Latitud (grados)", min_value=-90.0, max_value=90.0, value=default_lat, step=0.0001)
lon = st.sidebar.number_input("Longitud (grados)", min_value=-180.0, max_value=180.0, value=default_lon, step=0.0001)

# --- CRS Selection ---
st.sidebar.header("Seleccione un CRS proyectado")
crs_options = {
    "UTM Zona 18N (Colombia)": "epsg:32618",
    "Magna Sirgas (Colombia Region central)": "epsg:3116",
    "Origen Nacional (Colombia)": "epsg:9377",
}
selected_crs_name = st.sidebar.selectbox("Elija un PCS:", list(crs_options.keys()))
selected_epsg_code = crs_options[selected_crs_name]

# --- Coordinate Transformations ---
st.header("2. Conversión de coordenadas: : Geografico (GRS) a Proyectado (PCS)")
st.markdown(f"""
Aquí, convertiremos sus coordenadas de entrada de **WGS84 (GCS)** a su **Sistema de coordenadas proyectadas (PCS)** seleccionado.
""")
try:
	# Define the two CRS using pyproj
	wgs84 = Proj(init='epsg:4326')
	pcs = Proj(init=selected_epsg_code)

	# Perform the transformation
	utm_x, utm_y = transform(wgs84, pcs, lon, lat)

	st.subheader("Sus coordenadas:")
	col1, col2 = st.columns(2)
	with col1:
		st.metric("WGS84 (GCS)", f"Latitud: {lat:.4f}, Longitud: {lon:.4f}")
	with col2:
		st.metric(f"{selected_crs_name} (PCS)", f"Estes (E): {utm_x:.2f} m, Nortes (N): {utm_y:.2f} m")

except Exception as e:
    st.error(f"Se produjo un error durante la transformación de coordenadas: {e}. Por favor, revise sus datos..")

# --- Map Visualization ---
st.header("3. Mapa de visualization")
st.markdown("""
El mapa a continuación muestra la ubicación seleccionada. Un **GCS** define este punto en la superficie curva de la Tierra, mientras que un **PCS** define su ubicación en un mapa plano y cuadriculado.
""")

# Create a Folium map centered on the input coordinates
m = folium.Map(location=[lat, lon], zoom_start=12)

# Add a marker for the user's selected point
folium.Marker(
    [lat, lon],
    tooltip="Punto seleccionado",
    icon=folium.Icon(color="red", icon="info-sign")
).add_to(m)

# Display the map
folium_static(m)

# --- Initial data for the editable table ---
initial_data = {
    'SRC': [
        'Geografico (4326)',
        'UTM (32618)',
        'MagnaSirgas (3116)',
        'Origen Nacional (9377)'
    ],
    'Latitud': [
        '',
        '',
        '',
        ''
    ],
    'Longitud': [
        '',
        '',
        '',
        ''
    ]
}

df = pd.DataFrame(initial_data).set_index('SRC')

# --- Use st.data_editor for the interactive table ---
st.header("Tabla comparativa")
st.info("Edite las celdas a continuación para ingresar los valores correspondientes")
edited_df = st.data_editor(
    df,
    use_container_width=True,
    height=250
)
st.markdown("---")

st.markdown("---")

lugar = st.text_input("Describa el lugar seleccionado:")
st.write(f"Descripcion: {lugar}")

autor = st.text_input("Ingrese su nombre y apellido:")
st.write(f"Realizado por: {autor}")

st.markdown("### Actividad")
st.markdown("""
1. Hacer las consultas requeridas.
2. Ingresar los resultados en la tabla.
3. Enviar por email el resultado.
""")