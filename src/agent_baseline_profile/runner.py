"""Evaluate a portable AssureOps report against the scoped profile."""

from __future__ import annotations

from collections import Counter
from typing import Any

from agent_baseline_profile.canonical import content_digest, is_sha256
from agent_baseline_profile.methods import METHODS


class EvaluationArtifactError(ValueError):
    """Raised when the source artifact is malformed or outside the profile contract."""


def _validate_report(report: dict[str, Any], protocol: str) -> None:
    required = {
        "protocol_version",
        "target",
        "repeats",
        "passed",
        "metrics",
        "gates",
        "runs",
        "report_digest",
    }
    missing = required - set(report)
    if missing:
        raise EvaluationArtifactError(f"evaluation report missing: {sorted(missing)}")
    if report["protocol_version"] != protocol:
        raise EvaluationArtifactError(
            f"expected protocol {protocol}, got {report['protocol_version']}"
        )
    if not is_sha256(report["report_digest"]):
        raise EvaluationArtifactError("source report_digest must be sha256")

    report_identity = {key: report[key] for key in required if key != "report_digest"}
    expected_report_digest = content_digest(report_identity)
    if report["report_digest"] != expected_report_digest:
        raise EvaluationArtifactError("source report_digest does not match report content")

    seen_runs: set[tuple[object, object]] = set()
    for run in report["runs"]:
        identity = (run.get("scenario_id"), run.get("repetition"))
        if identity in seen_runs:
            raise EvaluationArtifactError(f"duplicate source run identity: {identity!r}")
        seen_runs.add(identity)
        observation_digest = run.get("observation_digest")
        if not is_sha256(observation_digest):
            raise EvaluationArtifactError("source observation_digest must be sha256")
        if observation_digest != content_digest(run.get("observation")):
            raise EvaluationArtifactError(
                f"observation_digest does not match content for {identity!r}"
            )

    metrics = report["metrics"]
    if metrics.get("run_count") != len(report["runs"]):
        raise EvaluationArtifactError("source run_count does not match runs")
    scenario_count = len({run.get("scenario_id") for run in report["runs"]})
    if metrics.get("scenario_count") != scenario_count:
        raise EvaluationArtifactError("source scenario_count does not match runs")


def evaluate_report(
    profile: dict[str, Any],
    source_report: dict[str, Any],
    *,
    source_file_sha256: str,
) -> dict[str, Any]:
    """Return a deterministic, digest-bound control assessment."""

    protocol = profile["system_under_test"]["evaluation_protocol"]
    _validate_report(source_report, protocol)
    controls: list[dict[str, Any]] = []

    for control in profile["controls"]:
        declared_state = control["state"]
        method_name = control.get("method")
        checks: list[dict[str, Any]] = []
        effective_state = declared_state
        if method_name is not None:
            method = METHODS.get(method_name)
            if method is None:
                raise EvaluationArtifactError(f"unknown method: {method_name}")
            checks = method(source_report)
            if not checks or not all(check["passed"] for check in checks):
                effective_state = "gap"

        controls.append(
            {
                "id": control["id"],
                "outcome": control["outcome"],
                "title": control["title"],
                "declared_state": declared_state,
                "effective_state": effective_state,
                "method": method_name,
                "rationale": control["rationale"],
                "checks": checks,
            }
        )

    counts = Counter(control["effective_state"] for control in controls)
    body = {
        "profile": profile["profile"],
        "baseline": profile["baseline"],
        "system_under_test": profile["system_under_test"],
        "source_evaluation": {
            "protocol_version": source_report["protocol_version"],
            "target": source_report["target"],
            "report_digest": source_report["report_digest"],
            "file_sha256": source_file_sha256,
            "passed": source_report["passed"],
            "scenario_count": source_report["metrics"]["scenario_count"],
            "run_count": source_report["metrics"]["run_count"],
        },
        "summary": {
            "control_count": len(controls),
            "executable_method_count": sum(control["method"] is not None for control in controls),
            "evidenced": counts["evidenced"],
            "partial": counts["partial"],
            "gap": counts["gap"],
            "not_assessed": counts["not_assessed"],
        },
        "controls": controls,
    }
    return {**body, "profile_report_digest": content_digest(body)}
