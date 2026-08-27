# Perceptual Delivery Contract — R3

Use this reference only after the canonical artifact has passed semantic, layout, and static artifact validation.

R3 answers a different question:

> **Can a reader actually inspect and use the exact delivered artifact at the supported desktop viewports?**

A deterministic pass cannot answer that question by itself.

## Evidence pipeline

```text
artifact SHA-256
  ↓
real Chromium render
  ↓
automated viewport evidence
  ↓
screenshots + contact sheet
  ↓
identified reviewer inspects evidence
  ↓
review receipt
  ↓
review-binding validator
  ↓
perceptually-passed | perceptually-failed | skipped
```

No step may silently imply a later one.

## Stage 1 — Browser evidence

Run:

```bash
node scripts/visual_check.mjs output.html output.visual-evidence/
```

The checker uses Chromium/Chrome when available and renders the exact self-contained HTML bytes through Chrome DevTools. It never edits or rerenders the artifact through a second renderer.

Required desktop viewports:

- 1440×900;
- 1600×1000;
- 1920×1080;
- 2048×1320.

Canonical screenshots are captured at 1440×900 and 2048×1320. The remaining viewports are measured even when no screenshot is retained.

### Automated checks

The evidence pass verifies only observable browser conditions:

- inline SVG has non-zero rendered size;
- document has no horizontal overflow;
- the diagram panel has no horizontal scroll at supported desktop viewports;
- node text does not escape its node box;
- projected node-label text is at least 12px;
- projected relationship-label text is at least 9px;
- body text is at least 14px;
- screenshot capture succeeds.

Suspected text clipping and unusually long pages are warnings. They require reviewer attention but do not automatically become perceptual judgments.

The evidence receipt is `visual-evidence-receipt/v1` and always reports:

```text
perceptual_review: pending
```

Even when every automated browser check passes.

## Stage 2 — Review the actual evidence

A capable human or vision-capable model must inspect the exact screenshots produced from the artifact.

Inspect at minimum:

- hierarchy and obvious reading direction;
- line/route visibility;
- node and relationship-label readability;
- clipping or occlusion;
- confusing whitespace or crowding;
- whether important relationships visually disappear;
- whether semantic emphasis matches the explanation;
- whether the artifact feels materially harder to parse than its prose equivalent.

Suggested defect codes:

- `clipping`;
- `node-overlap`;
- `label-overlap`;
- `hidden-route`;
- `stacked-edge`;
- `weak-hierarchy`;
- `ambiguous-direction`;
- `tiny-text`;
- `low-contrast`;
- `unbalanced-whitespace`;
- `visual-noise`;
- `semantic-emphasis-mismatch`.

Do not invent a defect because an automated metric looks unusual. Inspect the pixels.

## Stage 3 — Reviewer receipt

Author a `visual-perceptual-review/v1` receipt:

```json
{
  "schema_version": "visual-perceptual-review/v1",
  "artifact_sha256": "<artifact SHA from evidence>",
  "evidence_sha256": "<SHA-256 of exact evidence JSON bytes>",
  "reviewer": {
    "id": "<human name or model/session identifier>",
    "type": "human"
  },
  "status": "passed",
  "defects": [],
  "notes": "Inspected both retained desktop screenshots."
}
```

`reviewer.type` is `human` or `model`.

Rules:

- `passed` requires automated evidence status `passed` and **zero defects**;
- `failed` requires at least one concrete defect with severity and evidence;
- `skipped` requires a reason;
- reviewer identity cannot be empty;
- the review must bind to both artifact and evidence hashes.

## Stage 4 — Validate the review claim

Run:

```bash
python3 scripts/validate_perceptual_review.py \
  output.visual-evidence/output.visual-evidence.json \
  review.json --json
```

A valid combined receipt reports one of:

- `perceptually-passed`;
- `perceptually-failed`;
- `perceptual-review-skipped`.

The validator checks provenance and revision binding. For a `passed` review it also independently verifies the evidence surface rather than trusting declarations alone:

- all four required desktop viewports are present;
- both required retained screenshots are present;
- each screenshot reference is a safe relative filename;
- each referenced PNG exists beside the evidence receipt;
- each PNG SHA-256 matches the browser evidence receipt;
- each PNG byte count matches the browser evidence receipt.

Deleting, replacing, or tampering with a retained PNG therefore invalidates a later `perceptually-passed` claim even if the evidence JSON itself was not edited.

The validator does **not** inspect pixels itself. The reviewer remains responsible for the perceptual judgment.

## Immutability

Any change to the HTML bytes invalidates:

- browser evidence;
- screenshots;
- evidence hash;
- perceptual review.

Capture and review again.

A reviewer must never approve screenshots from a previous artifact revision.

Likewise, changing or deleting the retained screenshots invalidates the review-binding gate.

## Correction loop

Maximum: **two focused correction rounds** before reporting unresolved perceptual defects.

If review fails:

1. identify the concrete visual defect;
2. repair the narrowest responsible layer;
3. rerun all invalidated downstream gates;
4. recapture browser evidence;
5. inspect the new screenshots;
6. author a new review receipt.

Examples:

- CSS-only change → artifact validation + R3 evidence/review again;
- layout change → layout validation + artifact validation + R3 again;
- semantic topology change → semantic validation + layout + artifact + R3 again.

Never edit the reviewer receipt to turn a failed artifact into a pass.

## Mobile boundary

R3 v1 certifies the canonical desktop artifact at the four declared viewports. Narrow/mobile behavior may remain scroll-contained but is **not** part of the R3 perceptual pass claim yet.

Do not generalize a desktop perceptual pass into a mobile usability claim.

## Definition of done

A canonical visual delivery may claim `perceptually-passed` only when:

1. semantic validation passed;
2. layout validation passed;
3. static artifact validation passed;
4. browser evidence passed on every required desktop viewport;
5. both retained screenshots exist and their bytes match the evidence receipt;
6. an identified reviewer inspected those exact screenshots;
7. the reviewer reported no visible defects;
8. the review receipt passes artifact, evidence, viewport, and screenshot binding validation.
