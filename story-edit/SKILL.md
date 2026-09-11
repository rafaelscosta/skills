---
name: story-edit
description: Build or repair the narrative structure of a video from a VideoEditContract and evidence-grounded source material. Use when assemblies, rough cuts, interviews, documentaries, ads, explainers, VSLs, brand films, or other cuts have unresolved structure, progression, clarity, performance, tension, or payoff. Do not use for purely technical finishing or decorative pacing changes when structure is already locked.
---

# Story Edit

Choose what the viewer experiences, in what order, and why.

## Mission

Produce the strongest narrative structure supported by the available material and the governing `VideoEditContract`.

## Decision hierarchy

Unless the contract overrides it, prioritize:

1. truth and ethical integrity;
2. intended viewer outcome;
3. emotion and performance;
4. story / argument progression;
5. clarity of information;
6. attention and rhythm;
7. continuity;
8. surface polish.

A continuity-perfect cut may be rejected if it weakens performance or meaning. A beautiful shot may be removed if it performs no necessary function.

## Procedure

### 1. State the narrative hypothesis

Write one concise sentence describing what the viewer is meant to experience across the piece.

### 2. Map beats

For each beat, define:

- viewer state entering;
- new information, emotion, question, or proof;
- strongest available source moments;
- viewer state leaving;
- dependency on earlier beats.

### 3. Remove redundancy

Two adjacent elements should not perform the same narrative job unless repetition is intentional and earns its duration.

### 4. Protect performance

Prefer the moment with the strongest truthful intention when small technical imperfections can be repaired or safely tolerated.

### 5. Test causal and informational progression

Ask continuously:

```text
Why does this moment belong here?
What becomes possible because the previous moment happened?
What does the viewer now know, feel, or expect that they did not before?
```

### 6. Generate alternatives when ambiguity is material

If two structures are genuinely plausible, create contrasting hypotheses rather than microvariants of the same edit.

### 7. Record material decisions

For consequential decisions, capture:

- problem;
- diagnosis;
- decision;
- expected viewer effect;
- evidence used;
- confidence;
- reversibility.

Do not log every cut.

## Senior diagnostic rules

When feedback says `slow`, do not default to more cuts. Diagnose whether the cause is:

- late information;
- redundant beat;
- weak dramatic question;
- performance losing intention;
- visual state not evolving;
- audio not progressing;
- unnecessary explanation;
- excessive cognitive load.

When feedback says `dynamic`, do not default to zooms, speed ramps, or transition effects.

When a scene needs graphics or music to become understandable, first test whether the underlying structure is weak.

## Output

Return:

```markdown
## Narrative hypothesis
## Beat map
## Selected source moments
## Removed or deferred material
## Structural risks
## Material EditDecisions
## Handoff notes
```

## Acceptance gates

Reject the structure when any are true:

- the core argument requires external explanation;
- a payoff lacks setup;
- key sections repeat the same function without purpose;
- sequence order violates prerequisite understanding;
- material is retained mainly because it was expensive to produce;
- unsupported footage or claims are introduced;
- motion, music, or effects are masking an unresolved structural problem.

After structural acceptance, hand off to timing, attention, continuity, or finishing specialists as available.
