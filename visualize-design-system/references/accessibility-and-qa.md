# Accessibility and QA

A visual guide is documentation, but it can also become a testable contract. Validate both the guide itself and the system behavior it claims to represent.

## 1. Evidence QA

Check every important statement:

- exact token path exists;
- resolved value is current;
- public prop or variant exists;
- state can be produced;
- breakpoint matches implementation;
- usage rule has a source or is labeled proposed;
- deprecation status is current;
- screenshots correspond to the cited implementation version.

Reject orphan claims with no source and no provenance label.

## 2. Taxonomy QA

Check that:

- variants, sizes, and states are separated;
- foundations, components, and patterns are not mixed as peers;
- synonyms are not duplicated;
- internal helpers are not presented as public API;
- generated aliases are not counted as independent semantic decisions;
- the guide answers one dominant question.

## 3. Accessibility checks for documented UI

Apply the repository's stated standard. If none exists, use current WCAG 2.x AA expectations as the practical baseline and state the assumption.

### Color and contrast

- Verify text contrast against actual backgrounds.
- Verify non-text contrast for controls, focus indicators, and meaningful boundaries where applicable.
- Do not infer accessibility from hue alone.
- Record resolved values and calculation method.

### Keyboard and focus

- Confirm focus is reachable in a logical order.
- Capture real `:focus-visible` behavior.
- Ensure focus is not removed without an equivalent.
- Distinguish hover from focus in the guide.

### Semantics and naming

- Confirm labels, descriptions, roles, and states are exposed correctly.
- Distinguish disabled from read-only.
- Verify icon-only controls have accessible names.
- Do not use placeholder text as the only label.

### Targets and spacing

- Check the system's minimum target-size rule.
- Check adjacent-target spacing for dense controls.
- Avoid documenting tiny icon buttons as acceptable without context.

### Errors and status

- Errors must identify what happened and what the user can do.
- Meaning must not rely on red/green alone.
- Loading, success, and failure should be exposed to assistive technology when relevant.

### Motion

- Document reduced-motion behavior.
- Avoid presenting decorative motion as required interaction feedback.
- Record duration and easing only when verified or proposed.

## 4. Guide accessibility

The guide artifact itself should also be usable:

- HTML has a meaningful title and language;
- heading hierarchy is logical;
- images have alt text where meaningful;
- tables use real table semantics when appropriate;
- text remains selectable in HTML/PDF;
- contrast is sufficient;
- technical details are not encoded by color alone;
- reading order matches visual order;
- PDF export does not crop essential content.

A poster PNG is not an accessible replacement for HTML documentation. When accessibility matters, deliver both.

## 5. Visual QA

Inspect at target size and 50% scale:

- title dominance;
- section hierarchy;
- repeated-card consistency;
- row/column alignment;
- clear distinction between examples;
- no clipping or overflow;
- no tiny body copy;
- no accidental browser UI;
- no broken images or fonts;
- no placeholder or debug content;
- no watermark or reference-image residue.

## 6. Responsive QA

When the guide or docs page is responsive, inspect:

- target desktop width;
- one intermediate width;
- smallest supported width;
- overflow of matrices and code labels;
- whether reading order remains coherent;
- whether responsive examples retain their labels;
- whether print/export styles remain independent from screen styles.

## 7. Implementation QA

When integrating into a repository:

- run the relevant formatter and linter;
- run unit and interaction tests for changed files;
- run Storybook build if stories changed;
- run browser checks for the new docs route;
- inspect console errors;
- preserve unrelated repository files;
- verify generated files are intentionally tracked or ignored.

Do not create tests that merely assert the generated fixture you just wrote. Test the contract the guide claims, such as supported variants, token resolution, or absence of overflow.

## 8. QA report structure

Use `assets/qa-report.template.md` and include:

1. artifact and version;
2. sources inspected;
3. validation commands;
4. factual findings;
5. visual findings;
6. accessibility findings;
7. source conflicts;
8. assumptions and provenance;
9. unresolved limitations;
10. pass/fail conclusion.

## 9. Completion gates

### Gate A — Source integrity

Pass only when claims are traceable or clearly labeled as proposed/inferred.

### Gate B — Content integrity

Pass only when taxonomy, labels, and decision rules are coherent.

### Gate C — Visual integrity

Pass only when the guide is legible, unclipped, and visually consistent.

### Gate D — Accessibility integrity

Pass only when accessibility claims are verified and the artifact does not introduce obvious barriers.

### Gate E — Production integrity

Pass only when source, exports, asset paths, and validation results are complete.

A guide may ship with a documented warning, but it must not receive an unqualified pass when a gate fails.
