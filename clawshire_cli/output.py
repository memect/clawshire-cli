from __future__ import annotations

import csv
import io
import json
from typing import Any


def render(data: Any, *, output: str) -> None:
    output = output.lower()
    if output == "json":
        print(json.dumps(data, ensure_ascii=False, indent=2))
        return
    if output == "markdown":
        print(_to_markdown(data))
        return
    if output == "csv":
        print(_to_csv(data))
        return
    print(_to_table(data))


def _to_markdown(data: Any) -> str:
    if isinstance(data, list):
        if not data:
            return "_No data_"
        if all(isinstance(item, dict) for item in data):
            return _dict_list_to_markdown(data)
    if isinstance(data, dict):
        if "items" in data and isinstance(data["items"], list):
            head = {k: v for k, v in data.items() if k != "items"}
            parts = []
            if head:
                parts.append(_dict_to_bullets(head))
            parts.append(_dict_list_to_markdown(data["items"]))
            return "\n\n".join(part for part in parts if part)
        return _dict_to_bullets(data)
    return str(data)


def _to_table(data: Any) -> str:
    if isinstance(data, list):
        if not data:
            return "No data"
        if all(isinstance(item, dict) for item in data):
            return _dict_list_to_table(data)
    if isinstance(data, dict):
        if "items" in data and isinstance(data["items"], list):
            header = _dict_to_lines({k: v for k, v in data.items() if k != "items"})
            body = _dict_list_to_table(data["items"])
            if header:
                return f"{header}\n\n{body}"
            return body
        return _dict_to_lines(data)
    return str(data)


def _dict_to_lines(data: dict[str, Any]) -> str:
    return "\n".join(f"{key}: {_format_value(value)}" for key, value in data.items())


def _dict_to_bullets(data: dict[str, Any]) -> str:
    return "\n".join(f"- {key}: {_format_value(value)}" for key, value in data.items())


def _dict_list_to_table(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "No data"
    columns = []
    for row in rows:
        for key in row.keys():
            if key not in columns:
                columns.append(key)
    widths = {col: len(col) for col in columns}
    for row in rows:
        for col in columns:
            widths[col] = max(widths[col], len(_format_value(row.get(col))))
    header = " | ".join(col.ljust(widths[col]) for col in columns)
    sep = "-+-".join("-" * widths[col] for col in columns)
    body = [
        " | ".join(_format_value(row.get(col)).ljust(widths[col]) for col in columns)
        for row in rows
    ]
    return "\n".join([header, sep, *body])


def _dict_list_to_markdown(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_No data_"
    columns = []
    for row in rows:
        for key in row.keys():
            if key not in columns:
                columns.append(key)
    header = "| " + " | ".join(columns) + " |"
    sep = "| " + " | ".join("---" for _ in columns) + " |"
    body = []
    for row in rows:
        body.append("| " + " | ".join(_format_value(row.get(col)) for col in columns) + " |")
    return "\n".join([header, sep, *body])


def _to_csv(data: Any) -> str:
    rows: list[dict] = []
    if isinstance(data, list) and all(isinstance(i, dict) for i in data):
        rows = data
    elif isinstance(data, dict):
        rows = data.get("items") or data.get("data") or []
        if not rows:
            rows = [data]
    if not rows:
        return ""
    columns = list(dict.fromkeys(k for row in rows for k in row))
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(columns)
    for row in rows:
        w.writerow([_format_value(row.get(c)) for c in columns])
    return buf.getvalue().rstrip()


def _format_value(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, ensure_ascii=False)
    return str(value)
