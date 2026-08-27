# Visual Semantic Compiler v1.0.0 — Validation

## Deterministic checks executed

```bash
python3 -m py_compile scripts/validate_ir.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 scripts/validate_ir.py examples/concept-bridge-rag.json --json
python3 scripts/validate_ir.py examples/clarify-refund-flow.json --json
```

## Result

- Python compile: PASS
- Validator unit tests: **7/7 PASS**
- Concept Bridge RAG example: **VALID**, all semantic checks pass, 0 warnings
- Clarify refund-flow example: **VALID**, all semantic checks pass, 0 warnings

## Negative contracts covered

The unit suite verifies deterministic rejection for:

- dangling relationship endpoints;
- sequence relationships without unique positive ordering;
- invalid state entity/transition semantics;
- branching flow without branch labels;
- non-causal relationship kinds inside causal diagrams;
- mixed representation without both narrative and structural views.

## Scope boundary

R1 validates semantic IR only. `layout_geometry` remains explicitly `deferred`; this validation does not claim rendered containment, edge-crossing quality, typography, visual polish, or perceptual review.
