from datetime import date, datetime
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

MIN_AGE_YEARS = 16
MAX_AGE_YEARS = 100

Sex = Literal["male", "female"]
Goal = Literal["fat_loss", "muscle_gain", "maintain"]
ActivityLevel = Literal["sedentary", "light", "moderate", "active", "very_active"]
Item = Annotated[str, Field(min_length=1, max_length=100)]
Items = Annotated[list[Item], Field(default_factory=list, max_length=50)]


class ProfileFields(BaseModel):
    model_config = ConfigDict(extra="forbid", from_attributes=True)

    birth_date: date
    sex: Sex
    height_cm: float = Field(ge=100, le=250)
    training_years: float = Field(default=0.0, ge=0, le=60)
    activity_level: ActivityLevel
    goal: Goal
    equipment: Items
    injuries: Items
    chronic_conditions: Items
    medications: Items
    diet_restrictions: Items
    allergies: Items
    red_flags: Items


class ProfileIn(ProfileFields):
    @field_validator("birth_date")
    @classmethod
    def _age_in_range(cls, value: date) -> date:
        age_years = (date.today() - value).days / 365.25
        if not MIN_AGE_YEARS <= age_years <= MAX_AGE_YEARS:
            raise ValueError(f"age must be between {MIN_AGE_YEARS} and {MAX_AGE_YEARS}")
        return value


class ProfileOut(ProfileFields):
    updated_at: datetime
