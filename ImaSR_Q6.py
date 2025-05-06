# Imagenes SR
# Quiz 6

import streamlit as st

st.title('Quiz 6')
st.subheader('Pregunta 1:')

valor1 = st.radio("Cual es la diferencia principal entre los satelites privados y publicos?",
    ["Precio", "Globales", "Resolucion", "Todas"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("Las imagenes Landsat y Sentinel se pueden combinar?",
    ["Si", "No", "Algunas veces", "Todas las anteriores"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
