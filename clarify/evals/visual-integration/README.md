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

This implementation session authored the integration and observed the pilot. It is therefore not valid evidence for a blind behavioral comparison of model behavior before versus after the integration.

The correct status is:

```text
DETERMINISTIC INTEGRATION: PASSED
FRESH-CONTEXT BEHAVIORAL A/B: PENDING
```

## Behavioral A/B frontier

Use fresh isolated contexts to compare:

### Control

Clarify without the `visual-delivery.md` / Visual Semantic Compiler handoff.

### Treatment

Clarify v1.1 with source-bound invariant coverage and Visual Semantic Compiler v1.2.1 available.

Both conditions receive the same source material, audience, requested outcome, rendering capability, time/tool budget, and evaluation cases.

Do not expose either condition to expected answers, the opposite condition's output, prior judgments, or integration-development discussions before generation.

## Primary outcome

The treatment earns promotion only if it improves or preserves all of:

1. source-fidelity / invariant retention;
2. visual notation fit;
3. operational rule visibility;
4. failure/recovery visibility;
5. text-equivalent completeness;
6. artifact integrity;
7. perceptual usability;

without unacceptable regression in:

- time/token burden;
- unnecessary visual generation;
- verbosity;
- routing precision.

## Acceptance rule

Do not claim `CLARIFY VERIFIED VISUAL INTEGRATION: BEHAVIORALLY SUPERIOR` from the deterministic fixture alone.

A fresh-context A/B judge must be able to inspect immutable control and treatment outputs and report the denominators, wins/losses/ties, and any regression cluster.
