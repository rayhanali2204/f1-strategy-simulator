import pandas as pd

from src.preprocessing import clean_laps


def test_excludes_first_lap():
    laps = pd.DataFrame({
        "LapNumber": [1, 2, 3],
        "PitInTime": [pd.NaT, pd.NaT, pd.NaT],
        "PitOutTime": [pd.NaT, pd.NaT, pd.NaT],
        "IsAccurate": [True, True, True],
        "TrackStatus": ["1", "1", "1"],
        "Compound": ["MEDIUM", "MEDIUM", "MEDIUM"],
        "LapTime": pd.to_timedelta(
            [95.0, 93.5, 93.2], unit="s"
        ),
        "TyreLife": [1, 2, 3],
    })

    cleaned = clean_laps(laps)

    assert len(cleaned) == 2
    assert cleaned["LapNumber"].tolist() == [2, 3]

def test_excludes_pit_in_lap():
    laps = pd.DataFrame({
        "LapNumber": [10, 11],
        "PitInTime": pd.to_timedelta([None, 600], unit="s"),
        "PitOutTime": [pd.NaT, pd.NaT],
        "IsAccurate": [True, True],
        "TrackStatus": ["1", "1"],
        "Compound": ["HARD", "HARD"],
        "LapTime": pd.to_timedelta([93.0, 115.0], unit="s"),
        "TyreLife": [10, 11],
    })

    cleaned = clean_laps(laps)

    assert len(cleaned) == 1
    assert cleaned["LapNumber"].iloc[0] == 10