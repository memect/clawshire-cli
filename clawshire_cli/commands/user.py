from __future__ import annotations

from argparse import ArgumentParser, Namespace, _SubParsersAction

from clawshire_cli.context import build_client, resolve_output
from clawshire_cli.output import render


def register(subparsers: _SubParsersAction[ArgumentParser]) -> None:
    parser = subparsers.add_parser("user", help="用户信息与额度查询")
    user_subparsers = parser.add_subparsers(dest="user_command", required=True)

    info = user_subparsers.add_parser("info", help="查询余额、免费次数、配额等用户信息")
    info.set_defaults(handler=_handle_info)


def _handle_info(args: Namespace) -> int:
    client = build_client(args)
    data = client.get("/api/v1/api-key/info", auth_required=True)
    render(data, output=resolve_output(args))
    return 0
