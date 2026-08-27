# Canonical HTML + Inline SVG Renderer Contract — R2

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

## Static artifact validator

`validate_artifact.py` proves structural delivery properties only. It does not prove typography, balance, scanability, or visual polish.

The receipt must therefore remain:

`perceptual_review: pending`

until a capable image/browser reviewer inspects the exact artifact bytes.

## Atomic delivery

`render_html.py` writes the artifact only after semantic, layout, and static artifact checks pass. A failed new candidate must not replace a trusted previous artifact.
