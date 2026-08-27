---
name: visual-semantic-compiler
description: Compile an already-selected educational or explanatory visual plan into a provenance-aware Visual Semantic IR, validate its meaning, deterministically lay out supported representations, and deliver a self-contained HTML + inline-SVG artifact with semantic/layout/artifact receipts. Use after Clarify, Concept Bridge, or another reasoning skill decides that a visual materially helps; also use to validate diagram specifications or separate semantic correctness from layout/rendering/perceptual review. Do not choose visual necessity from scratch when an upstream skill owns that decision, and never treat deterministic checks as perceptual visual review.
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
perceptual review
```

Its job is not to make diagrams attractive. Its job is to make the intended meaning explicit, machine-checkable, provenance-aware, and renderer-independent.

## Core principle

Never ask one generation step to simultaneously decide meaning, invent topology, place geometry, style the artifact, and self-certify correctness.

Separate:

1. **semantic intent** — what question the visual answers;
2. **semantic structure** — entities, relationships, beats, groups, omissions, evidence;
3. **deterministic validation** — whether the structure obeys the selected representation contract;
4. **rendering** — layout, SVG/HTML/image production;
5. **perceptual review** — whether a human can actually read and use the rendered result.

A pass at one layer never implies a pass at a later layer.

## Invocation boundary

Use this skill when an upstream explanation skill has already selected a visual, or when the user explicitly asks for a diagram/specification that needs a semantic contract.

Typical upstreams:

- `$concept-bridge` — first mental model, minimal visual depth;
- `$clarify` — source-bound transformation, audit, flow, comparison, or teaching artifact;
- architecture/documentation skills that need a verified visual intermediate representation.

Do **not** silently override the upstream skill's pedagogical decision. If Concept Bridge says prose-only, this compiler does not manufacture a visual merely because it can.

## Source of truth

The canonical artifact is a JSON document matching:

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

Do not add geometry, coordinates, CSS, palette, icons, or renderer-specific fields to the IR.

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

The receipt separates:

- `schema_shape`;
- `unique_ids`;
- `relationship_integrity`;
- `representation_contract`;
- `type_contract`;
- `provenance_integrity`;
- `pedagogical_contract`;
- `layout_geometry` — intentionally `deferred` in R1.

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

If perceptual review later requires a semantic change, edit the IR and validate again. A prior receipt no longer applies to changed bytes.

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

The bundled validator currently enforces these semantic rules:

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
8. **Deterministic validation** — bundled validator passes on the frozen bytes.

## Hard failures

Never claim successful compilation when:

- a relationship points to a missing entity;
- IDs collide;
- a branching flow omits branch labels;
- a state diagram uses actions as states without an explicit modeling reason;
- sequence order is absent or ambiguous;
- a causal edge is merely correlational;
- mixed views answer the same question redundantly;
- source-bound inference is presented as explicit evidence;
- the text equivalent is missing;
- the validator returns non-zero;
- the candidate changed after the receipt without revalidation.

## Output

A successful compiler handoff should report:

```text
semantic_ir: <path>
semantic_ir_sha256: <validator receipt value>
validation: passed
checks: schema_shape, unique_ids, relationship_integrity, representation_contract, type_contract, provenance_integrity, pedagogical_contract
layout_geometry: deferred | passed
layout_sha256: <layout receipt value when rendered>
artifact_sha256: <artifact receipt value when rendered>
renderer_status: not_run | handed_off | rendered
perceptual_review: pending | passed | failed | skipped
```

Do not call `layout_geometry: deferred` a layout pass.

## Definition of done

The semantic compiler is done when a renderer receives a frozen semantic candidate whose meaning is explicit enough that independent renderers preserve the same important nodes, relationships, narrative beats, omissions, and evidence boundaries. When the built-in R2 renderer is requested, delivery is done only after semantic, layout, and static artifact gates pass; perceptual quality remains a separate review claim.
