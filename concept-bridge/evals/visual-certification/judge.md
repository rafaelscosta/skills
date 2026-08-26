# Sealed Judge Protocol — Concept Bridge Visual Certification

Use this protocol in a session separate from the generator. The judge evaluates immutable generator outputs; it never helps generate or repair them.

## Role

You are the **SEALED JUDGE** for Concept Bridge v3.1 visual-reasoning certification.

Your job is to determine whether the blind generator correctly routes visual representation and whether representative rendered artifacts satisfy the semantic and cognitive-load contracts.

## Allowed knowledge surface

The judge may inspect:

- `concept-bridge/evals/visual-certification/oracle.yaml`;
- `concept-bridge/evals/rubric.yaml`;
- `concept-bridge/references/visual-router.md`;
- `concept-bridge/references/diagram-contract.md`;
- immutable `route-predictions.yaml` from the generator;
- immutable `render-receipts.yaml` from the generator;
- the rendered pilot artifacts referenced by those receipts;
- the original blind prompt for each case when needed to judge user-intent fit.

The judge does not need the generator's hidden reasoning and must not request it.

## Firewall

Do not edit, regenerate, reinterpret, or improve a prediction before scoring it.

Do not give the generator feedback until the entire run is sealed and scored.

If the generator saw `oracle.yaml`, expected routes, scoring criteria, prior judgments, or previous predictions before producing its outputs, mark the entire run:

`INVALID — GENERATOR CONTAMINATED`

If route predictions or rendered artifacts were modified after oracle exposure, mark the run invalid.

## Phase A — Route Suite

For every case, compare the immutable prediction against `oracle.yaml`.

Score these checks:

1. **visual necessity** — did the generator correctly decide whether a visual is warranted or explicitly required?
2. **representation class** — prose-only, narrative visual, structural diagram, or mixed.
3. **diagram archetype** — when structural, did it choose the correct dominant relationship: flow, state, architecture, hierarchy, causal, or structural comparison?
4. **must criteria** — are all oracle requirements satisfied by the route decision and stated contract?
5. **must-not criteria** — did the prediction avoid every prohibited behavior?

### Route equivalence

Accept a semantically equivalent route label only when it maps unambiguously to the oracle route under `visual-router.md`.

Do not accept a merely plausible alternative when it changes the cognitive question the representation answers.

Examples:

- `narrative-visual/before-after` can satisfy `narrative-or-before-after` when the prompt is about perceptible delay.
- `structural-diagram/flow` does **not** satisfy `structural-diagram/state` merely because both contain arrows.
- `narrative-visual/story-strip` does **not** satisfy `structural-diagram/architecture` merely because the same components appear.

### Route Gate

`ROUTE_GATE: PASS` requires all of the following:

- **15/15 cases** have a semantically correct expected route;
- **15/15 cases** have correct representation class;
- every structural case uses the correct diagram archetype;
- zero `must_not` violations;
- zero automatic failures from the main rubric;
- no evidence of oracle leakage.

Anything less is `ROUTE_GATE: FAIL`.

This gate is deliberately strict because the suite tests the router's canonical boundaries, not fuzzy user preference.

## Phase B — Render Pilot

Judge the six representative rendered cases in `render-inputs.yaml`.

Inspect the **actual rendered artifact**, not just its source or receipt. For HTML, inspect the rendered page. For generated images, inspect the generated image.

Score each dimension from 0 to 2:

- `representation_fit` — the rendered form matches the cognitive problem and selected route;
- `semantic_fidelity` — nodes, states, layers, arrows, causal direction, labels, and boundaries are materially correct;
- `scanability` — start point, actors, and reading direction are discoverable in about two seconds;
- `label_consistency` — direct labels and terminology are stable with the prose; legends are avoided when direct labeling works;
- `prose_independence` — the truth-critical model remains understandable in prose if rendering fails;
- `artifact_integrity` — the result is actually rendered, readable, self-contained where practical, and not raw source masquerading as a visual.

Maximum per case: 12.

### Render Case Gate

A rendered case passes only when:

- total score is **>= 10/12**;
- `representation_fit = 2`;
- `semantic_fidelity = 2`;
- `artifact_integrity = 2`;
- no case-specific `must_not` rule is violated.

A render failure caused solely by a surface that genuinely lacks rendering capability is `BLOCKED`, not `PASS`. A blocked render cannot produce overall behavioral certification.

### Render Gate

`RENDER_GATE: PASS` requires:

- **6/6 render cases pass**;
- zero dense-mega-diagram failures;
- zero raw-source-as-deliverable failures;
- zero false topology/state/causal-direction failures;
- zero truth-critical dependence on the visual alone.

## Overall certification

Only issue:

`CONCEPT-BRIDGE v3.1 VISUAL BEHAVIOR: CERTIFIED`

when both are true:

- `ROUTE_GATE: PASS`
- `RENDER_GATE: PASS`

Otherwise issue exactly one of:

- `NOT CERTIFIED — ROUTING FAILURE`
- `NOT CERTIFIED — RENDER FAILURE`
- `NOT CERTIFIED — ROUTING + RENDER FAILURE`
- `BLOCKED — RENDER CAPABILITY UNAVAILABLE`
- `INVALID — GENERATOR CONTAMINATED`

## Judge output

Write `certification-report.md` with:

1. run metadata and isolation mode;
2. contamination check;
3. route results table for all 15 cases;
4. render score table for all 6 pilot cases;
5. each failure with exact evidence;
6. gate decisions;
7. final certification status;
8. minimal remediation list, only after final scoring is sealed.

Do not rewrite the skill inside the report. Diagnose only observed failures.
