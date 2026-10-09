from src.simulator import simulate_strategy


def optimise_one_stop(
    race_laps: int,
    base_paces: list[float],
    degradations: list[float],
    fuel_effect: float,
    pit_loss: float,
    min_stint_length: int = 5,
):
    if min_stint_length < 1:
        raise ValueError("Minimum stint length must be positive")
    
    if race_laps < 2 * min_stint_length:
        raise ValueError("Race is too short for two valid stints")

    if len(base_paces) != 2 or len(degradations) != 2:
        raise ValueError("A one-stop strategy requires two stints")

    best_time = float("inf")
    best_pit_lap = None

    for pit_lap in range(
        min_stint_length,
        race_laps - min_stint_length + 1,
    ):
        stint_lengths = [
            pit_lap,
            race_laps - pit_lap,
        ]

        total_time = simulate_strategy(
            stint_lengths=stint_lengths,
            base_paces=base_paces,
            degradations=degradations,
            fuel_effect=fuel_effect,
            pit_loss=pit_loss,
        )

        if total_time < best_time:
            best_time = total_time
            best_pit_lap = pit_lap

    return best_pit_lap, best_time

def optimise_two_stop(
    race_laps: int,
    base_paces: list[float],
    degradations: list[float],
    fuel_effect: float,
    pit_loss: float,
    min_stint_length: int = 5,
):
    if min_stint_length < 1:
        raise ValueError("Minimum stint length must be positive")

    if race_laps < 3 * min_stint_length:
        raise ValueError("Race is too short for three valid stints")

    if len(base_paces) != 3 or len(degradations) != 3:
        raise ValueError("A two-stop strategy requires three stints")

    best_time = float("inf")
    best_pit_laps = None

    for first_pit in range(
        min_stint_length,
        race_laps - 2 * min_stint_length + 1,
    ):
        for second_pit in range(
            first_pit + min_stint_length,
            race_laps - min_stint_length + 1,
        ):
            stint_lengths = [
                first_pit,
                second_pit - first_pit,
                race_laps - second_pit,
            ]

            total_time = simulate_strategy(
                stint_lengths=stint_lengths,
                base_paces=base_paces,
                degradations=degradations,
                fuel_effect=fuel_effect,
                pit_loss=pit_loss,
            )

            if total_time < best_time:
                best_time = total_time
                best_pit_laps = (first_pit, second_pit)

    return best_pit_laps, best_time

if __name__ == "__main__":
    one_pit, one_time = optimise_one_stop(
        race_laps=53,
        base_paces=[94.0, 94.3],
        degradations=[0.04, 0.02],
        fuel_effect=0.04,
        pit_loss=22.0,
    )

    two_pits, two_time = optimise_two_stop(
        race_laps=53,
        base_paces=[94.0, 94.3, 94.0],
        degradations=[0.04, 0.02, 0.04],
        fuel_effect=0.04,
        pit_loss=22.0,
    )

    print(f"Best one-stop: pit after lap {one_pit}")
    print(f"One-stop time: {one_time:.2f} seconds")

    print(f"\nBest two-stop: pit after laps {two_pits}")
    print(f"Two-stop time: {two_time:.2f} seconds")

    difference = abs(one_time - two_time)
    if abs(one_time - two_time) < 1e-6:
        winner = "Tie"
    elif one_time < two_time:
        winner = "One-stop"
    else:
        winner = "Two-stop"

    print(f"\nFastest strategy: {winner}")
    print(f"Advantage: {difference:.2f} seconds")