from collections.abc import Sequence


def exponential_smooth(values: Sequence[float], alpha: float = 0.1) -> list[float]:
    if not 0 < alpha <= 1:
        raise ValueError("alpha must be in (0, 1]")
    # alpha=0.1 约等效 19 天的平滑窗口，用于压制每日水分波动
    smoothed: list[float] = []
    for value in values:
        smoothed.append(
            value if not smoothed else alpha * value + (1 - alpha) * smoothed[-1]
        )
    return smoothed
