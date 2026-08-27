# Clarify Visual Integration — Blind Behavioral A/B Certification

This directory turns the visual-integration A/B from a development specification into an executable, contamination-resistant certification protocol.

## Goal

Test whether **Clarify v1.1 + Visual Semantic Compiler v1.2.1** is behaviorally better than the frozen pre-integration Clarify control under matched prompts, model, rendering capability, and tool budget.

The harness separates four roles:

```text
CONTROL GENERATOR
      ↓
sealed control bytes

TREATMENT GENERATOR
      ↓
sealed treatment bytes

PAIR SEALER
      ↓
candidate A / candidate B
      ↓
BLIND JUDGE
      ↓
sealed pre-unblind judgment
      ↓
POST-UNBLIND SCORER
      ↓
promotion pass / not proven
```

## Files

### Generator-safe

- `inputs.yaml` — prompts and source only; no invariants, scores, expected routes, or promotion criteria.
- `baselines.yaml` — exact frozen commits for control and treatment. A generator may be given only the baseline relevant to its own condition.
- `control-generator.md` — isolated control protocol.
- `treatment-generator.md` — isolated treatment protocol.
- `run-metadata.template.json` — run metadata shape.

### Controller-only

- `seal_pair.py` — blinds the two sealed condition outputs as candidate A/B.
- `private/condition-map.json` — generated per run; never give this to the Judge.

### Judge-only

- `oracle.yaml` — critical invariants, dimensions, and automatic failures.
- `judge.md` — blind Judge procedure.

### Post-judge

- `promotion-policy.json` — deterministic promotion gates.
- `score_ab.py` — reveals mapping only after judgment is sealed and computes the permitted claim.

### Harness integrity

- `validate_harness.py` — checks case parity, oracle leakage, baseline separation, and promotion-policy invariants.
- `STATUS.md` — current certification status.

`../ab-cases.yaml` is retained as the original development specification but is **judge-only / non-generator-safe** because it contains critical invariants and judge dimensions.

## Required isolation

A valid run uses at least three fresh contexts:

```text
Session/Context C — control generator
Session/Context T — treatment generator
Session/Context J — blind judge
```

The Controller/sealer may be a deterministic Codex/script surface that does not generate case answers.

The implementation conversation that created this harness is not eligible for any of C, T, or J.

## Control baseline

Control is pinned to:

`a10b7e80f3dbe29422226aa31758f7c679e829af`

This is the pre-integration Clarify baseline. Do not approximate control by disabling a few v1.1 instructions on current `main`; use the frozen checkout or exact materialized bytes.

## Treatment baseline

Treatment is pinned to:

`78cb5cde584ddc9b022b7b4de91930f1ac76a1b1`

This contains Clarify v1.1.0 plus Visual Semantic Compiler v1.2.1.

## Run sequence

### 1. Validate the harness

```bash
python3 validate_harness.py --json
```

Must pass before generation.

### 2. Generate control

Use a fresh context following `control-generator.md`. Do not expose treatment or oracle material.

### 3. Generate treatment

Use a different fresh context following `treatment-generator.md`. Do not expose control or oracle material.

### 4. Seal each condition

Each generator writes SHA-256 hashes and immutable case outputs before the other condition is visible.

### 5. Blind the pair

```bash
python3 seal_pair.py \
  runs/<RUN_ID>/control \
  runs/<RUN_ID>/treatment \
  runs/<RUN_ID>/sealed \
  --seed '<private-random-seed>'
```

Give the Judge only:

- `runs/<RUN_ID>/sealed/blinded/`;
- `inputs.yaml`;
- `oracle.yaml`;
- `judge.md`.

Do **not** give the Judge `sealed/private/condition-map.json`.

### 6. Blind judgment

The Judge creates and hashes `judge-preunblind.json` before mapping is revealed.

### 7. Post-unblind scoring

Only after the judgment is immutable:

```bash
python3 score_ab.py \
  judge-preunblind.json \
  runs/<RUN_ID>/sealed/private/condition-map.json \
  runs/<RUN_ID>/sealed/blinded \
  --json
```

## Promotion rule

Behavioral superiority is established only if all deterministic gates in `promotion-policy.json` pass, including:

- treatment wins at least 2 of 3 cases;
- treatment loses at most 1 case;
- zero critical-invariant regressions relative to control;
- zero treatment automatic failures;
- zero treatment fidelity losses;
- no aggregate score regression;
- catastrophic >2× time **and** tool-call burden fails unless treatment wins all 3 cases, when comparable metrics exist.

If any gate fails, the correct claim is:

`CLARIFY VISUAL INTEGRATION: BEHAVIORAL SUPERIORITY NOT PROVEN`

## What is intentionally not automated

The Judge still needs capable visual inspection. The deterministic scorer does not decide whether a diagram is readable or semantically effective; it only enforces the already-sealed judgment and promotion contract.
