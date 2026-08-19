# Draft test method: exact and independent approval binding

Status: implementation-backed local review draft; not submitted.

Primary control: `AUT-05` Independent approval.

Related controls: `AUT-02` Purpose and task-bound authority and `AUT-06`
Fail-closed authorization and circuit breaking.

## Problem

The existence of an approval record does not prove that the specific action was
independently authorized. A verifier must establish that the decision came from
an authenticated principal or deterministic decision point independent of the
requesting agent, and that it binds the exact action inputs. Any material change
must invalidate the decision before a side effect occurs.

## Proposed test method

Construct one action request whose identity includes:

- requesting agent and initiating principal or approved autonomous purpose;
- plan identifier and content revision;
- canonical plan digest;
- target resource and target version;
- requested action and parameter digest;
- approval conditions and validity period;
- authenticated reviewer or independent deterministic decision point.

Confirm that the unchanged, approved request may cross the authorization
boundary. Then repeat the decision after independently changing each bound
field, removing the approval, rejecting it, expiring it, and presenting a
reviewer identity that is unauthenticated or not independent of the requester.

Expected result: every invalid variant is denied before side effects. Each
denial identifies the failed binding or independence condition and remains
correlated to the original request and policy decision.

## Evidence produced

- stable test, request, run, agent, and initiating-principal identifiers;
- canonical plan and parameter digests;
- target resource, target version, requested action, and executed action;
- authenticated reviewer identity or decision-point identity;
- evidence that the reviewer or decision point is independent of the requester;
- decision time, validity period, policy decision, and denial reason;
- externally observed side-effect count;
- digest of the complete test report.

## Submission discipline

1. Open an issue against `AUT-05` before proposing a pull request.
2. Keep the method vendor-neutral; link implementation evidence separately.
3. Disclose the contributor's name and affiliation as required upstream.
4. Do not claim certification or complete Agent Baseline conformance.
5. Implementation prerequisite satisfied by AssureOps tag
   `agent-baseline-aut05-v2`: the application-API evaluation proves a
   Google-OIDC-mapped reviewer, requester-reviewer independence, exact
   plan/action binding, and zero side effects for forged, self, and
   unprivileged review attempts. Upstream submission still requires separate
   human review and authorization.
