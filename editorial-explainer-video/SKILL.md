---
name: editorial-explainer-video
description: Compile a verified editorial evidence ledger into a thesis, explanatory mechanism, source-bound script, and ordered ExplainerBeat plan for evidence-driven visual explainers. Use after $editorial-evidence when the user wants a factual narrated explainer, documentary-style explanation, or multi-scene educational/editorial video. Do not use as a renderer, generic video editor, or substitute for evidence verification.
---

# Editorial Explainer Video

Turn verified claims into an explanation whose **argument, narration, and visual intent remain traceable to evidence**.

Default narration and audience-facing text to Brazilian Portuguese unless the user requests another language. Keep ids, enums, routing labels, schemas, and implementation instructions in English.

## Mission

Compile:

```text
verified claim ledger
→ thesis
→ explanatory mechanism
→ narrative argument
→ source-bound script
→ viewer-state transitions
→ ExplainerBeat[]
```

This skill stops before audiovisual production. Motion, assets, audio, charts, diagrams, and renderers remain downstream concerns.

## Ownership boundary

This skill owns:

- the central explanatory question and thesis;
- the mechanism that connects evidence to the answer;
- narrative order and information dependency;
- script blocks bound to claim ids;
- `ExplainerBeat` planning and viewer-state transitions;
- visual **function** and representation intent, not pixels;
- deterministic cross-validation against the exact evidence-ledger bytes.

It does not re-verify sources, invent new claims, choose exact chart implementations, author animation code, source media, mix audio, or render video.

## Required input

Use a ledger produced by `$editorial-evidence` with schema `editorial-evidence-ledger/v1`.

Only consume claims whose `editorial_use` is `ALLOW` or `ALLOW_WITH_QUALIFICATION`. Never soften a blocked claim merely to make the story work.

Read `references/explainer-contract.md` before compiling a non-trivial explainer.

## Compile workflow

### 1. Bind the exact evidence bytes

Hash the ledger bytes and store the digest in `evidence_ledger_sha256`.

If the ledger changes later, the plan is stale and must be recompiled or revalidated. Do not carry forward a prior validation receipt across changed evidence bytes.

### 2. Lock one explanatory question

Write one question that the video actually answers. Prefer a mechanism question such as “why”, “how”, “what changed”, or “what explains the difference” over a vague topic label.

The thesis must answer that question in one bounded statement and name the `must_prove_claim_refs` needed to justify it.

Do not let the thesis be stronger than its strongest required claim.

### 3. Build the explanatory mechanism

State the smallest causal, structural, chronological, comparative, or definitional mechanism that connects the claims to the thesis.

If the evidence supports only correlation, interpretation, or a qualified cause, preserve that epistemic level in the mechanism and narration.

### 4. Write source-bound script blocks

Every factual script block must declare `claim_refs`.

A block may use prose for pacing, analogy, or transition without claim refs only when `fact_bearing` is false.

For any `ALLOW_WITH_QUALIFICATION` claim, copy every required qualifier into `qualifier_acknowledgements` for each factual script block or beat that materially relies on it.

Never introduce a statistic, quote, attribution, chronology, causal step, or factual example that does not exist in the ledger.

### 5. Compile ExplainerBeats

Read `references/beat-contract.md` when authoring beats.

Each beat is a semantic unit of understanding, not merely a shot. It must declare:

- what the viewer understands before;
- what new question or gap is resolved;
- which claims support the beat;
- what the narration says;
- what cognitive function the visual must perform;
- what the viewer should understand afterward;
- a closure test.

A beat that does not materially change viewer understanding should be merged, rewritten, or removed.

### 6. Route only by cognitive function

Read `references/capability-routing.md` only when preparing a downstream handoff.

This skill may select `visual.cognitive_function` and `representation_intent`; it must not prescribe coordinates, typography sizes, GSAP code, exact asset providers, or renderer-specific geometry.

### 7. Validate the plan against the ledger

Run:

```bash
python3 scripts/validate_plan.py <explainer-plan.json> <ledger.json> --json
```

The validator checks byte binding, claim existence and editorial permission, qualifier propagation, thesis coverage, script/beat traceability, beat ordering, and viewer-state progress.

A deterministic pass proves contract integrity. It does not prove that the explanation is insightful, elegant, or compelling; those require behavioral/editorial review.

## Canonical output

For non-trivial work, produce:

```text
explainer-plan.json
validation-receipt.json
```

The plan contains the thesis, mechanism, script blocks, and beats. Do not create renderer artifacts during this stage.

## Hard fails

Never certify when any of these are true:

- the evidence hash does not match the supplied ledger;
- a thesis, script block, or beat references a missing or blocked claim;
- a qualified claim is used without all required qualifiers;
- a must-prove claim is absent from the script or beat plan;
- a factual script block has no claim refs;
- two beats share the same id or order;
- `viewer_state_before` equals `viewer_state_after`;
- narration contains a factual assertion intentionally introduced outside the ledger;
- a causal mechanism is stated more strongly than the ledger permits.

## Definition of done

The explainer compiler is done when the exact evidence ledger is hash-bound to one coherent thesis, all material script/beat assertions are claim-traceable, every required qualifier survives into use, every beat advances viewer understanding, and the deterministic validator passes.
