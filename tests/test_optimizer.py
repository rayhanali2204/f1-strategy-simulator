import pytest
from src.optimizer import optimise_one_stop, optimise_two_stop


def test_optimal_one_stop():
    pit_lap, race_time = optimise_one_stop(
        race_laps=53,
        base_paces=[94.0, 94.3],
        degradations=[0.04, 0.02],
        fuel_effect=0.04,
        pit_loss=22.0,
    )

    assert pit_lap == 23
    assert race_time == pytest.approx(4976.70)


def test_short_race():
    with pytest.raises(ValueError):
        optimise_one_stop(
            race_laps=8,
            base_paces=[94.0, 94.3],
            degradations=[0.04, 0.02],
            fuel_effect=0.04,
            pit_loss=22.0,
            min_stint_length=5,
        )


def test_incorrect_stint_parameters():
    with pytest.raises(ValueError):
        optimise_one_stop(
            race_laps=53,
            base_paces=[94.0],
            degradations=[0.04, 0.02],
            fuel_effect=0.04,
            pit_loss=22.0,
        )

def test_optimal_two_stop():
    pit_laps, race_time = optimise_two_stop(
        race_laps=53,
        base_paces=[94.0, 94.3, 94.0],
        degradations=[0.04, 0.02, 0.04],
        fuel_effect=0.04,
        pit_loss=22.0,
    )

    assert pit_laps == (17, 36)
    assert race_time == pytest.approx(4990.88)


def test_two_stop_short_race():
    with pytest.raises(ValueError):
        optimise_two_stop(
            race_laps=14,
            base_paces=[94.0, 94.3, 94.0],
            degradations=[0.04, 0.02, 0.04],
            fuel_effect=0.04,
            pit_loss=22.0,
            min_stint_length=5,
        )


def test_two_stop_incorrect_parameters():
    with pytest.raises(ValueError):
        optimise_two_stop(
            race_laps=53,
            base_paces=[94.0, 94.3],
            degradations=[0.04, 0.02],
            fuel_effect=0.04,
            pit_loss=22.0,
        )

def test_one_stop_equal_pace_no_degradation():
    pit_lap, race_time = optimise_one_stop(
        race_laps=10,
        base_paces=[90.0, 90.0],
        degradations=[0.0, 0.0],
        fuel_effect=0.0,
        pit_loss=20.0,
        min_stint_length=2,
    )

    assert 2 <= pit_lap <= 8
    assert race_time == pytest.approx(920.0)

def test_one_stop_unique_optimal_pit():
    pit_lap, race_time = optimise_one_stop(
        race_laps=10,
        base_paces=[90.0, 90.0],
        degradations=[1.0, 1.0],
        fuel_effect=0.0,
        pit_loss=20.0,
        min_stint_length=2,
    )

    assert pit_lap == 5
    assert race_time == pytest.approx(940.0)

def test_one_stop_invalid_min_stint():
    with pytest.raises(ValueError):
        optimise_one_stop(
            race_laps=53,
            base_paces=[94.0, 94.3],
            degradations=[0.04, 0.02],
            fuel_effect=0.04,
            pit_loss=22.0,
            min_stint_length=0,
        )