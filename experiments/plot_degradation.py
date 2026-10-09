import pandas as pd
import matplotlib.pyplot as plt

from pathlib import Path


def plot_results():
    data_path = Path("results/degradation_experiment.csv")
    results = pd.read_csv(data_path)

    plt.figure(figsize=(9, 5))

    plt.plot(
        results["degradation_factor"],
        results["advantage"],
        marker="o",
        label="One-stop advantage",
    )

    plt.axhline(
        y=0,
        color="red",
        linestyle="--",
        label="Strategy break-even",
    )

    plt.xlabel("Tyre Degradation Multiplier")
    plt.ylabel("Two-stop Time − One-stop Time (seconds)")
    plt.title("Impact of Tyre Degradation on F1 Race Strategy")

    plt.grid(True, alpha=0.3)
    plt.legend()
    plt.tight_layout()

    output_path = Path("results/degradation_crossover.png")
    plt.savefig(output_path, dpi=200)

    plt.show()


if __name__ == "__main__":
    plot_results()