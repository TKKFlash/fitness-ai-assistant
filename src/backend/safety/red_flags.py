from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Severity = Literal["refer_to_clinician", "stop_training_advice"]


class RedFlagAnswers(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chest_pain_or_pressure: bool = False
    fainting_or_near_fainting: bool = False
    shortness_of_breath_at_rest: bool = False
    palpitations_or_irregular_heartbeat: bool = False
    unexplained_weight_loss: bool = False
    persistent_joint_pain_or_swelling: bool = False
    numbness_or_tingling: bool = False
    pregnant_or_postpartum_under_6_months: bool = False
    under_18: bool = False
    eating_disorder_history_or_current: bool = False
    diagnosed_heart_kidney_liver_or_thyroid_disease: bool = False
    diabetes_on_insulin_or_sulfonylurea: bool = False
    taking_anticoagulants_or_immunosuppressants: bool = False
    free_text: str = Field(default="", max_length=1000)


class RedFlagResult(BaseModel):
    triggered: bool
    reasons: list[str]
    severity: Severity | None = None


REFER_REASONS: dict[str, str] = {
    "chest_pain_or_pressure": "胸痛或胸闷",
    "fainting_or_near_fainting": "晕厥或接近晕厥",
    "shortness_of_breath_at_rest": "静息时气短",
    "palpitations_or_irregular_heartbeat": "心悸或心律不齐",
    "unexplained_weight_loss": "原因不明的体重下降",
    "persistent_joint_pain_or_swelling": "持续的关节疼痛或肿胀",
    "numbness_or_tingling": "麻木或刺痛",
    "pregnant_or_postpartum_under_6_months": "孕期或产后 6 个月内",
    "under_18": "未满 18 岁",
    "eating_disorder_history_or_current": "饮食失调史或当前症状",
    "diagnosed_heart_kidney_liver_or_thyroid_disease": "心、肾、肝或甲状腺疾病",
    "diabetes_on_insulin_or_sulfonylurea": "使用胰岛素或磺脲类降糖药的糖尿病",
    "taking_anticoagulants_or_immunosuppressants": "正在服用抗凝药或免疫抑制剂",
}


def evaluate_red_flags(answers: RedFlagAnswers) -> RedFlagResult:
    reasons = [
        label for field, label in REFER_REASONS.items() if getattr(answers, field)
    ]
    if reasons:
        return RedFlagResult(
            triggered=True, reasons=reasons, severity="refer_to_clinician"
        )
    return RedFlagResult(triggered=False, reasons=[])
