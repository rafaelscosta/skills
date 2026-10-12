# Example — Token architecture

## User request

```text
Use $visualize-design-system to turn our color tokens into a visual cascade showing primitive → semantic → component → state aliases. Highlight hard-coded values and broken or conflicting aliases.
```

## Expected output

- focused source map for token files and generated artifacts;
- five or fewer representative alias chains on the visual guide;
- a separate table of all discovered conflicts;
- exact token paths preserved;
- resolved swatches and values;
- provenance and confidence for every chain;
- editable HTML plus PNG/PDF exports.

## Failure modes to avoid

- listing every primitive swatch without semantic structure;
- treating aliases as separate colors;
- using generated CSS as the only source when an upstream token source exists;
- silently choosing between conflicting values.
