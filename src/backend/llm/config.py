from pathlib import Path
from typing import Literal

import yaml
from pydantic import BaseModel, ConfigDict, model_validator


class ProviderConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal["openai_compatible", "anthropic"]
    api_key_env: str
    base_url: str = ""


class RoleConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    provider: str
    model: str = ""


class LLMConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    providers: dict[str, ProviderConfig]
    roles: dict[str, RoleConfig]

    @model_validator(mode="after")
    def _roles_reference_known_providers(self) -> "LLMConfig":
        unknown = {role.provider for role in self.roles.values()} - set(self.providers)
        if unknown:
            raise ValueError(f"roles reference unknown providers: {sorted(unknown)}")
        return self


def load_llm_config(path: Path) -> LLMConfig:
    return LLMConfig.model_validate(yaml.safe_load(path.read_text(encoding="utf-8")))
