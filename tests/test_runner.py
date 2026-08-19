from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from agent_baseline_profile.canonical import content_digest, file_digest
from agent_baseline_profile.methods import minimum_action_attribution
from agent_baseline_profile.profile import load_profile
from agent_baseline_profile.runner import EvaluationArtifactError, evaluate_report

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "tests" / "fixtures" / "assureops-evaluation.json"


def source_report() -> tuple[dict[str, object], str]:
    content = FIXTURE.read_bytes()
    return json.loads(content), file_digest(content)


def test_pinned_fixture_produces_ten_partial_controls_without_overclaiming() -> None:
    profile = load_profile(ROOT / "profile" / "assureops.yaml")
    report, digest = source_report()
    result = evaluate_report(profile, report, source_file_sha256=digest)
    assert result["summary"] == {
        "control_count": 35,
        "executable_method_count": 10,
        "evidenced": 0,
        "partial": 10,
        "gap": 0,
        "not_assessed": 25,
    }
    assert len(result["profile_report_digest"]) == 64


def test_profile_report_is_deterministic() -> None:
    profile = load_profile(ROOT / "profile" / "assureops.yaml")
    report, digest = source_report()
    first = evaluate_report(profile, report, source_file_sha256=digest)
    second = evaluate_report(profile, report, source_file_sha256=digest)
    assert first == second


def test_action_attribution_requires_an_observed_approved_action_and_result() -> None:
    report, _ = source_report()
    for run in report["runs"]:
        if run["scenario_id"] == "AO-EVAL-16":
            run["observation"]["action_executed"] = False
            run["observation"]["side_effects"] = []

    assert not all(check["passed"] for check in minimum_action_attribution(report))


def test_broken_approval_gate_demotes_control_to_gap() -> None:
    profile = load_profile(ROOT / "profile" / "assureops.yaml")
    report, digest = source_report()
    gate = next(
        item for item in report["gates"] if item["name"] == "approval_plan_digest_target"
    )
    gate["passed"] = False
    identity = {key: value for key, value in report.items() if key != "report_digest"}
    report["report_digest"] = content_digest(identity)
    result = evaluate_report(profile, report, source_file_sha256=digest)
    control = next(item for item in result["controls"] if item["id"] == "AUT-02")
    assert control["declared_state"] == "partial"
    assert control["effective_state"] == "gap"


def test_rejects_tampered_report_content() -> None:
    profile = load_profile(ROOT / "profile" / "assureops.yaml")
    report, digest = source_report()
    report["runs"][0]["observation"]["decision"] = "tampered"

    with pytest.raises(EvaluationArtifactError, match="report_digest does not match"):
        evaluate_report(profile, report, source_file_sha256=digest)


def test_rejects_tampered_observation_digest_even_with_resigned_report() -> None:
    profile = load_profile(ROOT / "profile" / "assureops.yaml")
    report, digest = source_report()
    report = copy.deepcopy(report)
    report["runs"][0]["observation_digest"] = "b" * 64
    identity = {key: value for key, value in report.items() if key != "report_digest"}
    report["report_digest"] = content_digest(identity)

    with pytest.raises(EvaluationArtifactError, match="observation_digest does not match"):
        evaluate_report(profile, report, source_file_sha256=digest)
