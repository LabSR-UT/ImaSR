# Interpretacion SR
# Quiz 6

import streamlit as st

st.title('Quiz 6')
st.subheader('Pregunta 1:')

valor1 = st.radio("Cuales son los modelos de DEMs:?",
    ["DTM", "DKM", "DCM", "Todas las anteriores", "Ninguna de las anteriores"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("De que depende la calidad de un DEM?",
    ["Muestreo", "Interpolacion", "Resolucion", "Rugosidad","Todas las anteriores", "Ninguna de las anteriores"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
