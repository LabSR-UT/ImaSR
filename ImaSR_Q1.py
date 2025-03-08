# Imagenes SR
# Quiz 1

import streamlit as st

st.title('Quiz 1')
st.subheader('Pregunta 1:')

valor1 = st.radio("Cual fue la razon que el satelite Landsat 5 duro mas tiempo funcionando?",
    ["Calidad de los componentes", "Cantidad de combustible", "Orbita baja"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("Cual fue el principal aporte del satelite Landsat5 al programa Landsat?",
    ["Mayor cantidad de sensores", "Mayor capacidad de almacenamiento", "Permitio dar continuidad al programa"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
