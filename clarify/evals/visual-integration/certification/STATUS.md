# Clarify Visual Integration Behavioral A/B — Status

Current status: **PENDING FRESH-CONTEXT RUN**

The deterministic Clarify→Visual Semantic Compiler integration is implemented and the source-bound smoke pilot passed. That does not establish behavioral superiority.

This development session is **ineligible** as control generator, treatment generator, or blind judge because it has seen the integration rationale, case invariants, and promotion rule.

A valid certification requires, in order:

1. fresh isolated control generation from commit `a10b7e80f3dbe29422226aa31758f7c679e829af`;
2. separate fresh isolated treatment generation from commit `78cb5cde584ddc9b022b7b4de91930f1ac76a1b1`;
3. immutable SHA-256 sealing of both conditions;
4. `seal_pair.py` blinding to candidate A/B with the private map withheld;
5. a separate blind Judge that seals `judge-preunblind.json` before mapping is revealed;
6. deterministic post-unblind aggregation with `score_ab.py`;
7. only then, if every promotion gate passes, the claim:

`CLARIFY VERIFIED VISUAL INTEGRATION: BEHAVIORALLY SUPERIOR`

Until that sequence completes successfully, `clarify/config.yaml` must remain `behavioral_ab: pending`.
