# Guide architectures

Choose the architecture before visual styling. Every architecture below has a distinct teaching job and output contract.

## Shared header contract

A visual guide normally contains:

- eyebrow or collection label;
- dominant title;
- one-sentence learning promise;
- optional system/version/status label;
- source/provenance note outside the primary reading flow.

The title should describe the governed subject, not the artifact format. Prefer `SISTEMA DE BOTÕES` over `GUIA VISUAL DE BOTÕES` unless the collection needs the latter label.

## 1. Token sheet

**Question:** What decisions exist and what roles do they play?

Use for color, typography, spacing, radius, elevation, motion, breakpoints, or icon sizes.

Required fields per token:

- human-readable role;
- exact token path;
- resolved value or preview;
- usage note;
- provenance status;
- optional alias chain.

Recommended item count:

- 6–12 semantic roles on one page;
- 12–24 only when the copy is extremely short;
- larger foundations should become a series.

Do not show hundreds of primitive values without an organizing decision layer.

## 2. Token cascade

**Question:** How does a raw value reach a component state?

Structure:

```text
primitive → semantic → component → state
```

Show one to five complete chains. Use connecting lines and resolved previews. Call out broken aliases, duplicate semantics, or hard-coded escapes.

Best for engineering/design alignment and token migration.

## 3. Annotated anatomy

**Question:** What are the structural parts and constraints of this component?

Required sections:

- one large, accurate component sample;
- labeled slots;
- dimensional specs;
- token references;
- optional content and accessibility notes.

Keep callouts sparse. Six to ten labels are usually enough. If the component has many conditional slots, use separate anatomy states rather than crossing callout lines.

## 4. Variant/state matrix

**Question:** What combinations exist and how do they differ?

Typical axes:

- rows: variants or semantic hierarchy;
- columns: states;
- optional secondary strip: sizes.

Rules:

- keep labels and content identical across cells;
- change only the row/column variable;
- include only combinations supported by the public API;
- distinguish unavailable combinations from undocumented ones;
- do not simulate focus merely by drawing a ring if real keyboard focus behaves differently.

A readable page usually supports 3–5 rows and 4–6 columns. Split larger matrices.

## 5. Do/don't board

**Question:** What behavior or composition is correct, and why?

Each pair must compare the same context and differ in one meaningful decision.

Required fields:

- topic;
- `DO` sample;
- short rationale;
- `DON'T` sample;
- short rationale;
- optional governing token, component, or accessibility rule.

Do not create false anti-patterns merely to fill the board. Three to six strong pairs are better than twenty trivial ones.

## 6. Component-selection guide

**Question:** Which component should be used for this situation?

Use a decision table when criteria are stable and comparable. Use a decision tree when the choice is sequential.

Recommended columns:

- situation or user need;
- governing variables;
- recommended component/pattern;
- avoid;
- rationale;
- mobile or accessibility caveat.

Examples:

- checkbox vs switch;
- radio vs select vs segmented control;
- modal vs drawer vs inline expansion;
- toast vs alert vs inline validation;
- table vs cards;
- pagination vs infinite scroll.

## 7. Responsive breakpoint strip

**Question:** How does the same component or layout adapt across widths?

Show three to five widths. Keep content and state stable. Annotate:

- breakpoint or container condition;
- layout transformation;
- hidden/reordered elements;
- interaction change;
- minimum viable width.

Do not treat device names as authoritative when the system uses container queries or content-driven behavior.

## 8. Layout-pattern catalog

**Question:** What approved compositions solve recurring layout problems?

Each entry contains:

- wireframe or real example;
- pattern name;
- use case;
- information hierarchy;
- constraints;
- responsive behavior.

Use the same sample content across entries when the lesson is composition. Recommended count: 6–12 patterns.

## 9. Accessibility pass/fail sheet

**Question:** What implementation passes the system's accessibility contract?

Useful topics:

- contrast;
- focus visibility;
- target size;
- label/description relationships;
- error identification;
- keyboard order;
- reduced motion;
- color independence;
- disabled versus read-only semantics.

Pair visual evidence with the governing behavior. A color contrast number alone does not prove keyboard or screen-reader quality.

## 10. Motion storyboard

**Question:** How should a transition move and what perception should it create?

Show:

- start frame;
- one or more key frames;
- end frame;
- duration;
- easing/spring values;
- trigger;
- reduced-motion fallback;
- intended perceptual effect.

Prefer animated HTML for production documentation. A static poster should show frame progression, not pretend motion is fully documented by one image.

## 11. Content-pattern board

**Question:** How should interface language be written in this context?

Useful boards:

- button labels;
- validation errors;
- empty states;
- destructive confirmations;
- tooltips;
- notifications;
- loading messages.

Each entry should show context, weak wording, recommended wording, and the governing principle. Keep code identifiers separate from visible copy.

## 12. Master cheat sheet

**Question:** What compact mental model should a practitioner keep nearby?

Use when several related dimensions must be seen together, such as:

- anatomy;
- hierarchy;
- states;
- selection rules;
- do/don't examples.

A master sheet is not a dumping ground. Limit it to three or four coordinated sections and one dominant component family. For a whole system, create an atlas instead.

## 13. Visual atlas

**Question:** How can a full system be navigated and learned progressively?

Recommended output:

```text
00 Atlas index
01 Foundations overview
02 Token architecture
03 Component selection map
04–N Component-family guides
N+1 Patterns
N+2 Accessibility
N+3 Governance
```

Prioritize guide creation by:

1. usage frequency;
2. decision ambiguity;
3. implementation risk;
4. accessibility impact;
5. onboarding value;
6. documentation gaps.

Do not render the entire atlas before validating one representative guide. Establish the visual and data contract, test it, then scale.

## Density and splitting rules

Split a guide when any of these occur:

- body text would fall below practical mobile readability;
- more than one unrelated primary question exists;
- a matrix exceeds approximately 30 meaningful cells;
- more than six do/don't pairs require explanation;
- anatomy callouts cross excessively;
- the reader must zoom repeatedly to understand labels;
- the evidence status differs substantially across sections.

Prefer a numbered series over compressed typography.
