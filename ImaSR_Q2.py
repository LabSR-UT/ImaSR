# Imagenes SR
# Quiz 1

import streamlit as st

st.title('Quiz 2')
st.subheader('Pregunta 1:')

valor1 = st.radio("Que significa cada variable de la formula c = λ * f?",
    ["constante C, longitud, friccion", "velocidad de luz, longitud, frecuencia", "constante C, lambda, frecuencia", "Ninguna"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("Con que comportamiento se puede relacionar el albedo?",
    ["Transmision", "Absorcion", "Reflexion", "Ninguna"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
