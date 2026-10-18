import os

from langchain_anthropic import ChatAnthropic
from langchain_core.language_models import BaseChatModel
from langchain_openai import ChatOpenAI

from llm.config import LLMConfig


class LLMConfigError(RuntimeError):
    pass


def build_chat_model(config: LLMConfig, role: str) -> BaseChatModel:
    role_config = config.roles.get(role)
    if role_config is None:
        raise LLMConfigError(f"role is not configured: {role}")
    if not role_config.model:
        raise LLMConfigError(f"role {role} has no model set")

    provider = config.providers[role_config.provider]
    api_key = os.environ.get(provider.api_key_env, "")
    if not api_key:
        raise LLMConfigError(f"environment variable {provider.api_key_env} is not set")

    if provider.type == "anthropic":
        return ChatAnthropic(model=role_config.model, api_key=api_key)
    if not provider.base_url:
        raise LLMConfigError(f"provider {role_config.provider} has no base_url")
    return ChatOpenAI(
        model=role_config.model, api_key=api_key, base_url=provider.base_url
    )
