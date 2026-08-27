# Clarify → Visual Semantic Compiler Integration

Use this reference when Clarify has already determined that a visual materially improves comprehension or actionability and the user wants a rendered artifact, reusable visual specification, or verifiable diagram.

Clarify remains the owner of pedagogy and source fidelity. `$visual-semantic-compiler` owns semantic IR compilation, deterministic layout/rendering for supported representations, browser evidence, and perceptual-delivery proof.

## Ownership boundary

Clarify must decide and lock before handoff:

- audience and desired observable outcome;
- source truth and material invariants;
- known / inferred / uncertain / out-of-scope boundaries;
- selected visual notation and its primary question;
- source-dependent terminology;
- material exception/recovery paths;
- whether the visual is explanatory only or operationally binding.

The compiler may normalize those decisions into Visual Semantic IR, but must not silently:

- alter a rule, threshold, actor, condition, exception, or causal direction;
- strengthen inferred evidence into explicit evidence;
- remove a truthful relationship merely to simplify layout;
- invent missing topology;
- substitute a different diagram type because it is easier to render.

If rendering constraints expose a semantic conflict, return to Clarify and revise the semantic model explicitly.

## Handoff contract

When the visual is source-bound, provide enough structure for provenance-preserving compilation:

```yaml
clarify_visual_handoff:
  mode: flow | visual | deep | audit | compare | other
  audience: ""
  desired_outcome: ""
  primary_question: ""
  representation:
    class: narrative-visual | structural-diagram | mixed
    type: ""
    reading_direction: left-to-right | top-to-bottom | other
  invariants:
    - id: INV-001
      statement: ""
      source_ref: ""
      locator: ""
  epistemic_boundaries:
    known: []
    inferred: []
    uncertain: []
    out_of_scope: []
  required_terms: []
  required_exceptions: []
  omissions_allowed: []
  text_equivalent: ""
```

This is a logical contract, not mandatory user-visible YAML.

## Provenance mapping

Map Clarify evidence classes into Visual Semantic IR as follows:

| Clarify source class | Visual IR provenance |
|---|---|
| directly stated in source | `explicit` + `source_ref` + locator when available |
| reasonable interpretation | `inferred` + confidence |
| stable domain fact added only for orientation | `general-knowledge` |
| unresolved or missing | `unknown` |

A source-bound diagram should preserve provenance on every material node or relationship whose truth depends on the supplied source.

## Invariant coverage gate

Before render handoff, create an internal invariant-to-IR coverage map:

```text
INV-001 → entity/relationship/beat IDs
INV-002 → entity/relationship/beat IDs
...
```

Every visual-relevant material invariant must end in exactly one of:

- `represented` — appears explicitly in the IR;
- `text-only` — intentionally remains in the text equivalent because adding it visually would overload the view;
- `omitted-with-reason` — outside the selected visual question, but explicitly recorded;
- `blocked` — cannot be represented without resolving source ambiguity.

Never leave a material invariant silently unaccounted for.

## Canonical delivery path

When the selected representation is supported by the canonical renderer and the user wants a final visual artifact:

```text
Clarify source lock
→ Clarify visual handoff
→ Visual Semantic IR
→ semantic validation
→ invariant coverage validation
→ deterministic layout
→ static artifact validation
→ browser evidence
→ perceptual review
→ trusted visual artifact
```

Use `$visual-semantic-compiler` for all stages after the Clarify handoff.

## Unsupported renderer types

Clarify's visual grammar is intentionally broader than the compiler's canonical renderer.

If Clarify selects BPMN, C4, concept map, argument map, decision table, service blueprint, statistical chart, or another unsupported canonical renderer type:

1. preserve the semantic IR and selected notation;
2. fail closed on the canonical renderer;
3. route to an appropriate external/specialized renderer when available;
4. do not flatten the representation into generic boxes and arrows.

## Trusted visual delivery claim

Clarify may call a final visual `trusted` only when:

1. Clarify's fidelity gate passes;
2. every visual-relevant invariant has an accounted coverage state;
3. Visual Semantic IR semantic validation passes;
4. canonical layout/artifact gates pass when used;
5. browser evidence passes for the certified viewport set;
6. an identified perceptual reviewer inspects the current screenshots;
7. the perceptual review is hash-bound and reports no defects.

Otherwise report the strongest truthful state, such as:

- `clarified-with-visual-spec`;
- `semantic-visual-validated`;
- `rendered-unreviewed`;
- `perceptually-failed`;
- `perceptual-review-skipped`.

## Correction ownership

Repair the narrowest responsible layer:

- source/invariant defect → Clarify;
- provenance/semantic-IR defect → compiler semantic layer;
- overlap/crossing/layout defect → compiler layout layer;
- HTML/static-integrity defect → renderer/artifact layer;
- visible hierarchy/readability defect → perceptual correction loop.

If a downstream repair changes semantic meaning, invalidate downstream receipts and return to Clarify's fidelity gate.
