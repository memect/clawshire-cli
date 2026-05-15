from __future__ import annotations

from argparse import ArgumentParser, Namespace, _SubParsersAction

from clawshire_cli.context import add_format_args, build_client, resolve_format
from clawshire_cli.output import render

SPECIAL_PAGES = ["statistics", "companies", "tags", "recent", "quality", "doctor", "orphans", "freshness", "facets", "registry"]


def register(subparsers: _SubParsersAction[ArgumentParser]) -> None:
    parser = subparsers.add_parser("wiki", help="公告 Wiki 知识库查询")
    sub = parser.add_subparsers(dest="wiki_command", required=True)

    # search
    p = sub.add_parser("search", help="搜索公告 Wiki 条目")
    p.add_argument("--q", help="标题关键词")
    p.add_argument("--code", help="证券代码（6位）")
    p.add_argument("--ann-type", help="公告类型")
    p.add_argument("--tags", help="Tag 名称，逗号分隔")
    p.add_argument("--date-from", help="开始日期 YYYY-MM-DD")
    p.add_argument("--date-to", help="结束日期 YYYY-MM-DD")
    p.add_argument("--quality-min", type=int, help="最低质量等级 0-4")
    p.add_argument("--page", type=int, default=1)
    p.add_argument("--size", type=int, default=20)
    add_format_args(p)
    p.set_defaults(handler=_handle_search)

    # entry
    p = sub.add_parser("entry", help="查询公告 Wiki 详情")
    p.add_argument("ann_id", help="公告 ID")
    add_format_args(p)
    p.set_defaults(handler=_handle_entry)

    # company
    p = sub.add_parser("company", help="查询公司 Wiki 画像")
    p.add_argument("sec_code", help="证券代码（6位）")
    add_format_args(p)
    p.set_defaults(handler=_handle_company)

    # tag
    p = sub.add_parser("tag", help="按 Tag 主题查询")
    p.add_argument("tag_name", help="Tag 名称")
    add_format_args(p)
    p.set_defaults(handler=_handle_tag)

    # backlinks
    p = sub.add_parser("backlinks", help="查询反链")
    p.add_argument("page_type", choices=["company", "tag", "entity"], help="页面类型")
    p.add_argument("page_key", help="页面 key（证券代码/Tag名/实体key）")
    add_format_args(p)
    p.set_defaults(handler=_handle_backlinks)

    # resolve
    p = sub.add_parser("resolve", help="别名/简称解析为规范页面 ID")
    p.add_argument("q", help="公司简称、证券代码或 Tag 名称")
    add_format_args(p)
    p.set_defaults(handler=_handle_resolve)

    # special
    p = sub.add_parser("special", help=f"Special 页面查询（{', '.join(SPECIAL_PAGES)}）")
    p.add_argument("name", choices=SPECIAL_PAGES, help="Special 页面名称")
    add_format_args(p)
    p.set_defaults(handler=_handle_special)


def _handle_search(args: Namespace) -> int:
    client = build_client(args)
    data = client.wiki.search(
        q=args.q, code=args.code, ann_type=args.ann_type, tags=args.tags,
        date_from=args.date_from, date_to=args.date_to,
        quality_min=args.quality_min, page=args.page, size=args.size,
    )
    render(data, output=resolve_format(args))
    return 0


def _handle_entry(args: Namespace) -> int:
    render(build_client(args).wiki.entry(args.ann_id), output=resolve_format(args))
    return 0


def _handle_company(args: Namespace) -> int:
    render(build_client(args).wiki.company(args.sec_code), output=resolve_format(args))
    return 0


def _handle_tag(args: Namespace) -> int:
    render(build_client(args).wiki.tag(args.tag_name), output=resolve_format(args))
    return 0


def _handle_backlinks(args: Namespace) -> int:
    render(build_client(args).wiki.backlinks(args.page_type, args.page_key), output=resolve_format(args))
    return 0


def _handle_resolve(args: Namespace) -> int:
    render(build_client(args).wiki.resolve(args.q), output=resolve_format(args))
    return 0


def _handle_special(args: Namespace) -> int:
    render(build_client(args).wiki.special(args.name), output=resolve_format(args))
    return 0
