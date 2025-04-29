# Imagenes SR
# Quiz 5

import streamlit as st

st.title('Quiz 5')
st.subheader('Pregunta 1:')

valor1 = st.radio("Cual es la diferencia entre plataforma satelital y sensor satelital?",
    ["Resolucion espectral", "Velocidad", "Captura de imagenes", "Orbita"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("Cual es la diferencia principal entre los programas Landsat & Sentinel?",
    ["Sensores", "Resolucion temporal", "Objetivo", "Todas las anteriores"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
