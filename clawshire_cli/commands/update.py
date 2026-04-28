from __future__ import annotations

import shutil
import subprocess
import sys
from typing import Any
from argparse import ArgumentParser, Namespace, _SubParsersAction

import httpx
from packaging.version import Version

from clawshire_cli.context import add_format_args, resolve_format
from clawshire_cli.output import render
from clawshire_sdk import ClawShireApiError, ClawShireNetworkError


PACKAGE_NAME = "clawshire-cli"
PYPI_JSON_URL = f"https://pypi.org/pypi/{PACKAGE_NAME}/json"
PYPI_PROJECT_URL = f"https://pypi.org/project/{PACKAGE_NAME}/"


def register(subparsers: _SubParsersAction[ArgumentParser]) -> None:
    parser = subparsers.add_parser(
        "update",
        aliases=["upgrade"],
        help="升级当前 CLI 到最新版本",
    )
    parser.add_argument(
        "--manager",
        choices=["auto", "uv", "pipx", "pip"],
        default="auto",
        help="指定升级方式，默认自动检测",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只显示将要执行的升级命令，不实际执行",
    )
    parser.add_argument(
        "-y",
        "--yes",
        action="store_true",
        help="跳过确认提示，直接执行升级",
    )
    add_format_args(parser)
    parser.set_defaults(handler=_handle_update)


def _handle_update(args: Namespace) -> int:
    output = resolve_format(args)
    current_version = _read_current_version()

    # non-table output: keep structured payload mode
    if output != "table":
        latest_version, version_source = _read_latest_version()
        manager = _resolve_manager(args.manager)
        command = _build_update_command(manager)
        payload: dict[str, Any] = {
            "current_version": current_version,
            "latest_version": latest_version,
            "version_source": version_source,
            "project_url": PYPI_PROJECT_URL,
            "manager": manager,
            "command": " ".join(command),
            "dry_run": args.dry_run,
        }
        if latest_version is not None and Version(current_version) >= Version(latest_version):
            payload["message"] = "Already up to date."
        elif args.dry_run:
            payload["message"] = "New version available (dry-run, not installing)"
        else:
            payload["message"] = "New version available, installing..."
        render(payload, output=output)
        return 0

    # table (default): streaming progress output like `claude update`
    print(f"Current version: {current_version}")
    print("Checking for updates to latest version...")

    latest_version, version_source = _read_latest_version()
    manager = _resolve_manager(args.manager)
    command = _build_update_command(manager)

    if latest_version is not None and Version(current_version) >= Version(latest_version):
        print(f"Already up to date. (latest: {latest_version})")
        return 0

    if latest_version is None:
        print("Unable to confirm latest version from PyPI, attempting upgrade anyway...")
    else:
        print(f"New version available: {latest_version} (current: {current_version})")

    if args.dry_run:
        print(f"Dry-run — would execute: {' '.join(command)}")
        return 0

    if not args.yes and not _confirm_upgrade(command):
        print("Upgrade cancelled.")
        return 1

    print("Installing update...")
    print(f"Using {_manager_label(manager)} update method...")

    result = subprocess.run(command, check=False)
    if result.returncode != 0:
        raise ClawShireApiError(f"Upgrade failed. Run manually: {' '.join(command)}")

    print("Update complete. Run `clawshire version` to confirm.")
    return 0


def _manager_label(manager: str) -> str:
    labels = {"uv": "uv tool upgrade", "pipx": "pipx upgrade", "pip": "pip install --upgrade"}
    return labels.get(manager, manager)


def _resolve_manager(preferred: str) -> str:
    if preferred != "auto":
        if not _manager_available(preferred):
            raise ClawShireApiError(f"未检测到 {preferred}，请先安装或改用其他 manager")
        return preferred

    for candidate in ("uv", "pipx", "pip"):
        if _manager_available(candidate):
            return candidate
    raise ClawShireApiError("未检测到可用的升级工具，请安装 uv、pipx 或 pip 后重试")


def _manager_available(manager: str) -> bool:
    if manager == "pip":
        return True
    return shutil.which(manager) is not None


def _build_update_command(manager: str) -> list[str]:
    if manager == "uv":
        return ["uv", "tool", "upgrade", PACKAGE_NAME]
    if manager == "pipx":
        return ["pipx", "upgrade", PACKAGE_NAME]
    return [sys.executable, "-m", "pip", "install", "--upgrade", PACKAGE_NAME]


def _confirm_upgrade(command: list[str]) -> bool:
    answer = input(f"将执行升级命令: {' '.join(command)}\n继续? [y/N] ").strip().lower()
    return answer in {"y", "yes"}


def _read_current_version() -> str:
    try:
        from clawshire_cli.main import get_cli_version

        return get_cli_version()
    except Exception:
        return "unknown"


def _read_latest_version() -> tuple[str | None, str]:
    try:
        payload = _fetch_pypi_metadata()
    except ClawShireApiError:
        return None, "pypi-not-published"
    except ClawShireNetworkError:
        return None, "pypi-unreachable"

    info = payload.get("info")
    if not isinstance(info, dict):
        return None, "pypi-invalid-response"
    version = info.get("version")
    if not isinstance(version, str) or not version.strip():
        return None, "pypi-invalid-response"
    return version.strip(), "pypi"


def _fetch_pypi_metadata() -> dict[str, Any]:
    try:
        with httpx.Client(timeout=10.0) as client:
            response = client.get(PYPI_JSON_URL, headers={"Accept": "application/json"})
    except httpx.HTTPError as exc:
        raise ClawShireNetworkError(f"访问 PyPI 失败: {exc}") from exc

    if response.status_code == 404:
        raise ClawShireApiError(f"PyPI 上暂未发布 {PACKAGE_NAME}", status_code=404)
    if response.status_code >= 400:
        raise ClawShireApiError(
            f"读取 PyPI 版本失败: HTTP {response.status_code}",
            status_code=response.status_code,
        )
    try:
        payload = response.json()
    except ValueError as exc:
        raise ClawShireApiError("PyPI 返回了非 JSON 响应") from exc
    if not isinstance(payload, dict):
        raise ClawShireApiError("PyPI 返回了无效响应")
    return payload
