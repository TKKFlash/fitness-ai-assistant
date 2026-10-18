from typing import Literal

Sex = Literal["male", "female"]

ACTIVITY_FACTORS: dict[str, float] = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}

PROTEIN_KCAL_PER_G = 4
CARB_KCAL_PER_G = 4
FAT_KCAL_PER_G = 9

# 约值；实际体重变化受水分和代谢适应影响
KCAL_PER_KG_BODY_WEIGHT = 7700


def bmr_mifflin_st_jeor(
    sex: Sex, weight_kg: float, height_cm: float, age_years: int
) -> float:
    if sex not in ("male", "female"):
        raise ValueError(f"unsupported sex: {sex}")
    if not 20 <= weight_kg <= 300:
        raise ValueError("weight_kg out of range")
    if not 100 <= height_cm <= 250:
        raise ValueError("height_cm out of range")
    if not 16 <= age_years <= 100:
        raise ValueError("age_years out of range")
    base = 10 * weight_kg + 6.25 * height_cm - 5 * age_years
    return base + (5 if sex == "male" else -161)


def tdee(bmr: float, activity_level: str) -> float:
    if activity_level not in ACTIVITY_FACTORS:
        raise ValueError(f"unknown activity_level: {activity_level}")
    return bmr * ACTIVITY_FACTORS[activity_level]


def macro_targets(
    calories: float, weight_kg: float, protein_g_per_kg: float, fat_ratio: float
) -> dict[str, float]:
    if calories <= 0 or weight_kg <= 0 or protein_g_per_kg <= 0:
        raise ValueError("calories, weight_kg and protein_g_per_kg must be positive")
    if not 0 < fat_ratio < 1:
        raise ValueError("fat_ratio must be between 0 and 1")
    protein_g = weight_kg * protein_g_per_kg
    fat_kcal = calories * fat_ratio
    carb_kcal = calories - protein_g * PROTEIN_KCAL_PER_G - fat_kcal
    if carb_kcal < 0:
        raise ValueError(
            "macro targets infeasible: carbohydrate calories would be negative"
        )
    return {
        "protein_g": protein_g,
        "fat_g": fat_kcal / FAT_KCAL_PER_G,
        "carb_g": carb_kcal / CARB_KCAL_PER_G,
    }


def weekly_weight_change_kg(intake_kcal: float, expenditure_kcal: float) -> float:
    return (intake_kcal - expenditure_kcal) * 7 / KCAL_PER_KG_BODY_WEIGHT
