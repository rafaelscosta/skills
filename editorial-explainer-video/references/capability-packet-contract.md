# Capability Packet Contract

W4 converts a validated `editorial-explainer-plan/v1` into **bounded handoff packets**. A packet carries semantic intent and evidence constraints; it never reimplements the downstream skill.

## Invariants

Every packet is bound to the exact `plan_sha256` and `evidence_ledger_sha256`. Beat-scoped packets copy the beat's `claim_refs`, `qualifier_acknowledgements`, question, narration, viewer-state transition, and closure target without semantic strengthening.

The downstream owner remains authoritative for implementation. An adapter may provide hints such as `analytical_task`, `representation_type`, or `category_hint`, but those are routing hints rather than renderer commands.

## Capability chains

| Explainer function | Canonical chain |
| --- | --- |
| `SCALE`, `COMPARISON` | `data-viz-selector -> motion-graphics` |
| `CAUSALITY`, `MECHANISM`, `RELATIONSHIP`, `CHRONOLOGY` | `visual-semantic-compiler -> motion-graphics` |
| `EVIDENCE` | `media-use -> motion-graphics` |
| `LOCATION` | `motion-graphics` |
| `DEFINITION`, `CONTRAST`, `EMPHASIS`, `TRANSITION` | `motion-graphics` |
| `ATMOSPHERE` | `media-use -> motion-graphics` |

All motion-unit packets also depend on the project `motion-studio` creative-direction packet. The final `general-video` assembly packet depends on the creative-direction packet and every beat's terminal packet.

## Fail-closed behavior

Reject unknown or function-incompatible preferred owners. Do not silently substitute a different semantic owner because one is unavailable. Owner availability is an execution-time gate; the adapter contract remains valid without provider/network access.

Do not place coordinates, CSS, GSAP code, chart geometry, asset-provider choices, or generated visual content in an adapter packet.
