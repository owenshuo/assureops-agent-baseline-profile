"""Human-readable rendering of deterministic profile reports."""

from __future__ import annotations

from typing import Any


def render_markdown(report: dict[str, Any]) -> str:
    summary = report["summary"]
    system = report["system_under_test"]
    baseline = report["baseline"]
    lines = [
        "# AssureOps Agent Baseline Evidence Assessment",
        "",
        "> Scoped implementation evidence only. This is not certification and does",
        "> not assert complete Agent Baseline conformance.",
        "",
        "## Pinned inputs",
        "",
        f"- Agent Baseline: `{baseline['version']}` at `{baseline['commit']}`",
        f"- AssureOps: `{system['commit']}` / tag `{system['tag']}`",
        f"- Evaluation protocol: `{system['evaluation_protocol']}`",
        f"- Source report digest: `{report['source_evaluation']['report_digest']}`",
        f"- Profile report digest: `{report['profile_report_digest']}`",
        "",
        "## Summary",
        "",
        "| Controls | Executable methods | Evidenced | Partial | Gap | Not assessed |",
        "| ---: | ---: | ---: | ---: | ---: | ---: |",
        (
            f"| {summary['control_count']} | {summary['executable_method_count']} | "
            f"{summary['evidenced']} | {summary['partial']} | {summary['gap']} | "
            f"{summary['not_assessed']} |"
        ),
        "",
        "`Evidenced` applies only to the synthetic AssureOps scope and pinned version.",
        "",
        "## Control assessment",
        "",
        "| Control | Outcome | State | Executable method | Rationale |",
        "| --- | --- | --- | --- | --- |",
    ]
    for control in report["controls"]:
        method = control["method"] or "—"
        rationale = control["rationale"].replace("|", "\\|")
        lines.append(
            f"| {control['id']} | {control['outcome']} | {control['effective_state']} | "
            f"`{method}` | {rationale} |"
        )

    lines.extend(["", "## Executable evidence", ""])
    for control in report["controls"]:
        if control["method"] is None:
            continue
        passed = sum(check["passed"] for check in control["checks"])
        lines.extend(
            [
                f"### {control['id']} — {control['title']}",
                "",
                f"- State: `{control['effective_state']}`",
                f"- Method: `{control['method']}`",
                f"- Checks: `{passed}/{len(control['checks'])}` passed",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"
