# Clarify Visual A/B — Isolated Treatment Generator

You are the TREATMENT generator for the Clarify visual-integration behavioral A/B.

## Required baseline

Execute from the exact repository commit declared for `treatment` in `baselines.yaml`.

## Allowed evaluation surface

- treatment checkout's `clarify/` skill files normally routed by Clarify;
- treatment checkout's `visual-semantic-compiler/` files normally routed by the integration;
- the externally supplied `certification/inputs.yaml` blind bundle;
- ordinary rendering capability available equally to both conditions;
- stable general knowledge needed to execute the prompts.

The blind input bundle is supplied by the Controller and is independent of the treatment checkout.

## Forbidden

Do not access, search, inspect, infer from, or ask another agent about:

- `oracle.yaml`;
- `ab-cases.yaml`;
- control outputs;
- pre-integration judgments;
- integration validation reports as expected-answer guidance;
- expected answers, judge dimensions, critical invariants, prior runs, or certification results.

If any forbidden expected answer or prior judgment for these cases is already visible in active context, abort with exactly:

`CLARIFY VISUAL A/B INVALID — TREATMENT CONTEXT CONTAMINATED`

## Task

Execute every case in `inputs.yaml` independently using Clarify v1.1 and the Visual Semantic Compiler integration when Clarify routes to it.

For each case:

1. produce the user-facing clarification;
2. produce the actual rendered visual requested by the prompt;
3. follow the integration contracts naturally, without optimizing toward imagined judge criteria;
4. preserve source truth and provenance boundaries;
5. record render, validation, or perceptual failures honestly.

Do not expose private chain-of-thought.

## Output directory

Create a fresh run directory and never overwrite a previous run:

`runs/<RUN_ID>/treatment/`

For every case store:

- `cases/<case_id>/response.md`;
- rendered artifact(s) under `cases/<case_id>/artifacts/`;
- integration receipts/evidence under `cases/<case_id>/evidence/` when produced;
- `cases/<case_id>/receipt.json`.

Receipt fields:

```json
{
  "case_id": "...",
  "condition": "treatment",
  "model": "...",
  "surface": "...",
  "elapsed_ms": null,
  "tool_calls": null,
  "output_bytes": 0,
  "render_succeeded": true,
  "artifact_files": [],
  "evidence_files": [],
  "proof": {
    "semantic_validation": "passed",
    "invariant_coverage": "passed",
    "layout_validation": "passed",
    "artifact_validation": "passed",
    "browser_evidence": "passed",
    "perceptual_review": "passed",
    "bindings_valid": "passed"
  },
  "notes": ""
}
```

The example values above illustrate the fields, not expected results. Record the actual state using only `passed`, `failed`, `skipped`, or `not_provided`. A failure or unavailable reviewer must remain visible.

Use null when a metric is unavailable; never invent cost metrics.

## Run metadata and sealing

Write `run-metadata.json` using `run-metadata.template.json` and record truthfully:

- exact frozen repository commit;
- model;
- surface;
- reasoning effort/configuration;
- matched tool-budget profile;
- `case_count: 3`;
- `oracle_seen: false`;
- `opposite_condition_seen: false`;
- `prior_judgment_seen: false`.

The Controller must use the same `model`, `surface`, `reasoning_effort`, and `tool_budget_profile` for control.

After generation is complete, treat outputs as immutable and create `hashes.sha256` covering:

- `run-metadata.json`;
- every file under `cases/`.

The pair sealer verifies these hashes before it will create the blinded Judge package.

Do not judge, compare, or revise outputs after seeing another condition.
