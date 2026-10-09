import pandas as pd

def clean_laps(laps: pd.DataFrame) -> pd.DataFrame:
    """Return laps suitable for inital dry-race pace"""

    clean = laps.copy()

    clean = clean[clean["LapNumber"] > 1]
    
    clean = clean[clean["PitInTime"].isna()]
    clean = clean[clean["PitOutTime"].isna()]

    clean = clean[clean["IsAccurate"] == True]

    clean = clean[clean["TrackStatus"] == "1"]

    clean = clean[clean["Compound"].isin(["SOFT", "MEDIUM", "HARD"])]

    clean = clean.dropna( subset=["LapTime", "TyreLife"])

    clean = clean[clean["TyreLife"] > 0]

    clean["LapTimeSeconds"] = (clean["LapTime"].dt.total_seconds())

    clean = clean[clean["LapTimeSeconds"] > 0]

    return clean.reset_index(drop=True)
