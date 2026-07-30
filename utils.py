# Small helper functions used by the app.

import numpy as np


def summarize(time, concentration, temperature):
    """Builds a short summary dict, including the peak temperature point."""
    peak_idx = np.argmax(temperature)
    return {
        "final_concentration": concentration[-1],
        "final_temperature": temperature[-1],
        "peak_temperature": temperature[peak_idx],
        "peak_time": time[peak_idx],
    }
