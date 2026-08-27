# Clarify Visual A/B — Sealed Blind Judge

You are the JUDGE for the Clarify visual-integration behavioral A/B.

You evaluate **candidate A** and **candidate B** without knowing which is control or treatment.

## Allowed surface

- `inputs.yaml`;
- `oracle.yaml`;
- the sealed `blinded/` package produced by `seal_pair.py`;
- rendered artifacts/screenshots inside that package;
- this judge protocol.

## Forbidden before final judgment is sealed

Do not access or infer from:

- `private/condition-map.json`;
- `baselines.yaml`;
- control/treatment generator instructions;
- implementation PRs, commits, discussions, or validation reports;
- unblinded generator directories;
- previous A/B judgments.

If the condition mapping is already visible in active context, abort with exactly:

`CLARIFY VISUAL A/B INVALID — JUDGE UNBLINDED BEFORE SCORING`

## Evaluation procedure

For each case:

1. read the blind input and source;
2. read the case oracle;
3. inspect candidate A response and every delivered visual artifact;
4. inspect candidate B response and every delivered visual artifact;
5. check every critical invariant independently for A and B;
6. apply every automatic-failure rule independently;
7. score every case dimension for A and B on the 0–2 oracle scale;
8. compare operational usability, not decorative richness;
9. use the sanitized receipt only for execution-cost/proof claims that are actually present;
10. choose `A`, `B`, or `tie` as the case winner.

Do not reward a candidate merely for having more files, more prose, more diagrams, or more validation ceremony. Proof counts only when it supports a claim relevant to the requested outcome.

Do not penalize a candidate for omitting information from the visual when the same information is intentionally preserved as text-only and does not belong to the visual's primary question.

## Critical-invariant gate

For every invariant emit one of:

- `passed` — accurately preserved and operationally usable;
- `partial` — present but ambiguous/incomplete;
- `failed` — missing, contradicted, or materially distorted.

Any `failed` critical invariant is a critical regression for that candidate on that case.

## Automatic failures

Record each triggered automatic-failure rule verbatim by short code/description. Do not compensate an automatic failure with a high average score.

## Score scale

Use the oracle scale exactly:

- `0` — absent, wrong, materially unsafe, or unusable;
- `1` — partially correct but incomplete, ambiguous, or weakly evidenced;
- `2` — complete, correct, usable, and supported by supplied evidence.

## Case winner

Choose the winner after scoring, using this priority:

1. fewer failed critical invariants;
2. fewer automatic failures;
3. higher fidelity/epistemic correctness where present;
4. higher sum of case dimensions;
5. better operational/perceptual usability;
6. if differences are immaterial, `tie`.

## Required output

Create `judge-preunblind.json` with this shape:

```json
{
  "schema_version": "clarify-visual-ab-judgment/v1",
  "blinded_manifest_sha256": "<sha256 of blinded/manifest.json>",
  "judge": {"id": "<identifier>", "type": "human|model"},
  "condition_mapping_seen": false,
  "cases": [
    {
      "case_id": "...",
      "A": {
        "critical_invariants": {"<invariant>": "passed|partial|failed"},
        "automatic_failures": [],
        "scores": {"<dimension>": 0},
        "total": 0,
        "notes": "concise evidence-based notes"
      },
      "B": {
        "critical_invariants": {},
        "automatic_failures": [],
        "scores": {},
        "total": 0,
        "notes": ""
      },
      "winner": "A|B|tie",
      "winner_reason": "concise evidence-based reason"
    }
  ],
  "cost_observations": {
    "metrics_comparable": false,
    "A": {},
    "B": {},
    "notes": ""
  },
  "overall_blind_observation": "Do not identify conditions; summarize strengths/regressions only."
}
```

Requirements:

- exactly three cases, each exactly once;
- scores only for dimensions declared for that case;
- totals equal score sums;
- no condition guess;
- no promotion claim;
- no edits after condition mapping is revealed.

After writing the judgment, seal it with SHA-256. The condition map may be revealed only to the post-judge aggregator.
