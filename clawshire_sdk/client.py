from __future__ import annotations

from pathlib import Path
from typing import Any

import httpx

from clawshire_sdk.domains import AnnualReportsDomain, FilingsDomain
from clawshire_sdk.errors import (
    ClawShireApiError,
    ClawShireAuthError,
    ClawShireConfigError,
    ClawShireNetworkError,
)


class ClawShireClient:
    def __init__(
        self,
        *,
        base_url: str,
        api_key: str | None = None,
        timeout: float = 30.0,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self.filings = FilingsDomain(self)
        self.annual = AnnualReportsDomain(self)

    def get(
        self,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        auth_required: bool,
        unwrap: bool = True,
    ) -> dict[str, Any]:
        return self._request("GET", path, params=params, auth_required=auth_required, unwrap=unwrap)

    def post(
        self,
        path: str,
        *,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        auth_required: bool,
        unwrap: bool = True,
    ) -> dict[str, Any]:
        return self._request(
            "POST",
            path,
            json=json,
            data=data,
            files=files,
            auth_required=auth_required,
            unwrap=unwrap,
        )

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        json: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        auth_required: bool,
        unwrap: bool = True,
    ) -> dict[str, Any]:
        headers = self._build_headers(auth_required=auth_required)
        url = f"{self.base_url}{path}"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.request(
                    method,
                    url,
                    headers=headers,
                    params=params,
                    json=json,
                    data=data,
                    files=files,
                )
        except httpx.HTTPError as exc:
            raise ClawShireNetworkError(str(exc)) from exc

        payload = self._decode_payload(response)
        if response.status_code in (401, 403):
            raise ClawShireAuthError(self._extract_message(payload, fallback="认证失败"))
        if response.status_code >= 400:
            raise ClawShireApiError(
                self._extract_message(payload, fallback=f"请求失败: HTTP {response.status_code}"),
                status_code=response.status_code,
            )

        if unwrap and isinstance(payload, dict) and "code" in payload and "data" in payload:
            code = payload.get("code")
            if code != 200:
                raise ClawShireApiError(self._extract_message(payload, fallback="业务请求失败"))
            return payload["data"]
        return payload

    def download(
        self,
        path: str,
        *,
        dest: str | Path,
        auth_required: bool,
    ) -> Path:
        headers = self._build_headers(auth_required=auth_required)
        url = path if path.startswith(("http://", "https://")) else f"{self.base_url}{path}"
        target = Path(dest)
        try:
            with httpx.Client(timeout=self.timeout) as client:
                response = client.get(url, headers=headers)
                response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            payload = self._decode_payload(exc.response)
            raise ClawShireApiError(
                self._extract_message(payload, fallback=f"下载失败: HTTP {exc.response.status_code}"),
                status_code=exc.response.status_code,
            ) from exc
        except httpx.HTTPError as exc:
            raise ClawShireNetworkError(str(exc)) from exc

        target.write_bytes(response.content)
        return target

    def _build_headers(self, *, auth_required: bool) -> dict[str, str]:
        headers: dict[str, str] = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        elif auth_required:
            raise ClawShireConfigError("该命令需要 API Key。请设置 CLAWSHIRE_API_KEY 或使用 --api-key。")
        return headers

    @staticmethod
    def _decode_payload(response: httpx.Response) -> dict[str, Any]:
        try:
            return response.json()
        except ValueError as exc:
            raise ClawShireApiError("上游返回了非 JSON 响应", status_code=response.status_code) from exc

    @staticmethod
    def _extract_message(payload: Any, *, fallback: str) -> str:
        if isinstance(payload, dict):
            for key in ("message", "detail", "error"):
                value = payload.get(key)
                if isinstance(value, str) and value.strip():
                    return value
        return fallback
