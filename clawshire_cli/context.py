#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@File    :   context.py
@Time    :   2026/04/28 00:15
@Desc    :   CLI 运行上下文解析，包括客户端构造和输出格式参数
"""

from __future__ import annotations

from argparse import ArgumentParser, Namespace

from clawshire_cli.config import load_config
from clawshire_sdk import ClawShireClient


def build_client(args: Namespace) -> ClawShireClient:
    """根据命令行参数和本地配置构造 ClawShire API 客户端。"""
    config = load_config()
    base_url = args.base_url or config.base_url
    api_key = args.api_key if args.api_key is not None else config.api_key
    timeout = args.timeout if args.timeout is not None else config.timeout
    return ClawShireClient(base_url=base_url, api_key=api_key, timeout=timeout)


def add_format_args(parser: ArgumentParser) -> None:
    """为叶子命令添加统一输出格式参数。"""
    parser.add_argument("--format", choices=["table", "json", "markdown", "csv"], help="输出格式")
    parser.add_argument("--json", action="store_true", help="等价于 --format json")


def resolve_format(args: Namespace) -> str:
    """解析最终输出格式，--json 优先于 --format 和配置文件。"""
    config = load_config()
    if getattr(args, "json", False):
        return "json"
    return args.format or config.format
