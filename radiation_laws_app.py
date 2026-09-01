import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Constants
h = 6.62607015e-34      # Planck constant (J s)
c = 2.99792458e8        # Speed of light (m/s)
k = 1.380649e-23        # Boltzmann constant (J/K)
sigma = 5.670374419e-8  # Stefan-Boltzmann constant (W m^-2 K^-4)
b = 2.897771955e-3      # Wien's displacement constant (m K)

st.set_page_config(page_title="Radiation Laws Explorer", layout="wide")
st.title("🌡️ Thermal Radiation Laws Explorer")
st.markdown("Interactive tool to explore **Stefan–Boltzmann**, **Wien's displacement**, and **Kirchhoff's** radiation laws.")

st.sidebar.header("Settings")

# Temperature input
T = st.sidebar.slider("Temperature (K)", 100, 6000, 5778, 10, help="Absolute temperature of the blackbody")

# Wavelength range for Planck curve
lambda_min = st.sidebar.slider("Wavelength min (nm)", 1, 3000, 100, 10)
lambda_max = st.sidebar.slider("Wavelength max (nm)", 1001, 10000, 3000, 100)
lambda_min_m = lambda_min * 1e-9
lambda_max_m = lambda_max * 1e-9

# Kirchhoff emissivity
emissivity = st.sidebar.slider("Emissivity (ε) for Kirchhoff's law", 0.0, 1.0, 0.95, 0.01, help="Ratio of emitted to blackbody radiation (0–1)")

# Tabs for each law
tab1, tab2, tab3 = st.tabs(["Stefan–Boltzmann", "Wien's Displacement", "Kirchhoff's Law"])

# ---------- Stefan-Boltzmann ----------
with tab1:
    st.header("Stefan–Boltzmann Law")
    st.latex(r"M = \sigma T^4")
    st.markdown(f"**Total emitted power (exitance)** at T = {T} K:")
    M = sigma * T**4
    st.metric("M (W/m\u00B2)", f"{M:,.2f}")
    st.markdown("This law gives the **integrated** power over all wavelengths for a perfect blackbody.")

    # Plot Planck curve with area under curve annotated
    lambdas = np.linspace(lambda_min_m, lambda_max_m, 500)
    B_lambda = (2*h*c**2) / (lambdas**5 * (np.exp(h*c/(lambdas*k*T)) - 1))  # W sr^-1 m^-3
    # Convert to spectral exitance (integrate over hemisphere): M_lambda = pi * B_lambda
    M_lambda = np.pi * B_lambda  # W m^-3

    fig_sb = go.Figure()
    fig_sb.add_trace(go.Scatter(x=lambdas*1e9, y=M_lambda, mode="lines", name="Spectral exitance"))
    fig_sb.update_layout(
        title="Blackbody Spectral Exitance (Planck Curve)",
        xaxis_title="Wavelength (nm)",
        yaxis_title="Spectral Exitance (W m⁻\u00B3)",
        height=400
    )
    st.plotly_chart(fig_sb, use_container_width=True)

# ---------- Wien's Displacement ----------
with tab2:
    st.header("Wien's Displacement Law")
    st.latex(r"\lambda_{\text{max}} = \frac{b}{T}")
    lambda_max_wien = b / T
    st.markdown(f"**Peak wavelength** at T = {T} K:")
    st.metric("λ_max (nm)", f"{lambda_max_wien*1e9:.1f}")
    st.markdown("As temperature increases, the peak shifts to **shorter wavelengths** (bluer).")

    # Highlight peak on Planck curve
    fig_wien = go.Figure()
    fig_wien.add_trace(go.Scatter(x=lambdas*1e9, y=M_lambda, mode="lines", name="Spectral exitance"))
    fig_wien.add_trace(go.Scatter(
        x=[lambda_max_wien*1e9],
        y=[np.interp(lambda_max_wien, lambdas, M_lambda)],
        mode="markers+text",
        name="λ_max",
        marker=dict(size=10, color="red"),
        text=["λ_max"],
        textposition="top center"
    ))
    fig_wien.update_layout(
        title="Wien's Law: Peak Wavelength on Planck Curve",
        xaxis_title="Wavelength (nm)",
        yaxis_title="Spectral Exitance (W m⁻\u00B3)",
        height=400
    )
    st.plotly_chart(fig_wien, use_container_width=True)

# ---------- Kirchhoff's Law ----------
with tab3:
    st.header("Kirchhoff's Law of Thermal Radiation")
    st.latex(r"\varepsilon(\lambda, T) = \alpha(\lambda, T)")
    st.markdown(f"For a **gray body** with emissivity ε = {emissivity:.2f}:")
    M_real = emissivity * M
    st.metric("Real emitted power (W/m\u00B2)", f"{M_real:,.2f}")
    st.markdown("Kirchhoff's law states that **emissivity equals absorptivity** at each wavelength and temperature for a body in thermal equilibrium.")

    # Plot blackbody vs real emitter
    M_lambda_real = emissivity * M_lambda
    fig_kirch = go.Figure()
    fig_kirch.add_trace(go.Scatter(x=lambdas*1e9, y=M_lambda, mode="lines", name="Blackbody (ε=1)"))
    fig_kirch.add_trace(go.Scatter(x=lambdas*1e9, y=M_lambda_real, mode="lines", name=f"Real body (ε={emissivity:.2f})"))
    fig_kirch.update_layout(
        title="Blackbody vs Real Emitter (Kirchhoff's Law)",
        xaxis_title="Wavelength (nm)",
        yaxis_title="Spectral Exitance (W m⁻\u00B3)",
        height=400
    )
    st.plotly_chart(fig_kirch, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.info("Tip: Adjust temperature to see how the Planck curve, total power, and peak wavelength change.")
