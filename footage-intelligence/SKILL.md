---
name: footage-intelligence
description: Build an evidence-grounded inventory of raw video, audio, transcript, takes, technical state, coverage, and semantic moments before source-dependent editing. Use when the editor does not yet have a trustworthy map of the available material or when missing coverage, stale UI, weak audio, or source ambiguity could change editorial decisions. Do not use to decide the final story structure.
---

# Footage Intelligence

Turn raw media into a source-truth map that downstream editors can query without pretending unseen coverage exists.

## Output

Produce an `AssetManifest` containing only supported observations: clips and time ranges, speakers/subjects, transcript or dialogue, semantic topics, performance markers, visual and audio quality, camera/shot information when observable, continuity relationships, evidence-sensitive UI/product states, useful B-roll, technical defects, and missing coverage.

## Procedure

1. Inventory the available files and trustworthy metadata.
2. Segment long assets into semantically meaningful ranges.
3. Bind transcript/dialogue to source ranges when available.
4. Mark standout performances and hooks as evidence, not as automatic final selections.
5. Distinguish useful B-roll from merely attractive footage.
6. Flag obsolete UI, unsupported claims, privacy issues, continuity risks, and technical defects.
7. Record missing coverage explicitly instead of fabricating a substitute.
8. Keep inference separate from directly observable source truth.

## Boundary

This skill answers **what material exists and what it can support**. `$story-edit` owns narrative use and performance selection; `$attention-choreography` owns perceptual competition inside a candidate treatment.
