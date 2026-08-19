# Draft: test method for action-specific approval and evidence binding

Status: local draft; not submitted.

Target Agent Baseline controls:

- AUT-02 Purpose and task-bound authority
- AUT-05 Independent approval
- AUT-06 Fail-closed authorization and circuit breaking
- OBS-05 Intent-to-outcome evidence
- VAL-04 Agent outcome validation

## Problem

An approval record can exist and still be unsafe to reuse. A verifier must be
able to show that the approval applies to the exact proposed action, content
revision, target resource, target version, validity period, and approved
authority. A material change to any binding input must invalidate the approval.

Likewise, successful execution is not evidence that the intended business
outcome was achieved. Outcome evidence must bind to the same target version and
must be generated or independently verified after the authorized action.

## Proposed test method

For a consequential action, construct one valid plan and approval, then replay
the authorization decision after independently changing each field:

1. plan identifier;
2. content revision;
3. canonical plan digest;
4. target resource;
5. target version;
6. validity period;
7. requested action outside the allow-list.

Expected result: the unchanged plan may cross the authorization boundary once;
every changed or expired variant is denied before side effects, and the denial
is correlated to the original request and policy decision. A successful action
does not become `ready` until independently verified, exact-version outcome
evidence satisfies the required proof obligations.

## Evidence produced

- stable test and run identifier;
- canonical plan digest and target version;
- approval identity, decision, validity period, and bound digest;
- requested versus executed action;
- authorization decision and denial reason;
- side-effect count;
- post-action evidence subject and target version;
- final outcome decision;
- digest of the complete test report.

## Demonstration

The accompanying AssureOps profile exercises the method with synthetic data.
The source system and Agent Baseline catalogue are pinned by Git commit, the
source evaluation is repeatable, and the resulting profile report is
content-addressed. The profile deliberately reports partial coverage where
identity, deployment composition, credentialing, retention, or response
controls are outside the evidence artifact.
