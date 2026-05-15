from __future__ import annotations

import re
import shlex
from pathlib import Path

from clawshire_cli.main import build_parser


ROOT_DIR = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT_DIR / "skills"
SKILL_DIRS = sorted(path for path in SKILLS_DIR.iterdir() if path.is_dir())
EXPECTED_SKILLS = [
    "clawshire-annual-analysis",
    "clawshire-annual-report",
    "clawshire-data-query",
    "clawshire-shared",
]
RELATIVE_LINK_RE = re.compile(r"\[[^\]]+\]\((?!https?://)(?!#)([^)]+)\)")
FENCED_CODE_RE = re.compile(r"```(?:bash|text)?\n(.*?)```", re.DOTALL)
CLI_COMMAND_RE = re.compile(r"^\s*(clawshire|cs)\s+.+$", re.MULTILINE)
REQUIRED_SECTION_HEADINGS = [
    "## Agent Invariants",
    "## Quick Reference",
    "## Decision Tree",
    "## Common Workflows",
    "## References",
]


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
        parent[key] = _parse_scalar(value)

    return data


def _parse_scalar(value: str) -> object:
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip('"') for item in inner.split(",")]
    return value


def extract_relative_links(text: str) -> list[str]:
    return [match.group(1) for match in RELATIVE_LINK_RE.finditer(text)]


def extract_cli_commands(text: str) -> list[str]:
    commands: list[str] = []
    for block in FENCED_CODE_RE.findall(text):
        for line in block.splitlines():
            stripped = line.strip()
            if "<" in stripped or "..." in stripped:
                continue
            if stripped.startswith(("clawshire ", "cs ")):
                commands.append(stripped)
    return commands


def actual_cli_examples() -> list[str]:
    commands: list[str] = []
    for path in sorted(SKILLS_DIR.glob("**/*.md")):
        commands.extend(extract_cli_commands(read_text(path)))
    return commands


def test_skills_directory_matches_expected_bundle():
    assert [path.name for path in SKILL_DIRS] == EXPECTED_SKILLS


def test_each_skill_has_required_files():
    for skill_dir in SKILL_DIRS:
        skill_md = skill_dir / "SKILL.md"
        references_dir = skill_dir / "references"
        assert skill_md.exists(), f"missing {skill_md}"
        assert references_dir.is_dir(), f"missing {references_dir}"
        assert any(references_dir.iterdir()), f"{references_dir} is empty"


def test_skill_readme_lists_all_skills():
    text = read_text(SKILLS_DIR / "README.md")
    for skill_name in EXPECTED_SKILLS:
        assert f"`{skill_name}`" in text
    assert "## SKILL.md 模板约束" in text
    assert "## 必备正文章节" in text
    assert "## 业务型 Skill 的额外要求" in text


def test_skill_frontmatter_and_shared_rules_are_valid():
    for skill_dir in SKILL_DIRS:
        skill_md = skill_dir / "SKILL.md"
        text = read_text(skill_md)
        frontmatter = parse_frontmatter(skill_md)

        assert frontmatter["name"] == skill_dir.name
        assert frontmatter["version"] == "1.0.0"
        assert frontmatter["description"]
        assert isinstance(frontmatter.get("triggers"), list)
        assert frontmatter.get("triggers"), f"{skill_md} missing triggers"
        assert str(frontmatter.get("invocable")).lower() == "true"
        assert frontmatter.get("argument-hint")

        metadata = frontmatter.get("metadata")
        assert isinstance(metadata, dict), f"{skill_md} missing metadata block"
        requires = metadata.get("requires")
        assert isinstance(requires, dict), f"{skill_md} missing requires block"
        assert requires.get("bins") == ["clawshire"]
        assert metadata.get("cliHelp", "").startswith("clawshire ")

        for heading in REQUIRED_SECTION_HEADINGS:
            assert heading in text, f"{skill_md} missing section: {heading}"

        if skill_dir.name != "clawshire-shared":
            assert "../clawshire-shared/SKILL.md" in text
            assert "## Output Rules" in text, f"{skill_md} missing Output Rules"
            assert "--format json" in text, f"{skill_md} should include a json example"
        else:
            assert "## Output Modes" in text, f"{skill_md} missing Output Modes"


def test_markdown_relative_links_resolve():
    for path in sorted(SKILLS_DIR.glob("**/*.md")):
        text = read_text(path)
        for link in extract_relative_links(text):
            target = (path.parent / link).resolve()
            assert target.exists(), f"{path} has broken link: {link}"


def test_skill_markdown_contains_parseable_cli_examples():
    parser = build_parser()
    commands = actual_cli_examples()
    assert commands, "no concrete clawshire examples found in skills markdown"

    for command in commands:
        tokens = shlex.split(command)
        tokens.pop(0)
        if tokens and tokens[-1] == "--help":
            tokens = tokens[:-1]
        if not tokens:
            continue
        parser.parse_args(tokens)


def test_cli_help_commands_declared_in_frontmatter_are_valid():
    parser = build_parser()
    for skill_dir in SKILL_DIRS:
        frontmatter = parse_frontmatter(skill_dir / "SKILL.md")
        metadata = frontmatter["metadata"]
        cli_help = metadata["cliHelp"]
        tokens = shlex.split(str(cli_help))
        assert tokens.pop(0) == "clawshire"
        assert tokens[-1] == "--help"
        with _expect_help_exit():
            parser.parse_args(tokens)


class _expect_help_exit:
    def __enter__(self) -> None:
        return None

    def __exit__(self, exc_type, exc, _tb) -> bool:
        if exc_type is SystemExit and exc.code == 0:
            return True
        return False
