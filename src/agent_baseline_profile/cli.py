"""Command-line interface for deterministic profile evaluation."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from agent_baseline_profile.collector import collect_assureops_report
from agent_baseline_profile.profile import load_profile
from agent_baseline_profile.render import render_markdown
from agent_baseline_profile.runner import evaluate_report


def parser() -> argparse.ArgumentParser:
    command = argparse.ArgumentParser(description=__doc__)
    command.add_argument(
        "--profile",
        type=Path,
        default=Path("profile/assureops.yaml"),
        help="machine-readable profile path",
    )
    command.add_argument("--assureops-repo", type=Path, required=True)
    command.add_argument("--assureops-python", type=Path)
    command.add_argument("--output", type=Path, required=True)
    command.add_argument("--markdown-output", type=Path)
    return command


def main() -> int:
    args = parser().parse_args()
    profile = load_profile(args.profile.resolve())
    report, source_sha = collect_assureops_report(
        args.assureops_repo.resolve(),
        profile["system_under_test"],
        python=None if args.assureops_python is None else args.assureops_python.resolve(),
    )
    result = evaluate_report(profile, report, source_file_sha256=source_sha)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    if args.markdown_output is not None:
        args.markdown_output.parent.mkdir(parents=True, exist_ok=True)
        args.markdown_output.write_text(render_markdown(result), encoding="utf-8")
    print(
        "Agent Baseline profile: "
        f"{result['summary']['evidenced']} evidenced, "
        f"{result['summary']['partial']} partial, "
        f"{result['summary']['gap']} gap, "
        f"{result['summary']['not_assessed']} not assessed"
    )
    print(f"report digest: {result['profile_report_digest']}")
    print(f"output: {args.output}")
    if args.markdown_output is not None:
        print(f"markdown: {args.markdown_output}")
    return 0 if result["summary"]["gap"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
