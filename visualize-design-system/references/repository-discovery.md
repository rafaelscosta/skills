# Repository discovery

Use this reference for repository-backed work. The goal is to find the smallest reliable source set for the requested guide without flooding the main context.

## 1. Respect repository instructions

Read applicable `AGENTS.md` files from repository root to the target path. Follow existing documentation, formatting, testing, and generated-file conventions.

Do not assume the repository root from the current directory. Confirm it with the VCS or project structure.

## 2. Find the design-system surfaces

Inspect these sources in priority order.

### Runtime and stories

- Storybook configuration and story files
- documentation routes or component galleries
- visual-regression tests
- interaction tests
- example applications

Common paths:

```text
.storybook/
stories/
src/**/*.stories.*
docs/
apps/storybook/
packages/*-storybook/
examples/
playwright/
tests/visual/
```

### Components and public API

Look for:

- component source files;
- exported prop types;
- variant definitions;
- compound-component slots;
- data attributes used for states;
- ARIA behavior;
- class maps and recipes;
- deprecation annotations.

Common paths:

```text
src/components/
components/ui/
packages/ui/
packages/components/
lib/components/
```

### Tokens and foundations

Look for:

- CSS custom properties;
- JSON or YAML design tokens;
- Style Dictionary configuration;
- Tokens Studio exports;
- theme objects;
- Tailwind theme extensions;
- typography and icon manifests;
- motion and breakpoint constants.

Common paths:

```text
tokens/
theme/
styles/
src/styles/
src/theme/
packages/tokens/
packages/theme/
```

### Documentation and governance

Look for:

- usage guidance;
- do/don't rules;
- migration notes;
- changelogs;
- contribution criteria;
- accessibility targets;
- release status.

## 3. Detect common stacks

The inventory script detects many signals, but verify them manually.

| Signal | Likely implication |
|---|---|
| `@storybook/*` | Stories may be the fastest render harness |
| `tailwindcss` | Tokens may exist in config, CSS variables, or presets |
| `class-variance-authority` / `cva` | Variants may be defined close to component code |
| `@radix-ui/*` | Behavior may come from primitives while styling is local |
| `components.json` | shadcn/ui conventions or generated component paths |
| `@mui/*`, Chakra, Mantine, Ant | Theme API and component overrides may be authoritative |
| `style-dictionary` | Generated artifacts may not be the source of truth |
| `@vanilla-extract/*` | Theme contracts and recipes may encode tokens/variants |
| `styled-components` / Emotion | Theme values may be TypeScript objects rather than static files |
| `tokens.json`, `*.tokens.json` | Tokens Studio or DTCG-like sources may exist |

## 4. Use bounded searches

After the broad inventory, search only for the requested component or foundation.

Examples:

```bash
rg -n "Button|buttonVariants|cva\(" src packages components
rg -n "--[a-zA-Z0-9_-]+:" styles src packages
rg -n "disabled|loading|aria-busy|data-state|focus-visible" <component-path>
rg -n "breakpoint|media|container" styles theme src packages
```

Prefer file lists and targeted ranges over dumping large files.

## 5. Build the source map

For each important claim, record:

```json
{
  "claim": "Primary button height is 40px",
  "status": "implemented",
  "sources": [
    {
      "path": "src/components/Button.tsx",
      "locator": "size.default",
      "kind": "component-code"
    }
  ],
  "confidence": "high",
  "notes": "Confirmed in rendered Storybook story"
}
```

Record conflicts separately:

```json
{
  "topic": "Button radius",
  "sources": [
    {"path": "tokens/radius.json", "value": "8px"},
    {"path": "docs/buttons.mdx", "value": "6px"}
  ],
  "resolution": "Use 8px for current-state guide; flag docs drift"
}
```

## 6. Run the system when possible

Prefer this evidence sequence:

1. existing static Storybook build;
2. documented development command;
3. package-level Storybook or gallery;
4. a temporary isolated harness using existing components;
5. code-derived representation only.

Do not install or upgrade dependencies merely to make a guide unless the user requests it or the repository's normal setup requires it. Preserve lockfiles unless implementation changes are in scope.

## 7. Capture interaction states

Use browser automation when available:

- default: no interaction;
- hover: pointer over target;
- focus: keyboard focus, not forced CSS alone;
- active/pressed: pointer down or state prop when public API exposes it;
- disabled: real disabled prop/attribute;
- loading: official loading prop or documented composition;
- error/success: actual validation or status props;
- responsive: real viewport widths aligned to breakpoints.

A visual guide must not display a state that cannot be produced by the public component API unless it is explicitly labeled `proposed`.

## 8. Avoid context pollution

For large monorepos, delegate independent read-only inventories when subagents are available:

- agent A: tokens and foundations;
- agent B: component API and variants;
- agent C: Storybook/tests/runtime;
- agent D: accessibility and documentation conflicts.

Require each agent to return a compact evidence table with paths and conclusions, not raw file dumps. The coordinating thread owns the final source map and all writes.
