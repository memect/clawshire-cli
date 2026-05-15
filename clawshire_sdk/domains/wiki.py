from __future__ import annotations

from typing import Any


class WikiDomain:
    def __init__(self, client):
        self._client = client

    def search(self, *, q: str | None = None, code: str | None = None,
               ann_type: str | None = None, tags: str | None = None,
               date_from: str | None = None, date_to: str | None = None,
               quality_min: int | None = None, page: int = 1, size: int = 20) -> dict[str, Any]:
        params: dict[str, Any] = {"page": page, "size": size}
        if q:
            params["q"] = q
        if code:
            params["code"] = code
        if ann_type:
            params["ann_type"] = ann_type
        if tags:
            params["tags"] = tags
        if date_from:
            params["date_from"] = date_from
        if date_to:
            params["date_to"] = date_to
        if quality_min is not None:
            params["quality_min"] = quality_min
        return self._client.get("/api/v1/wiki", params=params, auth_required=True)

    def entry(self, ann_id: str) -> dict[str, Any]:
        return self._client.get(f"/api/v1/wiki/{ann_id}", auth_required=True)

    def company(self, sec_code: str) -> dict[str, Any]:
        return self._client.get(f"/api/v1/wiki/company/{sec_code}", auth_required=True)

    def tag(self, tag_name: str) -> dict[str, Any]:
        return self._client.get(f"/api/v1/wiki/tag/{tag_name}", auth_required=True)

    def backlinks(self, page_type: str, page_key: str) -> dict[str, Any]:
        return self._client.get(f"/api/v1/wiki/backlinks/{page_type}/{page_key}", auth_required=True)

    def resolve(self, q: str) -> dict[str, Any]:
        return self._client.get("/api/v1/wiki/resolve", params={"q": q}, auth_required=True)

    def special(self, name: str, **params) -> dict[str, Any]:
        return self._client.get(f"/api/v1/wiki/special/{name}", params=params or None, auth_required=True)
