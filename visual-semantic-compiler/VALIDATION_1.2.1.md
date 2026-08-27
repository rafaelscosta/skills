# Visual Semantic Compiler v1.2.1 — Clarify Operational-Flow Hardening

## Why this patch exists

The first source-bound Clarify integration pilot exposed two renderer gaps that the simpler R2 fixtures did not cover:

1. a truthful recovery edge (`solicitar dados → retomar análise`) was treated as an invalid reverse edge / generic DAG geometry;
2. an operationally decisive compound rule did not fit the previous single-line node label.

The patch fixes rendering/validation. It does not weaken or rewrite the semantic IR.

## Changes

### Recovery/back edges

For `flow`, a relation returning to an already-seen earlier step is classified as a layout back-edge and routed on an outer rail.

The layout validator accepts a reverse-direction flow edge only when its polyline proves an explicit outer back-route beyond the normal node envelope. Arbitrary backward arrows remain invalid.

### Multiline operational labels

Long flow-node labels wrap into SVG `<tspan>` lines and flow node height expands accordingly.

This allows a real decision rule such as:

```text
Até 7 dias E sem consumo premium?
```

to remain explicit rather than being shortened to a semantically weaker label such as `Elegível?` solely for layout.

## Regression matrix

Local deterministic regression executed against the integration runtime:

```text
VSC semantic-validator suite:           7/7 PASS
VSC existing R2 layout regression:     13/13 PASS
Clarify recovery-flow renderer tests:   4/4 PASS
Python compile checks:                       PASS
```

The dedicated integration tests prove:

- recovery flow layout passes geometry validation;
- recovery edge uses an outer rail;
- long operational decision expands node height;
- rendered SVG uses multiline `<tspan>` labels.

## Live browser evidence

The final Clarify refund fixture passed live Chromium evidence at:

```text
1440×900
1600×1000
1920×1080
2048×1320
```

with zero browser errors and zero node-text overflow at all four viewports.

Final rendered artifact SHA-256:

```text
759ec48781a26981799aa5811f3d7c461a646b1b602c5e1f04fa60bf8266b3d5
```

The retained screenshots were perceptually reviewed and the hash-bound gate returned `perceptually-passed` with zero defects. Full source-bound integration evidence is recorded in `../clarify/VALIDATION_VISUAL_INTEGRATION.md`.

## Claim boundary

This patch proves the renderer can preserve this class of operational recovery flow and long decision labels without regressing the existing R2 matrix.

It does not claim universal layout optimality, mobile certification, or behavioral superiority of Clarify v1.1. Those remain separate gates.
