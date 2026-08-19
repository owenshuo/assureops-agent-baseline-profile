"""Verify the profile against an exact Agent Baseline source checkout."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

import yaml

from agent_baseline_profile.canonical import file_digest


class BaselineSourceError(RuntimeError):
    """Raised when the external baseline source does not match the pin."""


def _git(repo: Path, *args: str) -> str:
    completed = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=False,
        capture_output=True,
        text=True,
    )
    if completed.returncode != 0:
        raise BaselineSourceError(completed.stderr.strip() or "git command failed")
    return completed.stdout.strip()


def verify_baseline_source(repo: Path, profile: dict[str, Any]) -> dict[str, Any]:
    baseline = profile["baseline"]
    actual_commit = _git(repo, "rev-parse", "HEAD")
    if actual_commit != baseline["commit"]:
        raise BaselineSourceError(
            f"Agent Baseline commit mismatch: expected {baseline['commit']}, got {actual_commit}"
        )

    controls_path = repo / baseline["controls_path"]
    content = controls_path.read_bytes()
    actual_sha = file_digest(content)
    if actual_sha != baseline["controls_sha256"]:
        raise BaselineSourceError(
            f"controls digest mismatch: expected {baseline['controls_sha256']}, got {actual_sha}"
        )

    source = yaml.safe_load(content)
    official_controls = source.get("controls", [])
    mapped = profile["controls"]
    official_identity = [
        (item["id"], item["outcome"], item["type"], item["title"])
        for item in official_controls
    ]
    mapped_identity = [
        (item["id"], item["outcome"], item["type"], item["title"])
        for item in mapped
    ]
    if official_identity != mapped_identity:
        raise BaselineSourceError("profile control identities differ from pinned controls.yaml")

    return {
        "version": baseline["version"],
        "commit": actual_commit,
        "controls_sha256": actual_sha,
        "control_count": len(official_controls),
        "mapping_exact": True,
    }
