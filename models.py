# Defines the reactor's parameters and the ODE system that describes it.

from dataclasses import dataclass

import config


@dataclass
class ReactorParams:
    """Groups all inputs needed to run one simulation."""
    k: float
    c0: float
    t0: float
    t_room: float
    sim_time: float
    alpha: float = config.ALPHA
    beta: float = config.BETA


def reactor_odes(t, y, params: ReactorParams):
    """ODE system passed to solve_ivp. y = [concentration, temperature]."""
    C, T = y
    dC_dt = -params.k * C
    dT_dt = params.alpha * C - params.beta * (T - params.t_room)
    return [dC_dt, dT_dt]
