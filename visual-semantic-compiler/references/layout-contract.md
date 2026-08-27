# Deterministic Layout Contract — R2

Use this reference after `visual-semantic-ir/v1` has passed semantic validation.

R2 adds a second frozen candidate: `visual-layout/v1`. It contains geometry only after meaning is already fixed.

## Pipeline boundary

```text
validated semantic IR
→ deterministic layout compiler
→ visual-layout/v1
→ geometry validator
→ frozen layout
→ renderer
```

A semantic pass never implies a layout pass.

## Canonical renderer support

R2 renders these types fail-closed:

- `architecture`
- `flow`
- `state`
- `sequence`
- `dataflow`
- `hierarchy`
- `causal`
- `structural-comparison`
- `story-strip`
- `before-after`
- `timeline`

Other IR types remain semantically valid but require another renderer. Do not silently fall back to generic boxes and arrows.

## Geometry gates

`validate_layout.py` checks:

1. viewport containment;
2. node separation with a 12px clear-gap floor;
3. edge-through-unrelated-node failures;
4. unrelated edge crossings;
5. relationship-label collisions with nodes or other labels;
6. dominant reading direction for non-return primary edges;
7. endpoint integrity and basic geometry shape.

When the semantic IR requests `target_zero_crossings: true`, any unrelated crossing is a hard failure. Otherwise crossings are warnings.

## Layout rules

- Geometry is deterministic from the frozen semantic IR.
- Author order is a stable tie-breaker.
- Primary DAG-like structure controls layers.
- `return` and `feedback` edges do not control primary layering and route outside the main rail.
- Reciprocal state transitions use separate rails.
- Sequence messages use semantic `order` for vertical chronology.
- Structural comparisons align comparison sides into parallel columns.
- Narrative beats become a vertical reading rail.

## Repair policy

If layout validation fails, repair layout logic or choose another renderer. Do not delete a truthful semantic relationship simply to make geometry pass.

Semantic changes require a new IR validation receipt.
