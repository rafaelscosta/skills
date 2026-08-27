# Visual Semantic Compiler v1.1.0 — R2 Validation

## Deterministic checks executed

```bash
python3 -m py_compile scripts/layout_core.py scripts/validate_layout.py scripts/validate_artifact.py scripts/render_html.py scripts/adapt_archify.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

## Result

- Python compile: PASS
- R2 test suite: **11/11 PASS**
- Existing Concept Bridge RAG IR → deterministic architecture layout: PASS
- Existing Clarify refund-flow IR → deterministic flow layout: PASS
- Sequence layout: PASS
- Story-strip layout: PASS
- State/dataflow/hierarchy/causal/structural-comparison smoke matrix: PASS
- Unsupported renderer type: fail-closed PASS
- HTML delivery with semantic-gate stub: layout + artifact validation PASS
- Archify architecture adapter contract: PASS

## Negative geometry contracts covered

- node overlap;
- edge through unrelated node;
- unrelated edge crossing under zero-crossing policy;
- external runtime in canonical HTML;
- unsupported canonical renderer type.

## Important scope boundary

The R2 tests isolate the new layout/render layer. The canonical delivery command calls the existing R1 semantic validator as a subprocess before layout. The local R2 test harness stubs that semantic receipt for the HTML-delivery unit test because the repository was not cloned into the isolated test container; R1 semantic validation remains independently covered by its existing 7/7 suite.

No automated static check is claimed as perceptual review. Every successful render receipt remains `perceptual_review: pending` until the exact artifact is visually inspected.
