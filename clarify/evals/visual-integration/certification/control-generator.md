# Clarify Visual A/B — Isolated Control Generator

You are the CONTROL generator for the Clarify visual-integration behavioral A/B.

## Required baseline

Execute from the exact repository commit declared for `control` in `baselines.yaml`.

Do not run from current `main` and do not inspect later commits to reconstruct what changed.

## Allowed evaluation surface

- the control checkout's `clarify/SKILL.md` and only the Clarify references it normally routes to;
- `certification/inputs.yaml`;
- the source named by each blind input;
- ordinary rendering capability available equally to both conditions;
- stable general knowledge needed to execute the prompts.

## Forbidden

Do not access, search, inspect, infer from, or ask another agent about:

- `oracle.yaml`;
- `ab-cases.yaml`;
- treatment outputs;
- current Clarify v1.1 integration files;
- `visual-semantic-compiler/`;
- integration validation reports or PR discussions;
- expected answers, judge dimensions, critical invariants, prior runs, or certification results.

If any forbidden expected answer or prior judgment for these cases is already visible in active context, abort with exactly:

`CLARIFY VISUAL A/B INVALID — CONTROL CONTEXT CONTAMINATED`

## Task

Execute every case in `inputs.yaml` independently using the frozen control Clarify behavior.

For each case:

1. produce the user-facing clarification;
2. produce an actual rendered visual when the prompt asks for one;
3. do not intentionally imitate or anticipate the treatment architecture;
4. preserve source truth using only the control skill's normal behavior;
5. record failures honestly.

Do not expose private chain-of-thought.

## Output directory

Create a fresh run directory and never overwrite a previous run:

`runs/<RUN_ID>/control/`

For every case store:

- `cases/<case_id>/response.md`;
- rendered artifact(s) under `cases/<case_id>/artifacts/`;
- `cases/<case_id>/receipt.json`.

Receipt fields:

```json
{
  "case_id": "...",
  "condition": "control",
  "model": "...",
  "surface": "...",
  "elapsed_ms": null,
  "tool_calls": null,
  "output_bytes": 0,
  "render_succeeded": true,
  "artifact_files": [],
  "proof": {
    "semantic_validation": "not_provided",
    "invariant_coverage": "not_provided",
    "layout_validation": "not_provided",
    "artifact_validation": "not_provided",
    "browser_evidence": "not_provided",
    "perceptual_review": "not_provided",
    "bindings_valid": "not_provided"
  },
  "notes": ""
}
```

If the control's ordinary behavior independently produces equivalent proof, record it truthfully using only `passed`, `failed`, `skipped`, or `not_provided`. Do not simulate treatment-specific proof just to improve the score.

Use null when a metric is not available; never invent cost metrics.

At the end write `run-metadata.json` with the exact tested commit, model, surface, case count, and `oracle_seen: false`.

Seal the generated files with SHA-256 in `hashes.sha256`.

Do not judge, compare, or revise outputs after seeing another condition.
