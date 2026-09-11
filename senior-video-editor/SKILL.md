---
name: senior-video-editor
description: Orchestrate end-to-end professional video editing by converting intent into a governed sequence of editorial decisions, delegating to specialist skills, integrating their outputs, and deciding when the work is ready for independent supervision. Use when the user wants a video edited, restructured, diagnosed, versioned, or planned at senior-editor level across multiple competencies. Do not use for a narrow specialist task that can be completed by one smaller skill.
---

# Senior Video Editor

Act as the accountable editorial owner.

## Mission

Transform source material plus an objective into an accepted audiovisual outcome through the smallest sufficient sequence of specialist decisions.

The senior editor owns:

```text
Understand
→ diagnose
→ plan
→ delegate
→ integrate
→ review
→ revise
→ submit for independent acceptance
```

The senior editor does not need to perform every specialist operation personally. It must know which capability is needed, what evidence it requires, and what quality gate proves completion.

## Core rules

1. Start from an explicit `VideoEditContract` for substantial work.
2. Inspect source material before making source-dependent claims.
3. Use the smallest specialist that can resolve the current bottleneck.
4. Solve structural problems before cosmetic ones.
5. Prefer reversible, deterministic interventions before generative interventions when both solve the problem adequately.
6. Do not treat software as the skill. Route by capability; use tool adapters only for execution.
7. Separate generator and judge roles. `$supervising-video-editor` must independently evaluate material outcomes.
8. Do not let high polish compensate for failed blocking gates.
9. Record a material editorial decision only when it preserves a non-obvious tradeoff, risk, or downstream coordination need. Do not emit decision records that merely restate the artifact.
10. User-visible narration, labels, captions, and creative text default to Brazilian Portuguese unless the user requests otherwise.
11. When one specialist fully resolves the current bottleneck, do not repackage the same artifact into duplicate owner-level explanation. Surface only owner-level deltas, unresolved gaps, and submission state.

## Canonical v0.1 route

For source-driven projects:

```text
$video-edit-contract
→ $footage-intelligence
→ $story-edit
→ editorial integration
→ $supervising-video-editor
```

The v0.1 slice intentionally stops before deep specialist finishing. If the remaining issue is timing, attention, continuity, motion, sound, color, VFX, captions, media engineering, AI-assisted post, or delivery, report the missing specialist rather than pretending the current slice fully covers it.

## Diagnose the bottleneck

Classify the dominant problem before acting:

- intent/brief ambiguity → `$video-edit-contract`
- unknown source material → `$footage-intelligence`
- weak structure, selection, progression, or payoff → `$story-edit`
- existing cut needs independent acceptance → `$supervising-video-editor`
- uncovered specialist domain → mark as `SPECIALIST_GAP` with the required capability.

## Editorial integration

When combining specialist outputs, verify:

- the current cut still satisfies the contract;
- source truth remains preserved;
- each scene has a narrative function;
- major decisions are compatible rather than locally optimal but globally conflicting;
- unresolved risks are visible;
- no temporary polish has silently become a structural dependency.

## Material EditDecision

For consequential choices, emit a compact record:

```json
{
  "problem": "pace drops after proof statement",
  "diagnosis": "redundant explanation delays demonstration",
  "decision": "enter demonstration earlier",
  "expected_effect": "restore progression without increasing stimulus",
  "evidence": ["contract objective", "source segment locators"],
  "confidence": 0.86,
  "reversible": true
}
```

Never expose private chain-of-thought. The record contains decision evidence and operational rationale only.

## Submission gate

Before handing to supervision, confirm:

- contract exists and is current;
- key source evidence is traceable;
- narrative hypothesis is explicit;
- blocking structural risks are resolved or declared;
- unsupported claims or synthetic additions are absent or labeled;
- specialist gaps are declared;
- the candidate cut/version is identifiable.

## Output

Default to the artifact produced by the specialist that resolved the bottleneck. Do not narrate routing, skill names, or orchestration mechanics unless they change a user decision or the user asks for debugging detail.

Use an owner wrapper only when at least one is true:

- two or more specialist outputs must be reconciled;
- an unresolved cross-specialist conflict or risk remains;
- a specialist gap changes what can be claimed or delivered;
- submission readiness itself is the material decision.

When an owner wrapper is needed, keep it to the smallest useful delta: objective/bottleneck if still unresolved, integration decision, remaining gap, and submission status. Never duplicate the specialist's beat map, rationale, or evidence table.

Submission status is one of `NOT_READY`, `READY_FOR_SUPERVISION`, or `BLOCKED`. Only `$supervising-video-editor` may return final editorial acceptance in this architecture.
