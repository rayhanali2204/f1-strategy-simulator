import fastf1
from src.preprocessing import clean_laps

def load_race(year: int, grand_prix: str):
    session = fastf1.get_session(year, grand_prix, "R")
    session.load(telemetry=False, weather=False)

    return session.laps

if __name__ == "__main__":
    laps = load_race(2025, "Japan")

    columns = [
        "Driver",
        "LapNumber",
        "LapTime",
        "Compound",
        "TyreLife",
        "Stint",
        "PitInTime",
        "PitOutTime",
        "TrackStatus",
        "IsAccurate",
    ]

    print(laps[columns].head(10))
    print(f"\nTotal lap records: {len(laps)}")
    print(f"Drivers: {laps['Driver'].nunique()}")
    print("\nMissing values:")
    print(laps[columns].isna().sum())

    print("\nTyre compounds:")
    print(laps["Compound"].value_counts())

    print("\nAccurate vs inaccurate laps:")
    print(laps["IsAccurate"].value_counts())

    print("\nTrack statuses:")
    print(laps["TrackStatus"].value_counts())

    print("\nPit-in laps:")
    print(laps["PitInTime"].notna().sum())

    print("\nPit-out laps:")
    print(laps["PitOutTime"].notna().sum())

    print("\nLap times in seconds:")
    print(laps["LapTime"].dt.total_seconds().describe())

    cleaned = clean_laps(laps)

    print("\n--- PREPROCESSING RESULTS ---")
    print(f"Original laps: {len(laps)}")
    print(f"Cleaned laps: {len(cleaned)}")
    print(f"Excluded laps: {len(laps) - len(cleaned)}")

    print("\nCleaned compound distribution:")
    print(cleaned["Compound"].value_counts())

    print("\nCleaned lap-time statistics:")
    print(cleaned["LapTimeSeconds"].describe())

    print("\nCleaned tyre-age statistics:")
    print(cleaned["TyreLife"].describe())

    from pathlib import Path

    output_path = Path("data/japan_2025_clean_laps.csv")

    cleaned.to_csv(output_path, index=False)

    print(f"\nSaved cleaned data to: {output_path}")