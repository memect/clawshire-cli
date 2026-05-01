from __future__ import annotations

import re


def normalize_search_text(value: object) -> str:
    return re.sub(r"\s+", "", str(value or "")).lower()
