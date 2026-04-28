from __future__ import annotations

from argparse import ArgumentParser, Namespace, _SubParsersAction

from clawshire_cli.context import add_format_args, build_client, resolve_format
from clawshire_cli.output import render


def register(subparsers: _SubParsersAction[ArgumentParser]) -> None:
    parser = subparsers.add_parser("notice", help="公告查询")
    notice_subparsers = parser.add_subparsers(dest="notice_command", required=True)

    search = notice_subparsers.add_parser("search", help="按日期范围查询公告")
    _add_search_args(search)
    search.set_defaults(handler=_handle_search)

    stock = notice_subparsers.add_parser("stock", help="按证券代码查询公告")
    stock.add_argument("sec_code", help="证券代码")
    _add_search_args(stock)
    stock.set_defaults(handler=_handle_stock)

    link = notice_subparsers.add_parser("link", help="按公告原文链接查询")
    link.add_argument("--met-link", required=True, help="公告原文链接")
    add_format_args(link)
    link.set_defaults(handler=_handle_link)


def _add_search_args(parser: ArgumentParser) -> None:
    parser.add_argument("--start-date", required=True, help="开始日期 YYYY-MM-DD")
    parser.add_argument("--end-date", required=True, help="结束日期 YYYY-MM-DD")
    parser.add_argument("--keyword", help="关键词（证券代码或公司名称）")
    parser.add_argument("--infotype", help="公告类别")
    parser.add_argument("--page", type=int, default=1, help="页码")
    parser.add_argument("--page-size", type=int, default=20, help="每页数量")
    parser.add_argument("--page-all", action="store_true", help="自动翻页获取全部结果")
    add_format_args(parser)


def _fetch_all(fetch_fn, **kwargs) -> dict:
    page, items = 1, []
    while True:
        data = fetch_fn(**kwargs, page=page, page_size=100)
        batch = data.get("items") or data.get("data") or []
        items.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return {"items": items, "total": len(items)}


def _handle_search(args: Namespace) -> int:
    client = build_client(args)
    kw = dict(start_date=args.start_date, end_date=args.end_date,
               keyword=args.keyword, infotype=args.infotype)
    if args.page_all:
        data = _fetch_all(client.filings.search, **kw)
    else:
        data = client.filings.search(**kw, page=args.page, page_size=args.page_size)
    render(data, output=resolve_format(args))
    return 0


def _handle_stock(args: Namespace) -> int:
    client = build_client(args)
    kw = dict(start_date=args.start_date, end_date=args.end_date,
               keyword=args.keyword, infotype=args.infotype)
    if args.page_all:
        data = _fetch_all(lambda **k: client.filings.stock(args.sec_code, **k), **kw)
    else:
        data = client.filings.stock(args.sec_code, **kw, page=args.page, page_size=args.page_size)
    render(data, output=resolve_format(args))
    return 0


def _handle_link(args: Namespace) -> int:
    client = build_client(args)
    data = client.filings.link(args.met_link)
    render(data, output=resolve_format(args))
    return 0
