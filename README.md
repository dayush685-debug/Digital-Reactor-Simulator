# Digital Reactor Simulator

A Streamlit app that simulates a simple chemical reactor: reactant
concentration decays over time, and the reactor temperature responds to the
reaction and to heat loss into the surroundings. The system is solved
numerically with `scipy.integrate.solve_ivp`.

## Folder Structure

```
Digital_Reactor_Simulator_2/
├── app.py            # Streamlit UI - sidebar inputs, plots, summary
├── simulation.py      # Runs solve_ivp and returns the results
├── models.py           # ReactorParams dataclass and the ODE system
├── config.py             # Default values and physical constants
├── plots.py                # Matplotlib figures
├── utils.py                  # Summary stats helper
├── requirements.txt
└── README.md
```

## Mathematical Model

```
dC/dt = -k * C
dT/dt = alpha * C - beta * (T - T_room)
```

- `C` - reactant concentration (mol/L)
- `T` - reactor temperature (K)
- `k` - reaction rate constant, set by the user
- `alpha` - heat released per unit of reactant consumed (fixed constant)
- `beta` - rate of heat loss to the surroundings (fixed constant)
- `T_room` - room temperature, set by the user

Concentration follows simple first-order decay. Temperature rises as the
reaction proceeds and falls back towards room temperature as heat is lost.
Both equations are solved together using the `RK45` method, an adaptive
Runge-Kutta solver well suited to smooth, non-stiff systems like this one.

## Technologies Used

- Python 3
- Streamlit - UI
- NumPy - array handling
- SciPy - `solve_ivp` for the ODE solver
- Matplotlib - plotting

## How to Run

```
pip install -r requirements.txt
streamlit run app.py
```

Then open the local URL Streamlit prints, set your parameters in the
sidebar, and click **Run Simulation**.

## Future Improvements

- Let the user adjust `alpha` and `beta` from the sidebar
- Add a CSV download button for the simulation results
- Compare multiple reactions on the same plot
- Add basic input validation (e.g. warn if T0 is unrealistic)
