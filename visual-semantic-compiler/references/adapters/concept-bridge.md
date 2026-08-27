# Concept Bridge Adapter

Concept Bridge owns:

- whether a visual is needed;
- audience knowledge boundary;
- depth L0–L4;
- prose mental model;
- representation class (`narrative-visual`, `structural-diagram`, `mixed`);
- visual archetype selection.

Visual Semantic Compiler owns only the next step: translating that decision into a minimal validated IR.

## Handoff rules

1. Preserve Concept Bridge's selected depth. Do not add implementation detail merely to satisfy a renderer.
2. Preserve canonical terminology from the prose.
3. Default source provenance to `general-knowledge` for stable conceptual explanations unless the answer depends on researched or supplied evidence.
4. Use `omissions` aggressively enough to keep the first mental model honest and small.
5. Use `max_primary_nodes` consistent with the first-model budget; 3–7 is a strong default for structural diagrams unless truth requires more.
6. Preserve prose independence through `text_equivalent`.
7. If Concept Bridge selected prose-only, do not invoke this compiler.

## Router extension

The compiler recognizes `sequence` and `dataflow` as distinct structural types. These can be used when Concept Bridge's cognitive question is respectively:

- who sends what to whom, in what order;
- how information moves or transforms.

Do not collapse either into generic architecture when chronology or data custody is the actual concept.
