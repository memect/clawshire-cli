from __future__ import annotations

from argparse import ArgumentParser, Namespace, _SubParsersAction

from clawshire_cli.context import build_client, resolve_output
from clawshire_cli.output import render


def register(subparsers: _SubParsersAction[ArgumentParser]) -> None:
    parser = subparsers.add_parser("annual-report", help="年报查询")
    annual_report_subparsers = parser.add_subparsers(dest="annual_report_command", required=True)

    latest = annual_report_subparsers.add_parser("latest", help="获取最新年报列表")
    latest.add_argument("--page", type=int, default=1, help="页码")
    latest.add_argument("--page-size", type=int, default=20, help="每页数量")
    latest.add_argument("--year", type=int, help="年份，如 2025")
    latest.add_argument("--exchange", help="交易所，如 bj")
    latest.add_argument("--keyword", help="关键词或公司代码")
    latest.set_defaults(handler=_handle_latest)

    data = annual_report_subparsers.add_parser("data", help="获取年报结构化数据")
    data.add_argument("met_uuid", help="年报 met_uuid")
    data.set_defaults(handler=_handle_data)


def _handle_latest(args: Namespace) -> int:
    client = build_client(args)
    data = client.annual.latest(
        page=args.page,
        page_size=args.page_size,
        year=args.year,
        exchange=args.exchange,
        keyword=args.keyword,
    )
    render(data, output=resolve_output(args))
    return 0


def _handle_data(args: Namespace) -> int:
    client = build_client(args)
    data = client.annual.data(args.met_uuid)
    render(data, output=resolve_output(args))
    return 0
