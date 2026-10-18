from collections.abc import Iterator
from typing import Annotated

from db.profile_repo import get_profile, save_profile
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from api.auth import require_auth
from api.schemas import ProfileIn, ProfileOut

router = APIRouter(
    prefix="/api/profile", tags=["profile"], dependencies=[Depends(require_auth)]
)


def get_session(request: Request) -> Iterator[Session]:
    session = request.app.state.session_factory()
    try:
        yield session
    finally:
        session.close()


SessionDep = Annotated[Session, Depends(get_session)]


@router.get("", response_model=ProfileOut)
def read_profile(session: SessionDep) -> ProfileOut:
    profile = get_profile(session)
    if profile is None:
        raise HTTPException(status_code=404, detail="profile not set")
    return ProfileOut.model_validate(profile)


@router.put("", response_model=ProfileOut)
def write_profile(body: ProfileIn, session: SessionDep) -> ProfileOut:
    profile = save_profile(session, body.model_dump())
    return ProfileOut.model_validate(profile)
