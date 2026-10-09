# F1 Race Strategy Simulator

A Python-based Formula 1 race strategy simulator that compares optimised one-stop and two-stop pit strategies using a simplified lap-time model.

The project also explores real Formula 1 lap data using FastF1 and investigates how tyre degradation and pit-stop time losses influence the relative performance of different strategies.

## Features

- Load and clean real F1 race lap data using FastF1.
- Explore tyre performance and estimate apparent degradation trends.
- Simulate lap times using fuel effects, tyre age and compound-specific parameters.
- Optimise one-stop and two-stop pit strategies using exhaustive search.
- Investigate strategy sensitivity to pit-stop losses and tyre degradation.
- Export experimental results to CSV and generate visualisations.
- Validate core simulation and optimisation behaviour with 21 automated tests.

## Methodology

### Lap-time model

Each simulated lap time is calculated as:

`lap_time = base_pace - fuel_effect * (race_lap - 1) + degradation * (tyre_age - 1)`

Where:

- `base_pace` is the initial lap time for the selected tyre configuration.
- `fuel_effect` represents the assumed lap-time improvement per completed race lap.
- `race_lap` is the current race lap number.
- `degradation` represents the assumed lap-time penalty per additional tyre lap.
- `tyre_age` is the current lap number within the stint.

The model assumes a constant linear fuel effect and constant linear tyre degradation within each stint.

### Strategy optimisation

The optimiser evaluates feasible pit-stop combinations subject to a minimum stint length.

For each candidate strategy, the simulator calculates total race