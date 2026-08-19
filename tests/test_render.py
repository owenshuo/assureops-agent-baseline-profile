from __future__ import annotations

import json
from pathlib import Path

from agent_baseline_profile.canonical import file_digest
from agent_baseline_profile.profile import load_profile
from agent_baseline_profile.render import render_markdown
from agent_baseline_profile.runner import evaluate_report

ROOT = Path(__file__).resolve().parents[1]


def test_markdown_is_deterministic_and_disclaims_certification() -> None:
    fixture = ROOT / "tests" / "fixtures" / "assureops-evaluation.json"
    content = fixture.read_bytes()
    profile = load_profile(ROOT / "profile" / "assureops.yaml")
    report = evaluate_report(
        profile,
        json.loads(content),
        source_file_sha256=file_digest(content),
    )
    first = render_markdown(report)
    second = render_markdown(report)
    assert first == second
    assert "not certification" in first
    assert "No control currently reaches `evidenced`" in first
    assert "| AUT-05 | AUT | partial |" in first
    assert "| VAL-04 | VAL | not_assessed |" in first
    assert "| RES-01 | RES | not_assessed |" in first
