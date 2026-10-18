import pytest
from langchain_anthropic import ChatAnthropic
from langchain_openai import ChatOpenAI
from llm.config import LLMConfig, load_llm_config
from llm.factory import LLMConfigError, build_chat_model

RAW = {
    "providers": {
        "deepseek": {
            "type": "openai_compatible",
            "base_url": "https://example.test/v1",
            "api_key_env": "TEST_DEEPSEEK_KEY",
        },
        "anthropic": {"type": "anthropic", "api_key_env": "TEST_ANTHROPIC_KEY"},
    },
    "roles": {
        "router": {"provider": "deepseek", "model": "chat-model"},
        "planner": {"provider": "anthropic", "model": "claude-opus-5-5"},
        "empty": {"provider": "deepseek", "model": ""},
    },
}


def _config() -> LLMConfig:
    return LLMConfig.model_validate(RAW)


def test_openai_compatible_role_uses_base_url_and_env_key(monkeypatch):
    monkeypatch.setenv("TEST_DEEPSEEK_KEY", "sk-test")
    model = build_chat_model(_config(), "router")
    assert isinstance(model, ChatOpenAI)
    assert model.model_name == "chat-model"
    assert str(model.openai_api_base) == "https://example.test/v1"


def test_anthropic_role_builds_claude_client(monkeypatch):
    monkeypatch.setenv("TEST_ANTHROPIC_KEY", "sk-ant-test")
    model = build_chat_model(_config(), "planner")
    assert isinstance(model, ChatAnthropic)
    assert model.model == "claude-opus-5-5"


def test_missing_key_fails_fast(monkeypatch):
    monkeypatch.delenv("TEST_DEEPSEEK_KEY", raising=False)
    with pytest.raises(LLMConfigError, match="TEST_DEEPSEEK_KEY"):
        build_chat_model(_config(), "router")


def test_empty_model_name_fails_fast(monkeypatch):
    monkeypatch.setenv("TEST_DEEPSEEK_KEY", "sk-test")
    with pytest.raises(LLMConfigError, match="no model"):
        build_chat_model(_config(), "empty")


def test_unknown_role_fails_fast(monkeypatch):
    monkeypatch.setenv("TEST_DEEPSEEK_KEY", "sk-test")
    with pytest.raises(LLMConfigError, match="not configured"):
        build_chat_model(_config(), "missing")


def test_role_referencing_unknown_provider_is_rejected():
    bad = {"providers": {}, "roles": {"router": {"provider": "nope", "model": "m"}}}
    with pytest.raises(ValueError, match="unknown providers"):
        LLMConfig.model_validate(bad)


def test_unknown_config_key_is_rejected():
    bad = {**RAW, "extra": 1}
    with pytest.raises(ValueError):
        LLMConfig.model_validate(bad)


def test_load_llm_config_reads_yaml(tmp_path):
    path = tmp_path / "llm.yaml"
    path.write_text(
        "providers:\n  p:\n    type: anthropic\n    api_key_env: K\nroles:\n  r:\n    provider: p\n    model: m\n",
        encoding="utf-8",
    )
    config = load_llm_config(path)
    assert config.roles["r"].model == "m"
