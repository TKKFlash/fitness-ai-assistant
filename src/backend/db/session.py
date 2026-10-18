from pathlib import Path

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

SQLITE_PREFIX = "sqlite:///"


def make_engine(database_url: str) -> Engine:
    connect_args: dict[str, bool] = {}
    if database_url.startswith(SQLITE_PREFIX):
        Path(database_url.removeprefix(SQLITE_PREFIX)).parent.mkdir(
            parents=True, exist_ok=True
        )
        connect_args["check_same_thread"] = False
    return create_engine(database_url, connect_args=connect_args)


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    return sessionmaker(bind=engine, expire_on_commit=False)
