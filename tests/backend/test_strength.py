import pytest
from calc.strength import estimate_1rm


def test_epley_estimate():
    assert estimate_1rm(100, 5, "epley") == pytest.approx(116.667, abs=1e-3)


def test_brzycki_estimate():
    assert estimate_1rm(100, 5, "brzycki") == pytest.approx(112.5)


def test_brzycki_single_rep_equals_load():
    assert estimate_1rm(100, 1, "brzycki") == pytest.approx(100)


@pytest.mark.parametrize("reps", [0, 11])
def test_rejects_reps_outside_range(reps):
    with pytest.raises(ValueError):
        estimate_1rm(100, reps)


def test_rejects_unknown_formula():
    with pytest.raises(ValueError):
        estimate_1rm(100, 5, "lombardi")  # type: ignore[arg-type]
