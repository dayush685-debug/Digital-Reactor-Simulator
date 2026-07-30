# Runs the reactor simulation by solving the ODE system numerically.

import numpy as np
from scipy.integrate import solve_ivp

import config
from models import ReactorParams, reactor_odes


def run_simulation(params: ReactorParams):
    """Solves the ODE system with RK45 and returns time, C and T arrays."""
    t_span = (0, params.sim_time)
    t_eval = np.linspace(0, params.sim_time, config.N_POINTS)
    y0 = [params.c0, params.t0]

    result = solve_ivp(
        reactor_odes,
        t_span,
        y0,
        args=(params,),
        t_eval=t_eval,
        method="RK45",
    )

    time = result.t
    concentration = result.y[0]
    temperature = result.y[1]
    return time, concentration, temperature
