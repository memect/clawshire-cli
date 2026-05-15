from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT_DIR / "scripts" / "check_skill_drift.py"


def run_check(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(SCRIPT_PATH), "--root", str(root)],
        capture_output=True,
        text=True,
        check=False,
    )


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def canonical_skill() -> str:
    return """---
name: clawshire-data-query
version: 1.0.0
description: "Canonical skill"
triggers: ["notice search"]
invocable: true
argument-hint: "[search]"
metadata:
  requires:
    bins: ["clawshire"]
  cliHelp: "clawshire notice --help"
---

# Canonical
"""


def derived_skill(source_path: str) -> str:
    return f"""---
name: clawshire-data-query
version: 1.0.0
description: "Derived skill"
triggers: ["notice search"]
invocable: true
argument-hint: "[search]"
metadata:
  requires:
    bins: ["clawshire"]
  cliHelp: "clawshire notice --help"
  sourceSkill: "{source_path}"
---

# Derived
"""


def test_drift_check_skips_when_no_derived_skill_roots(tmp_path: Path):
    write(tmp_path / "skills" / "clawshire-data-query" / "SKILL.md", canonical_skill())

    result = run_check(tmp_path)

    assert result.returncode == 0
    assert "no derived skill bundles found; skipped" in result.stdout


def test_drift_check_accepts_valid_derived_skill(tmp_path: Path):
    write(tmp_path / "skills" / "clawshire-data-query" / "SKILL.md", canonical_skill())
    write(
        tmp_path / "agent-skills" / "research-agent" / "clawshire-data-query" / "SKILL.md",
        derived_skill("../../../skills/clawshire-data-query/SKILL.md"),
    )

    result = run_check(tmp_path)

    assert result.returncode == 0
    assert "skill drift check: ok" in result.stdout


def test_drift_check_rejects_missing_source_skill_annotation(tmp_path: Path):
    write(tmp_path / "skills" / "clawshire-data-query" / "SKILL.md", canonical_skill())
    write(
        tmp_path / "agent-bundles" / "research-agent" / "clawshire-data-query" / "SKILL.md",
        canonical_skill(),
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "metadata.sourceSkill" in result.stderr


def test_drift_check_rejects_source_outside_canonical_skills(tmp_path: Path):
    write(tmp_path / "skills" / "clawshire-data-query" / "SKILL.md", canonical_skill())
    write(tmp_path / "docs" / "fake-skill.md", "# not a canonical skill\n")
    write(
        tmp_path / "agent-skills" / "risk-agent" / "clawshire-data-query" / "SKILL.md",
        derived_skill("../../../docs/fake-skill.md"),
    )

    result = run_check(tmp_path)

    assert result.returncode == 1
    assert "source skill must point into" in result.stderr
