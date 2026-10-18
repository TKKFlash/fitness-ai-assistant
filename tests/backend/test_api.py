import pytest
from api.auth import issue_token, verify_token
from api.main import create_app
from db.base import Base
from db.session import make_engine
from fastapi.testclient import TestClient
from settings import Settings

PASSCODE = "correct-horse-battery"
SECRET = "s" * 40
VALID_PROFILE = {
    "birth_date": "1995-06-01",
    "sex": "male",
    "height_cm": 178,
    "training_years": 2,
    "activity_level": "moderate",
    "goal": "muscle_gain",
    "equipment": ["dumbbell", "bench"],
    "injuries": [],
    "chronic_conditions": [],
    "medications": [],
    "diet_restrictions": [],
    "allergies": [],
    "red_flags": [],
}


def _settings(tmp_path) -> Settings:
    return Settings(
        database_url=f"sqlite:///{(tmp_path / 'test.db').as_posix()}",
        passcode=PASSCODE,
        secret_key=SECRET,
        _env_file=None,
    )


@pytest.fixture()
def client(tmp_path):
    settings = _settings(tmp_path)
    Base.metadata.create_all(make_engine(settings.database_url))
    with TestClient(create_app(settings)) as test_client:
        yield test_client


@pytest.fixture()
def authed(client):
    token = client.post("/api/auth/login", json={"passcode": PASSCODE}).json()["token"]
    client.headers["Authorization"] = f"Bearer {token}"
    return client


def test_healthz_is_public(client):
    assert client.get("/healthz").json() == {"status": "ok"}


def test_profile_requires_auth(client):
    assert client.get("/api/profile").status_code == 401
    assert client.put("/api/profile", json=VALID_PROFILE).status_code == 401


def test_echo_requires_auth(client):
    assert client.post("/echo", json={"text": "x"}).status_code == 401


def test_login_rejects_wrong_passcode(client):
    assert client.post("/api/auth/login", json={"passcode": "nope"}).status_code == 401


def test_login_issues_usable_token(authed):
    assert authed.get("/api/profile").status_code == 404
    assert authed.post("/echo", json={"text": "hi"}).json() == {"reply": "hi"}


def test_login_locks_after_repeated_failures(client):
    for _ in range(5):
        client.post("/api/auth/login", json={"passcode": "wrong"})
    response = client.post("/api/auth/login", json={"passcode": PASSCODE})
    assert response.status_code == 429


def test_profile_put_then_get_round_trip(authed):
    assert authed.put("/api/profile", json=VALID_PROFILE).status_code == 200
    body = authed.get("/api/profile").json()
    assert body["sex"] == "male"
    assert body["equipment"] == ["dumbbell", "bench"]
    assert "updated_at" in body


def test_profile_put_overwrites_existing(authed):
    authed.put("/api/profile", json=VALID_PROFILE)
    authed.put("/api/profile", json={**VALID_PROFILE, "goal": "fat_loss"})
    assert authed.get("/api/profile").json()["goal"] == "fat_loss"


def test_profile_rejects_unknown_field(authed):
    response = authed.put("/api/profile", json={**VALID_PROFILE, "name": "张三"})
    assert response.status_code == 422


def test_profile_rejects_out_of_range_height(authed):
    response = authed.put("/api/profile", json={**VALID_PROFILE, "height_cm": 500})
    assert response.status_code == 422


def test_profile_rejects_underage_birth_date(authed):
    response = authed.put(
        "/api/profile", json={**VALID_PROFILE, "birth_date": "2015-01-01"}
    )
    assert response.status_code == 422


def test_profile_rejects_invalid_enum(authed):
    response = authed.put("/api/profile", json={**VALID_PROFILE, "goal": "bulk-fast"})
    assert response.status_code == 422


def test_token_expires():
    token, _ = issue_token(SECRET, ttl_seconds=60, now=1000)
    assert verify_token(SECRET, token, now=1059)
    assert not verify_token(SECRET, token, now=1061)


def test_token_rejects_wrong_key():
    token, _ = issue_token(SECRET, ttl_seconds=60, now=1000)
    assert not verify_token("x" * 40, token, now=1001)


def test_app_refuses_to_start_without_passcode(tmp_path):
    with pytest.raises(RuntimeError):
        create_app(
            Settings(
                database_url=f"sqlite:///{(tmp_path / 'x.db').as_posix()}",
                passcode="",
                secret_key=SECRET,
                _env_file=None,
            )
        )
