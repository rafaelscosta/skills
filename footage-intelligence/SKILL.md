---
name: footage-intelligence
description: Inspect, index, and reason over raw video, audio, transcripts, stills, and supporting assets to create an evidence-grounded map of usable editorial material. Use when story construction depends on understanding what was actually captured in the source material. Do not use to invent missing coverage, select a final narrative structure, or perform finishing.
---

# Footage Intelligence

Build a trustworthy semantic map of the source material before editing.

## Mission

Convert a pile of media into an `AssetManifest` that lets downstream agents find moments by meaning, performance, continuity, technical condition, and editorial usefulness.

## Rules

1. Inspect source media rather than inferring unseen content from filenames or transcripts alone.
2. Keep observation separate from interpretation.
3. Preserve source timecodes or stable locators whenever available.
4. Do not call a take `best` without naming the criterion.
5. A technically imperfect take may be editorially strongest; record both dimensions.
6. Never fabricate a shot, reaction, phrase, or coverage relationship that does not exist.
7. Generated or transformed media must be labeled as such.

## Analyze each usable segment

Capture when observable:

- stable source locator or time range;
- speaker / subject / object;
- literal content or action;
- topic and semantic tags;
- performance quality;
- emotional state;
- visual quality;
- audio quality;
- camera size / angle / movement;
- continuity direction and eyeline clues;
- notable gestures and reactions;
- product or brand visibility;
- technical defects;
- rights/provenance notes;
- possible editorial functions.

Use `references/asset-manifest.schema.json` for structured output.

## Procedure

### 1. Inventory

Identify source files and their relationships: camera originals, synced audio, proxies, transcripts, stills, music, graphics, references, generated media, and previous cuts.

### 2. Segment semantically

Segment by meaningful editorial event, not arbitrary fixed duration when better boundaries are observable.

### 3. Score dimensions independently

Keep separate ratings or notes for:

- performance;
- clarity;
- visual quality;
- audio quality;
- continuity usefulness;
- uniqueness;
- emotional value.

Do not collapse all quality into one scalar.

### 4. Build retrieval hooks

Make the manifest answer queries such as:

```text
strongest emotional reaction
clearest explanation of mechanism X
clean product demonstration
left-to-right motion usable after shot Y
reaction shot that can cover sentence Z
B-roll that adds information instead of repeating narration
```

### 5. Detect gaps and risks

Record missing coverage, contradictory statements, continuity traps, unusable audio, uncertain sync, duplicated content, and source-truth conflicts.

## Output

Return:

```markdown
## Source inventory
## Semantic map
## Strong candidate moments
## Performance opportunities
## Continuity relationships
## Technical risks
## Missing coverage
## Retrieval queries supported
```

Do not choose the final story. Hand the manifest to `$story-edit` or `$senior-video-editor`.

## Acceptance gate

Fail closed if the manifest cannot distinguish observed evidence from inference, or if key assets were not inspected but are presented as understood.
