# Explainer Eval Rubric

This rubric separates deterministic integrity from reviewer judgment. Never convert a proxy metric into a perceptual or editorial verdict.

## Evaluation layers

1. `machine-eval` — exact bindings, traceability, qualifier survival, route coverage, handoff fidelity, and diagnostic pacing proxies.
2. `reviewer-eval` — explanation quality, narrative coherence, beat closure, visual explanatory value, cognitive load, audiovisual craft, and provenance/rights at the artifact stage actually inspected.
3. `eval-summary` — combines the exact machine receipt and reviewer receipt. Hard fails override scores.

## Reviewer dimensions

| Dimension | What the reviewer judges |
| --- | --- |
| `factual_epistemic_integrity` | Claims, uncertainty, qualifiers, causality, numbers, quotes, and visual truthfulness remain faithful to evidence. |
| `explanatory_clarity` | The audience can reconstruct the answer/mechanism without hidden inferential leaps. |
| `narrative_coherence` | Beat order creates a necessary argument rather than a list of facts. |
| `beat_closure` | Each beat resolves its declared question and produces the intended viewer-state change. |
| `visual_explanatory_value` | Visuals add explanatory information rather than merely decorate or repeat narration. |
| `audiovisual_coherence` | Narration, visual attention, on-screen text, evidence, and sound reinforce the same idea at the same time. |
| `motion_editing_craft` | Motion, transitions, cuts, composition, and temporal hierarchy feel directed rather than templated. |
| `audio_quality` | Voice, music, SFX, silence, intelligibility, and mix support comprehension. |
| `pacing_cognitive_load` | Reading, listening, visual decoding, concept introduction, and tempo stay within a usable cognitive budget. |
| `provenance_rights` | Load-bearing assets and evidence have usable provenance/rights and synthetic material is not presented as authentic evidence. |

## Stage requirements and weights

### `plan`

- factual_epistemic_integrity: 20
- explanatory_clarity: 20
- narrative_coherence: 20
- beat_closure: 15
- visual_explanatory_value: 15
- pacing_cognitive_load: 10

### `owner_output`

- factual_epistemic_integrity: 20
- explanatory_clarity: 15
- narrative_coherence: 10
- beat_closure: 10
- visual_explanatory_value: 20
- pacing_cognitive_load: 10
- provenance_rights: 5
- audiovisual_coherence: 10

### `rough_cut` and `final`

- factual_epistemic_integrity: 20
- explanatory_clarity: 15
- narrative_coherence: 15
- visual_explanatory_value: 15
- audiovisual_coherence: 10
- motion_editing_craft: 10
- audio_quality: 5
- pacing_cognitive_load: 5
- provenance_rights: 5

Scores are 0–5. The weighted percentage is an operational acceptance heuristic, not a scientific measurement.

## Acceptance heuristic

A reviewer receipt can be accepted only when all required stage dimensions are scored and every score is at least 3.

- `PASS`: weighted score >= 85 and zero hard fails.
- `REVISE`: 70–84.99, or any required dimension below 4 but none below 3.
- `FAIL`: score < 70, any required dimension below 3, or any hard fail.

The final summary cannot be `PASS` unless the machine eval also passes.

## Hard fails

Any one of these forces `FAIL` regardless of weighted score:

- `UNSUPPORTED_CRITICAL_CLAIM`
- `QUALIFIER_DROPPED`
- `CAUSALITY_OVERSTATED`
- `VISUAL_CONTRADICTS_CLAIM`
- `STALE_EVIDENCE_BINDING`
- `MISSING_REQUIRED_OWNER_OUTPUT`
- `UNREADABLE_LOAD_BEARING_VISUAL`
- `NARRATION_VISUAL_MISMATCH`
- `RIGHTS_OR_PROVENANCE_BLOCKER`

## Diagnostics that are not verdicts

Machine eval may report narration words/second, claims/beat, evidence-required beats, and duration totals. These are signals for review, not automatic evidence of quality or failure.
