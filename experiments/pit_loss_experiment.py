from src.optimizer import optimise_one_stop, optimise_two_stop


def run_experiment():
    pit_losses = [5, 7, 7.82, 8, 10, 15, 20, 22, 25, 30]

    for pit_loss in pit_losses:
        one_pit, one_time = optimise_one_stop(
            race_laps=53,
            base_paces=[94.0, 94.3],
            degradations=[0.04, 0.02],
            fuel_effect=0.04,
            pit_loss=pit_loss,
        )

        two_pits, two_time = optimise_two_stop(
            race_laps=53,
            base_paces=[94.0, 94.3, 94.0],
            degradations=[0.04, 0.02, 0.04],
            fuel_effect=0.04,
            pit_loss=pit_loss,
        )

        advantage = two_time - one_time

        if abs(advantage) < 0.005:
            winner = "TIE"
        elif advantage > 0:
            winner = "ONE-STOP"
        else:
            winner = "TWO-STOP"

        print(
            f"Pit loss: {pit_loss:5.2f}s | "
            f"One-stop: {one_time:.2f}s | "
            f"Two-stop: {two_time:.2f}s | "
            f"Advantage: {advantage:+.2f}s | "
            f"Winner: {winner}"
        )


if __name__ == "__main__":
    run_experiment()