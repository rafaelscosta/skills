# Example — Component state matrix

## User request

```text
Use $visualize-design-system to inspect our Button component and create a 4:5 guide showing variants, sizes, states, hierarchy, accessibility rules, and do/don't examples. Use actual Storybook renders and do not change production code.
```

## Expected behavior

1. Inspect `AGENTS.md`, the Button implementation, public props, tokens, stories, and tests.
2. Run Storybook or an isolated approved harness.
3. Separate variants, sizes, and states.
4. Exclude combinations that do not exist.
5. Create a state matrix plus one anatomy or do/don't section.
6. Compose exact visible copy deterministically.
7. Export HTML, PNG, and PDF.
8. Record sources, conflicts, and QA.

## Acceptance criteria

- Every cell maps to a public component configuration or genuine interaction state.
- Focus is captured through keyboard focus when possible.
- The same label and dimensions remain stable across state comparisons.
- Unsupported loading/error states are not invented.
