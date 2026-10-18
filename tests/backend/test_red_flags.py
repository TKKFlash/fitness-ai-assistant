import pytest
from safety.red_flags import RedFlagAnswers, evaluate_red_flags


def test_no_flags_passes():
    result = evaluate_red_flags(RedFlagAnswers())
    assert result.triggered is False
    assert result.reasons == []
    assert result.severity is None


@pytest.mark.parametrize(
    "field",
    [
        "chest_pain_or_pressure",
        "fainting_or_near_fainting",
        "shortness_of_breath_at_rest",
        "pregnant_or_postpartum_under_6_months",
        "under_18",
        "eating_disorder_history_or_current",
        "diabetes_on_insulin_or_sulfonylurea",
        "taking_anticoagulants_or_immunosuppressants",
    ],
)
def test_each_flag_triggers_referral(field):
    result = evaluate_red_flags(RedFlagAnswers(**{field: True}))
    assert result.triggered is True
    assert result.severity == "refer_to_clinician"
    assert len(result.reasons) == 1


def test_multiple_flags_are_all_reported():
    result = evaluate_red_flags(
        RedFlagAnswers(chest_pain_or_pressure=True, under_18=True)
    )
    assert len(result.reasons) == 2


def test_free_text_alone_does_not_trigger():
    result = evaluate_red_flags(RedFlagAnswers(free_text="膝盖有点不舒服"))
    assert result.triggered is False


def test_unknown_field_is_rejected():
    with pytest.raises(ValueError):
        RedFlagAnswers(made_up_flag=True)
