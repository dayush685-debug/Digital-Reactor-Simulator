# Streamlit app for the Digital Reactor Simulator.

import streamlit as st

import config
from models import ReactorParams
from simulation import run_simulation
from plots import plot_concentration, plot_temperature
from utils import summarize

st.set_page_config(page_title="Digital Reactor Simulator", layout="centered")

st.title("Digital Reactor Simulator")
st.write(
    "This app simulates a simple chemical reactor. It models how the "
    "concentration of a reactant drops over time, and how the reactor "
    "temperature changes because of the reaction and heat loss to the "
    "surroundings."
)

st.sidebar.header("Simulation Parameters")
k = st.sidebar.number_input(
    "Reaction rate constant (k)", value=config.DEFAULT_K, min_value=0.0, step=0.01
)
c0 = st.sidebar.number_input(
    "Initial concentration (C0)", value=config.DEFAULT_C0, min_value=0.0, step=0.1
)
t0 = st.sidebar.number_input(
    "Initial temperature (K)", value=config.DEFAULT_T0, step=1.0
)
t_room = st.sidebar.number_input(
    "Room temperature (K)", value=config.DEFAULT_TROOM, step=1.0
)
sim_time = st.sidebar.number_input(
    "Simulation time (s)", value=config.DEFAULT_TIME, min_value=1.0, step=10.0
)

run_button = st.sidebar.button("Run Simulation")

if run_button:
    params = ReactorParams(k=k, c0=c0, t0=t0, t_room=t_room, sim_time=sim_time)
    time, concentration, temperature = run_simulation(params)
    summary = summarize(time, concentration, temperature)

    st.subheader("Concentration over Time")
    st.pyplot(plot_concentration(time, concentration))

    st.subheader("Temperature over Time")
    st.pyplot(plot_temperature(
        time, temperature, t_room, summary["peak_time"], summary["peak_temperature"]
    ))

    st.subheader("Simulation Summary")
    st.write(f"Final concentration: {summary['final_concentration']:.3f} mol/L")
    st.write(f"Final temperature: {summary['final_temperature']:.2f} K")
    st.write(
        f"Peak temperature: {summary['peak_temperature']:.2f} K "
        f"at t = {summary['peak_time']:.1f} s"
    )
else:
    st.info("Set your parameters in the sidebar and click 'Run Simulation' to begin.")
