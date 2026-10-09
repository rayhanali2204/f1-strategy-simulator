from src.optimizer import optimise_one_stop, optimise_two_stop
import csv
from pathlib import Path

def run_experiment():
    degradation_factors = [4.0, 4.02, 4.04, 4.05, 4.1, 4.5, 5.0]
    results = []

    for factor in degradation_factors:
        medium_deg = 0.04 * factor
        hard_deg = 0.02 * factor

        one_pit, one_time = optimise_one_stop(
            race_laps=53,
            base_paces=[94.0, 94.3],
            degradations=[medium_deg, hard_deg],
            fuel_effect=0.04,
            pit_loss=22.0,
        )

        two_pits, two_time = optimise_two_stop(
            race_laps=53,
            base_paces=[94.0, 94.3, 94.0],
            degradations=[medium_deg, hard_deg, medium_deg],
            fuel_effect=0.04,
            pit_loss=22.0,
        )

        advantage = two_time - one_time

        if abs(advantage) < 0.005:
            winner = "TIE"
        elif advantage > 0:
            winner = "ONE-STOP"
        else:
            winner = "TWO-STOP"

        results.append({
            "degradation_factor": factor,
            "one_stop_pit": one_pit,
            "one_stop_time": one_time,
            "two_stop_first_pit": two_pits[0],
            "two_stop_second_pit": two_pits[1],
            "two_stop_time": two_time,
            "advantage": advantage,
            "winner": winner,
        })

        print(
            f"Factor: {factor:.2f}x | "
            f"One-stop: {one_time:.2f}s (pit {one_pit}) | "
            f"Two-stop: {two_time:.2f}s (pits {two_pits}) | "
            f"Advantage: {advantage:+.2f}s | "
            f"Winner: {winner}"
        )

    output_path = Path("results/degradation_experiment.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"\nResults saved to {output_path}")


if __name__ == "__main__":
    run_experiment()