import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Set the page title and a brief introduction
st.set_page_config(page_title="Teoria de la Radiacion", layout="wide")

st.title("☀️ Leyes de la radiacion")
st.markdown("""
Esta app interactiva ayuda a comprender y visualizar los tres principios fundamentales de la radiacion termal: ley de Stefan-Boltzmann, ley de desplazamiento de Wien, y ley de Kirchhoff's.
""")
st.markdown("---")

# --- Stefan-Boltzmann Law Section ---
st.header("1. Ley de Stefan-Boltzmann")
st.write("""
La **ley de Stefan-Boltzmann** establece que la energía térmica radiante total emitida por una superficie es proporcional a la cuarta potencia de su temperatura absoluta.

$P = \sigma \epsilon A T^4$

* $P$ = Potencia total radiada ($W$)
* $\sigma$ = Constante de Stefan-Boltzmann ($5.67 * 10^{-8} \, W \cdot m^{-2} \cdot K^{-4}$)
* $\epsilon$ = Emisividad (de 0 a 1, donde 1 representa un cuerpo negro perfecto)
* $A$ = Área superficial ($m^2$)
* $T$ = Temperatura absoluta ($K$)
""")

# Create interactive widgets for the Stefan-Boltzmann law
with st.container():
    st.subheader("Interactividad:")
    col1, col2 = st.columns(2)
    with col1:
        temperature = st.slider("Seleccione una Temperatura (Kelvin)", 200, 3000, 500, step=50, help="Temperaturas típicas de objetos como una estufa caliente o una estrella.")
    with col2:
        emissivity = st.slider("Seleccione una Emisividad (ε)", 0.0, 1.0, 1.0, step=0.01, help="1.0 para un cuerpo negro perfecto, 0.2 para metales brillantes.")

    stefan_boltzmann_constant = 5.67e-8
    area = 1.0 # Assume a fixed area of 1 m^2 for simplicity

    # Calculate the power and format the output
    power = stefan_boltzmann_constant * emissivity * area * (temperature**4)
    st.metric(label=f"Potencia total radiada (W) for T={temperature}K, ε={emissivity}", value=f"{power:.2f}")

st.markdown("---")

# --- Wien's Displacement Law Section ---
st.header("2. Ley de Desplazamiento de Wien")
st.write("""
La **ley de desplazamiento de Wien** muestra la relación entre la temperatura de un objeto y la longitud de onda máxima de su radiación emitida. A medida que un objeto se calienta, su emisión máxima se desplaza hacia longitudes de onda más cortas y energéticas.

$\lambda_{max}$ = $\frac{b}{T}$

* $\lambda_{max}$ = Longitud de onda máxima de emisión ($m$)
* $b$ = Constante de desplazamiento de Wien ($2.898 \times 10^{-3} \, m \cdot K$)
* $T$ = Temperatura absoluta ($K$)
""")

# Interactive widgets for Wien's law
with st.container():
    st.subheader("Interactividad:")
    temperature_wien = st.slider("Seleccione una Temperatura para la Ley de Wien (Kelvin)", 500, 6000, 2500, step=100)
    wien_constant = 2.898e-3

    # Calculate the peak wavelength in meters and nanometers
    peak_wavelength_m = wien_constant / temperature_wien
    peak_wavelength_nm = peak_wavelength_m * 1e9

    # Display the results
    st.metric(label=f"Longitud de onda máxima (λ_max) for T={temperature_wien}K", value=f"{peak_wavelength_nm:.2f} nm")

    # Determine the region of the electromagnetic spectrum
    if peak_wavelength_nm < 400:
        spectrum_region = "Ultravioleta"
    elif 400 <= peak_wavelength_nm <= 700:
        spectrum_region = "Luz visible"
    else:
        spectrum_region = "Infrarroja"

    st.info(f"La emisión máxima para esta temperatura está en la región **{spectrum_region}** del espectro electromagnético.")

    # Visualization of Planck's Law to show Wien's Law
    st.subheader("Curva de radiación de cuerpo negro")
    st.write("Esta gráfica muestra la radiancia espectral de un cuerpo negro a diferentes temperaturas. Observe cómo el pico se desplaza hacia la izquierda (longitudes de onda más cortas) a medida que aumenta la temperatura.")

    def planck_radiation(wavelength, temp):
        h = 6.626e-34  # Planck's constant
        c = 3.0e8      # Speed of light
        k = 1.38e-23   # Boltzmann constant
        
        # Wavelength must be in meters for the formula
        wavelength_m = wavelength * 1e-9

        numerator = 2 * h * c**2
        denominator = (wavelength_m**5) * (np.exp((h * c) / (wavelength_m * k * temp)) - 1)
        return numerator / denominator

    # Generate data for the plot
    wavelengths = np.linspace(100, 3000, 500) # Wavelengths in nm
    temps = [2000, 3000, 4000, 5000, 6000]

    fig = go.Figure()

    for t in temps:
        radiance = planck_radiation(wavelengths, t)
        fig.add_trace(go.Scatter(x=wavelengths, y=radiance, mode='lines', name=f'{t} K'))

    fig.update_layout(
        title="Radiancia espectral del cuerpo negro vs. longitud de onda",
        xaxis_title="Longitud de onda (nm)",
        yaxis_title="Radiancia espectral (W/m²/sr/nm)",
        legend_title="Temperatura",
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- Kirchhoff's Law Section ---
st.header("3. Ley de Radiacion termal de Kirchhoff")
st.write("""
La **ley de Kirchhoff** establece que, para un cuerpo en equilibrio térmico, su emisividad ($\epsilon$) es igual a su absortividad ($\alpha$) para la misma longitud de onda y temperatura.

$\epsilon(\lambda, T)$ = $\alpha(\lambda, T)$

* Un buen emisor también es un buen absorbente.
* Un mal emisor también es un mal absorbente (y un buen reflector).

Por eso, las superficies oscuras y mate se calientan rápidamente al sol (buenos absorbentes) y también irradian calor eficientemente, mientras que las superficies brillantes y claras reflejan la mayor parte de la radiación entrante y, por lo tanto, se mantienen más frías.
""")

st.subheader("Interactividad:")
material = st.selectbox(
    "Seleccione un material",
    ["Cuerpo negro perfecto (ideal)", "Plata pulida", "Madera", "Asfalto"],
    help="Observe la relación entre la absortividad y la emisividad."
)

if material == "Cuerpo negro perfecto (ideal)":
    st.metric(label="Emisividad (ε)", value=1.0)
    st.metric(label="Absorción (α)", value=1.0)
    st.info("Un cuerpo negro absorbe toda la radiación que cae sobre él y también es el emisor más eficiente de radiación térmica.")
elif material == "Plata pulida":
    st.metric(label="Emisividad (ε)", value=0.02)
    st.metric(label="Absorción (α)", value=0.02)
    st.info("La plata pulida absorbe mal y, por lo tanto, es un emisor deficiente. Es un excelente reflector de la radiación térmica.")
elif material == "Madera":
    st.metric(label="Emisividad (ε)", value=0.9)
    st.metric(label="Absorción (α)", value=0.9)
    st.info("La madera es un absorbente y emisor relativamente bueno, lo que la hace adecuada para cosas como utensilios de cocina que necesitan transferir bien el calor.")
elif material == "Asfalto":
    st.metric(label="Emisividad (ε)", value=0.95)
    st.metric(label="Absorción (α)", value=0.95)
    st.info("El asfalto oscuro absorbe casi toda la radiación solar y la emite en forma de calor, razón por la cual las carreteras pueden calentarse tanto.")

st.markdown("---")

autor = st.text_input("Ingrese su nombre y apellido:")
st.write(f"Realizado por: {autor}")

st.markdown("### Actividad")
st.markdown("""
1. Hacer las consultas requeridas.
2. Ingresar los resultados en la tabla.
3. Enviar por email el resultado.
""")
