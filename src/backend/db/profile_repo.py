from collections.abc import Mapping

from sqlalchemy import select
from sqlalchemy.orm import Session

from db.models import Profile

DEFAULT_USER_ID = "owner"


def get_profile(session: Session, user_id: str = DEFAULT_USER_ID) -> Profile | None:
    return session.scalar(select(Profile).where(Profile.user_id == user_id))


def save_profile(
    session: Session, values: Mapping[str, object], user_id: str = DEFAULT_USER_ID
) -> Profile:
    profile = get_profile(session, user_id)
    if profile is None:
        profile = Profile(user_id=user_id)
        session.add(profile)
    for key, value in values.items():
        setattr(profile, key, value)
    session.commit()
    session.refresh(profile)
    return profile
