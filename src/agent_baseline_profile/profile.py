"""Load and validate the machine-readable control profile."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

EXPECTED_OUTCOMES = {"DIS", "CON", "AUT", "OBS", "VAL", "RES"}
EXPECTED_STATES = {"evidenced", "partial", "gap", "not_assessed"}
EXPECTED_CONTROL_IDS = tuple(
    [f"DIS-{number:02d}" for number in range(1, 8)]
    + [f"CON-{number:02d}" for number in range(1, 5)]
    + [f"AUT-{number:02d}" for number in range(1, 10)]
    + [f"OBS-{number:02d}" for number in range(1, 7)]
    + [f"VAL-{number:02d}" for number in range(1, 5)]
    + [f"RES-{number:02d}" for number in range(1, 6)]
)


class ProfileError(ValueError):
    """Raised when the profile contract is internally inconsistent."""


def load_profile(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ProfileError("profile root must be a mapping")
    controls = payload.get("controls")
    if not isinstance(controls, list) or len(controls) != 35:
        raise ProfileError("profile must contain exactly 35 controls")

    ids: list[str] = []
    for control in controls:
        if not isinstance(control, dict):
            raise ProfileError("each control must be a mapping")
        control_id = control.get("id")
        outcome = control.get("outcome")
        state = control.get("state")
        if not isinstance(control_id, str) or not control_id.startswith(f"{outcome}-"):
            raise ProfileError(f"invalid control identity: {control_id!r}")
        if outcome not in EXPECTED_OUTCOMES:
            raise ProfileError(f"unknown outcome for {control_id}: {outcome!r}")
        if state not in EXPECTED_STATES:
            raise ProfileError(f"unknown state for {control_id}: {state!r}")
        method = control.get("method")
        if state in {"evidenced", "partial"} and not isinstance(method, str):
            raise ProfileError(f"{control_id} requires an executable method")
        if state in {"gap", "not_assessed"} and method is not None:
            raise ProfileError(f"{control_id} must not claim a method for state {state}")
        ids.append(control_id)

    if len(ids) != len(set(ids)):
        raise ProfileError("control identifiers must be unique")
    if tuple(ids) != EXPECTED_CONTROL_IDS:
        raise ProfileError("control identifiers must match the complete ordered catalogue")
    return payload
