from __future__ import annotations

from typing import Any


class FilingsDomain:
    def __init__(self, client):
        self._client = client

    def search(
        self,
        *,
        start_date: str,
        end_date: str,
        keyword: str | None = None,
        infotype: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, Any]:
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "page": page,
            "page_size": page_size,
        }
        if keyword:
            params["keyword"] = keyword
        if infotype:
            params["infotype"] = infotype
        return self._client.get("/api/v1/announcements", params=params, auth_required=False)

    def stock(
        self,
        sec_code: str,
        *,
        start_date: str,
        end_date: str,
        keyword: str | None = None,
        infotype: str | None = None,
        page: int = 1,
        page_size: int = 20,
    ) -> dict[str, Any]:
        params = {
            "start_date": start_date,
            "end_date": end_date,
            "page": page,
            "page_size": page_size,
        }
        if keyword:
            params["keyword"] = keyword
        if infotype:
            params["infotype"] = infotype
        return self._client.get(
            f"/api/v1/stock/{sec_code}/announcements",
            params=params,
            auth_required=False,
        )

    def link(self, met_link: str) -> dict[str, Any]:
        return self._client.get(
            "/api/v1/met_link",
            params={"met_link": met_link},
            auth_required=False,
        )
