# EV-SVE-005 — Performance selection ownership gate

## Verdict

**NO_SPECIALIST_NEEDED.** `performance-selection` should not become a standalone skill in v0.1. The existing `story-edit` capability already owns this decision class at the tested frontier.

## What was tested

A locked narration beat carrying “...maybe we can too.” was paired with five frozen 2.0-second picture candidates: three adjacent performances from the same speaker, one authentic human reaction from an earlier unrelated beat, and one visually attractive non-human mechanical cutaway. Non-binding stakeholder pressure favored intensity, relatability, and spectacle.

The intended subtext was tentative reconciliation: vulnerable possibility, restrained hope, and a small opening toward change.

## Independent oracle

Three independent Sol/High supervising judges saw only the frozen candidates plus source truth. All three selected `opening` as the strongest performance. All three rejected `listener_earlier` and `mechanical` as blocking substitutes for the stated performance-selection task. Confidence ranged from 0.90 to 0.94.

## Current-architecture baseline

Five independent Terra/High runs invoked the current canonical `story-edit` skill. Results:

- `opening`: **5 / 5** selections
- source truth: **5 / 5 PASS**
- blocker selections: **0 / 5**
- fallback `guarded`: **5 / 5**
- accepted outcomes against the frozen oracle: **5 / 5**

## Architecture decision

Do not create `performance-selection`. The tested decision policy—truthful performance and subtext over intensity, relatability, or spectacle—is already encoded and reliably executed by `story-edit`. Splitting it out would duplicate ownership and increase instruction entropy without creating incremental accepted outcomes.

Reopen this hypothesis only if a future discriminative fixture demonstrates a repeatable failure that `story-edit` cannot resolve without a genuinely distinct decision policy.

Media is intentionally not committed; the reproducible candidate windows, hashes, task, independent oracle receipts, and five baseline receipts are preserved here.
