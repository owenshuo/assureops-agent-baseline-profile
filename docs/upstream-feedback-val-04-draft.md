# Draft test method: post-action business outcome validation

Status: design gap; not ready for upstream submission.

Primary control: `VAL-04` Agent outcome validation.

Related control: `OBS-05` Intent-to-outcome evidence.

## Problem

Successful tool execution is not proof that the intended business outcome was
achieved. A completed action can return success while changing the wrong target,
producing an invalid state, or satisfying an old version of the requirement.

## Proposed test method

For one consequential action, define the expected business outcome and its
target version before authorization. Execute the exact approved action, then
collect outcome evidence from a source independent of the requesting agent and
the executor. Verify that the evidence was produced after the action, binds to
the same target and version, and satisfies the stated outcome criteria.

Exercise at least these variants:

1. exact post-action outcome passes;
2. action succeeds but the business outcome fails;
3. outcome evidence is missing or unverifiable;
4. outcome evidence belongs to another target or version;
5. outcome evidence predates the action;
6. a high-impact proposed outcome fails pre-finalization validation.

Expected result: only the exact, independently verified outcome may satisfy the
business objective. Every other variant remains incomplete or not ready without
inventing evidence or treating tool success as outcome success.

## Evidence produced

- business intent and expected outcome identifier;
- action, approval, target, and target-version bindings;
- execution receipt and completion time;
- outcome evidence source, observation time, subject, version, and digest;
- validation method and result;
- final business decision and reason;
- correlation identifier joining intent, action, evidence, and decision.

## Readiness gap

The current portable AssureOps evaluation validates evidence-state decisions,
but it does not run a post-action business-outcome scenario. This draft must
remain unsubmitted until such a scenario and an independent outcome source are
implemented and reproducible.
