import pytest
from src.simulator import (
    predict_lap_time,
    simulate_stint,
    simulate_strategy,
)


def test_first_lap():
    result = predict_lap_time(1, 1, 94.0, 0.04, 0.03)
    assert result == pytest.approx(94.0)


def test_fuel_and_degradation():
    result = predict_lap_time(20, 10, 94.0, 0.04, 0.03)
    assert result == pytest.approx(93.51)


def test_invalid_lap_number():
    with pytest.raises(ValueError):
        predict_lap_time(0, 10, 94.0, 0.04, 0.03)


def test_single_lap_stint():
    result = simulate_stint(1, 1, 94.0, 0.04, 0.03)
    assert result == pytest.approx(94.0)


def test_twenty_lap_stint():
    result = simulate_stint(1, 20, 94.0, 0.04, 0.03)
    assert result == pytest.approx(1878.10)


def test_invalid_stint_length():
    with pytest.raises(ValueError):
        simulate_stint(1, 0, 94.0, 0.04, 0.03)    

def test_strategy_without_pit_stop():
    result = simulate_strategy(
        stint_lengths=[2],
        base_paces=[94.0],
        degradations=[0.0],
        fuel_effect=0.0,
        pit_loss=22.0,
    )

    assert result == pytest.approx(188.0)


def test_strategy_with_one_pit_stop():
    result = simulate_strategy(
        stint_lengths=[2, 2],
        base_paces=[94.0, 94.0],
        degradations=[0.0, 0.0],
        fuel_effect=0.0,
        pit_loss=22.0,
    )

    assert result == pytest.approx(398.0)


def test_mismatched_strategy_parameters():
    with pytest.raises(ValueError):
        simulate_strategy(
            stint_lengths=[20, 33],
            base_paces=[94.0],
            degradations=[0.04, 0.02],
            fuel_effect=0.04,
            pit_loss=22.0,
        )


def test_negative_pit_loss():
    with pytest.raises(ValueError):
        simulate_strategy(
            stint_lengths=[20, 33],
            base_paces=[94.0, 94.3],
            degradations=[0.04, 0.02],
            fuel_effect=0.04,
            pit_loss=-5.0,
        )

