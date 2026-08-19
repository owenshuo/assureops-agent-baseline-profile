# AssureOps Agent Baseline Evidence Profile

This repository evaluates a pinned AssureOps release against selected controls
from Agent Baseline `v1.0-draft`. It is deliberately separate from both the
AssureOps submission repository and the production Quality Ontology Platform.

The project does four things:

1. catalogues all 35 Agent Baseline controls without claiming certification;
2. records an explicit `evidenced`, `partial`, `gap`, or `not_assessed` state;
3. runs 10 scoped test methods against AssureOps' public evaluation artifact;
4. emits a deterministic, digest-bound evidence report suitable for review.

It does **not** modify AssureOps, copy private product code, publish internal
data, or treat a passing scoped test as full Agent Baseline conformance.

## Pinned inputs

- Agent Baseline repository commit:
  `8954684dd3221ae0613a55dabfc1b6bc10d23705`
- Agent Baseline controls SHA-256:
  `23864515ef28e54522977ed630265a98b638216d3618ecb6c319a21ed9242666`
- AssureOps repository commit:
  `73a6aa0bb28ea8e475d2d0db16bdb5845dc99ae3`
- AssureOps immutable tag: `all-things-agentic-2026-submission`

These values live in `profile/assureops.yaml` and are enforced by the runner.

## Install

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
```

The unit tests use the committed portable evaluation fixture and do not need a
live AssureOps checkout:

```powershell
.venv\Scripts\ruff check .
.venv\Scripts\python -m pytest
```

## Reproduce the integration evidence

Clone the two external inputs beside this repository, then check out the exact
versions listed under **Pinned inputs**. The commands below assume the sibling
directories are named `assureops-agent` and `agentbaseline`.

From this repository on the current workspace:

```powershell
.venv\Scripts\python scripts/run_profile.py `
  --assureops-repo ..\assureops-agent `
  --output evidence\assureops-agent-baseline.json `
  --markdown-output docs\assessment.md
```

The runner:

- refuses a dirty or unexpected AssureOps checkout;
- executes `scripts/run_evaluation.py` into a temporary directory;
- prevents Python bytecode writes in the AssureOps checkout;
- validates the report protocol, gates, scenarios, digests, and replay stability;
- writes only the requested report in this repository.

Verify that the local Agent Baseline source is the exact pinned catalogue:

```powershell
.venv\Scripts\python scripts/verify_baseline_source.py `
  --baseline-repo ..\agentbaseline
```

The committed JSON and Markdown are reference results from the pinned release.
Re-running the profile must reproduce the same `profile_report_digest`.

## State meanings

| State | Meaning |
| --- | --- |
| `evidenced` | Every requirement of the control is supported by executable evidence for the stated scope. |
| `partial` | Some required behavior is evidenced, but the complete control is not. |
| `gap` | The profile looked for required evidence and did not find it. |
| `not_assessed` | This profile does not yet test the control; absence is not inferred. |

## Repository boundary

```text
Agent Baseline controls (pinned external source)
               |
               v
this profile -> temporary black-box AssureOps evaluation -> deterministic report

ontology_refactor: not imported, not executed, not modified
assureops_agent:   executed at an immutable commit, not modified
```

## Upstream contribution

`docs/upstream-feedback-aut-05-draft.md` contains a review-first, vendor-neutral
proposal for exact approval binding. `docs/upstream-feedback-val-04-draft.md`
records a separate post-action validation method that is not yet ready to
submit because the current profile does not implement it. Nothing is submitted
to Agent Baseline without separate review and authorization.
