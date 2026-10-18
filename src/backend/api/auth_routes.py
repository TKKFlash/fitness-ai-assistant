from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel, ConfigDict, Field

from api.auth import LoginThrottle, issue_token, passcode_matches

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    passcode: str = Field(min_length=1, max_length=200)


class TokenOut(BaseModel):
    token: str
    expires_at: int


@router.post("/login", response_model=TokenOut)
def login(body: LoginIn, request: Request) -> TokenOut:
    throttle: LoginThrottle = request.app.state.login_throttle
    if throttle.is_locked():
        raise HTTPException(status_code=429, detail="too many failed attempts")
    settings = request.app.state.settings
    if not passcode_matches(settings.passcode, body.passcode):
        throttle.record_failure()
        raise HTTPException(status_code=401, detail="invalid passcode")
    throttle.reset()
    token, expires_at = issue_token(settings.secret_key, settings.token_ttl_seconds)
    return TokenOut(token=token, expires_at=expires_at)
