# Concept Bridge v3.1 — Blind Visual Behavioral Certification

This directory turns the v3.1 visual-reasoning specification into a **blind Generator → sealed Judge certification** that can be run in native ChatGPT or Codex sessions without an API harness.

## Why this exists

`../visual-cases.yaml` is a useful human-readable development specification, but it contains prompts and expected behavior together. It is therefore **not generator-safe evidence** for behavioral certification.

The certification firewall separates:

```text
GENERATOR SURFACE                 JUDGE-ONLY SURFACE
SKILL.md                          oracle.yaml
visual-router.md                  evals/rubric.yaml
diagram-contract.md               immutable predictions
inputs.yaml                       immutable rendered artifacts
or render-inputs.yaml             judge.md
generator.md
```

The generator must never see the right-hand oracle surface before its outputs are sealed.

## Files

- `inputs.yaml` — 15 blind routing prompts; no expectations.
- `render-inputs.yaml` — 6 representative blind render prompts.
- `oracle.yaml` — sealed expected routes and case requirements; judge only.
- `generator.md` — isolated generator protocol.
- `judge.md` — sealed judge protocol and gates.
- `../../scripts/validate_visual_certification.py` — zero-dependency structural firewall validator.

## Certification stages

### Stage 0 — Validate the firewall

From the `concept-bridge` directory:

```bash
python3 scripts/validate_visual_certification.py
```

This validates that:

- blind inputs contain no `expected_route`, `must`, or `must_not` fields;
- every blind input ID has exactly one oracle entry;
- the oracle does not contain extra/missing cases;
- render-pilot IDs are a subset of blind route IDs;
- certification protocol files are present.

A structural pass does **not** certify model behavior. It only proves the eval packaging is not trivially leaking its oracle.

### Stage 1 — Blind Route Suite

Create a fresh native model context containing only:

- `SKILL.md`;
- `references/visual-router.md`;
- `references/diagram-contract.md`;
- `evals/visual-certification/generator.md`;
- `evals/visual-certification/inputs.yaml`.

Do not give the session repository access if that access would allow it to inspect the oracle or development evals.

Run the generator protocol and preserve the result as:

```text
route-predictions.yaml
```

Preferred evidence: one fresh context per case.

Accepted lower-cost evidence: one blind batch with no feedback between cases and immutable per-case outputs. Label that run `blind_batch`.

### Stage 2 — Blind Render Pilot

Use a fresh blind generator context with the same skill/reference surface but replace `inputs.yaml` with `render-inputs.yaml`.

Generate the six representative real artifacts and preserve:

```text
render-receipts.yaml
artifacts/
  <case artifacts>
```

The pilot intentionally covers:

1. story strip;
2. architecture diagram;
3. state diagram;
4. mixed narrative + structural composition;
5. crossing-edge/layout pressure;
6. HTML with embedded inline-SVG preference.

### Stage 3 — Seal evidence

Before the judge sees the run, make predictions and artifacts immutable for evaluation purposes.

At minimum record SHA-256 hashes for text outputs and every artifact file when the surface supports files:

```bash
shasum -a 256 route-predictions.yaml render-receipts.yaml artifacts/*
```

Store the hashes with the run metadata.

No generator output may be changed after oracle exposure.

### Stage 4 — Sealed Judge

Create a separate judge context containing:

- `judge.md`;
- `oracle.yaml`;
- `../rubric.yaml`;
- `../../references/visual-router.md`;
- `../../references/diagram-contract.md`;
- immutable generator outputs;
- immutable rendered artifacts;
- hashes/run metadata.

The judge scores without regenerating or repairing anything.

Write:

```text
certification-report.md
```

## Gates

### Route Gate

Requires **15/15** semantically correct routes, correct representation classes and structural archetypes, zero `must_not` violations, zero rubric automatic failures, and no oracle leakage.

### Render Gate

Requires **6/6** rendered cases to pass the visual scoring contract in `judge.md`, including perfect scores for representation fit, semantic fidelity, and artifact integrity.

### Overall

Only a run with both gates passing may claim:

```text
CONCEPT-BRIDGE v3.1 VISUAL BEHAVIOR: CERTIFIED
```

Until such a sealed report exists, the correct status is:

```text
CERTIFICATION HARNESS READY — BEHAVIORAL CERTIFICATION PENDING
```

## Run storage

Persist completed evidence under a dated immutable run directory, for example:

```text
evals/visual-certification/runs/2026-08-26-gpt-5.6/
├── run-metadata.yaml
├── route-predictions.yaml
├── render-receipts.yaml
├── artifact-hashes.txt
├── artifacts/
└── certification-report.md
```

Do not overwrite prior certification runs. New model versions, skill versions, or material prompt changes require a new run directory.

## Validity boundaries

A passing report proves behavior only for:

- the exact skill version tested;
- the model/product configuration recorded in run metadata;
- the supplied cases and artifacts;
- the stated isolation mode.

It does not prove every possible concept will route perfectly.

Use failures to improve the skill only **after** the run is sealed. Then execute a new blind run rather than editing failed predictions in place.
