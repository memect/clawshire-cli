from __future__ import annotations

import time
from pathlib import Path
from argparse import ArgumentParser, Namespace, _SubParsersAction

from clawshire_cli.context import build_client, resolve_output
from clawshire_cli.output import render


def register(subparsers: _SubParsersAction[ArgumentParser]) -> None:
    parser = subparsers.add_parser("annual-analysis", help="年报分析")
    annual_analysis_subparsers = parser.add_subparsers(dest="annual_analysis_command", required=True)

    pdf_file = annual_analysis_subparsers.add_parser("pdf-file", help="通过本地 PDF 文件提交分析")
    pdf_file.add_argument("pdf_path", help="本地 PDF 路径")
    _add_job_submit_args(pdf_file)
    pdf_file.set_defaults(handler=_handle_pdf_file)

    pdf_url = annual_analysis_subparsers.add_parser("pdf-url", help="通过 PDF 链接提交分析")
    pdf_url.add_argument("pdf_url", help="PDF 直链")
    _add_job_submit_args(pdf_url)
    pdf_url.set_defaults(handler=_handle_pdf_url)

    company = annual_analysis_subparsers.add_parser("company", help="通过公司代码或简称分析最新年报")
    company.add_argument("keyword", help="公司证券代码或简称")
    company.add_argument("--year", type=int, help="年份，如 2025")
    company.add_argument("--exchange", choices=["sz", "sh", "bj"], help="交易所过滤")
    company.add_argument("--notify-email", help="分析完成后通知邮箱")
    company.set_defaults(handler=_handle_company)

    get_cmd = annual_analysis_subparsers.add_parser("get", help="查询年报分析任务")
    get_cmd.add_argument("task_or_job_id", help="分析任务 ID。支持 direct job_id 或 company task_id")
    get_cmd.add_argument("--save-report-to", help="已完成时将 HTML 报告保存到指定路径")
    get_cmd.set_defaults(handler=_handle_get)


def _add_job_submit_args(parser: ArgumentParser) -> None:
    parser.add_argument("--lang", default="zh", choices=["zh", "en"], help="报告语言")
    parser.add_argument("--wait", action="store_true", help="阻塞等待任务完成")
    parser.add_argument("--poll-interval", type=int, default=10, help="轮询间隔秒数")
    parser.add_argument("--max-polls", type=int, default=60, help="最大轮询次数")


def _handle_pdf_file(args: Namespace) -> int:
    client = build_client(args)
    data = client.annual.analyze_submit(args.pdf_path, lang=args.lang)
    data = _attach_follow_up_command(data, id_key="job_id")
    return _render_or_wait_job(client, data, args)


def _handle_pdf_url(args: Namespace) -> int:
    client = build_client(args)
    data = client.annual.analyze_submit_pdf_url(args.pdf_url, lang=args.lang)
    data = _attach_follow_up_command(data, id_key="job_id")
    return _render_or_wait_job(client, data, args)


def _handle_company(args: Namespace) -> int:
    client = build_client(args)
    data = client.annual.analyze_company(
        args.keyword,
        year=args.year,
        exchange=args.exchange,
        notify_email=args.notify_email,
    )
    data = _attach_follow_up_command(data, id_key="task_id")
    render(data, output=resolve_output(args))
    return 0


def _handle_get(args: Namespace) -> int:
    client = build_client(args)
    if str(args.task_or_job_id).isdigit():
        data = client.annual.get_analysis_task(int(args.task_or_job_id))
        data = _maybe_download_report(client, data, args)
    else:
        data = client.annual.analyze_get(args.task_or_job_id)
    render(data, output=resolve_output(args))
    return 0


def _maybe_download_report(client, data: dict, args: Namespace) -> dict:
    if data.get("status") != "completed":
        return data
    report_url = data.get("report_url")
    met_uuid = data.get("met_uuid")
    if not report_url or not met_uuid:
        return data

    dest = args.save_report_to
    saved_path = client.annual.download_report(
        met_uuid=met_uuid,
        report_url=report_url,
        company_name=data.get("company_name"),
        dest=dest,
    )
    enriched = dict(data)
    enriched["saved_report_path"] = str(Path(saved_path).resolve())
    return enriched


def _attach_follow_up_command(data: dict, *, id_key: str) -> dict:
    task_id = data.get(id_key)
    if not task_id:
        return data
    enriched = dict(data)
    enriched["next_command"] = f"clawshire annual-analysis get {task_id}"
    return enriched


def _render_or_wait_job(client, data: dict, args: Namespace) -> int:
    if not args.wait:
        render(data, output=resolve_output(args))
        return 0

    job_id = data.get("job_id")
    if not job_id:
        render(data, output=resolve_output(args))
        return 0

    for attempt in range(args.max_polls):
        result = client.annual.analyze_get(job_id)
        status = result.get("status", "unknown")
        print(f"[{attempt + 1}/{args.max_polls}] status={status}")
        if status in {"completed", "failed"}:
            render(result, output=resolve_output(args))
            return 0
        time.sleep(args.poll_interval)

    print(f"轮询超时，job_id={job_id}")
    return 1
