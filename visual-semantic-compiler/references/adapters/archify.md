# Archify Adapter — R2

Archify is an optional downstream renderer, never the canonical semantic source.

`adapt_archify.py` currently supports **architecture only**. It translates a validated Visual Semantic IR into an Archify `architecture` candidate using Archify's public schema vocabulary.

## Boundary

- Visual Semantic IR remains authoritative.
- Adapter output is renderer-specific and may be regenerated.
- Adapter does not invoke Archify or require Node/npm.
- Unsupported representation types fail closed.
- Archify must run its own `validate`/`deliver` gates before its HTML can be trusted.

The adapter intentionally does not copy Archify geometry controls, viewer state, or brand semantics into the canonical IR.
