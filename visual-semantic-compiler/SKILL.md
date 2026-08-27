---
name: visual-semantic-compiler
description: Compile an already-selected educational or explanatory visual plan into a provenance-aware Visual Semantic IR, validate its meaning, deterministically lay out supported representations, deliver self-contained HTML + inline SVG, capture browser evidence, and bind a separate perceptual review before claiming trusted visual delivery. Use after Clarify, Concept Bridge, or another reasoning skill decides that a visual materially helps; also use to validate diagram specifications or separate semantic correctness from layout/rendering/perceptual review. Do not choose visual necessity from scratch when an upstream skill owns that decision, and never treat deterministic or browser checks as perceptual visual review.
---

# Visual Semantic Compiler

Compile visual reasoning into a **typed semantic artifact before pixels**.

The compiler sits between pedagogical reasoning and rendering:

```text
reasoning skill
  ↓
representation decision
  ↓
VISUAL SEMANTIC IR
  ↓
deterministic validator
  ↓
frozen semantic candidate
  ↓
deterministic layout candidate
  ↓
geometry validator
  ↓
canonical renderer or adapter
  ↓
artifact validator
  ↓
browser evidence
  ↓
identified perceptual reviewer
```

Its job is not to make diagrams attractive. Its job is to make intended meaning explicit, machine-checkable, provenance-aware, renderer-independent, and provable at each downstream layer.

## Core principle

Never ask one generation step to simultaneously decide meaning, invent topology, place geometry, style the artifact, and self-certify correctness.

Separate:

1. **semantic intent** — what question the visual answers;
2. **semantic structure** — entities, relationships, beats, groups, omissions, evidence;
3. **deterministic semantic validation** — whether the structure obeys the selected representation contract;
4. **rendering and layout** — geometry, SVG/HTML/image production;
5. **browser evidence** — whether the exact delivered bytes remain contained and legible at declared viewports;
6. **perceptual review** — whether an identified human or vision-capable model can actually read and use the rendered result.

A pass at one layer never implies a pass at a later layer.

## Invocation boundary

Use this skill when an upstream explanation skill has already selected a visual, or when the user explicitly asks for a diagram/specification that needs a semantic contract.

Typical upstreams:

- `$concept-bridge` — first mental model, minimal visual depth;
- `$clarify` — source-bound transformation, audit, flow, comparison, or teaching artifact;
- architecture/documentation skills that need a verified visual intermediate representation.

Do **not** silently override the upstream skill's pedagogical decision. If Concept Bridge says prose-only, this compiler does not manufacture a visual merely because it can.

## Source of truth

The canonical semantic artifact is a JSON document matching:

`visual-semantic-ir/v1`

Read `references/ir-contract.md` for the field contract when authoring or repairing a candidate.

The JSON Schema in `schemas/visual-ir.schema.json` documents the portable shape. Runtime validation is performed by the bundled zero-dependency validator:

```bash
python3 scripts/validate_ir.py <candidate.json> --json
```

Do not claim validation unless that command, or an equivalent trusted execution of the bundled validator, actually passed.

## Compile pipeline

### 1. Bind the upstream decision

Capture only the already-decided cognitive contract:

- source skill;
- audience;
- depth;
- primary question;
- representation class;
- representation type;
- reading direction;
- desired outcome.

Do not reopen the full pedagogical strategy unless the incoming decision is internally contradictory.

### 2. Build the minimum semantic model

Author only what the reader needs at the selected depth:

- `entities` — the meaningful things;
- `relationships` — what one thing does to, sends to, contains, causes, or depends on;
- `narrative_beats` — temporal beats when narrative comprehension matters;
- `groups` — real boundaries, lanes, layers, phases, or comparison sides;
- `views` — only for mixed artifacts where different representations answer different questions;
- `omissions` — important complexity intentionally excluded;
- `text_equivalent` — a usable prose equivalent of the truth-critical model.

Do not add geometry, coordinates, CSS, palette, icons, or renderer-specific fields to the semantic IR.

### 3. Preserve provenance

When the upstream task is source-bound, attach provenance to material nodes, relationships, and narrative beats.

Use:

- `explicit` — directly supported by named evidence;
- `inferred` — reasonable interpretation, with confidence;
- `general-knowledge` — stable non-source-specific domain knowledge;
- `unknown` — unresolved rather than invented.

Never upgrade an inference to an explicit fact merely to make the visual cleaner.

For Clarify, source-bound causal or procedural relationships should usually carry explicit or inferred provenance.

For Concept Bridge, general-knowledge provenance is acceptable when the task is conceptual rather than source-bound.

### 4. Author candidate first

Write the candidate JSON before inspecting renderer internals or planning coordinates.

The semantic compiler should not reason about routing geometry unless a later renderer reports a layout diagnostic.

### 5. Validate deterministically

Run:

```bash
python3 scripts/validate_ir.py candidate.json --json
```

The R1 receipt separates:

- `schema_shape`;
- `unique_ids`;
- `relationship_integrity`;
- `representation_contract`;
- `type_contract`;
- `provenance_integrity`;
- `pedagogical_contract`;
- `layout_geometry` — intentionally `deferred` in the semantic-only receipt.

Exit code:

- `0` — semantic IR valid;
- `1` — candidate invalid;
- `2` — validator invocation/read failure.

A valid IR does **not** prove good layout or visual polish.

### 6. Repair only diagnosed subjects

When invalid:

1. read validator error codes;
2. change only the failed semantic subject;
3. rerun validation;
4. stop after two focused repair rounds if the semantic model is not converging;
5. report unresolved errors instead of fabricating a pass.

Do not rewrite the whole artifact because one edge is invalid.

### 7. Freeze semantic bytes

After the candidate passes, do not modify it casually during rendering.

Record the validator's `input_sha256` as the semantic candidate digest.

If downstream review later requires a semantic change, edit the IR and validate again. A prior receipt no longer applies to changed bytes.

## Representation contract

### Narrative visual

Use when the selected question is primarily temporal.

Supported first-class types:

- `story-strip`;
- `before-after`;
- `storyboard`;
- `timeline`.

Requires at least two ordered narrative beats.

### Structural diagram

Use when spatial relationships carry meaning.

First-class contracts:

- `flow` — ordered path with material branching;
- `state` — states and event-driven transitions;
- `architecture` — components and connections;
- `sequence` — participants/messages over time;
- `dataflow` — information movement/transformation;
- `hierarchy` — containment or dependency levels;
- `causal` — causal mechanism and feedback;
- `structural-comparison` — aligned structural alternatives.

The IR also permits broader Clarify visual types such as decision trees/tables, concept maps, argument maps, swimlanes, BPMN, SIPOC, service blueprints, C4, Event Storming, and statistical charts. R1 applies universal semantic checks to those; deeper type validators can be added without changing the canonical IR.

### Mixed

Use only when at least one narrative view and one structural view answer **different** cognitive questions.

Examples:

- OAuth: user consent story + actor/message structure;
- incident response: human sequence + state/lifecycle model.

Do not use mixed merely to make an artifact richer.

## Type-specific invariants

The bundled semantic validator currently enforces these rules:

### Flow

If one node branches to multiple outgoing paths, every branch must be labeled.

### State

State diagrams use `entity.kind: state` and `relationship.kind: transition`.

### Sequence

Every relationship must have one unique positive `order`.

### Dataflow

Relationships use `data`, `reads`, `writes`, or `flow` semantics.

### Hierarchy

Hierarchy relationships use containment/dependency semantics and may not form a directed cycle.

### Causal

Relationships use `causation` or `feedback`. Do not encode correlation as causation.

### Structural comparison

Requires at least two `comparison-side` groups.

## Relationship discipline

Every relationship must answer:

> What does this edge actually mean?

Use `semantic` as a short verb or relationship phrase.

Examples:

- `envia pergunta`;
- `solicita contexto`;
- `transiciona ao aprovar`;
- `contém`;
- `causa aumento de fila`;
- `lê registros`.

Do not create edges merely because two entities can technically communicate.

## Direct labels

Every entity has its actual reader-facing label in the IR.

Do not replace semantic names with numeric legend keys when direct labels are possible.

A renderer may abbreviate visually only if the canonical term remains available and the abbreviation is unambiguous.

## Omissions are part of truth

A first mental model is intentionally incomplete.

Use `omissions` to make that incompleteness explicit rather than silently pretending the visual is exhaustive.

Good:

```json
"omissions": ["pipeline de ingestão", "reranking", "detalhes de embeddings"]
```

This lets Concept Bridge stay minimal without turning minimality into a false claim of completeness.

## Text-equivalent invariant

Every IR must include `text_equivalent`.

The prose equivalent must preserve the truth-critical model if rendering fails or is inaccessible.

A visual may increase comprehension. It may not become the only place where a critical fact exists.

## Renderer boundary

R1 deliberately does not prescribe one renderer.

Possible downstreams:

- inline SVG;
- deterministic HTML/CSS;
- image generation;
- Archify adapter;
- future dedicated renderers.

The renderer consumes validated meaning; it does not get to silently reinterpret semantic topology.

## R2 deterministic render path

After the semantic IR passes R1 validation, R2 may continue to a deterministic renderer for supported types.

Read `references/layout-contract.md` and `references/renderer-contract.md` only when rendering is actually requested.

Canonical command:

```bash
python3 scripts/render_html.py candidate.json output.html --layout-output output.layout.json --json
```

The delivery path is fail-closed:

```text
semantic validator PASS
→ visual-layout/v1
→ geometry validator PASS
→ HTML + inline SVG
→ static artifact validator PASS
→ atomic commit
→ perceptual review PENDING
```

R2 canonical rendering currently supports:

- `architecture`;
- `flow`;
- `state`;
- `sequence`;
- `dataflow`;
- `hierarchy`;
- `causal`;
- `structural-comparison`;
- `story-strip`;
- `before-after`;
- `timeline`.

Unsupported types fail explicitly. A semantically valid BPMN, C4, concept map, statistical chart, or other IR must use another renderer rather than being flattened into generic boxes and arrows.

### Geometry receipt

The R2 layout validator checks viewport containment, node separation, edge-through-node, unrelated crossings, relationship-label collisions, endpoint integrity, and dominant reading direction.

When `target_zero_crossings` is true, unrelated crossings are hard failures.

Do not delete truthful semantic relationships merely to make layout pass. If geometry cannot preserve the frozen model, change the renderer or revise the semantic model and revalidate it.

### Canonical artifact

The built-in renderer produces self-contained HTML with inline SVG. It embeds the semantic IR SHA-256, preserves the text equivalent in visible prose and SVG accessibility text, records omissions, and requires no external diagram runtime.

`validate_artifact.py` proves only static artifact properties. Its success never upgrades `perceptual_review` beyond `pending`.

### Optional Archify adapter

`adapt_archify.py` is an optional renderer adapter. R2 supports only `architecture` and fails closed for other types. The adapter produces an Archify candidate but does not invoke Archify. Archify must still run its own `validate` and `deliver` gates.

Read `references/adapters/archify.md` when using it. The Visual Semantic IR remains authoritative.

## R3 perceptual delivery gate

R3 is required only when claiming a **trusted final visual delivery** from the canonical renderer. Semantic-only compilation and ordinary rendered handoff may stop earlier with truthful status.

Read `references/perceptual-contract.md` before starting R3.

### Stage 1 — Capture browser evidence

After R2 semantic, layout, and artifact gates pass, run:

```bash
node scripts/visual_check.mjs output.html output.visual-evidence/
```

The checker renders the exact self-contained artifact bytes in Chromium/Chrome and measures:

- 1440×900;
- 1600×1000;
- 1920×1080;
- 2048×1320.

It retains screenshots at 1440×900 and 2048×1320 and writes a `visual-evidence-receipt/v1` bound to the artifact SHA-256.

Automated evidence checks include:

- SVG visible/non-zero;
- no document horizontal overflow;
- no diagram-panel horizontal scroll at certified desktop sizes;
- node text contained by node boxes;
- projected node labels at least 12px;
- projected relationship labels at least 9px;
- body text at least 14px;
- successful screenshot capture.

A browser evidence PASS still reports:

```text
perceptual_review: pending
```

It is not a visual-quality verdict.

If Chrome/Chromium is unavailable, report evidence as skipped. Do not synthesize screenshots or upgrade the run to passed.

### Stage 2 — Inspect the pixels

An identified human or vision-capable model must inspect the exact retained screenshots.

The reviewer checks hierarchy, routes, labels, clipping, crowding/whitespace, contrast, reading direction, and semantic emphasis. A visible defect is recorded rather than repaired silently inside the review receipt.

Author a `visual-perceptual-review/v1` receipt using the exact artifact SHA and evidence-receipt SHA.

A pass requires:

- browser evidence status `passed`;
- identified reviewer;
- exact artifact binding;
- exact evidence binding;
- zero known defects.

A failed review requires at least one concrete defect with severity and evidence. A skipped review requires a reason.

### Stage 3 — Validate the perceptual claim

Run:

```bash
python3 scripts/validate_perceptual_review.py \
  output.visual-evidence/output.visual-evidence.json \
  review.json --json
```

Only a valid combined receipt with:

```text
delivery_status: perceptually-passed
```

may be described as a trusted perceptual delivery.

The validator proves review identity and byte bindings. It does not inspect the pixels itself.

### Stale evidence rule

Any change to the delivered HTML bytes invalidates all R3 evidence and review receipts.

The browser checker removes previous known sidecars before recapture so a failed or skipped run cannot leave old screenshots positioned as current evidence.

Never reuse a prior screenshot set after artifact revision.

### Perceptual correction loop

Maximum: **two focused correction rounds**.

Repair the narrowest responsible layer, then rerun every invalidated downstream gate:

- CSS/artifact change → artifact validation + R3 again;
- geometry/layout change → layout + artifact + R3 again;
- semantic topology change → semantic + layout + artifact + R3 again.

Do not edit a failed review receipt into a pass.

### Mobile boundary

R3 v1 certifies only the declared desktop viewports. Do not generalize a desktop perceptual pass into a mobile/narrow usability claim.

## Archify relationship

This skill adopts architectural lessons from typed-IR visual systems but is **not coupled to Archify**.

Do not copy Archify-specific component enums, geometry controls, viewer chrome, themes, or runtime fields into the canonical IR.

An adapter may translate a validated Visual Semantic IR into an Archify candidate when that renderer is appropriate. The canonical IR remains upstream and renderer-neutral.

## Upstream adapters

Read only when that upstream is active:

- `references/adapters/concept-bridge.md`
- `references/adapters/clarify.md`

These adapters define what each skill owns before handoff and what this compiler is allowed to change.

## Quality gate

Before handoff, verify:

1. **Question** — exactly one primary question per simple view.
2. **Truth** — no relationship is stronger than its evidence.
3. **Vocabulary** — canonical terms match upstream prose.
4. **Minimality** — every entity/edge earns its place at the selected depth.
5. **Representation fit** — IR class/type matches the upstream decision.
6. **Evidence** — source-bound facts preserve explicit/inferred/unknown distinctions.
7. **Text equivalent** — truth-critical meaning survives without rendering.
8. **Semantic validation** — bundled semantic validator passes on frozen bytes.
9. **Layout/artifact validation** — when canonical rendering is used, geometry and static artifact gates pass.
10. **Browser evidence** — when trusted final visual delivery is claimed, every certified desktop viewport passes current evidence capture.
11. **Perceptual grounding** — a trusted visual pass is backed by an identified reviewer inspecting exact current screenshots.
12. **Revision binding** — artifact, browser evidence, and perceptual review hashes refer to the same revision.

## Hard failures

Never claim successful compilation or trusted delivery when:

- a relationship points to a missing entity;
- IDs collide;
- a branching flow omits branch labels;
- a state diagram uses actions as states without an explicit modeling reason;
- sequence order is absent or ambiguous;
- a causal edge is merely correlational;
- mixed views answer the same question redundantly;
- source-bound inference is presented as explicit evidence;
- the text equivalent is missing;
- a semantic/layout/artifact validator returns non-zero while the corresponding layer is claimed passed;
- browser evidence fails or is skipped while a perceptual pass is claimed;
- a perceptual pass has no identified reviewer;
- the reviewer did not inspect screenshots from the exact artifact revision;
- a passed review contains known defects;
- artifact/evidence review hashes do not match current bytes;
- stale screenshots are presented as current evidence;
- a desktop pass is described as mobile-certified.

## Output

A successful compiler handoff should report only the layers actually executed:

```text
semantic_ir: <path>
semantic_ir_sha256: <semantic validator receipt>
semantic_validation: passed
layout_geometry: deferred | passed
layout_sha256: <layout receipt when rendered>
artifact_sha256: <artifact receipt when rendered>
renderer_status: not_run | handed_off | rendered
browser_evidence: not_run | passed | failed | skipped
browser_evidence_receipt: <path when run>
perceptual_review: pending | passed | failed | skipped
perceptual_review_receipt: <path when reviewed>
delivery_status: semantic-only | rendered-unreviewed | perceptually-passed | perceptually-failed | perceptual-review-skipped
```

Do not call `layout_geometry: deferred` a layout pass. Do not call browser evidence a perceptual pass.

## Definition of done

The semantic compiler is done when a renderer receives a frozen semantic candidate whose meaning is explicit enough that independent renderers preserve the same important nodes, relationships, narrative beats, omissions, and evidence boundaries.

When the built-in renderer is requested, rendered handoff requires semantic, layout, and static artifact gates to pass.

When a **trusted final visual delivery** is requested, done additionally requires current browser evidence across every certified desktop viewport plus a hash-bound zero-defect perceptual review from an identified human or vision-capable model.
