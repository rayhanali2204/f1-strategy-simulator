import matplotlib.pyplot as plt
import numpy as np

from src.data_loader import load_race
from src.preprocessing import clean_laps


def plot_driver_laps(laps, driver):
    driver_laps = laps[laps["Driver"] == driver]

    for compound in driver_laps["Compound"].unique():
        compound_laps = driver_laps[
            driver_laps["Compound"] == compound
        ]

        plt.scatter(
            compound_laps["TyreLife"],
            compound_laps["LapTimeSeconds"],
            label=compound,
        )

    plt.xlabel("Tyre Age (laps)")
    plt.ylabel("Lap Time (seconds)")
    plt.title(f"{driver} — Tyre Age vs Lap Time")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def plot_race_pace(laps, driver):
    driver_laps = laps[laps["Driver"] == driver]

    for compound in driver_laps["Compound"].unique():
        compound_laps = driver_laps[
            driver_laps["Compound"] == compound
        ]

        plt.scatter(
            compound_laps["LapNumber"],
            compound_laps["LapTimeSeconds"],
            label=compound,
        )

    plt.xlabel("Race Lap Number")
    plt.ylabel("Lap Time (seconds)")
    plt.title(f"{driver} - Race Pace")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def plot_fuel_corrected_laps(laps, driver):
    driver_laps = laps[laps["Driver"] == driver]

    for compound in driver_laps["Compound"].unique():
        compound_laps = driver_laps[
            driver_laps["Compound"] == compound
        ]

        plt.scatter(
            compound_laps["TyreLife"],
            compound_laps["FuelCorrectedLapTime"],
            label=compound,
        )

    plt.xlabel("Tyre Age (laps)")
    plt.ylabel("Fuel-Corrected Lap Time (seconds)")
    plt.title(f"{driver} — Fuel-Corrected Tyre Performance")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

def apply_fuel_correction(laps, fuel_effect=0.04):
    corrected = laps.copy()

    corrected["FuelCorrectedLapTime"] = (
        corrected["LapTimeSeconds"]
        + fuel_effect * (corrected["LapNumber"] - 1)
    )

    return corrected

def estimate_degradation(laps, driver, compound):
    selected = laps[
        (laps["Driver"] == driver)
        & (laps["Compound"] == compound)
    ]

    if len(selected) < 3:
        raise ValueError("Not enough laps to estimate degradation")

    tyre_age = selected["TyreLife"].to_numpy()
    lap_times = selected["FuelCorrectedLapTime"].to_numpy()

    slope, intercept = np.polyfit(tyre_age, lap_times, 1)

    return slope, intercept

if __name__ == "__main__":
    laps = load_race(2025, "Japan")
    cleaned = clean_laps(laps)

    fuel_effects = [0.02, 0.03, 0.04, 0.05, 0.06]

    for fuel_effect in fuel_effects:
        corrected = apply_fuel_correction(
            cleaned, fuel_effect=fuel_effect
        )

        print(f"\nFuel effect: {fuel_effect:.2f} s/race lap")

        for compound in ["MEDIUM", "HARD"]:
            slope, intercept = estimate_degradation(
                corrected, "VER", compound
            )

            print(f"  {compound}: {slope:+.4f} s/tyre lap")