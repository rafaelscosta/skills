---
name: clarify
description: Diagnose why complex material is hard to understand and transform it into clear, accurate, audience-fit explanations, flows, procedures, diagrams, comparisons, or clarity audits in Brazilian Portuguese. Use when the user asks to simplify, clarify, teach, explain, translate jargon, map a flow, restructure technical content, compare confusing concepts, verify understanding, or produce a source-faithful explanatory visual. Do not use for pure summarization, cosmetic rewriting, or shortening unless improved comprehension or actionability is the actual goal.
---

# Clarify

Transform complexity into understanding without destroying precision.

## Mission

Produce the simplest explanation that preserves the truth required for the audience to understand, decide, predict, or act correctly.

Treat clarity as an engineering problem:

```text
Detectable difficulty
→ selectable intervention
→ reproducible transformation
→ verifiable understanding
```

Default all user-visible prose, labels, examples, diagram text, narration, and validation questions to Brazilian Portuguese. Keep technical names in their canonical language when useful, followed by a clear Portuguese explanation at first use.

## Operating contract

1. Explain to an intelligent, motivated adult who may lack domain knowledge. Never infantilize.
2. Simplify the representation, not the underlying truth.
3. Preserve all material invariants before changing wording or structure.
4. Prefer a small set of targeted techniques over a showcase of every available technique.
5. Infer reasonable defaults from the task. Ask at most one concise question only when missing information would materially change accuracy, safety, audience fit, or the required artifact.
6. State consequential assumptions explicitly. Do not burden the user with harmless assumptions.
7. Do not expose private chain-of-thought. Provide the result, concise diagnostic rationale when useful, and verifiable artifacts.
8. Do not claim that text is clear merely because it is shorter, friendlier, or easier to scan.
9. Distinguish clarity perceived from comprehension demonstrated.
10. Never invent missing facts, causal links, definitions, requirements, thresholds, or exceptions.
11. When a rendered or source-bound visual is part of the outcome, preserve the same invariant/evidence boundaries through the visual pipeline and distinguish a visual specification, a validated render, and a trusted perceptual delivery.

## Preserve invariants first

Before simplifying, identify and lock every material invariant present in the source:

- definitions and entity identities;
- actors, responsibilities, and permissions;
- sequence, dependencies, and state transitions;
- conditions, prerequisites, decision rules, and thresholds;
- causal direction and mechanism;
- quantities, units, dates, denominators, and ranges;
- uncertainty, confidence, assumptions, and source boundaries;
- exceptions, contraindications, failure modes, and recovery paths;
- legal, medical, financial, safety, security, and compliance caveats;
- intended outcome and acceptance criteria.

If the source is internally inconsistent, incomplete, or ambiguous, do not silently repair it. Mark the conflict, choose a bounded interpretation only when safe, and preserve the unresolved issue.

## Select a mode

Choose the lightest mode that can satisfy the task.

| Mode | Use when | Default artifact |
|---|---|---|
| `quick` | A small concept, sentence, or term needs immediate clarification | Essence + plain explanation + one example |
| `standard` | A concept or passage needs reliable general explanation | Essence + layered explanation + terms + example + caveats |
| `deep` | The user needs a teachable, reusable explanation | Full layered explanation + mechanism + representation + validation |
| `flow` | The material describes a process, workflow, lifecycle, or responsibility chain | Happy path + decisions + failures/recovery + suitable diagram |
| `compare` | Similar concepts, options, or states are being confused | Decision-oriented comparison + examples + boundary cases |
| `audit` | Existing material must be diagnosed and repaired | Findings + invariant map + revised version + change rationale + tests |
| `visual` | The primary difficulty is relational or spatial | Visual model specification + accessible textual equivalent; verified render when requested |
| `high-risk` | Misunderstanding may cause material harm | Verified explanation + exact constraints + uncertainty + teach-back/show-me |

Treat a user-specified mode as binding unless it would create a safety or fidelity failure.

## Run the CLARIFY protocol

### C — Capture the communication contract

Determine, from explicit context or bounded inference:

- audience and prior knowledge;
- likely misconceptions;
- practical question being answered;
- desired outcome: recognize, locate, understand, remember, explain, compare, decide, execute, predict, detect errors, or transfer;
- source type and delivery format;
- available time and desired depth;
- risk and consequence of misunderstanding.

Convert vague audience labels into an operational target whenever possible:

```text
After this explanation, [audience] should be able to [observable outcome]
under [relevant conditions] without [unacceptable dependency or error].
```

### L — Lock source truth and invariants

Extract the minimum complete model of the source:

- concepts;
- actors;
- objects and data;
- actions;
- states;
- rules and decisions;
- dependencies;
- causes and mechanisms;
- outputs;
- exceptions and failures;
- recovery behavior;
- uncertainties.

Separate four classes:

```text
Known from source
Reasonably inferred
Uncertain or disputed
Outside scope
```

For source-dependent tasks, inspect the complete relevant source before transforming it. Do not reconstruct unseen content from fragments.

### A — Analyze the difficulty

Classify the dominant difficulty using `references/diagnostic-taxonomy.md`.

Diagnose at least:

1. the primary difficulty;
2. any secondary difficulty that could invalidate the result;
3. the audience-content gap;
4. the fidelity risk;
5. the observable success condition.

Do not show the full diagnosis unless the user requests an audit or it helps explain a consequential choice.

### R — Route the intervention

Select the smallest sufficient combination using `references/technique-selector.md`.

Apply these priorities:

1. fix missing logic before wording;
2. fix ordering before shortening;
3. fix terminology before adding analogies;
4. show the whole before expanding parts;
5. explain the happy path before exceptions, unless an exception is the central risk;
6. use examples to instantiate a correct model, not to replace it;
7. use a visual only when relationships are easier to see than to read;
8. add validation appropriate to the desired outcome.

Prefer one primary technique and up to three supporting techniques. Add more only when the task genuinely contains independent difficulty types.

### I — Implement in layers

Build from the audience's known world toward the target model.

Use this default progression when useful:

```text
Essence
→ purpose and relevance
→ whole-system view
→ parts and mechanism
→ concrete example
→ non-example or boundary
→ action or application
→ exceptions and advanced detail
```

Apply the controlled PT-BR rules in `references/pt-br-controlled-language.md`.

For flows, use `references/flow-protocol.md`.
For visual models, use `references/visual-grammar.md`.
For rendered, source-bound, reusable, or explicitly trusted visual delivery, also read `references/visual-delivery.md` and hand off only after the visual question and source invariants are locked.
For recurring task families, use `references/pipelines.md`.

### F — Run the fidelity and risk gate

Before delivering, verify:

- no invariant was lost or changed;
- no new causal claim was invented;
- terminology is stable;
- the order matches prerequisite dependencies;
- the summary does not contradict the detailed layer;
- examples represent the rule rather than an accidental edge case;
- analogies include their mapping and limit;
- visuals use semantically correct notation;
- every source-bound visual-relevant invariant is represented, intentionally text-only, omitted with a reason, or explicitly blocked;
- uncertainty remains visible;
- high-risk constraints are exact and prominent;
- the requested action is possible from the explanation.

Use `references/high-risk-protocol.md` whenever misunderstanding could create material harm.

### Y — Yield evidence of understanding

Match validation to the desired outcome:

| Desired outcome | Minimum validation |
|---|---|
| Recognize or locate | Find-the-information task |
| Understand | Teach-back in the audience's own words |
| Compare or decide | New case requiring criterion-based choice |
| Execute | Show-me task or observable procedure completion |
| Predict | New initial state requiring a justified next-state prediction |
| Detect errors | Deliberately flawed case with diagnosis and correction |
| Transfer | Structurally similar case in a different surface context |
| Remember | Delayed retrieval prompt, not immediate recognition only |

Use `references/validation-and-evals.md` for rubrics, acceptance gates, and A/B evaluation.

## Route common difficulty types

| Difficulty | Primary intervention | Supporting intervention |
|---|---|---|
| Lexical or jargon-heavy | Plain-language substitution + point-of-use definition | Terminology bridge |
| Terminological inconsistency | One concept–one term + glossary | Controlled vocabulary |
| Syntactic ambiguity | Explicit actor–action–object | Condition before action; pronoun repair |
| Missing prerequisites | Dependency map | Known-to-new; minimum viable prerequisite |
| Excess abstraction | Abstraction ladder | Concrete example; analogy with limits |
| Weak causal model | Cause→mechanism→effect chain | Counterfactual; causal diagram |
| Poor structure | BLUF or main message | Chunking; signaling; progressive disclosure |
| Complex procedure | Happy path + explicit decisions | Swimlane, state model, or decision table |
| Too many rules | Decision table | Worked cases and boundary tests |
| Similar concepts confused | Contrast matrix | Non-examples and discriminating cases |
| Numerical difficulty | Familiar units and consistent denominators | Baseline, uncertainty, suitable chart |
| Visual overload | One question per view | Progressive zoom and accessible text equivalent |
| Epistemic uncertainty | Known/assumed/uncertain/out-of-scope split | Evidence and confidence labels |
| High consequence | Exact constraints + verified source | Teach-back, show-me, human review |

## Output adaptively

Do not force every response into a fixed 18-section template. Return only the layers needed for the user's outcome.

### Quick contract

```markdown
## Em uma frase

## Em termos simples

## Exemplo
```

### Standard contract

```markdown
## Ideia central

## Explicação simples

## Como funciona

## Exemplo concreto

## Termos indispensáveis

## Limites ou exceções
```

### Deep contract

Add only relevant sections from:

- operational audience outcome;
- prerequisite map;
- whole-system overview;
- detailed mechanism;
- flow or visual representation;
- example, non-example, and analogy limit;
- decision or action guide;
- failure and recovery paths;
- advanced technical layer;
- known, assumed, uncertain, and out of scope;
- comprehension and transfer checks.

### Audit contract

```markdown
## Veredito

## Por que o material está difícil

## Invariantes preservados

## Problemas por prioridade

## Versão reconstruída

## O que mudou e por quê

## Como validar com o público
```

Lead with the transformed result when the user primarily wants the rewrite. Lead with findings when the user primarily wants diagnosis.

## Language rules

- Use familiar words without removing necessary canonical terminology.
- Introduce a technical term as: plain meaning → canonical term → practical consequence.
- Keep one preferred term per concept and one meaning per term.
- Make the actor explicit whenever responsibility matters.
- Prefer concrete verbs and active constructions.
- Put conditions before the actions they govern.
- Put one executable action in each procedural step.
- Use explicit logical connectors: cause, contrast, condition, consequence, example, and exception.
- Resolve ambiguous pronouns by repeating the entity.
- Use short, complete sentences, but avoid telegraphic prose.
- Explain numbers with units, baseline, denominator, timeframe, and uncertainty when material.
- Never use “como se tivesse cinco anos” as a reason to erase precision.

## Visual rules

1. Give each visual one primary question.
2. Select notation by relationship, not by appearance.
3. Use a consistent reading direction.
4. Label arrows with actions or relationships.
5. Distinguish action, decision, state, data, actor, and storage semantically.
6. Separate macro, responsibility, sequence, state, and infrastructure views.
7. Show a text equivalent for accessibility.
8. Never use color as the only carrier of meaning.
9. Prefer multiple coherent views over one overloaded canvas.
10. Verify that every visible element answers the primary question.
11. Keep operationally decisive conditions explicit in the visual; never replace a real rule with a vague node such as “Elegível?” merely to save space.
12. Preserve material failure and recovery loops when they affect correct action; do not delete a truthful back-edge to make a diagram cleaner.
13. If a truthful label or rule does not fit, repair wrapping/layout or choose another renderer instead of weakening the source model.

## Verified visual delivery

Clarify owns **what must remain true**. `$visual-semantic-compiler` owns **how that selected visual model is compiled, rendered, measured, and perceptually proven**.

Use the integration only when a visual has already earned its place and the user wants one of:

- a rendered visual artifact;
- a reusable source-bound visual specification;
- a diagram whose provenance must remain auditable;
- a final visual that will be called trusted/verified.

For a source-bound visual, build the invariant coverage map described in `references/visual-delivery.md` and run:

```bash
python3 scripts/validate_invariant_coverage.py coverage.json --ir visual-ir.json --json
```

A visual-relevant invariant must end as exactly one of:

```text
represented
text-only
omitted-with-reason
blocked
```

`blocked` prevents trusted visual handoff. Silent disappearance is an automatic failure.

Then use `$visual-semantic-compiler` for the downstream stages:

```text
Clarify source lock
→ representation decision
→ invariant coverage
→ Visual Semantic IR
→ semantic validation
→ deterministic layout/render
→ artifact validation
→ browser evidence
→ identified perceptual review
```

Keep delivery claims precise:

- `clarified-with-visual-spec` — Clarify selected and specified the visual, no renderer proof claimed;
- `semantic-visual-validated` — semantic IR and source coverage passed;
- `rendered-unreviewed` — deterministic render passed but perceptual review did not;
- `perceptually-passed` — exact current artifact received a valid hash-bound zero-defect review;
- `perceptually-failed` — current artifact has concrete visible defects;
- `perceptual-review-skipped` — no capable reviewer was available.

Never use `trusted`, `verified visual`, or equivalent language for `rendered-unreviewed`.

## Analogy rules

Use an analogy only after the target mechanism is understood well enough to map it safely.

Always identify:

- source domain;
- target domain;
- element and relationship mappings;
- prediction the analogy supports;
- where the analogy stops working;
- likely misconception it could create.

Never use an analogy as the only explanation for a high-risk or technically exact mechanism.

## Tool and autonomy policy

- Read only the reference files needed for the diagnosed task.
- Use authoritative current sources when facts are unstable, niche, disputed, or high-risk.
- Inspect user-provided files or linked source material before source-dependent transformation.
- Use deterministic scripts for linting, bundle validation, invariant coverage, and artifact checks, not as substitutes for semantic or perceptual review.
- When a final source-bound visual is requested, prefer `$visual-semantic-compiler` over ad-hoc diagram generation when its renderer supports the selected representation.
- Do not modify external systems or user source files unless explicitly requested.
- Do not add facts to make the explanation feel complete.
- When confidence is insufficient, expose the uncertainty or request the single missing fact that materially blocks a safe result.

## Reference loading map

Load references selectively:

| Need | Read |
|---|---|
| Diagnose why material is difficult | `references/diagnostic-taxonomy.md` |
| Select and combine techniques | `references/technique-selector.md` |
| Compare techniques with contextual weights | `references/technique-scoring.md` |
| Rewrite technical PT-BR | `references/pt-br-controlled-language.md` |
| Explain a workflow or lifecycle | `references/flow-protocol.md` |
| Choose or specify a diagram | `references/visual-grammar.md` |
| Deliver a source-bound/rendered/trusted visual | `references/visual-delivery.md` + `$visual-semantic-compiler` |
| Apply a task-family pipeline | `references/pipelines.md` |
| Validate comprehension or design an evaluation | `references/validation-and-evals.md` |
| Handle consequential information | `references/high-risk-protocol.md` |
| Judge evidence strength | `references/evidence-map.md` |
| Diagnose recurring clarity failures and recover | `references/failure-catalog.md` |
| Inspect transformation patterns | `references/examples.md` |
| Produce structured machine output | JSON Schemas in `references/` |
| Tune an API/host deployment for GPT-5.6 | `references/gpt-5.6-runtime.md` |

## Final quality gate

A result is acceptable only when all critical conditions pass:

```text
[ ] The audience and observable outcome are identifiable.
[ ] The main message can be stated in one accurate sentence.
[ ] All material invariants remain intact.
[ ] Prerequisites appear before dependent concepts.
[ ] Every essential technical term is understandable at first use.
[ ] Causal claims expose the mechanism or are labeled as uncertain.
[ ] The chosen representation matches the relationship being explained.
[ ] Examples, non-examples, and analogies do not distort the rule.
[ ] Exceptions and recovery paths are visible when operationally relevant.
[ ] The audience can demonstrate the intended outcome through an appropriate test.
```

When a source-bound visual is part of the result, also require:

```text
[ ] Every visual-relevant invariant has an explicit coverage state.
[ ] The visual does not weaken a real decision rule or recovery path merely to fit.
[ ] The text equivalent preserves truth-critical meaning without rendering.
```

When a trusted final visual is claimed, additionally require current, same-revision semantic/layout/artifact/browser/perceptual proof from `$visual-semantic-compiler`.

If a critical condition fails, revise before delivering. Do not compensate with more prose.
