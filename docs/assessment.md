# AssureOps Agent Baseline Evidence Assessment

> Scoped implementation evidence only. This is not certification and does
> not assert complete Agent Baseline conformance.

## Pinned inputs

- Agent Baseline: `1.0-draft` at `8954684dd3221ae0613a55dabfc1b6bc10d23705`
- AssureOps: `73a6aa0bb28ea8e475d2d0db16bdb5845dc99ae3` / tag `all-things-agentic-2026-submission`
- Evaluation protocol: `assureops-evaluation-v1`
- Source report digest: `b84c5dfb631a28d440345051decc09c69214bfa4f7a9ba07e6e3fa4c8349a8e4`
- Profile report digest: `2f79fa6839746a72eb765ba65c231fa843435a2055e0e2e9217605592831a914`

## Summary

| Controls | Executable methods | Evidenced | Partial | Gap | Not assessed |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 35 | 12 | 5 | 7 | 0 | 23 |

`Evidenced` applies only to the synthetic AssureOps scope and pinned version.

## Control assessment

| Control | Outcome | State | Executable method | Rationale |
| --- | --- | --- | --- | --- |
| DIS-01 | DIS | not_assessed | `—` | The portable evaluation artifact does not expose an authoritative deployment registry. |
| DIS-02 | DIS | not_assessed | `—` | Ownership and risk classification are outside the current artifact. |
| DIS-03 | DIS | not_assessed | `—` | Historical operating and exception status are not tested by this profile. |
| DIS-04 | DIS | not_assessed | `—` | Model, skill, plugin, MCP, and tool inventory is not present in the evaluation report. |
| DIS-05 | DIS | not_assessed | `—` | Runtime-resolved component composition is not present in the evaluation report. |
| DIS-06 | DIS | not_assessed | `—` | Effective identities, credentials, and data access are not tested by this profile. |
| DIS-07 | DIS | not_assessed | `—` | No discovery-to-registry reconciliation artifact is available. |
| CON-01 | CON | partial | `assureops.admission_exact_release` | Exact target and stale evidence are rejected, but deployment admission is not exercised. |
| CON-02 | CON | not_assessed | `—` | Capability-combination analysis is not in the portable evaluation artifact. |
| CON-03 | CON | not_assessed | `—` | Container and runtime confinement require deployment evidence outside this profile. |
| CON-04 | CON | not_assessed | `—` | Versioned runtime capability profiles are not exercised by this artifact. |
| AUT-01 | AUT | partial | `assureops.minimum_action_attribution` | Plan, target, action, result, and trace are present; initiating principal and deployment identity are absent. |
| AUT-02 | AUT | evidenced | `assureops.authority_binding` | Wrong plan, digest, revision, target, expiry, and action are deterministically denied. |
| AUT-03 | AUT | not_assessed | `—` | The evaluated slice has no downstream-agent delegation chain. |
| AUT-04 | AUT | not_assessed | `—` | Credential issuance and model-context exclusion require runtime identity evidence. |
| AUT-05 | AUT | evidenced | `assureops.independent_approval` | Only the exact approved plan can execute; missing or rejected review is denied. |
| AUT-06 | AUT | evidenced | `assureops.fail_closed` | Unverifiable evidence, approval, target, or action never produces false-ready or unauthorized effects. |
| AUT-07 | AUT | not_assessed | `—` | Re-authentication and stronger-factor behavior are not part of the synthetic slice. |
| AUT-08 | AUT | not_assessed | `—` | Temporary authority elevation is intentionally absent from the evaluated slice. |
| AUT-09 | AUT | not_assessed | `—` | Sender-constrained credentials require identity-provider integration evidence. |
| OBS-01 | OBS | partial | `assureops.telemetry_minimum` | Scenario, policy result, target, action, and trace data exist, but the full identity/model/tool composition is absent. |
| OBS-02 | OBS | partial | `assureops.trace_correlation` | Stable per-scenario traces and digests exist; cross-system MCP/tool/target correlation is not proven. |
| OBS-03 | OBS | not_assessed | `—` | No runtime behavioral baseline or drift detector is evaluated. |
| OBS-04 | OBS | not_assessed | `—` | The suite blocks unauthorized effects but does not monitor technically permitted harmful actions. |
| OBS-05 | OBS | partial | `assureops.intent_to_outcome` | Approval, plan digest, action, result, and target are linked; business intent and identity are not complete. |
| OBS-06 | OBS | partial | `assureops.evidence_integrity` | Canonical digests and deterministic replay are evidenced; access, retention, encryption, and legal hold are not. |
| VAL-01 | VAL | evidenced | `assureops.agent_security_testing` | Twenty-seven adversarial scenarios run twice with hard failure thresholds and deterministic replay. |
| VAL-02 | VAL | not_assessed | `—` | Component-level release evidence is not represented in the portable report. |
| VAL-03 | VAL | not_assessed | `—` | Equivalent security, quality, and license checks for generated artifacts are not tested here. |
| VAL-04 | VAL | evidenced | `assureops.outcome_validation` | Positive, negative, missing, stale, and unknown outcomes are independently classified before readiness. |
| RES-01 | RES | not_assessed | `—` | Stop and credential revocation response time are not exercised. |
| RES-02 | RES | not_assessed | `—` | Version, model, tool, skill, and MCP quarantine are not exercised. |
| RES-03 | RES | not_assessed | `—` | Incident impact scoping and preservation workflows are outside this artifact. |
| RES-04 | RES | partial | `assureops.safe_failure_fallback` | Unverified high-impact actions fail closed and model failure has a deterministic fallback; an approved non-agent continuity workflow is not proven. |
| RES-05 | RES | not_assessed | `—` | Pinned source identity exists, but runtime rejection of unapproved component changes is not exercised. |

## Executable evidence

### CON-01 — Admission enforcement

- State: `partial`
- Method: `assureops.admission_exact_release`
- Checks: `4/4` passed

### AUT-01 — Distinct identity and action attribution

- State: `partial`
- Method: `assureops.minimum_action_attribution`
- Checks: `1/1` passed

### AUT-02 — Purpose and task-bound authority

- State: `evidenced`
- Method: `assureops.authority_binding`
- Checks: `8/8` passed

### AUT-05 — Independent approval

- State: `evidenced`
- Method: `assureops.independent_approval`
- Checks: `3/3` passed

### AUT-06 — Fail-closed authorization and circuit breaking

- State: `evidenced`
- Method: `assureops.fail_closed`
- Checks: `13/13` passed

### OBS-01 — Agent-native telemetry

- State: `partial`
- Method: `assureops.telemetry_minimum`
- Checks: `1/1` passed

### OBS-02 — End-to-end correlation

- State: `partial`
- Method: `assureops.trace_correlation`
- Checks: `1/1` passed

### OBS-05 — Intent-to-outcome evidence

- State: `partial`
- Method: `assureops.intent_to_outcome`
- Checks: `1/1` passed

### OBS-06 — Evidence integrity, completeness and protection

- State: `partial`
- Method: `assureops.evidence_integrity`
- Checks: `3/3` passed

### VAL-01 — Agent-specific security testing

- State: `evidenced`
- Method: `assureops.agent_security_testing`
- Checks: `6/6` passed

### VAL-04 — Agent outcome validation

- State: `evidenced`
- Method: `assureops.outcome_validation`
- Checks: `6/6` passed

### RES-04 — Safe failure and non-agent fallback

- State: `partial`
- Method: `assureops.safe_failure_fallback`
- Checks: `4/4` passed
