---
name: visualize-design-system
description: Create repository-grounded visual design-system guides: token sheets, component anatomy, variant/state matrices, do/don't boards, selection guides, responsive patterns, accessibility sheets, and visual atlases. Use when asked to document, visualize, audit, explain, or publish a design system or component library from code, Storybook, tokens, screenshots, or specifications. Ground current-system claims in evidence, label inferred/proposed rules, prefer real rendered components, and produce deterministic editable outputs with QA. Do not use for ordinary UI implementation, branding, or generic infographics.
---

# Visualize Design Systems

Turn a design system into accurate, compact, visually teachable documentation that functions as a shared contract between design, engineering, content, QA, and product.

The default result is not a concept image. It is a source-grounded production package with an editable guide specification, deterministic HTML, exportable PNG/PDF, and a QA report.

## Execution contract

- Complete the requested work end to end. Do not stop after producing a plan, outline, or prompt when the repository and tools permit implementation.
- Inspect available sources before asking questions. Ask at most one question, and only when the missing answer would materially change the artifact or risk modifying the wrong target.
- Do not narrate routine progress or issue an upfront plan unless the user asks for one. Surface only material blockers, approval boundaries, and the final result.
- Resolve ambiguity with explicit defaults and record assumptions in the output package.
- Prefer dedicated file, browser, test, and image-inspection tools over improvised shell parsing when those tools are available.
- Use parallel subagents only for independent read-heavy work such as token inventory, component inventory, accessibility review, or documentation comparison. Keep writing and final synthesis in one coordinating thread unless files are cleanly partitioned.
- Do not change production components, tokens, or application behavior unless the user explicitly requests implementation changes. Place generated documentation in a separate output directory by default.
- Never invent an existing token, prop, variant, state, breakpoint, accessibility behavior, or usage rule. Mark unsupported material as `inferred`, `proposed`, or `missing`.

## Default outputs

Unless the user requests another mode, create a **production package**:

```text
docs/design-system-guides/<guide-slug>/
├── source-map.json
├── guide-spec.json
├── guide.html
├── exports/
│   ├── guide.png
│   └── guide.pdf
└── qa-report.md
```

Use a different destination only when the repository already has an established documentation structure or the user provides one.

## Select the operating mode

| User intent | Mode | Required result |
|---|---|---|
| “Analyze,” “audit,” “what exists?” | Audit | Inventory, gaps, conflicts, recommended guide set |
| “Create a guide about buttons/colors/etc.” | Single guide | One validated production guide |
| “Document the whole design system” | Visual atlas | Index plus a prioritized guide series |
| “Add this to Storybook/docs” | Integrated documentation | Guide assets plus repository integration and tests |
| “Design a system and document it” | Greenfield proposal | Clearly labeled proposed system plus guides |
| “Give me only the copy/prompt” | Blueprint or copy deck | Exact structured content without pretending production is complete |

If the request is ambiguous but a repository is present, default to a repository-backed single guide for the most central requested subject. If no repository or source exists, create a labeled greenfield proposal rather than implying that the rules are implemented.

## Establish truth and provenance

The user's explicit desired outcome controls what to build. For claims about the current system, use this evidence order:

1. rendered runtime behavior and interaction tests;
2. component implementation and public types;
3. token source files and generated theme artifacts;
4. Storybook stories, tests, and examples;
5. maintained design-system documentation;
6. screenshots and static mockups;
7. inference from naming or visual similarity.

Attach one provenance status to every important rule or value:

- `implemented` — confirmed in runtime or implementation;
- `documented` — stated in maintained documentation but not fully verified in code;
- `inferred` — reasonable conclusion from incomplete evidence;
- `proposed` — new recommendation or future-state rule;
- `missing` — expected information or behavior was not found;
- `deprecated` — present but explicitly obsolete.

When sources conflict, do not silently choose one. Record the mismatch in `source-map.json`, use the source that matches the requested target state, and call out the discrepancy in `qa-report.md`.

Read `references/repository-discovery.md` before a repository-backed task and `references/design-system-domain-model.md` before normalizing design-system concepts.

## Repository discovery workflow

1. Read all applicable `AGENTS.md` files before editing.
2. Identify the repository root and existing documentation conventions.
3. Resolve this skill's directory as `SKILL_DIR`, then run the bundled inventory script:

```bash
python "$SKILL_DIR/scripts/inventory_design_system.py" \
  <repo-root> \
  --out <output-dir>/source-map.json
```

4. Verify the automated inventory with targeted searches. Inspect likely sources such as:

```text
package.json
components.json
tailwind.config.*
tokens/**/*
theme/**/*
styles/**/*
src/components/**/*
**/*.stories.*
**/*.test.*
**/*.spec.*
.storybook/**/*
docs/**/*
```

5. Detect the actual stack: Storybook, Tailwind, CSS variables, Style Dictionary, Tokens Studio exports, Radix, shadcn/ui, Material UI, Chakra, Mantine, vanilla-extract, styled-components, Emotion, or a custom system.
6. Build a focused evidence map for the requested guide. Do not load the entire repository into the main context when a bounded path is sufficient.
7. Run the component library or Storybook when possible. A rendered component is stronger evidence than a filename or static type alone.

## Choose the visual guide architecture

Select the architecture that answers one dominant question.

| Dominant question | Architecture |
|---|---|
| What tokens exist and how do they map? | Token sheet or token cascade |
| What are the parts of this component? | Annotated anatomy |
| Which variants, sizes, and states exist? | State matrix |
| What should and should not be done? | Mirrored do/don't board |
| Which component should I choose? | Decision table or decision tree |
| How does it respond across widths? | Breakpoint strip |
| What layout patterns are approved? | Pattern catalog |
| How should motion feel and behave? | Motion storyboard or animated guide |
| What accessibility rules apply? | Pass/fail sheet or QA checklist |
| How is the system organized overall? | Master cheat sheet or visual atlas |
| How should UX copy be written? | Content pattern board |

Read `references/guide-architectures.md` for the required fields, item-count limits, and composition rules for each architecture.

## Author the content model

Every guide must satisfy these rules:

- Answer one primary question.
- Use the smallest complete set of entries; never force an arbitrary “20.”
- Keep entries at the same abstraction level.
- Separate foundations, components, patterns, and product-specific compositions.
- Distinguish a **variant** from a **state**, a **size** from a **density**, and a **component** from a **pattern**.
- Show the same content and context while changing one teaching variable whenever comparison is the lesson.
- Include decision guidance, not only inventory. Add `use when`, `avoid when`, or a selection rule where applicable.
- Use exact token and prop names in technical annotations. Use human-readable labels in the visible teaching layer.
- Preserve deprecated or missing behavior as evidence, but do not present it as recommended practice.
- Keep the visual layer concise; move traceability, source paths, and lengthy caveats to the source map or QA report.

Create `guide-spec.json` from `assets/guide-spec.schema.json`. Start from `assets/guide-spec.example.json` when useful.

## Capture real components

For guides that display UI components:

1. Prefer actual components rendered from Storybook, a documentation route, a test harness, or the application itself.
2. Reuse the repository's fonts, tokens, icon set, and component CSS.
3. Capture each required state deliberately. Use browser automation for hover, focus, pressed, selected, disabled, loading, error, and responsive states when those states genuinely exist.
4. Keep the sample label, surrounding context, viewport, and content stable while changing the documented variable.
5. Create temporary harnesses inside the guide output directory or a repository-approved examples area. Do not patch production behavior merely to make documentation easier.
6. If the runtime cannot be launched, use code-derived representations and mark them `inferred`; do not imply that they are visual regression evidence.
7. Do not use generated images to fake existing UI. Image generation is appropriate only for optional illustrations, textures, or conceptual material that is not a system component.

For screenshot-driven reconstruction, inspect all provided reference images, extract reusable hierarchy and composition principles, and create an original design. Do not copy signatures, watermarks, proprietary artwork, or exact layouts.

## Apply copy and localization rules

- Default visible language: Brazilian Portuguese.
- Write image-generation, art-direction, and video prompts in English.
- Put exact visible strings in a clearly labeled `VISIBLE TEXT — PT-BR` block when prompts are part of the deliverable.
- Keep component names, token paths, API identifiers, and code literals unchanged.
- Use concise, parallel descriptions. Prefer concrete actions and observable effects.
- Do not translate established technical terms when translation would break alignment with the codebase; explain them instead.
- Use sentence case for explanatory copy unless the design system explicitly defines another convention.

Read `references/copy-and-localization.md` for copy budgets and examples.

## Produce deterministic visual artifacts

For text-heavy guides, compose the final artifact in HTML/CSS, SVG, or the repository's documentation framework. Do not rely on an image model to typeset the final page.

Use the bundled pipeline when a custom repository renderer is not already better:

```bash
python "$SKILL_DIR/scripts/validate_guide_spec.py" \
  <output-dir>/guide-spec.json

python "$SKILL_DIR/scripts/render_guide.py" \
  <output-dir>/guide-spec.json \
  --output <output-dir>/guide.html

python "$SKILL_DIR/scripts/capture_guide.py" \
  <output-dir>/guide.html \
  --png <output-dir>/exports/guide.png \
  --pdf <output-dir>/exports/guide.pdf
```

Use actual component screenshots as assets inside the specification when the generic renderer cannot reproduce the system faithfully.

Default format for a social/teaching poster is 1080 × 1350. Prefer A4/Letter for printable internal references, 1440-pixel desktop canvases for documentation pages, and a multi-page atlas when one page would force unreadable text.

Read `references/visual-production.md` before creating a production artifact or adapting a reference image.

## Validate before completion

Run the bundled validator and inspect the rendered output visually at full size and at 50% scale. When a browser runtime exists, also inspect relevant breakpoints and console output.

At minimum, verify:

- every displayed token, prop, state, and rule is traceable;
- no rows, columns, or labels are missing or duplicated;
- actual states match the system implementation;
- text is legible, unclipped, and not reduced merely to fit excess content;
- hierarchy remains clear on a phone-sized preview;
- color contrast and focus treatment meet the system's stated accessibility target;
- meaning is not communicated by color alone;
- interactive samples have adequate labels and target sizes;
- responsive examples reflect real breakpoints or are marked proposed;
- local assets resolve and exports have the requested dimensions;
- no placeholder text, accidental watermark, broken glyph, or temporary path remains;
- production code was not modified outside the user's requested scope.

Read `references/accessibility-and-qa.md` and use `assets/qa-report.template.md`.

## Completion criteria

Do not describe the task as complete until all applicable items exist:

1. a source map with provenance and conflicts;
2. a normalized guide specification;
3. an editable deterministic artifact;
4. requested exports;
5. a QA report with validation results and remaining limitations;
6. no unresolved placeholder or unmarked assumption.

If a prerequisite prevents completion, still create the highest-confidence partial package, label the limitation precisely, and state the exact missing source or runtime requirement. Do not disguise a concept mockup as verified documentation.

## Progressive disclosure map

Read only the references needed for the task:

- `references/repository-discovery.md` — repository and Storybook inspection;
- `references/design-system-domain-model.md` — normalization of tokens, components, patterns, and provenance;
- `references/guide-architectures.md` — architecture contracts and guide-series planning;
- `references/copy-and-localization.md` — concise instructional copy and PT-BR handling;
- `references/visual-production.md` — layout, capture, deterministic rendering, and exports;
- `references/accessibility-and-qa.md` — accessibility, visual checks, and completion gates;
- `references/gpt-5.6-execution.md` — difficult multi-source, multi-agent, or long-horizon work.

## Example invocations

```text
Use $visualize-design-system to inspect this repository and create a 4:5 visual guide for the Button component showing anatomy, variants, sizes, states, accessibility rules, and do/don't examples. Use the implemented tokens and export HTML, PNG, and PDF.
```

```text
Use $visualize-design-system to turn our token files into a visual token cascade showing primitive → semantic → component aliases. Mark undocumented or conflicting aliases and generate a QA report.
```

```text
Use $visualize-design-system to audit the design system and propose a prioritized visual-atlas roadmap. Do not modify production code.
```
