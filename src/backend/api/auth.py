import hashlib
import hmac
import re
import time
from collections import deque
from collections.abc import Callable
from threading import Lock

from fastapi import HTTPException, Request

MIN_SECRET_KEY_LENGTH = 32
MAX_FAILED_ATTEMPTS = 5
FAILURE_WINDOW_SECONDS = 15 * 60
_EXPIRY_PATTERN = re.compile(r"[0-9]{1,12}")


def passcode_matches(expected: str, given: str) -> bool:
    return hmac.compare_digest(expected.encode(), given.encode())


def issue_token(
    secret_key: str, ttl_seconds: int, now: float | None = None
) -> tuple[str, int]:
    expires_at = int((time.time() if now is None else now) + ttl_seconds)
    return f"{expires_at}.{_sign(secret_key, expires_at)}", expires_at


def verify_token(secret_key: str, token: str, now: float | None = None) -> bool:
    expires_part, separator, signature = token.partition(".")
    if not separator or not _EXPIRY_PATTERN.fullmatch(expires_part):
        return False
    expires_at = int(expires_part)
    if expires_at <= (time.time() if now is None else now):
        return False
    expected = _sign(secret_key, expires_at)
    return hmac.compare_digest(signature.encode(), expected.encode())


def _sign(secret_key: str, expires_at: int) -> str:
    return hmac.new(
        secret_key.encode(), str(expires_at).encode(), hashlib.sha256
    ).hexdigest()


class LoginThrottle:
    def __init__(self, clock: Callable[[], float] = time.time) -> None:
        self._clock = clock
        self._failures: deque[float] = deque()
        self._lock = Lock()

    def is_locked(self) -> bool:
        with self._lock:
            self._prune()
            return len(self._failures) >= MAX_FAILED_ATTEMPTS

    def record_failure(self) -> None:
        with self._lock:
            self._prune()
            self._failures.append(self._clock())

    def reset(self) -> None:
        with self._lock:
            self._failures.clear()

    def _prune(self) -> None:
        cutoff = self._clock() - FAILURE_WINDOW_SECONDS
        while self._failures and self._failures[0] < cutoff:
            self._failures.popleft()


def require_auth(request: Request) -> None:
    scheme, _, token = request.headers.get("authorization", "").partition(" ")
    if scheme.lower() != "bearer" or not verify_token(
        request.app.state.settings.secret_key, token
    ):
        raise HTTPException(status_code=401, detail="unauthorized")
