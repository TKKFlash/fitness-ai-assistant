import pytest
from calc.metabolism import (
    bmr_mifflin_st_jeor,
    macro_targets,
    tdee,
    weekly_weight_change_kg,
)


def test_bmr_male_matches_hand_calculation():
    assert bmr_mifflin_st_jeor("male", 80, 180, 30) == pytest.approx(1780)


def test_bmr_female_matches_hand_calculation():
    assert bmr_mifflin_st_jeor("female", 60, 165, 28) == pytest.approx(1330.25)


def test_tdee_applies_activity_factor():
    assert tdee(1780, "moderate") == pytest.approx(2759)


@pytest.mark.parametrize(
    "kwargs",
    [
        {"sex": "other", "weight_kg": 80, "height_cm": 180, "age_years": 30},
        {"sex": "male", "weight_kg": 0, "height_cm": 180, "age_years": 30},
        {"sex": "male", "weight_kg": 80, "height_cm": 180, "age_years": 12},
    ],
)
def test_bmr_rejects_invalid_input(kwargs):
    with pytest.raises(ValueError):
        bmr_mifflin_st_jeor(**kwargs)


def test_tdee_rejects_unknown_activity_level():
    with pytest.raises(ValueError):
        tdee(1780, "extreme")


def test_macro_targets_split_calories():
    result = macro_targets(
        calories=2500, weight_kg=80, protein_g_per_kg=1.8, fat_ratio=0.25
    )
    assert result["protein_g"] == pytest.approx(144)
    assert result["fat_g"] == pytest.approx(625 / 9)
    assert result["carb_g"] == pytest.approx(1299 / 4)


def test_macro_targets_rejects_negative_carbs():
    with pytest.raises(ValueError):
        macro_targets(calories=1000, weight_kg=100, protein_g_per_kg=2.2, fat_ratio=0.3)


def test_weekly_change_for_500_kcal_daily_deficit():
    assert weekly_weight_change_kg(2000, 2500) == pytest.approx(-500 * 7 / 7700)
