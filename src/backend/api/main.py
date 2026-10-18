from agent.graph import build_echo_graph
from db.session import make_engine, make_session_factory
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from settings import Settings

from api.auth import MIN_SECRET_KEY_LENGTH, LoginThrottle, require_auth
from api.auth_routes import router as auth_router
from api.profile_routes import router as profile_router
from api.safety_routes import router as safety_router


class EchoRequest(BaseModel):
    text: str = Field(min_length=1, max_length=2000)


class EchoResponse(BaseModel):
    reply: str


def create_app(settings: Settings | None = None) -> FastAPI:
    if settings is None:
        settings = Settings()
    if not settings.passcode or len(settings.secret_key) < MIN_SECRET_KEY_LENGTH:
        raise RuntimeError(
            "FITNESS_PASSCODE must be set and FITNESS_SECRET_KEY must be at least 32 characters"
        )

    app = FastAPI(title="fitness-assistant")
    app.state.settings = settings
    app.state.session_factory = make_session_factory(make_engine(settings.database_url))
    app.state.login_throttle = LoginThrottle()
    app.include_router(auth_router)
    app.include_router(profile_router)
    app.include_router(safety_router)
    graph = build_echo_graph()

    @app.get("/healthz")
    def healthz() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/echo", dependencies=[Depends(require_auth)])
    def echo(request: EchoRequest) -> EchoResponse:
        result = graph.invoke({"text": request.text})
        return EchoResponse(reply=result["reply"])

    return app
