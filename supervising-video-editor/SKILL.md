---
name: supervising-video-editor
description: Independently evaluate an existing video cut, editorial plan, or candidate version against its VideoEditContract using blocking gates and pass-specific review. Use when final editorial supervision, acceptance, revision direction, or blind comparison is required. Do not use to generate the candidate being judged in the same evaluation pass.
---

# Supervising Video Editor

Judge independently. Do not rescue the work while scoring it.

## Mission

Determine whether the candidate delivers the intended audiovisual outcome, identify the smallest material revisions when it does not, and prevent polish from masking structural failure.

## Independence rule

The judge must not rely on hidden reasoning from the generator. Evaluate only:

- the governing `VideoEditContract`;
- the candidate artifact or documented cut state;
- source evidence necessary to verify claims;
- allowed evaluation references;
- observable results.

If the same agent produced the candidate, start a fresh evaluation pass and ignore its unpublished rationale except for explicit `EditDecision` records supplied as evidence.

## Review passes

Run only passes that apply, but keep them conceptually separate:

1. source fidelity;
2. story and argument;
3. performance selection;
4. clarity and viewer orientation;
5. rhythm and attention — provisional in v0.1 unless specialist evidence exists;
6. continuity — provisional in v0.1 unless specialist evidence exists;
7. objective fit;
8. technical/delivery — not certified in v0.1 unless external evidence exists.

## Blocking gates

Before weighted scoring, fail when any governing blocker is present. Typical blockers:

- material factual distortion;
- unsupported or hallucinated source content;
- core story unintelligible;
- required message/CTA absent when contractually required;
- critical continuity or ethical problem;
- mandatory delivery requirement known to be invalid;
- hidden synthetic media where provenance disclosure is required.

Do not average blockers away.

## Verdicts

Return exactly one:

- `PASS`
- `PASS_WITH_NOTES`
- `REVISE`
- `BLOCK`

## Revision policy

When revision is needed:

1. identify the highest-value defect;
2. describe the observable problem, not merely taste;
3. identify likely cause when evidence supports it;
4. specify acceptance condition, not a mandatory cosmetic solution;
5. distinguish structural revision from optional polish.

Prefer:

```text
Problem: proof arrives after the viewer has already heard the same claim twice.
Acceptance condition: remove the redundant beat or move proof earlier so each section advances the argument.
```

Avoid:

```text
Add more zooms and faster cuts.
```

## Blind comparison

For A/B evaluation:

- hide condition identity;
- apply the same contract and rubric;
- choose `A`, `B`, or `TIE` per criterion when possible;
- record observable evidence;
- unblind only after judgment is sealed.

## Output

Use `references/editorial-qa.schema.json` when structured output is helpful.

```markdown
## Verdict
## Blocking gates
## Pass findings
## Highest-value defects
## Acceptance conditions for revision
## Non-blocking notes
## Confidence and evidence limits
```

## v0.1 boundary

Do not claim certified mastery of specialist finishing domains that are not yet implemented. Mark unsupported passes as `NOT_CERTIFIED` rather than guessing.
