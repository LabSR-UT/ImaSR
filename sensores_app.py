import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("🛰️ Resoluciones de Sensores")

# --- Satellite dataset ---
data = [
    {
        "Satelite": "Landsat 8",
        "Espacial (m)": "15 (pan), 30 (multiespectral), 100 (térmico)",
        "Bandas espectrales": 11,
        "Temporal (dias)": 16,
        "Radiometrica (bits)": 16
    },
    {
        "Satelite": "Sentinel-2",
        "Espacial (m)": "10, 20, 60",
        "Bandas espectrales": 13,
        "Temporal (dias)": 5,
        "Radiometrica (bits)": 16
    },
    {
        "Satelite": "MODIS",
        "Espacial (m)": "250, 500, 1000",
        "Bandas espectrales": 36,
        "Temporal (dias)": 1,
        "Radiometrica (bits)": 12
    },
    {
        "Satelite": "WorldView-3",
        "Espacial (m)": "0,31 (pan), 1,24 (multiespectral)",
        "Bandas espectrales": 29,
        "Temporal (dias)": "<1",
        "Radiometrica (bits)": 11
    }
]

df = pd.DataFrame(data)

# --- Display Table ---
st.subheader("📊 Comparacion de Resoluciones de Sensores")
st.dataframe(df, use_container_width=True)

# --- Satellite Selection ---
sat1 = st.selectbox("Seleccione Satelite 1", df["Satelite"])
sat2 = st.selectbox("Seleccione Satelite 2", df["Satelite"], index=1)

row1 = df[df["Satelite"] == sat1].iloc[0]
row2 = df[df["Satelite"] == sat2].iloc[0]

# --- Comparison Display ---
st.subheader("⚖️ Comparacion")

col1, col2 = st.columns(2)

with col1:
    st.markdown(f"### {sat1}")
    st.json(row1.to_dict())

with col2:
    st.markdown(f"### {sat2}")
    st.json(row2.to_dict())

# --- Explanation Section ---
st.subheader("📘 Que significan estas resoluciones?")

st.markdown("""
- **Resolución espacial**: Tamaño de un píxel en el terreno (menor = mayor detalle)
- **Resolución espectral**: Número de bandas de longitud de onda capturadas
- **Resolución temporal**: Frecuencia con la que el satélite revisita la misma zona
- **Resolución radiométrica**: Sensibilidad a las diferencias de energía (profundidad de bits)
""")


# --- User Input ---
st.subheader("💬 Preguntas (justifique la respuesta)")

question1 = st.text_input("1) ¿Qué satélite seria mas util para enfrentar un incendio forestal?")
st.write("**Respuesta:**", question1)

question2 = st.text_input("2) ¿Qué satélite seria mas util para detectar cambios en tipos de cobertura?")
st.write("**Respuesta:**", question2)

question3 = st.text_input("3) ¿Qué satélite seria apropiado para ayudar en un terremoto?")
st.write("**Respuesta:**", question3)

