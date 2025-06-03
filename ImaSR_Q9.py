# Interpretacion SR
# Quiz 9

import streamlit as st

st.title('Quiz 6')
st.subheader('Pregunta 1:')

valor1 = st.radio("Cual satelite no tiene banda termal?",
    ["ASTER", "TIMS", "Sentinel2", "Lansat8", "Todas las anteriores", "Ninguna de las anteriores"],
	index=None,
)

st.write("Usted selecciono: ", valor1)

st.subheader('Pregunta 2:')

valor2 = st.radio("Cual factor no influye en la interpretacion de imagenes termales?",
    ["Geometria del dosel", "Cobertura de nubes", "Topografia", "Zonas geotermales","Todas las anteriores", "Ninguna de las anteriores"],
	index=None,
)

st.write("Usted selecciono: ", valor2)
