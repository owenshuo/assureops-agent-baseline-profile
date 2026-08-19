"""Collect the public AssureOps evaluation artifact without modifying its checkout."""

from __future__ import annotations

import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from agent_baseline_profile.canonical import file_digest


class SourceRepositoryError(RuntimeError):
    """Raised when the pinned source repository cannot be trusted or executed."""


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise SourceRepositoryError(completed.stderr.strip() or "git command failed")
    return completed.stdout.strip()


def verify_source_repository(repo: Path, expected: dict[str, Any]) -> None:
    if not (repo / ".git").exists():
        raise SourceRepositoryError(f"not a git checkout: {repo}")
    dirty = _git(repo, "status", "--porcelain")
    if dirty:
        raise SourceRepositoryError("AssureOps checkout must be clean for evidence collection")
    actual_commit = _git(repo, "rev-parse", "HEAD")
    if actual_commit != expected["commit"]:
        raise SourceRepositoryError(
            f"AssureOps commit mismatch: expected {expected['commit']}, got {actual_commit}"
        )
    tag_commit = _git(repo, "rev-list", "-n", "1", expected["tag"])
    if tag_commit != actual_commit:
        raise SourceRepositoryError(f"tag {expected['tag']} does not resolve to pinned commit")


def discover_python(repo: Path, explicit: Path | None = None) -> Path:
    candidates = [explicit] if explicit is not None else []
    candidates.extend(
        [
            repo / ".venv" / "Scripts" / "python.exe",
            repo / ".venv" / "bin" / "python",
        ]
    )
    for candidate in candidates:
        if candidate is not None and candidate.exists():
            return candidate
    raise SourceRepositoryError("no AssureOps Python interpreter found; use --assureops-python")


def collect_assureops_report(
    repo: Path,
    expected: dict[str, Any],
    *,
    python: Path | None = None,
) -> tuple[dict[str, Any], str]:
    verify_source_repository(repo, expected)
    interpreter = discover_python(repo, python)
    environment = os.environ.copy()
    environment["PYTHONPATH"] = str(repo / "src")
    environment["PYTHONDONTWRITEBYTECODE"] = "1"

    with tempfile.TemporaryDirectory(prefix="assureops-agent-baseline-") as temporary:
        output = Path(temporary) / "evaluation.json"
        completed = subprocess.run(
            [
                str(interpreter),
                str(repo / "scripts" / "run_evaluation.py"),
                "--format",
                "json",
                "--output",
                str(output),
            ],
            cwd=repo,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        if completed.returncode != 0:
            raise SourceRepositoryError(
                completed.stderr.strip() or completed.stdout.strip() or "evaluation failed"
            )
        content = output.read_bytes()
        return json.loads(content.decode("utf-8")), file_digest(content)
