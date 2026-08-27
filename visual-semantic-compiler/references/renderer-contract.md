# Canonical HTML + Inline SVG Renderer Contract — R2/R2.1

The canonical renderer turns a validated semantic IR plus a passing deterministic layout into one self-contained HTML artifact.

## Acceptance chain

```text
semantic validator PASS
→ layout validator PASS
→ artifact static validator PASS
→ atomic HTML commit
→ perceptual review PENDING
```

## Required artifact properties

- inline SVG, never raw diagram source as the visual;
- SVG `role="img"`, `<title>`, and `<desc>`;
- semantic IR SHA-256 embedded in HTML metadata;
- text-equivalent visible outside the SVG as well as available to assistive technology;
- no required external script or stylesheet runtime;
- omissions shown as bounded scope, not hidden;
- stable artifact SHA-256 and byte count in the render receipt.

## Operational-flow fidelity

The renderer must adapt geometry to truthful operational content, not adapt truth to geometry.

For `flow` diagrams:

- material recovery/back edges remain present and route outside the dominant forward rail when needed;
- a recovery loop must not be deleted or converted into prose merely because generic DAG layout is easier;
- operationally decisive node labels may wrap across multiple SVG lines;
- node height must expand when wrapping is needed;
- a real rule such as `Até 7 dias E sem consumo premium?` must not be weakened to a vague label such as `Elegível?` solely to fit a box;
- branch labels remain explicit when the semantic validator requires them.

If truthful content still cannot pass geometry after focused repair, fail closed or choose another renderer. Do not shorten away the rule or relation.

## Static artifact validator

`validate_artifact.py` proves structural delivery properties only. It does not prove typography, balance, scanability, or visual polish.

The receipt must therefore remain:

`perceptual_review: pending`

until a capable image/browser reviewer inspects the exact artifact bytes.

## Atomic delivery

`render_html.py` writes the artifact only after semantic, layout, and static artifact checks pass. A failed new candidate must not replace a trusted previous artifact.
