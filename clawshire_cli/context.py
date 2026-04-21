from __future__ import annotations

from argparse import Namespace

from clawshire_cli.config import load_config
from clawshire_sdk import ClawShireClient


def build_client(args: Namespace) -> ClawShireClient:
    config = load_config()
    base_url = args.base_url or config.base_url
    api_key = args.api_key if args.api_key is not None else config.api_key
    timeout = args.timeout if args.timeout is not None else config.timeout
    return ClawShireClient(base_url=base_url, api_key=api_key, timeout=timeout)


def resolve_output(args: Namespace) -> str:
    config = load_config()
    return args.output or config.output
