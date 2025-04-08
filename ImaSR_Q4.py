# Imagenes SR
# Quiz 1

import streamlit as st

st.title('Quiz 4')
st.subheader('Pregunta 1:')

valor1 = st.radio("Que elementos conforman un Sistema de Referencia Espacial?",
    ["Sistema de Coordenadas/Proyeccion/Unidades", "Sistema de Coordenadas/Proyeccion/Datum", "Unidades/Proyeccion/Datum"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("Cual es la diferencia el Sistema de Coordenadas UTM (Universal Transverse Mercator) vs MS (MagnaSirgas)?",
    ["Cobertura global vs local", "Longitud de la faja", "Ancho de la faja", "Todas las anteriores"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
