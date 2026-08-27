# Clarify v1.1 → Visual Semantic Compiler v1.2.1 — Integration Validation

## Scope

This report validates the deterministic and rendered integration path for one source-bound operational fixture. It does **not** claim a fresh-context behavioral A/B win over Clarify without the compiler.

Correct status:

```text
DETERMINISTIC INTEGRATION: PASSED
END-TO-END SOURCE-BOUND PILOT: PERCEPTUALLY PASSED
FRESH-CONTEXT BEHAVIORAL A/B: PENDING
```

## Fixture

Source:

`evals/visual-integration/refund-policy.md`

The source intentionally combines:

- a compound eligibility rule: within 7 days **and** no premium consumption;
- approve/deny branches;
- an incomplete-data recovery loop that must return to analysis;
- a 3–5 business day finance timing fact that happens after approval and must not change eligibility.

## Regression checks

Executed against the integration runtime:

```text
Clarify invariant-coverage suite:        7/7 PASS
Clarify rubric-v2 scorer suite:         10/10 PASS
VSC semantic-validator suite:            7/7 PASS
VSC existing R2 layout regression:      13/13 PASS
Clarify recovery-flow renderer tests:    4/4 PASS
VSC R3 perceptual/binding regression:   12/12 PASS
Python / Node syntax checks:                  PASS
```

Total targeted automated tests across the final integration regression: **53/53 PASS**.

### Scorer v2 compatibility proof

`score_clarity.py` now supports the two new visual proof dimensions without breaking the original 14-dimension contract.

Verified behavior:

- legacy `risk_level` payloads retain `clarify-rubric/v1-legacy`, maximum 28, and the original critical gates;
- explicit non-visual rubric-v2 profiles still score only the original 14 dimensions, so visual-proof points cannot inflate prose/operational scores;
- `trusted_visual` requires all 16 dimensions, maximum 32, threshold 30;
- `visual_invariant_coverage` and `visual_delivery_proof` are hard `2` gates for `trusted_visual`;
- `high_risk` remains reachable without artificial visual dimensions, maximum 28 and threshold 27;
- boolean values are rejected rather than being accepted as Python integers.

The v2 rubric threshold for non-visual `high_risk` is therefore 27. The earlier draft value 31 was internally unreachable without visual dimensions and was corrected before merge.

### Bundle structural check

The final branch was checked against the contract implemented by `scripts/validate_bundle.py`:

- valid `clarify` frontmatter with positive `Use when` and negative `Do not use` boundaries;
- `SKILL.md` remains below the 500-line warning threshold;
- every newly referenced `references/`, `scripts/`, and `evals/` path exists in the branch tree;
- metadata still contains the required interface fields and explicit `$clarify` invocation;
- changed/new Python modules compile and their unit tests pass;
- changed/new JSON fixtures parse successfully.

The repository container had no external DNS and could not clone the branch to invoke `validate_bundle.py` against a fresh checkout. The only expected finding from that script beyond these checks is the pre-existing non-blocking `B025` warning for keeping `clarify/README.md` in the portable bundle.

## Why the renderer changed

The initial realistic Clarify handoff exposed two defects that simpler fixtures did not:

1. the missing-data recovery edge was treated like an ordinary forward DAG edge, creating crossings / edge-through-node failures;
2. making the real eligibility rule visible in the node (`Até 7 dias E sem consumo premium?`) caused browser-detected node-text overflow with the old single-line renderer.

The accepted repair was deliberately downstream:

- `flow` recovery/back edges route on an outer rail;
- long operational node labels wrap across SVG `<tspan>` lines;
- flow node height expands to preserve the full label;
- the geometry validator permits a reverse-direction edge only when its polyline proves an explicit outer back-route.

The semantic model was **not** weakened to make layout easier.

## Final source-bound pilot

### Semantic IR gate

```text
status: valid
semantic_ir_sha256:
6f1ec704525ff90773b8da8290780a9b8f1963890b2b3ac2ab3004091d9f2213
errors: 0
warnings: 0
```

### Clarify invariant coverage gate

```text
status: valid
invariants: 5
visual_relevant: 4
represented: 4
text_only: 1
omitted: 0
blocked: 0
```

The post-decision 3–5 day finance timing is intentionally `text-only`; the four operationally visual invariants are represented by source-bound IR nodes/relationships.

### Deterministic render gate

```text
status: success
artifact_sha256:
759ec48781a26981799aa5811f3d7c461a646b1b602c5e1f04fa60bf8266b3d5
```

Layout and static artifact validation passed before delivery.

### Browser evidence gate

Live Chromium:

```text
Chromium 144.0.7559.96 built on Debian GNU/Linux 13 (trixie)
```

Result:

```text
browser_evidence: passed
1440×900:   PASS
1600×1000:  PASS
1920×1080:  PASS
2048×1320:  PASS
nodeTextOverflow: 0 at all 4 viewports
browser errors: 0
```

Retained screenshots:

```text
1440×900
sha256: 9d14eed2b61a480bb1ab11ae30560f2227749f1277f03b2a2694ec29599a7267
bytes: 73689

2048×1320
sha256: 3731ea8e2631af21781fa69ebca4a82bd87324f1bb86fcdd0cb42cbe92c84cd2
bytes: 114263
```

The automated browser probe emitted `text-clipping-suspected` warnings from its generic scroll heuristic. The retained screenshots were therefore inspected rather than upgrading the warnings automatically.

### Perceptual gate

An identified vision-capable GPT-5.6 Sol reviewer inspected both retained screenshots.

Observed:

- the compound eligibility rule is explicit and readable;
- the missing-data recovery loop is traceable back to `Dados completos?`;
- yes/no branches remain visually discriminable;
- approve and deny outcomes are distinct;
- no visible node-label clipping remains;
- the 3–5 business day finance timing is correctly excluded from the decision diagram while preserved in the text-equivalent / omission boundary.

Hash-bound review result:

```text
status: valid
delivery_status: perceptually-passed
review_status: passed
defects: 0
artifact_sha256:
759ec48781a26981799aa5811f3d7c461a646b1b602c5e1f04fa60bf8266b3d5
evidence_sha256:
4d5ef5aaf115f16e27ed2b7ff450c0b34f8d9e42be4da532f6b3ffaaf6f3f068
```

## What this proves

This pilot proves that the integration contracts can preserve source-bound operational truth through semantic compilation, invariant coverage, deterministic layout, HTML/SVG rendering, browser evidence, and perceptual review.

It also proves that the gates can expose real integration defects before handoff: the recovery-loop and long-label defects were both caught and repaired without deleting source truth.

The scorer regression additionally proves that adopting verified visuals does not silently alter the score surface for legacy/non-visual Clarify evaluations.

## What this does not prove

It does not prove that GPT-5.6 will always choose or author a better visual when Clarify v1.1 is invoked in the wild.

It does not prove superiority over Clarify-only behavior.

It does not certify mobile/narrow rendering.

The next valid frontier is the isolated control-vs-treatment run defined in `evals/visual-integration/README.md` and `ab-cases.yaml`.
