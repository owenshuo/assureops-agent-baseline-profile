from __future__ import annotations

import subprocess
from pathlib import Path

import pytest

from agent_baseline_profile.collector import SourceRepositoryError, verify_source_repository


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, capture_output=True)


def test_source_repository_must_be_clean_and_pinned(tmp_path: Path) -> None:
    git(tmp_path, "init")
    git(tmp_path, "config", "user.email", "profile@example.invalid")
    git(tmp_path, "config", "user.name", "Profile Test")
    file = tmp_path / "README.md"
    file.write_text("fixture\n", encoding="utf-8")
    git(tmp_path, "add", "README.md")
    git(tmp_path, "commit", "-m", "fixture")
    commit = subprocess.run(
        ["git", "-C", str(tmp_path), "rev-parse", "HEAD"],
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()
    git(tmp_path, "tag", "fixture-tag")

    expected = {"commit": commit, "tag": "fixture-tag"}
    verify_source_repository(tmp_path, expected)

    file.write_text("dirty\n", encoding="utf-8")
    with pytest.raises(SourceRepositoryError, match="must be clean"):
        verify_source_repository(tmp_path, expected)
