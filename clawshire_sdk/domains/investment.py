from __future__ import annotations

from typing import Any


class InvestmentDomain:
    def __init__(self, client):
        self._client = client

    def industries(self) -> dict[str, Any]:
        """返回所有申万一级行业名称列表（免费）。"""
        return self._client.get("/api/v1/wiki/investment/industries", auth_required=True)

    def company_deltas(self, sec_code: str, size: int = 20) -> dict[str, Any]:
        """返回公司最近研判变化记录。"""
        return self._client.get(
            f"/api/v1/wiki/investment/company/{sec_code}/deltas",
            params={"size": size},
            auth_required=True,
        )

    def industry_thesis(self, industry_name: str) -> dict[str, Any]:
        """返回行业研判汇总（industry_name 需为申万一级标准名）。"""
        return self._client.get(
            f"/api/v1/wiki/investment/industry/{industry_name}/thesis",
            auth_required=True,
        )

    def company_summary(self, sec_code: str) -> dict[str, Any]:
        """返回公司综合研判摘要。"""
        return self._client.get(
            f"/api/v1/wiki/investment/company/{sec_code}/summary",
            auth_required=True,
        )
