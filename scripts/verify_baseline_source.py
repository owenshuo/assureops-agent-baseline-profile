"""Verify the exact external Agent Baseline catalogue used by this profile."""

# ruff: noqa: E402, I001

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from agent_baseline_profile.baseline import verify_baseline_source
from agent_baseline_profile.profile import load_profile


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--baseline-repo", type=Path, required=True)
    parser.add_argument(
        "--profile",
        type=Path,
        default=ROOT / "profile" / "assureops.yaml",
    )
    args = parser.parse_args()
    profile = load_profile(args.profile.resolve())
    result = verify_baseline_source(args.baseline_repo.resolve(), profile)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
