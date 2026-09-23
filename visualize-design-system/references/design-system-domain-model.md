# Design-system domain model

Use this model to normalize repository evidence before authoring a guide. Do not mix levels merely because they are visually related.

## 1. System layers

### Foundations

Raw visual and behavioral principles:

- color;
- typography;
- spacing;
- sizing;
- radius;
- border;
- elevation;
- opacity;
- grid;
- breakpoints;
- motion;
- iconography;
- density.

### Tokens

A token is a named decision, not merely a literal value.

Recommended levels:

```text
primitive → semantic → component → state
```

Example:

```text
blue.600
  ↓
color.action.primary
  ↓
button.background.primary
  ↓
button.background.primary.hover
```

Do not present generated aliases as independent decisions when they resolve to the same source.

### Components

Reusable UI units with a defined public API. Describe:

- purpose;
- anatomy/slots;
- variants;
- sizes;
- states;
- behavior;
- content rules;
- responsive behavior;
- accessibility contract;
- token dependencies.

### Patterns

Compositions that solve a recurring user or product problem, such as:

- form validation;
- empty states;
- filtering;
- destructive confirmation;
- loading feedback;
- master-detail navigation;
- data-table actions.

A pattern can contain several components. Do not document it as if it were a component variant.

### Templates and product compositions

Page or feature arrangements tied to a specific product context. Include them only when the design system intentionally governs them.

### Governance

Rules for contribution, ownership, versioning, deprecation, release status, and adoption. Governance can be visualized, but it is not a visual foundation.

## 2. Terms that must remain distinct

### Variant

A supported stylistic or semantic configuration selected through the public API, such as `primary`, `secondary`, `ghost`, or `destructive`.

### State

A temporary condition produced by interaction, validation, data, or availability, such as `hover`, `focus`, `pressed`, `disabled`, `loading`, or `error`.

### Size

A dimensional option such as `sm`, `md`, or `lg`.

### Density

A system-wide or context-level information-density setting. Density may affect several components together and is not always a component size.

### Slot

A named structural region of a component, such as leading icon, label, description, or trailing action.

### Property

A public configuration input. A property may control a variant, state, content, or behavior.

### Status

Lifecycle status of the design-system artifact: experimental, stable, deprecated, or internal. Do not confuse with an interaction state.

## 3. Component documentation contract

A complete component entry should answer:

1. What job does this component perform?
2. When should it be chosen?
3. When should it not be chosen?
4. What are its structural parts?
5. Which variants and sizes are public?
6. Which states can actually occur?
7. Which tokens control it?
8. What content rules apply?
9. How does it behave responsively?
10. What accessibility behavior is required?
11. What is its lifecycle status?

A one-page guide may not fit all eleven. Select the subset needed to answer the guide's dominant question and link the rest through the source package.

## 4. Selection guidance model

When comparing components, use observable decision variables rather than taste.

Useful variables include:

- number of choices;
- whether choices must remain visible;
- selection frequency;
- single versus multiple selection;
- reversibility;
- task criticality;
- required focus;
- available space;
- expected content length;
- need for comparison;
- mobile behavior;
- accessibility constraints.

Example:

```text
2–4 mutually exclusive choices that should remain visible → radio group
few options with frequent switching → segmented control
a long or dynamic option list → select or combobox
```

## 5. Provenance and confidence

Use provenance status and confidence separately.

| Status | Meaning |
|---|---|
| `implemented` | Exists in implementation or runtime |
| `documented` | Stated in maintained docs |
| `inferred` | Derived from incomplete evidence |
| `proposed` | New recommendation |
| `missing` | Expected but absent |
| `deprecated` | Intentionally obsolete |

| Confidence | Typical evidence |
|---|---|
| `high` | Runtime plus implementation, or multiple agreeing sources |
| `medium` | One strong source or several indirect sources |
| `low` | Naming inference, screenshot-only evidence, or unresolved conflict |

A high-confidence `proposed` rule is still proposed. A low-confidence `implemented` claim means implementation was found but interpretation remains uncertain.

## 6. Guide-series taxonomy

For a complete visual atlas, group guides by layer:

```text
01 Foundations
02 Tokens
03 Components
04 Interaction states
05 Content and UX writing
06 Layout and responsive behavior
07 Patterns
08 Accessibility
09 Motion
10 Governance and contribution
```

Within a component family, use this repeatable sequence:

```text
01 Purpose and selection
02 Anatomy
03 Variants
04 Sizes and density
05 States
06 Content rules
07 Responsive behavior
08 Accessibility
09 Do / Don't
10 Implementation map
```

Do not create all ten automatically. Choose only guides that add real decision or execution value.

## 7. Common normalization failures

Reject these patterns:

- listing `primary`, `hover`, and `small` as peer variants;
- treating `modal` and `confirmation flow` as equivalent levels;
- mixing palette swatches with semantic roles in one undifferentiated list;
- presenting internal implementation helpers as public components;
- documenting every CSS class as a token;
- using screenshots to infer inaccessible states without code evidence;
- calling a one-off product layout a system pattern without reuse evidence;
- presenting a design recommendation as an existing rule.
