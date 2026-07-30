# Interview Notes

Prep notes for explaining this project in a technical interview.

## 1. Overall Architecture

Six small files, each with one job:

- `config.py` holds the default values and constants
- `models.py` defines the reactor's state and the ODE system
- `simulation.py` runs the numerical solver
- `plots.py` builds the matplotlib figures
- `utils.py` computes summary numbers
- `app.py` wires everything together into a Streamlit page

No classes for the sake of classes, no layers of indirection - just
functions that take inputs and return outputs, called in sequence from
`app.py`.

## 2. Data Flow

1. User sets `k`, `C0`, `T0`, `T_room`, and simulation time in the sidebar.
2. On clicking **Run Simulation**, `app.py` builds a `ReactorParams` object.
3. `run_simulation()` passes that object to `solve_ivp`, which repeatedly
   calls `reactor_odes()` to integrate the system forward in time.
4. `solve_ivp` returns arrays of time, concentration, and temperature.
5. `summarize()` computes the final and peak values.
6. `plots.py` turns the arrays into two matplotlib figures.
7. Streamlit renders both figures plus the summary text.

## 3. Purpose of Each File

- **config.py** - default slider values and the two fixed physical
  constants (`ALPHA`, `BETA`) that aren't exposed in the UI.
- **models.py** - `ReactorParams` (a dataclass bundling the simulation
  inputs) and `reactor_odes()`, the function `solve_ivp` integrates.
- **simulation.py** - `run_simulation()`, a thin wrapper around
  `solve_ivp` that sets up the time span and initial conditions.
- **plots.py** - `plot_concentration()` and `plot_temperature()`, each
  builds one matplotlib figure.
- **utils.py** - `summarize()`, pulls final and peak values out of the
  result arrays.
- **app.py** - the Streamlit page: sidebar inputs, run button, and
  rendering the plots and summary.

## 4. Major Functions

**`reactor_odes(t, y, params)`** - the right-hand side of the ODE system.
Takes the current state `y = [C, T]` and returns `[dC/dt, dT/dt]`. This is
the function signature `solve_ivp` expects: `f(t, y, *args)`.

**`run_simulation(params)`** - builds the time grid with `np.linspace`,
sets initial conditions `[C0, T0]`, and calls `solve_ivp` with method
`RK45`. Returns the time, concentration, and temperature arrays.

**`summarize(time, concentration, temperature)`** - finds the peak
temperature with `np.argmax` and returns a dict of the final and peak
values, used both in the text summary and to mark the peak on the plot.

**`plot_concentration` / `plot_temperature`** - straightforward matplotlib
calls: create a figure, plot the line(s), label the axes, return the
figure for `st.pyplot()` to render.

## 5. What `solve_ivp` Does

`solve_ivp(fun, t_span, y0, method, t_eval, args)` numerically integrates
a system of first-order ODEs `dy/dt = f(t, y)`.

- `fun` is `reactor_odes` - given the state, returns the derivatives.
- `t_span` is the start and end time.
- `y0` is the initial state `[C0, T0]`.
- `t_eval` are the specific time points we want back (otherwise `solve_ivp`
  picks its own adaptive steps and we'd get an uneven grid).
- `method="RK45"` selects an explicit Runge-Kutta (4th/5th order) scheme -
  the default and a good general-purpose choice for smooth, non-stiff
  systems.

Internally it takes adaptive steps, estimating error at each step to
decide how big the next step should be, and interpolates back onto
`t_eval` for the output.

## 6. The Differential Equations

```
dC/dt = -k * C
dT/dt = alpha * C - beta * (T - T_room)
```

- First equation: standard first-order decay - concentration drops
  proportionally to how much is left. Has the closed-form solution
  `C(t) = C0 * exp(-k*t)`, which is a good sanity check against the
  numerical output.
- Second equation: temperature has two competing effects - it's driven up
  by the reaction (`alpha * C`, proportional to how much reactant is being
  consumed) and pulled back toward room temperature by Newton's law of
  cooling (`-beta * (T - T_room)`). As `C` decays to zero, temperature
  settles back down to `T_room`.

## 7. Why SciPy

Both equations are coupled (temperature depends on concentration), so
there's no clean closed-form solution for the pair. `solve_ivp` handles
that numerically without having to hand-roll a Runge-Kutta integrator or
worry about step-size stability.

## 8. Why Streamlit

Streamlit turns a plain Python script into a web UI with almost no
boilerplate - `number_input` and `button` calls instead of writing HTML,
routes, or a request/response cycle. For a small simulation tool where the
goal is quick interactivity rather than a production web app, it's a much
faster path than Flask/Django plus a front end.

## 9. Possible Interviewer Questions

- Why RK45 instead of another method?
- What happens if `k` is 0? Negative?
- Why is `ReactorParams` a dataclass instead of separate arguments?
- How would you validate user input?
- What if the system were stiff - would RK45 still work?
- How would you extend this to more than one reactant?
- Why not use `odeint` instead of `solve_ivp`?
- Where would you add tests?

## 10. Short Answers

**Why RK45?** It's the default in `solve_ivp` and works well for smooth,
non-stiff systems like this one - no reason to reach for something more
specialized.

**What if k is 0?** Concentration stays constant at `C0`, so temperature
also stays constant (no reaction driving it up, and it's already at
whatever `T0` is relative to `T_room`). Negative `k` would mean
concentration grows without bound, which isn't physically meaningful -
the UI restricts `k` to be non-negative.

**Why a dataclass for ReactorParams?** It's cleaner than passing five
separate arguments through `run_simulation` and `reactor_odes`, and it
gives each field a name instead of a positional index.

**How would you validate input?** Streamlit's `min_value` on the number
inputs already stops negative `k`, `C0`, or simulation time. Beyond that,
I'd add a check that `T0` and `T_room` are physically reasonable before
running the solver.

**Stiff systems?** If the rates in the two equations were on very
different time scales, RK45 would need tiny steps to stay stable, and an
implicit method like `Radau` or `BDF` (both available in `solve_ivp`)
would be a better fit.

**More than one reactant?** Extend `y` to more state variables and add
more terms to `reactor_odes` - the `solve_ivp` call itself wouldn't
change.

**solve_ivp vs odeint?** `solve_ivp` is the newer SciPy interface, offers
multiple methods (RK45, Radau, BDF, etc.) through one function, and
returns a richer result object. `odeint` is the older, LSODA-only
interface kept for backward compatibility.

**Where would you add tests?** Unit tests for `reactor_odes` (correct
derivative signs) and `run_simulation` (concentration decays monotonically,
temperature approaches `T_room` for large `t`), likely with `pytest`.
