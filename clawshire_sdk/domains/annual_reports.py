from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import httpx

from clawshire_sdk.errors import ClawShireApiError, ClawShireNetworkError
from clawshire_sdk.search_normalization import normalize_search_text


class AnnualReportsDomain:
    def __init__(self, client):
        self._client = client

    def latest(
        self,
        *,
        page: int = 1,
        page_size: int = 20,
        year: int | None = None,
        exchange: str | None = None,
        keyword: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {"page": page, "page_size": page_size}
        if year is not None:
            params["year"] = year
        if exchange:
            params["exchange"] = exchange
        if keyword:
            params["keyword"] = keyword
        return self._client.get("/api/v1/annual-report/latest", params=params, auth_required=True)

    def data(self, met_uuid: str) -> dict[str, Any]:
        return self._client.get(f"/api/v1/annual-report/data/{met_uuid}", auth_required=True)

    def analyze_submit(self, pdf_path: str, *, lang: str = "zh") -> dict[str, Any]:
        path = Path(pdf_path)
        content = path.read_bytes()
        return self.analyze_submit_bytes(content, filename=path.name, lang=lang)

    def analyze_submit_bytes(
        self,
        content: bytes,
        *,
        filename: str = "report.pdf",
        lang: str = "zh",
    ) -> dict[str, Any]:
        files = {"file": (filename, content, "application/pdf")}
        data = {"lang": lang}
        return self._client.post(
            "/api/v1/financial-analysis/jobs",
            files=files,
            data=data,
            auth_required=True,
        )

    def analyze_submit_pdf_url(self, pdf_url: str, *, lang: str = "zh") -> dict[str, Any]:
        try:
            with httpx.Client(timeout=self._client.timeout) as client:
                response = client.get(pdf_url)
                response.raise_for_status()
        except httpx.HTTPError as exc:
            raise ClawShireNetworkError(f"下载 PDF 失败: {exc}") from exc

        filename = Path(urlparse(pdf_url).path).name or "report.pdf"
        return self.analyze_submit_bytes(response.content, filename=filename, lang=lang)

    def analyze_get(self, job_id: str) -> dict[str, Any]:
        return self._client.get(
            f"/api/v1/financial-analysis/jobs/{job_id}",
            auth_required=True,
            unwrap=False,
        )

    def analyze_company(
        self,
        keyword: str,
        *,
        year: int | None = None,
        exchange: str | None = None,
        notify_email: str | None = None,
    ) -> dict[str, Any]:
        reports = self.latest(page=1, page_size=20, year=year, exchange=exchange, keyword=keyword)
        items = reports.get("items", [])
        if not items:
            if year is not None:
                raise ClawShireApiError(f"未找到与 {keyword} 匹配的 {year} 年年报")
            raise ClawShireApiError(f"未找到与 {keyword} 匹配的年报")

        selected = self._pick_report(items, keyword)
        payload: dict[str, Any] = {"notify_email": notify_email or ""}

        task = self._client.post(
            f"/api/v1/annual-report/analyze/{selected['met_uuid']}",
            json=payload,
            auth_required=True,
        )
        return {
            **task,
            "selected_report": {
                "met_uuid": selected.get("met_uuid"),
                "company_code": selected.get("company_code"),
                "company_name": selected.get("company_name"),
                "pdf_url": selected.get("pdf_url"),
                "publish_time": selected.get("publish_time"),
            },
        }

    def get_analysis_task(self, task_id: int) -> dict[str, Any]:
        tasks = self._client.get("/api/v1/annual-report/analysis-tasks", auth_required=True)
        if isinstance(tasks, list):
            for task in tasks:
                if int(task.get("task_id", -1)) == int(task_id):
                    return task
        raise ClawShireApiError(f"未找到 task_id={task_id} 的分析任务")

    def download_report(
        self,
        *,
        met_uuid: str,
        report_url: str,
        company_name: str | None = None,
        dest: str | Path | None = None,
    ) -> Path:
        target = Path(dest) if dest is not None else Path(self._default_report_filename(met_uuid, company_name))
        return self._client.download(report_url, dest=target, auth_required=True)

    @staticmethod
    def _pick_report(items: list[dict[str, Any]], keyword: str) -> dict[str, Any]:
        normalized = keyword.strip().lower()
        normalized_for_search = normalize_search_text(keyword)
        for item in items:
            if str(item.get("company_code", "")).strip().lower() == normalized:
                return item
        for item in items:
            if str(item.get("company_name", "")).strip().lower() == normalized:
                return item
        for item in items:
            if normalize_search_text(item.get("company_name", "")) == normalized_for_search:
                return item
        return items[0]

    @staticmethod
    def _default_report_filename(met_uuid: str, company_name: str | None) -> str:
        base = company_name.strip() if company_name else "annual-report-analysis"
        safe = re.sub(r"[^\w\-.]+", "-", base, flags=re.UNICODE).strip("-") or "annual-report-analysis"
        return f"{safe}-{met_uuid}.html"
