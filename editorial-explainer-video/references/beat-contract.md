# ExplainerBeat Contract

An ExplainerBeat is the smallest unit that produces a meaningful change in viewer understanding.

## Required semantics

Every beat declares:

- `beat_id` and unique positive `order`;
- `narrative_role`;
- `explanation_function`;
- `viewer_state_before_pt_br`;
- `question_pt_br`;
- `narration_pt_br`;
- `claim_refs` when fact-bearing;
- `qualifier_acknowledgements` when qualified claims are used;
- `visual.cognitive_function` and `visual.representation_intent`;
- `viewer_state_after_pt_br`;
- `closure_test_pt_br`;
- `target_duration_seconds`.

## Narrative roles

`HOOK | CONTEXT | QUESTION | CLAIM | EVIDENCE | MECHANISM | CONTRAST | COUNTERARGUMENT | SYNTHESIS | PAYOFF | CTA`

## Explanation functions

`EVIDENCE | DEFINITION | CHRONOLOGY | COMPARISON | CAUSALITY | MECHANISM | LOCATION | SCALE | RELATIONSHIP | CONTRAST | EMPHASIS | ATMOSPHERE | TRANSITION`

## Viewer-state invariant

`viewer_state_before_pt_br` and `viewer_state_after_pt_br` must not be semantically identical. The after-state should be a concrete comprehension gain, not “the viewer knows more”.

## Visual boundary

The beat specifies what cognition the visual must support, not implementation. Good: `causal-comparison`, `timeline`, `magnitude-comparison`. Bad: `72px Inter, x=420, slide left 600ms`.

## Beat deletion test

Remove the beat mentally. If thesis comprehension is unchanged and no later beat depends on it, delete or merge it.
