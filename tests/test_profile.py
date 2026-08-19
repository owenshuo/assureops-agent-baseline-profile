from __future__ import annotations

from pathlib import Path

from agent_baseline_profile.methods import METHODS
from agent_baseline_profile.profile import EXPECTED_CONTROL_IDS, load_profile

ROOT = Path(__file__).resolve().parents[1]


def test_profile_has_all_35_unique_controls_and_six_outcomes() -> None:
    profile = load_profile(ROOT / "profile" / "assureops.yaml")
    controls = profile["controls"]
    assert len(controls) == 35
    assert len({control["id"] for control in controls}) == 35
    assert tuple(control["id"] for control in controls) == EXPECTED_CONTROL_IDS
    assert {control["outcome"] for control in controls} == {
        "DIS",
        "CON",
        "AUT",
        "OBS",
        "VAL",
        "RES",
    }


def test_every_claimed_method_exists_and_exactly_10_are_executable() -> None:
    profile = load_profile(ROOT / "profile" / "assureops.yaml")
    methods = [control["method"] for control in profile["controls"] if "method" in control]
    assert len(methods) == 10
    assert set(methods) <= set(METHODS)
