import pytest
from calc.trend import exponential_smooth


def test_smoothing_starts_at_first_value_and_blends():
    assert exponential_smooth([80, 81], alpha=0.5) == pytest.approx([80, 80.5])


def test_smoothing_empty_input():
    assert exponential_smooth([]) == []


@pytest.mark.parametrize("alpha", [0, 1.5])
def test_rejects_invalid_alpha(alpha):
    with pytest.raises(ValueError):
        exponential_smooth([80], alpha=alpha)
