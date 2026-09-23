# Visual production

The visual guide should feel like part of the design system it documents. Use the system's own tokens and components whenever possible.

## 1. Production hierarchy

Use this order:

```text
source evidence
→ normalized guide specification
→ real component renders or faithful diagrams
→ deterministic composition
→ browser inspection
→ export
→ QA
```

Do not start with a one-shot image prompt for text-heavy output.

## 2. Canvas defaults

| Use | Recommended canvas |
|---|---|
| Social/teaching poster | 1080 × 1350, 4:5 |
| Story/vertical reference | 1080 × 1920, 9:16 |
| Square card | 1080 × 1080 |
| Documentation page | 1440px desktop, responsive |
| Print | A4 or Letter with print CSS |
| Presentation | 16:9, usually 1920 × 1080 |

The requested medium overrides these defaults.

## 3. Visual grammar

A strong guide usually contains:

- a small category label;
- one dominant title;
- a precise learning promise;
- repeated modules with consistent anatomy;
- actual component or token evidence;
- restrained color usage;
- a final decision rule, checklist, or takeaway.

Use one icon family and one illustration/rendering language. Avoid mixing emojis, outline icons, filled icons, 3D assets, and unrelated photography.

## 4. Use the documented system

Prefer:

- repository fonts;
- semantic colors;
- established spacing scale;
- real radii and borders;
- existing components for labels, badges, and controls;
- actual iconography;
- system density rules.

A documentation guide may use a larger editorial title scale, but it should not introduce a competing visual identity.

When the system is incomplete, define a minimal documentation theme and label it as a documentation layer, not as an implemented product token set.

## 5. Comparison discipline

When teaching a variable, lock everything else:

- same copy;
- same component width;
- same context;
- same viewport;
- same surrounding surface;
- same icon and content length;
- same capture scale.

Change only the relevant variable, such as variant, state, size, density, breakpoint, or pattern.

## 6. Real renders and screenshots

Preferred capture order:

1. existing Storybook story or docs example;
2. application route with a stable fixture;
3. isolated test harness using the real component;
4. faithful code-derived specimen;
5. schematic diagram.

When capturing:

- wait for fonts and assets;
- disable accidental caret or selection artifacts;
- use deterministic fixture data;
- capture at a known device scale;
- avoid browser chrome unless it is part of the lesson;
- crop consistently;
- preserve focus outlines and shadows;
- include transparent background only when composition requires it.

## 7. Layout families

### Catalog grid

Use for tokens, layout patterns, icon sizes, or component types. Maintain identical card anatomy.

### Matrix

Use for variants × states, size × density, or component comparisons. Keep row/column headers visible and cells aligned.

### Anatomy

Use a dominant central specimen and sparse callouts. Avoid crossing leaders and tiny labels.

### Mirrored pairs

Use for do/don't. Keep both examples at the same scale and context.

### Strip or storyboard

Use for responsive behavior or motion. Keep progression directional and label each step.

### Master sheet

Use three or four coordinated sections, not a page of unrelated mini-guides.

## 8. Typography and density

For a 1080 × 1350 poster, sensible starting ranges are:

- eyebrow: 18–24px;
- title: 54–92px depending on length;
- subtitle: 22–30px;
- section title: 22–30px;
- card title: 18–24px;
- body: 15–20px;
- technical label: 12–16px.

These are starting points, not fixed rules. Inspect at 50% scale and on a phone preview.

Do not place more content by shrinking every text style. First reduce repetition, then split the guide.

## 9. Color and contrast

Use the system's semantic roles rather than arbitrary swatches. Reserve accent color for hierarchy, not decoration everywhere.

For a guide that audits contrast, show:

- foreground token;
- background token;
- resolved values;
- contrast ratio;
- target threshold;
- pass/fail status;
- context such as text size or non-text control.

## 10. Deterministic rendering

The bundled renderer creates standalone HTML from `guide-spec.json`. It supports common section types and simple UI specimens.

Use repository-native rendering instead when it provides higher fidelity. The guide spec remains useful as the content contract.

Benefits of deterministic composition:

- exact copy;
- stable alignment;
- editable source;
- reusable tokens;
- predictable exports;
- easier visual regression;
- no image-model text errors.

## 11. Browser iteration loop

After rendering:

1. open the page at the target viewport;
2. inspect the complete page visually;
3. check overflow, clipping, alignment, and hierarchy;
4. inspect at 50% scale;
5. inspect the smallest relevant viewport when responsive;
6. fix the source, not the screenshot;
7. recapture;
8. repeat until the guide passes.

Do not declare success from a successful render command alone.

## 12. Export rules

- Preserve an editable source file.
- Export PNG at exact requested pixel dimensions.
- Export PDF with backgrounds enabled and zero unintended margins.
- Use SVG when the guide is primarily vector and the repository workflow supports it.
- Do not rasterize actual text earlier than necessary.
- Check file size and embedded asset paths.
- Avoid linking to local absolute paths from the final standalone artifact.

## 13. Reference-image adaptation

Extract principles rather than copying:

- hierarchy;
- modular rhythm;
- content density;
- section bands;
- icon-to-copy ratio;
- use of repeated subjects;
- palette discipline;
- visual demonstration of differences.

Do not reproduce a creator's signature, watermark, exact wording, proprietary images, or distinctive page arrangement. Build an original system-aligned composition.
