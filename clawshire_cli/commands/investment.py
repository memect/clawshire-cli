from __future__ import annotations

from argparse import ArgumentParser, Namespace, _SubParsersAction

from clawshire_cli.context import add_format_args, build_client, resolve_format
from clawshire_cli.output import render


def register(subparsers: _SubParsersAction[ArgumentParser]) -> None:
    parser = subparsers.add_parser("investment", help="投资逻辑分析查询")
    sub = parser.add_subparsers(dest="investment_command", required=True)

    # industries
    p = sub.add_parser("industries", help="列出所有申万一级行业名称（免费）")
    add_format_args(p)
    p.set_defaults(handler=_handle_industries)

    # company
    p = sub.add_parser("company", help="查询公司投资逻辑变化记录")
    p.add_argument("sec_code", help="证券代码（6位）")
    p.add_argument("--size", type=int, default=20, help="返回条数，默认 20")
    add_format_args(p)
    p.set_defaults(handler=_handle_company)

    # industry
    p = sub.add_parser("industry", help="查询行业投资逻辑研判")
    p.add_argument("industry_name", help="申万一级行业名称，如「银行」「医药生物」")
    add_format_args(p)
    p.set_defaults(handler=_handle_industry)

    # summary
    p = sub.add_parser("summary", help="查询公司综合研判摘要")
    p.add_argument("sec_code", help="证券代码（6位）")
    add_format_args(p)
    p.set_defaults(handler=_handle_summary)


def _handle_industries(args: Namespace) -> int:
    render(build_client(args).investment.industries(), output=resolve_format(args))
    return 0


def _handle_company(args: Namespace) -> int:
    render(build_client(args).investment.company_deltas(args.sec_code, size=args.size), output=resolve_format(args))
    return 0


def _handle_industry(args: Namespace) -> int:
    render(build_client(args).investment.industry_thesis(args.industry_name), output=resolve_format(args))
    return 0


def _handle_summary(args: Namespace) -> int:
    render(build_client(args).investment.company_summary(args.sec_code), output=resolve_format(args))
    return 0
