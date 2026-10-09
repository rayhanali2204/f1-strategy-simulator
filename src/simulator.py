def predict_lap_time(
    race_lap: int,
    tyre_age: int,
    base_pace: float,
    fuel_effect: float,
    degradation: float,
) -> float:
    """Predict lap time using a simplified linear pace model."""

    if race_lap < 1 or tyre_age < 1:
        raise ValueError("Race lap and tyre age must be positive")

    return (
        base_pace
        - fuel_effect * (race_lap - 1)
        + degradation * (tyre_age - 1)
    )

def simulate_stint(
    start_lap: int,
    stint_length: int,
    base_pace: float,
    fuel_effect: float,
    degradation: float,
) -> float:

    if start_lap < 1 or stint_length < 1:
        raise ValueError("Start lap and string length must be positive")

    total_time = 0.0

    for tyre_age in range(1, stint_length + 1):
        race_lap = start_lap + tyre_age - 1

        lap_time = predict_lap_time(
            race_lap,
            tyre_age,
            base_pace,
            fuel_effect,
            degradation,

        )

        total_time += lap_time

    return total_time

def simulate_strategy(
    stint_lengths: list[int],
    base_paces: list[float],
    degradations: list[float],
    fuel_effect: float,
    pit_loss: float,
) -> float:

    if not (
        len(stint_lengths)
        == len(base_paces)
        == len(degradations)
    ):
        raise ValueError("Each stint needs a pace and degradation value")

    if not stint_lengths or any(length < 1 for length in stint_lengths):
        raise ValueError("Stint lengths must be positive")

    if pit_loss < 0:
        raise ValueError("Pit loss cannot be negative")

    total_time = 0.0
    start_lap = 1

    for length, pace, degradation in zip(
        stint_lengths, base_paces, degradations
    ):
        stint_time = simulate_stint(
            start_lap=start_lap,
            stint_length=length,
            base_pace=pace,
            fuel_effect=fuel_effect,
            degradation=degradation,
        )

        total_time += stint_time
        start_lap += length

    pit_stops = len(stint_lengths) - 1
    total_time += pit_stops * pit_loss

    return total_time

if __name__ == "__main__":
    one_stop = simulate_strategy(
        stint_lengths=[20, 33],
        base_paces=[94.0, 94.3],
        degradations=[0.04, 0.02],
        fuel_effect=0.04,
        pit_loss=22.0,
    )

    two_stop = simulate_strategy(
        stint_lengths=[18, 18, 17],
        base_paces=[94.0, 94.3, 94.0],
        degradations=[0.04, 0.02, 0.04],
        fuel_effect=0.04,
        pit_loss=22.0,
    )

    print(f"One-stop strategy: {one_stop:.2f} seconds")
    print(f"Two-stop strategy: {two_stop:.2f} seconds")
    print(f"Difference: {abs(one_stop - two_stop):.2f} seconds")


