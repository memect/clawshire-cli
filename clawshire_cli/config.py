from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
import tomli_w
import tomllib


DEFAULT_BASE_URL = "https://api.clawshire.cn"
CONFIG_PATH = Path.home() / ".config" / "clawshire" / "config.toml"


@dataclass
class CliConfig:
    base_url: str = DEFAULT_BASE_URL
    api_key: str | None = None
    output: str = "table"
    timeout: float = 30.0


def load_config() -> CliConfig:
    config = CliConfig()

    if CONFIG_PATH.exists():
        data = tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        config.base_url = str(data.get("base_url") or config.base_url)
        config.api_key = data.get("api_key") or config.api_key
        config.output = str(data.get("output") or config.output)
        timeout = data.get("timeout")
        if timeout is not None:
            config.timeout = float(timeout)

    config.base_url = os.getenv("CLAWSHIRE_BASE_URL", config.base_url)
    config.api_key = os.getenv("CLAWSHIRE_API_KEY", config.api_key)
    config.output = os.getenv("CLAWSHIRE_OUTPUT", config.output)

    env_timeout = os.getenv("CLAWSHIRE_TIMEOUT")
    if env_timeout:
        config.timeout = float(env_timeout)
    return config


def save_config(config: CliConfig) -> Path:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    data = {
        "base_url": config.base_url,
        "api_key": config.api_key,
        "output": config.output,
        "timeout": config.timeout,
    }
    CONFIG_PATH.write_text(tomli_w.dumps(data), encoding="utf-8")
    return CONFIG_PATH


def mask_api_key(api_key: str | None) -> str:
    if not api_key:
        return ""
    if len(api_key) <= 8:
        return "*" * len(api_key)
    return f"{api_key[:6]}...{api_key[-4:]}"
