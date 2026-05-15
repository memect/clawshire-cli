#!/usr/bin/env python3
from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
import sys


DERIVED_SKILL_ROOT_NAMES = ("agent-skills", "agent-bundles")


@dataclass
class DriftCheckResult:
    checked_files: int = 0
    derived_roots: int = 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate derived skill bundles declare a canonical source skill."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parents[1],
        help="Repository root. Defaults to the clawshire-cli project root.",
    )
    return parser.parse_args()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def parse_frontmatter(path: Path) -> dict[str, object]:
    text = read_text(path)
    if not text.startswith("---\n"):
        raise AssertionError(f"{path} is missing YAML frontmatter")
    try:
        _, frontmatter, _ = text.split("---\n", 2)
    except ValueError as exc:
        raise AssertionError(f"{path} has invalid YAML frontmatter block") from exc

    data: dict[str, object] = {}
    stack: list[tuple[int, dict[str, object]]] = [(-1, data)]

    for raw_line in frontmatter.splitlines():
        if not raw_line.strip():
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()
        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise AssertionError(f"{path} has invalid frontmatter indentation: {raw_line}")
        parent = stack[-1][1]
        key, _, value = line.partition(":")
        value = value.strip()
        if not value:
            nested_parent: dict[str, object] = {}
            parent[key] = nested_parent
            stack.append((indent, nested_parent))
            continue
        parent[key] = parse_scalar(value)

    return data


def parse_scalar(value: str) -> object:
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip('"') for item in inner.split(",")]
    return value


def assert_path_is_relative(source_value: object, path: Path) -> Path:
    if not isinstance(source_value, str) or not source_value.strip():
        raise AssertionError(
            f"{path} must declare metadata.sourceSkill as a non-empty relative path"
        )
    source_path = Path(source_value)
    if source_path.is_absolute():
        raise AssertionError(f"{path} metadata.sourceSkill must be relative, got: {source_value}")
    return source_path


def ensure_within_root(path: Path, root: Path, message: str) -> None:
    try:
        path.relative_to(root)
    except ValueError as exc:
        raise AssertionError(message) from exc


def validate_derived_skill(path: Path, canonical_skills_root: Path) -> None:
    frontmatter = parse_frontmatter(path)
    metadata = frontmatter.get("metadata")
    if not isinstance(metadata, dict):
        raise AssertionError(f"{path} is missing metadata block")

    source_value = metadata.get("sourceSkill")
    source_path = assert_path_is_relative(source_value, path)
    resolved_source = (path.parent / source_path).resolve()

    if not resolved_source.exists():
        raise AssertionError(f"{path} points to missing source skill: {source_value}")

    ensure_within_root(
        resolved_source,
        canonical_skills_root.resolve(),
        f"{path} source skill must point into {canonical_skills_root}",
    )

    if resolved_source.name != "SKILL.md":
        raise AssertionError(f"{path} source skill must point to a SKILL.md file: {source_value}")


def check_skill_drift(root: Path) -> DriftCheckResult:
    root = root.resolve()
    canonical_skills_root = root / "skills"
    if not canonical_skills_root.is_dir():
        raise AssertionError(f"missing canonical skills directory: {canonical_skills_root}")

    result = DriftCheckResult()

    for root_name in DERIVED_SKILL_ROOT_NAMES:
        derived_root = root / root_name
        if not derived_root.is_dir():
            continue
        result.derived_roots += 1
        for skill_md in sorted(derived_root.glob("**/SKILL.md")):
            result.checked_files += 1
            validate_derived_skill(skill_md, canonical_skills_root)

    return result


def main() -> int:
    args = parse_args()
    try:
        result = check_skill_drift(args.root)
    except AssertionError as exc:
        print(f"skill drift check failed: {exc}", file=sys.stderr)
        return 1

    if result.derived_roots == 0 or result.checked_files == 0:
        print("skill drift check: no derived skill bundles found; skipped")
        return 0

    print(
        "skill drift check: ok "
        f"({result.checked_files} derived skill files across {result.derived_roots} roots)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
