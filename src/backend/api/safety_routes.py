from fastapi import APIRouter, Depends
from safety.red_flags import RedFlagAnswers, RedFlagResult, evaluate_red_flags

from api.auth import require_auth

router = APIRouter(
    prefix="/api/safety",
    tags=["safety"],
    dependencies=[Depends(require_auth)],
)


@router.post("/red-flags", response_model=RedFlagResult)
def check_red_flags(answers: RedFlagAnswers) -> RedFlagResult:
    return evaluate_red_flags(answers)
