import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Configuración de la página
st.set_page_config(page_title="Teoría de la Radiación", layout="wide")

st.title("☀️ Leyes de la Radiación")
st.markdown("""
Esta app interactiva ayuda a comprender y visualizar los tres principios fundamentales de la radiación térmica: 
la **Ley de Stefan-Boltzmann**, la **Ley de Desplazamiento de Wien** y la **Ley de Kirchhoff**.
""")
st.markdown("---")

# --- Sección 1: Ley de Stefan-Boltzmann ---
st.header("1. Ley de Stefan-Boltzmann")
st.write(r"""
La **ley de Stefan-Boltzmann** establece que la energía térmica radiante total emitida por una superficie es proporcional a la cuarta potencia de su temperatura absoluta.

$$P = \sigma \cdot \epsilon \cdot A \cdot T^4$$

* $P$: Potencia total radiada ($W$)
* $\sigma$: Constante de Stefan-Boltzmann ($5.67 \times 10^{-8} \, W \cdot m^{-2} \cdot K^{-4}$)
* $\epsilon$: Emisividad (de 0 a 1)
* $A$: Área superficial ($m^2$)
* $T$: Temperatura absoluta ($K$)
""")

with st.container():
    st.subheader("Interactividad:")
    col1, col2, col3 = st.columns(3)
    with col1:
        temperature = st.slider("Temperatura (Kelvin)", 200, 3000, 500, step=10)
    with col2:
        emissivity = st.slider("Emisividad (ε)", 0.0, 1.0, 1.0, step=0.01)
    with col3:
        area = st.number_input("Area (m2)", value=0.0, placeholder="Ingrese el area del objeto" )

    stefan_boltzmann_constant = 5.67e-8
    #area = 1.0  # Área fija de 1 m^2
    power = stefan_boltzmann_constant * emissivity * area * (temperature**4)
    
    st.metric(label=f"Potencia total radiada (W) para T={temperature}K", value=f"{power:.2f} W")

st.markdown("---")

# --- Sección 2: Ley de Desplazamiento de Wien ---
st.header("2. Ley de Desplazamiento de Wien")
st.write(r"""
Muestra la relación entre la temperatura y la longitud de onda donde la emisión es máxima ($\lambda_{max}$). 
A mayor temperatura, el pico se desplaza hacia longitudes de onda más cortas.

$$\lambda_{max} = \frac{b}{T}$$

* $b = 2.898 \times 10^{-3} \, m \cdot K$ (Constante de Wien)
""")



with st.container():
    st.subheader("Visualización de la Ley de Planck")
    temp_wien = st.slider("Ajustar Temperatura para el gráfico (Kelvin)", 0, 6000, 3000, step=10)
    
    wien_constant = 2.898e-3
    peak_m = wien_constant / temp_wien
    peak_nm = peak_m * 1e9

    st.metric(label="Longitud de onda máxima (λ_max)", value=f"{peak_nm:.2f} nm")

    # Función de Planck corregida
    def planck_radiation(wavelength_nm, temp):
        h = 6.626e-34
        c = 3.0e8
        k = 1.38e-23
        w_m = wavelength_nm * 1e-9
        
        exponent = (h * c) / (w_m * k * temp)
        # Evitar overflow en exp
        with np.errstate(over='ignore'):
            denominator = np.exp(exponent) - 1
        
        radiance = (2 * h * c**2) / (w_m**5 * denominator)
        return radiance / 1e9 # Convertir a por nm para el eje Y

    wavelengths = np.linspace(100, 3000, 600)
    fig = go.Figure()

    # Añadir curvas de referencia
    for t in [3000, 4000, 5000]:
        fig.add_trace(go.Scatter(x=wavelengths, y=planck_radiation(wavelengths, t), 
                                 name=f"{t}K", line=dict(dash='dash', width=1)))
    
    # Curva interactiva
    fig.add_trace(go.Scatter(x=wavelengths, y=planck_radiation(wavelengths, temp_wien), 
                             name=f"Actual: {temp_wien}K", line=dict(color='orange', width=3)))

    fig.update_layout(title="Espectro de Cuerpo Negro", xaxis_title="λ (nm)", yaxis_title="Radiancia")
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- Sección 3: Ley de Kirchhoff ---
st.header("3. Ley de Kirchhoff")
st.write(r"En equilibrio térmico: $\epsilon(\lambda, T) = \alpha(\lambda, T)$")

material = st.selectbox(
    "Seleccione un material",
    ["Cuerpo negro perfecto", "Plata pulida", "Madera", "Asfalto"]
)

material_data = {
    "Cuerpo negro perfecto": (1.0, "Absorbe y emite al máximo nivel teórico."),
    "Plata pulida": (0.02, "Refleja casi todo; emite y absorbe muy poco."),
    "Madera": (0.90, "Buen emisor de infrarrojos."),
    "Asfalto": (0.95, "Casi un cuerpo negro; se calienta mucho bajo el sol.")
}

val, desc = material_data[material]
col_a, col_b = st.columns(2)
col_a.metric("Emisividad (ε)", val)
col_b.metric("Absorptividad (α)", val)
st.info(desc)

st.markdown("---")

res1 = st.text_input("Potencia total radiada (W) del planeta Tierra")
if res1:
    st.write(f"{res1}")
res2 = st.text_input("Longitud de onda donde la emisión del planeta tierra es máxima")
if res2:
    st.write(f"{res2}")
res3 = st.text_input("Si la absorvancia de la tierra es 70%, cual es su emisividad?")
if res3:
    st.write(f"{res3}")
autor = st.text_input("Realizado por:")
if autor:
    st.write(f"Autor: **{autor}**")