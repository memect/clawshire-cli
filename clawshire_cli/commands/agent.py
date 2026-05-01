#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    :   agent.py
@Time    :   2026/04/28 00:15
@Desc    :   Agent 观测与结构化反馈 CLI 命令
"""

from __future__ import annotations

import json
from argparse import SUPPRESS, ArgumentParser, Namespace, _SubParsersAction
from pathlib import Path
from typing import Any

from clawshire_cli.context import add_format_args, build_client, resolve_format
from clawshire_cli.output import render
from clawshire_sdk import ClawShireConfigError


def register(subparsers: _SubParsersAction[ArgumentParser]) -> None:
    """注册 agent 命令组及 feedback 子命令。"""
    parser = subparsers.add_parser("agent", help="Agent 观测与反馈")
    agent_subparsers = parser.add_subparsers(dest="agent_command", required=True)

    feedback = agent_subparsers.add_parser("feedback", help="提交 Agent 阻塞反馈")
    feedback.add_argument("--intent", help="Agent 想完成什么")
    feedback.add_argument("--attempted", help="已尝试的步骤、命令或工具调用；可传 JSON 或文本")
    feedback.add_argument("--blocked-by", help="卡在哪里")
    feedback.add_argument("--expected-capability", help="期望 ClawShire 提供什么能力")
    feedback.add_argument(
        "--severity",
        choices=["low", "medium", "high", "critical"],
        help="严重程度",
    )
    feedback.add_argument("--trace-id", default=SUPPRESS, help="关联 trace_id；默认也可用 CLAWSHIRE_TRACE_ID")
    feedback.add_argument("--related-tool", help="相关工具，如 notice.search / annual_report.latest")
    feedback.add_argument("--agent-name", default=SUPPRESS, help="Agent 名称；默认也可用 CLAWSHIRE_AGENT_NAME")
    feedback.add_argument("--client", default=SUPPRESS, help="来源，如 cli / skill / mcp；默认来自 CLAWSHIRE_CLIENT 或 cli")
    feedback.add_argument("--from-json", help="从 JSON 文件读取完整 feedback payload")
    add_format_args(feedback)
    feedback.set_defaults(handler=_handle_feedback)


def _handle_feedback(args: Namespace) -> int:
    """构造 feedback payload 并提交到 ClawShire API。"""
    payload = _load_payload(args)
    _validate_required(payload, ["intent", "blocked_by", "expected_capability"])
    client = build_client(args)
    _apply_feedback_attribution(client, payload)
    data = client.post("/api/v1/agent/feedback", json=payload, auth_required=True)
    render(data, output=resolve_format(args))
    return 0


def _apply_feedback_attribution(client, payload: dict[str, Any]) -> None:
    """将 feedback 参数同步到 SDK header，保证业务日志主字段可追踪。"""
    if payload.get("client"):
        client.client_name = str(payload["client"])
    if payload.get("agent_name"):
        client.agent_name = str(payload["agent_name"])
    if payload.get("trace_id"):
        client.trace_id = str(payload["trace_id"])


def _load_payload(args: Namespace) -> dict[str, Any]:
    """从命令行参数和 JSON 文件合并出最终 feedback payload。"""
    payload: dict[str, Any] = {}
    if args.from_json:
        path = Path(args.from_json)
        payload.update(json.loads(path.read_text(encoding="utf-8")))

    overrides = {
        "intent": args.intent,
        "attempted": _parse_attempted(args.attempted),
        "blocked_by": args.blocked_by,
        "expected_capability": args.expected_capability,
        "severity": args.severity,
        "trace_id": getattr(args, "trace_id", None),
        "related_tool": args.related_tool,
        "agent_name": getattr(args, "agent_name", None),
        "client": getattr(args, "client", None),
    }
    for key, value in overrides.items():
        if value is not None:
            payload[key] = value
    return payload


def _parse_attempted(value: str | None) -> Any:
    """解析 attempted 参数，优先识别 JSON，失败时保留原文本。"""
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    if stripped[0] in "[{":
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            return stripped
    return stripped


def _validate_required(payload: dict[str, Any], fields: list[str]) -> None:
    """校验 feedback 必填字段，缺失时抛出配置错误。"""
    missing = [field for field in fields if not str(payload.get(field) or "").strip()]
    if missing:
        names = ", ".join(f"--{field.replace('_', '-')}" for field in missing)
        raise ClawShireConfigError(f"缺少必填 feedback 参数: {names}")
