# Builds the matplotlib figures shown in the Streamlit app.

import matplotlib.pyplot as plt


def plot_concentration(time, concentration):
    fig, ax = plt.subplots()
    ax.plot(time, concentration, color="tab:blue")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Concentration (mol/L)")
    ax.set_title("Concentration vs Time")
    ax.grid(True)
    return fig


def plot_temperature(time, temperature, t_room, peak_time, peak_temp):
    fig, ax = plt.subplots()
    ax.plot(time, temperature, color="tab:red", label="Reactor Temperature")
    ax.axhline(t_room, color="gray", linestyle="--", label="Room Temperature")
    ax.scatter([peak_time], [peak_temp], color="black", zorder=5, label="Peak Temperature")
    ax.set_xlabel("Time (s)")
    ax.set_ylabel("Temperature (K)")
    ax.set_title("Temperature vs Time")
    ax.legend()
    ax.grid(True)
    return fig
