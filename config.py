# Default values and constants used by the reactor simulation.

# Default input values (used to pre-fill the Streamlit sidebar)
DEFAULT_K = 0.1  # reaction rate constant (1/s)
DEFAULT_C0 = 1.0  # initial concentration (mol/L)
DEFAULT_T0 = 300.0  # initial temperature (K)
DEFAULT_TROOM = 298.0  # room temperature (K)
DEFAULT_TIME = 100.0  # total simulation time (s)

# Fixed physical constants used in the temperature equation.
# These aren't exposed in the UI to keep things simple.
ALPHA = 5.0  # heat released per unit of reactant consumed
BETA = 0.05  # rate of heat loss to the surroundings

# Number of points used when plotting the solution
N_POINTS = 300
