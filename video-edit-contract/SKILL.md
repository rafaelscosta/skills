---
name: video-edit-contract
description: Convert a video brief, raw request, script, campaign goal, or source package into a precise editorial contract that downstream editing agents can execute and verify. Use before substantial editing when objective, audience, format, success criteria, constraints, source truth, or delivery requirements are not yet explicit. Do not use as a substitute for story editing, finishing, or creative execution.
---

# Video Edit Contract

Turn ambiguous intent into an executable audiovisual contract.

## Mission

Create the smallest complete specification that lets an editing system decide what success means before it starts cutting.

## Operating principles

1. Optimize for the intended audience outcome, not generic visual polish.
2. Separate business or communication objective from implementation preference.
3. Preserve source truth, rights constraints, mandatory claims, legal copy, identity, and factual boundaries.
4. Distinguish hard constraints from preferences.
5. Do not invent platform requirements, KPIs, brand rules, or delivery specs.
6. Infer harmless defaults when they are reversible; expose consequential assumptions.
7. The contract is authoritative for downstream editorial trade-offs until explicitly revised.

## Required contract fields

Capture or derive:

- `objective`
- `audience`
- `viewer_outcome`
- `format_profile`
- `aspect_ratio`
- `target_duration`
- `primary_experience`
- `primary_metric` when applicable
- `secondary_metrics` when applicable
- `must_preserve`
- `must_avoid`
- `brand_constraints`
- `source_truth`
- `delivery_constraints`
- `risk_level`
- `open_questions`
- `assumptions`

Use `references/video-edit-contract.schema.json` for machine-readable output.

## Procedure

### 1. Identify the real outcome

Translate vague requests such as `make it dynamic`, `make it premium`, or `increase retention` into an observable target.

Prefer:

```text
After watching this piece, [audience] should [understand / feel / believe / remember / do] X.
```

### 2. Separate objective from tactics

Treat requested effects, transitions, music, pacing, captions, or AI use as implementation preferences unless the user explicitly makes them mandatory.

### 3. Bind the source truth

Record facts, claims, quotes, names, products, chronology, continuity-sensitive details, licensed assets, and any material that must not be altered or synthesized.

### 4. Define editorial priorities

Rank what wins when constraints conflict. Default order unless the project says otherwise:

1. factual and ethical integrity;
2. intended audience outcome;
3. story and performance;
4. clarity and attention;
5. rhythm;
6. visual and sonic polish;
7. convenience of execution.

### 5. Define acceptance gates

State which failures block approval. Typical gates:

- source fidelity;
- story clarity;
- required message or CTA present;
- no material continuity error;
- delivery spec valid;
- rights/provenance constraints satisfied.

Never let a high aesthetic score compensate for a blocking failure.

## Output

Return:

```markdown
## Editorial objective
## Audience and viewer outcome
## Format and delivery
## Source truth and invariants
## Creative priorities
## Must preserve
## Must avoid
## Acceptance gates
## Assumptions and open questions
```

When structured output is useful, emit a JSON object conforming to `references/video-edit-contract.schema.json`.

## Handoff

A valid contract may route to:

- `$footage-intelligence` when source media must be understood;
- `$story-edit` when structure must be created or repaired;
- `$senior-video-editor` when end-to-end orchestration is required;
- `$supervising-video-editor` when an existing cut must be judged against the contract.

## Failure conditions

Block rather than guess when a missing fact would materially alter factual integrity, rights, safety, mandatory claims, or delivery compliance.
