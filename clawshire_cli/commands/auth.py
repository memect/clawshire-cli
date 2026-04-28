from __future__ import annotations

from argparse import ArgumentParser, Namespace, _SubParsersAction

from clawshire_cli.config import CONFIG_PATH, load_config, mask_api_key, save_config
from clawshire_cli.context import add_format_args, build_client, resolve_format
from clawshire_cli.output import render
from clawshire_sdk import ClawShireApiError, ClawShireAuthError, ClawShireNetworkError


def register(subparsers: _SubParsersAction[ArgumentParser]) -> None:
    parser = subparsers.add_parser("auth", help="认证与连通性检查")
    parser.set_defaults(handler=_handle_interactive)
    auth_subparsers = parser.add_subparsers(dest="auth_command")

    set_key = auth_subparsers.add_parser("set-key", help="保存 API Key 到本地配置")
    set_key.add_argument("api_key", help="ClawShire API Key")
    set_key.set_defaults(handler=_handle_set_key)

    clear_key = auth_subparsers.add_parser("clear-key", help="清除本地保存的 API Key")
    clear_key.set_defaults(handler=_handle_clear_key)

    logout = auth_subparsers.add_parser("logout", help="退出登录并清除本地保存的 API Key")
    logout.set_defaults(handler=_handle_clear_key)

    show = auth_subparsers.add_parser("show", help="查看当前认证配置")
    add_format_args(show)
    show.set_defaults(handler=_handle_show)

    status = auth_subparsers.add_parser("status", help="查看当前认证状态")
    add_format_args(status)
    status.set_defaults(handler=_handle_status)

    check = auth_subparsers.add_parser("check", help="检查当前认证是否可用")
    check.set_defaults(handler=_handle_check)

    whoami = auth_subparsers.add_parser("whoami", help="检查当前 API Key")
    add_format_args(whoami)
    whoami.set_defaults(handler=_handle_whoami)


def _handle_interactive(args: Namespace) -> int:
    config = load_config()
    if config.api_key:
        print(f"Current API Key: {mask_api_key(config.api_key)}")
        print("Already configured. Enter a new key to replace it, or press Enter to skip.")
        key = input("API Key: ").strip()
        if not key:
            return 0
    else:
        print("Welcome to ClawShire CLI!")
        print("Get your API Key at https://clawshire.cn")
        key = input("API Key: ").strip()
        if not key:
            print("No API Key entered. Skipped.")
            return 1
    config.api_key = key
    path = save_config(config)
    print(f"API Key saved to {path}")
    print(f"Key: {mask_api_key(key)}")
    return 0


def _handle_set_key(args: Namespace) -> int:
    config = load_config()
    config.api_key = args.api_key
    path = save_config(config)
    print(f"API Key 已保存到 {path}")
    print(f"当前 Key: {mask_api_key(args.api_key)}")
    return 0


def _handle_clear_key(args: Namespace) -> int:
    config = load_config()
    config.api_key = None
    path = save_config(config)
    print(f"API Key 已清除: {path}")
    return 0


def _handle_show(args: Namespace) -> int:
    config = load_config()
    render(
        {
            "base_url": config.base_url,
            "api_key": mask_api_key(config.api_key),
            "format": config.format,
            "timeout": config.timeout,
        },
        output=resolve_format(args),
    )
    return 0


def _handle_status(args: Namespace) -> int:
    source = _resolve_api_key_source()
    config = load_config()
    payload = {
        "base_url": config.base_url,
        "config_path": str(CONFIG_PATH),
        "api_key_source": source,
        "api_key": mask_api_key(config.api_key),
        "configured": bool(config.api_key),
        "authenticated": False,
        "message": "未配置 API Key",
    }
    if not config.api_key:
        render(payload, output=resolve_format(args))
        return 1

    client = build_client(args)
    try:
        client.get("/api/v1/api-key/info", auth_required=True)
        payload["authenticated"] = True
        payload["message"] = "认证可用"
    except (ClawShireAuthError, ClawShireApiError, ClawShireNetworkError) as exc:
        payload["message"] = str(exc)

    render(payload, output=resolve_format(args))
    return 0 if payload["authenticated"] else 1


def _handle_check(args: Namespace) -> int:
    client = build_client(args)
    try:
        client.get("/api/v1/api-key/info", auth_required=True)
        print("ok")
        return 0
    except (ClawShireAuthError, ClawShireApiError, ClawShireNetworkError):
        return 1


def _handle_whoami(args: Namespace) -> int:
    client = build_client(args)
    data = client.get("/api/v1/api-key/info", auth_required=True)
    render(data, output=resolve_format(args))
    return 0


def _resolve_api_key_source() -> str:
    import os

    if os.getenv("CLAWSHIRE_API_KEY"):
        return "env"
    if CONFIG_PATH.exists():
        return "config"
    return "none"
