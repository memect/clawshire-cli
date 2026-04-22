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

    # 环境变量作为默认值
    config.base_url = os.getenv("CLAWSHIRE_BASE_URL", config.base_url)
    config.api_key = os.getenv("CLAWSHIRE_API_KEY", config.api_key)
    config.output = os.getenv("CLAWSHIRE_OUTPUT", config.output)
    env_timeout = os.getenv("CLAWSHIRE_TIMEOUT")
    if env_timeout:
        config.timeout = float(env_timeout)

    # 配置文件优先级高于环境变量
    if CONFIG_PATH.exists():
        data = tomllib.loads(CONFIG_PATH.read_text(encoding="utf-8"))
        if "base_url" in data:
            config.base_url = str(data["base_url"])
        if "api_key" in data:
            config.api_key = data["api_key"]
        if "output" in data:
            config.output = str(data["output"])
        if "timeout" in data:
            config.timeout = float(data["timeout"])

    return config


def save_config(config: CliConfig) -> Path:
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    data: dict = {
        "base_url": config.base_url,
        "output": config.output,
        "timeout": config.timeout,
    }
    if config.api_key is not None:
        data["api_key"] = config.api_key
    CONFIG_PATH.write_text(tomli_w.dumps(data), encoding="utf-8")
    return CONFIG_PATH


def mask_api_key(api_key: str | None) -> str:
    if not api_key:
        return ""
    if len(api_key) <= 8:
        return "*" * len(api_key)
    return f"{api_key[:6]}...{api_key[-4:]}"
