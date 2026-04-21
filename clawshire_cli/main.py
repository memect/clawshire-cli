from __future__ import annotations

import argparse
import sys
from importlib.metadata import PackageNotFoundError, version as package_version

from clawshire_cli.commands import annual_analysis, annual_report, auth, notice, user
from clawshire_sdk import (
    ClawShireApiError,
    ClawShireAuthError,
    ClawShireConfigError,
    ClawShireNetworkError,
)

CLI_WEBSITE_URL = "https://clawshire.cn"
CLI_API_URL = "https://api.clawshire.cn"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="clawshire",
        description="ClawShire CLI",
    )
    parser.add_argument("--base-url", help="API 基础地址，如 https://api.clawshire.cn")
    parser.add_argument("--api-key", help="API Key，优先级高于本地配置")
    parser.add_argument("--output", choices=["table", "json", "markdown", "csv"], help="输出格式")
    parser.add_argument("--timeout", type=float, help="HTTP 超时秒数")

    subparsers = parser.add_subparsers(dest="command", required=True)
    notice.register(subparsers)
    annual_report.register(subparsers)
    annual_analysis.register(subparsers)
    auth.register(subparsers)
    user.register(subparsers)
    version_parser = subparsers.add_parser("version", help="查看 CLI 版本")
    version_parser.set_defaults(handler=handle_version)
    return parser


def get_cli_version() -> str:
    try:
        return package_version("clawshire-cli")
    except PackageNotFoundError:
        return "unknown"


def render_welcome() -> None:
    print("ClawShire CLI")
    print(f"version: {get_cli_version()}")
    print(f"website: {CLI_WEBSITE_URL}")
    print(f"api: {CLI_API_URL}")
    print("")
    print("常用命令:")
    print("  clawshire auth set-key <your_api_key>")
    print("  clawshire user info")
    print("  clawshire notice search --start-date 2026-04-19 --end-date 2026-04-20 --keyword 603402")
    print("  clawshire annual-report latest --year 2025 --keyword 平安银行")
    print("  clawshire annual-analysis company 000001 --year 2025")
    print("")
    print("更多帮助:")
    print("  clawshire --help")
    print("  clawshire version")
    print("  clawshire auth --help")
    print("  clawshire notice --help")
    print("  clawshire annual-report --help")
    print("  clawshire annual-analysis --help")


def handle_version(_: argparse.Namespace) -> int:
    print(get_cli_version())
    return 0


def run(argv: list[str] | None = None) -> int:
    argv = list(argv or sys.argv[1:])
    if not argv:
        render_welcome()
        return 0
    if argv:
        alias_map = {"gg": "notice", "ar": "annual-report", "aa": "annual-analysis"}
        if argv[0] in alias_map:
            argv[0] = alias_map[argv[0]]
    parser = build_parser()
    args = parser.parse_args(argv)
    handler = getattr(args, "handler", None)
    if handler is None:
        parser.print_help()
        return 2
    try:
        return int(handler(args) or 0)
    except ClawShireConfigError as exc:
        print(f"配置错误: {exc}", file=sys.stderr)
        return 2
    except ClawShireAuthError as exc:
        print(f"认证失败: {exc}", file=sys.stderr)
        return 3
    except ClawShireNetworkError as exc:
        print(f"网络错误: {exc}", file=sys.stderr)
        return 4
    except ClawShireApiError as exc:
        print(f"接口错误: {exc}", file=sys.stderr)
        return 5


def main() -> None:
    raise SystemExit(run())


if __name__ == "__main__":
    main()
