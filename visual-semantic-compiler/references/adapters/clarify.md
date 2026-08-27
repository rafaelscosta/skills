# Clarify Adapter

Clarify owns:

- source truth and invariant locking;
- audience/outcome contract;
- difficulty diagnosis;
- intervention selection;
- visual grammar choice;
- high-risk and uncertainty policy.

Visual Semantic Compiler turns the selected visual intervention into a validated semantic IR without changing those decisions.

## Handoff rules

1. Material source invariants become entities, relationships, beats, omissions, or text-equivalent facts without semantic weakening.
2. Source-bound nodes and relationships should carry provenance when the evidence is available.
3. Preserve `explicit`, `inferred`, `unknown`, and general-knowledge boundaries.
4. A source conflict remains a conflict; do not normalize it away for a cleaner diagram.
5. Keep actor responsibility and causal direction exact.
6. Use `omissions` only for intentionally deferred complexity, never for inconvenient exceptions that materially govern the action.
7. `text_equivalent` must remain usable by the target audience.

## Broad visual grammar

Clarify may select types beyond the compiler's deeply validated core, including swimlane, BPMN, SIPOC, decision tree/table, concept map, argument map, service blueprint, C4, Event Storming, and statistical chart.

R1 accepts these through universal IR checks while preserving the chosen type. Do not silently remap them to a simpler renderer type merely because a downstream renderer has fewer capabilities.
