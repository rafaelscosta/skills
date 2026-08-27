# Clarify v1.1 — Visual Semantic Compiler Integration Eval

This suite verifies the integration boundary between Clarify and `visual-semantic-compiler` without turning deterministic fixtures into a behavioral-model claim.

## What is already proven

The checked-in refund-policy fixture exercises a source-bound operational flow with:

- a compound eligibility rule;
- yes/no branches;
- a post-decision timing fact that should remain text-only;
- an incomplete-data recovery loop that returns to analysis.

The integration smoke proves that the contracts can carry those invariants through:

```text
source
→ Clarify invariant lock
→ invariant coverage
→ Visual Semantic IR
→ semantic validation
→ deterministic flow layout
→ HTML + inline SVG
→ browser evidence
→ perceptual review
```

See `../../VALIDATION_VISUAL_INTEGRATION.md` for the dated implementation evidence.

## What is not yet proven

The implementation session authored the integration and observed the pilot. It is therefore not valid evidence for a blind behavioral comparison of model behavior before versus after the integration.

The correct status is:

```text
DETERMINISTIC INTEGRATION: PASSED
FRESH-CONTEXT BEHAVIORAL A/B: PENDING
BLIND A/B HARNESS: READY
```

## Behavioral A/B certification

The executable blind protocol now lives in:

`certification/README.md`

It replaces ad-hoc control/treatment comparison with:

```text
frozen control generator
+ separate frozen treatment generator
→ immutable outputs
→ candidate A/B blinding
→ separate blind Judge
→ sealed pre-unblind judgment
→ deterministic post-unblind promotion scorer
```

Key protections:

- control pinned to the pre-integration commit;
- treatment pinned to Clarify v1.1 + VSC v1.2.1;
- generator-safe `inputs.yaml` contains no critical invariants or judge dimensions;
- `oracle.yaml` is judge-only;
- `seal_pair.py` removes condition/version/commit identity from Judge receipts;
- `private/condition-map.json` is withheld until judgment is sealed;
- `score_ab.py` enforces the promotion policy after unblinding.

`ab-cases.yaml` remains the original development specification and is **not generator-safe** because it contains critical invariants and judge dimensions.

## Primary outcome

The treatment earns promotion only if it improves or preserves all of:

1. source-fidelity / invariant retention;
2. visual notation fit;
3. operational rule visibility;
4. failure/recovery visibility;
5. text-equivalent completeness;
6. artifact integrity;
7. perceptual usability;

without unacceptable regression in execution cost or routing precision.

## Acceptance rule

Do not claim `CLARIFY VERIFIED VISUAL INTEGRATION: BEHAVIORALLY SUPERIOR` from the deterministic fixture alone.

That claim is permitted only when the fresh-context blind run completes and `certification/score_ab.py` returns a passing promotion receipt.
