# Contributing

This repository is a scoped evidence profile, not a certification authority.
Contributions must keep that boundary explicit.

Before opening a change:

1. preserve the complete, ordered Agent Baseline control catalogue;
2. pin upstream source changes by commit and `controls.yaml` SHA-256;
3. add executable tests for every new evidence method;
4. distinguish `partial` from `evidenced` conservatively;
5. do not add private product code, credentials, internal addresses, or customer data;
6. run `ruff check .` and `pytest`.

Changes to a control state or rationale should explain the evidence boundary in
the pull request. Upstream feedback remains a separate, review-first action.
