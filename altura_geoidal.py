import streamlit as st

import numpy as np
import requests
import io

st.title('Altura GEOIDAL')

enlace_compartido = "https://drive.google.com/file/d/1j2Vey8zp1dGaTtSxhPSoXnzMqN432Zqu/view?usp=sharing"
archivo_id = enlace_compartido.split("/")[-2]
enlace_descarga = f"https://drive.google.com/uc?id={archivo_id}&export=download"
contenido = requests.get(enlace_descarga).content
data = np.loadtxt(io.BytesIO(contenido))
filas, columnas = data.shape

def calcular_interpolacion(latitud_deg, latitud_min, latitud_sec, longitud_deg, longitud_min, longitud_sec):
    latitud = latitud_deg + latitud_min/60 + latitud_sec/3600
    longitud = longitud_deg + longitud_min/60 + longitud_sec/3600
    longitud = longitud*-1

    latitud_superior_izquierda = 14.983333
    longitud_superior_izquierda = -79.983333
    resolucion = 0.03333333333333333

    # Cálculo de los índices de los puntos más cercanos
    fila = int((latitud_superior_izquierda - latitud) / resolucion)
    columna = int((longitud - longitud_superior_izquierda) / resolucion)

    lat1 = latitud_superior_izquierda - fila * resolucion
    lon1 = longitud_superior_izquierda + columna * resolucion
    lat2 = lat1 - resolucion
    lon2 = lon1 + resolucion

    val1 = data[fila, columna]
    val2 = data[fila, columna + 1]
    val3 = data[fila + 1, columna]
    val4 = data[fila + 1, columna + 1]

    interp_lat = ((latitud - lat1) / (lat2 - lat1)) * (val3 - val1) + val1
    interp_lat2 = ((latitud - lat1) / (lat2 - lat1)) * (val4 - val2) + val2
    interp_lon = ((longitud - lon1) / (lon2 - lon1)) * (interp_lat2 - interp_lat) + interp_lat

    return interp_lon
	
def decdeg2dms(dd):
   is_positive = dd >= 0
   dd = abs(dd)
   minutes,seconds = divmod(dd*3600,60)
   degrees,minutes = divmod(minutes,60)
   degrees = degrees if is_positive else -degrees
   return (degrees,minutes,seconds)

if data is not None:
	col1, col2 = st.columns(2)
	with col1:
		lat_dec = st.number_input("Ingrese latitud (decimal): (ej. 4.43)", value=0.0, placeholder="Ingrese el numero...")
		lon_dec = st.number_input("Ingrese longitud (decimal): (ej. 75.21 )", value=0.0, placeholder="Ingrese el numero...")
			
		latd,latm,lats = decdeg2dms(lat_dec)
		lond,lonm,lons = decdeg2dms(lon_dec)	

	with col2:
		valor = calcular_interpolacion(latd,latm,lats,lond,lonm,lons)
		st.write(f"La ondulación es: {valor} metros")

