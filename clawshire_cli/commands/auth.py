from __future__ import annotations

from argparse import ArgumentParser, Namespace, _SubParsersAction

from clawshire_cli.config import load_config, mask_api_key, save_config
from clawshire_cli.context import build_client, resolve_output
from clawshire_cli.output import render


def register(subparsers: _SubParsersAction[ArgumentParser]) -> None:
    parser = subparsers.add_parser("auth", help="认证与连通性检查")
    auth_subparsers = parser.add_subparsers(dest="auth_command", required=True)

    set_key = auth_subparsers.add_parser("set-key", help="保存 API Key 到本地配置")
    set_key.add_argument("api_key", help="ClawShire API Key")
    set_key.set_defaults(handler=_handle_set_key)

    clear_key = auth_subparsers.add_parser("clear-key", help="清除本地保存的 API Key")
    clear_key.set_defaults(handler=_handle_clear_key)

    show = auth_subparsers.add_parser("show", help="查看当前认证配置")
    show.set_defaults(handler=_handle_show)

    whoami = auth_subparsers.add_parser("whoami", help="检查当前 API Key")
    whoami.set_defaults(handler=_handle_whoami)


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
            "output": config.output,
            "timeout": config.timeout,
        },
        output=resolve_output(args),
    )
    return 0


def _handle_whoami(args: Namespace) -> int:
    client = build_client(args)
    data = client.get("/api/v1/api-key/info", auth_required=True)
    render(data, output=resolve_output(args))
    return 0
