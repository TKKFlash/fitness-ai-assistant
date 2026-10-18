from typing import Literal

Formula = Literal["epley", "brzycki"]

# 通常认为 Epley/Brzycki 在 1-10 次内较可靠，次数更高时误差明显变大
MAX_REPS_FOR_ESTIMATE = 10


def estimate_1rm(weight_kg: float, reps: int, formula: Formula = "epley") -> float:
    if weight_kg <= 0:
        raise ValueError("weight_kg must be positive")
    if not 1 <= reps <= MAX_REPS_FOR_ESTIMATE:
        raise ValueError(f"reps must be between 1 and {MAX_REPS_FOR_ESTIMATE}")
    if formula == "epley":
        return weight_kg * (1 + reps / 30)
    if formula == "brzycki":
        return weight_kg * 36 / (37 - reps)
    raise ValueError(f"unknown formula: {formula}")
