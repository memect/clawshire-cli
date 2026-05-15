from __future__ import annotations

from collections import Counter
from argparse import ArgumentParser, Namespace, _SubParsersAction
from typing import Any

from clawshire_cli.context import add_format_args, build_client, resolve_format
from clawshire_cli.output import render

EVENT_RULES = [
    ("share_repurchase", "回购", ("回购",)),
    ("holdings_increase", "增持", ("增持",)),
    ("holdings_reduction", "减持", ("减持",)),
    ("earnings_forecast", "业绩预告", ("业绩预告",)),
    ("earnings_express", "业绩快报", ("业绩快报",)),
    ("major_contract", "重大合同/中标", ("重大合同", "中标", "中标候选人")),
    ("mna_restructuring", "并购重组", ("并购", "重组", "重大资产重组", "购买资产", "收购")),
    ("equity_pledge", "股权质押", ("质押", "解除质押")),
    ("regulatory_action", "监管处罚/问询", ("立案", "行政处罚", "监管函", "问询函", "警示函")),
    ("litigation_arbitration", "诉讼仲裁", ("诉讼", "仲裁")),
]


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

    detect_events = notice_subparsers.add_parser("detect-events", help="按公告标题识别事件类型")
    detect_events.add_argument("--sec-code", help="证券代码；传入后优先按证券代码查询")
    _add_search_args(detect_events)
    detect_events.add_argument(
        "--event-type",
        action="append",
        choices=[rule[0] for rule in EVENT_RULES],
        help="只保留指定事件类型，可重复传入",
    )
    detect_events.set_defaults(handler=_handle_detect_events)


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


def _fetch_notice_items(args: Namespace) -> dict[str, Any]:
    client = build_client(args)
    kw = dict(
        start_date=args.start_date,
        end_date=args.end_date,
        keyword=args.keyword,
        infotype=args.infotype,
    )
    if getattr(args, "sec_code", None):
        if args.page_all:
            return _fetch_all(lambda **k: client.filings.stock(args.sec_code, **k), **kw)
        return client.filings.stock(args.sec_code, **kw, page=args.page, page_size=args.page_size)
    if args.page_all:
        return _fetch_all(client.filings.search, **kw)
    return client.filings.search(**kw, page=args.page, page_size=args.page_size)


def _pick_title(item: dict[str, Any]) -> str:
    for key in ("announcement_title", "met_title", "title", "name"):
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _pick_field(item: dict[str, Any], *keys: str) -> Any:
    for key in keys:
        if key in item and item[key] not in (None, ""):
            return item[key]
    return None


def detect_events(items: list[dict[str, Any]], allowed_event_types: set[str] | None = None) -> dict[str, Any]:
    detected_items: list[dict[str, Any]] = []
    event_counter: Counter[str] = Counter()

    for item in items:
        title = _pick_title(item)
        if not title:
            continue

        matched_events = []
        for event_type, label, keywords in EVENT_RULES:
            if allowed_event_types and event_type not in allowed_event_types:
                continue
            matched_keywords = [keyword for keyword in keywords if keyword in title]
            if matched_keywords:
                matched_events.append(
                    {
                        "event_type": event_type,
                        "event_label": label,
                        "matched_keywords": matched_keywords,
                        "confidence": "high",
                    }
                )
                event_counter[event_type] += 1

        if not matched_events:
            continue

        detected_items.append(
            {
                "met_uuid": _pick_field(item, "met_uuid"),
                "sec_code": _pick_field(item, "sec_code", "company_code"),
                "sec_name": _pick_field(item, "sec_name", "company_name"),
                "announcement_title": title,
                "announcement_time": _pick_field(item, "announcement_time", "publish_time", "date"),
                "pdf_url": _pick_field(item, "pdf_url", "met_link", "url"),
                "events": matched_events,
            }
        )

    return {
        "total": len(detected_items),
        "event_counts": dict(sorted(event_counter.items())),
        "items": detected_items,
    }


def _handle_detect_events(args: Namespace) -> int:
    source_data = _fetch_notice_items(args)
    source_items = source_data.get("items") or source_data.get("data") or []
    allowed_event_types = set(args.event_type or [])
    result = detect_events(source_items, allowed_event_types or None)
    result.update(
        {
            "source_total": source_data.get("total", len(source_items)),
            "query": {
                "start_date": args.start_date,
                "end_date": args.end_date,
                "sec_code": args.sec_code,
                "keyword": args.keyword,
                "infotype": args.infotype,
                "page_all": args.page_all,
            },
        }
    )
    render(result, output=resolve_format(args))
    return 0
