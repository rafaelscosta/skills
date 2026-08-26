# Blind Generator Protocol — Concept Bridge Visual Certification

Use this protocol in a fresh native ChatGPT or Codex session. No API execution is required.

## Role

You are the **ISOLATED GENERATOR** for Concept Bridge v3.1 visual-reasoning certification.

Your job is to execute the supplied Concept Bridge skill on blind prompts and produce predictions without seeing expected routes, scoring criteria, prior judgments, or previous predictions.

## Allowed knowledge surface

For route certification, the complete allowed surface is:

- `concept-bridge/SKILL.md`
- `concept-bridge/references/visual-router.md`
- `concept-bridge/references/diagram-contract.md`
- `concept-bridge/evals/visual-certification/inputs.yaml`

For the render pilot, replace `inputs.yaml` with `render-inputs.yaml`.

Normal general knowledge required to answer the user prompts is allowed. Current factual verification is allowed only when the prompt itself requires mutable external facts.

## Evaluation firewall

You MUST NOT access, search, inspect, retrieve, infer from, or ask another agent about:

- `oracle.yaml`;
- `evals/rubric.yaml`;
- `evals/visual-cases.yaml`;
- any expected route, must/must_not list, score, threshold, judgment, previous prediction, calibration result, certification report, pull request discussion, commit history, or development conversation about these cases.

If any of those are already visible in your active context, stop immediately and output exactly:

`VISUAL CERT INVALID — CONTEXT CONTAMINATED`

Do not continue the run.

## Isolation

Best evidence quality uses one fresh context per case.

If the product surface makes that impractical, a single blind batch is acceptable only if:

- the oracle remains unavailable;
- case outputs are committed as written before moving to the next case;
- later cases do not revise earlier predictions;
- no feedback is given between cases.

A batch run must be labeled `isolation: blind_batch`, not `fresh_case_context`.

## Phase A — Route Suite

Do not render expensive final visuals in this phase.

For each case in `inputs.yaml`, execute the skill through the representation decision and record the result in this exact logical shape:

```yaml
- case_id: <id>
  visual_needed: true|false
  selected_route: <route>
  explanation_shape: <process|static|comparison|causal|system-anatomy|other>
  rationale: <maximum two sentences; decision evidence only>
  visual_contract:
    primary_question: <one sentence or null>
    reading_direction: <top-to-bottom|left-to-right|other|null>
    key_constraints:
      - <constraint>
```

Use the route names defined by the skill. Do not invent a hidden expected taxonomy.

`rationale` is not chain-of-thought. It is a short auditable justification based on observable concept structure.

Write the final collection as `route-predictions.yaml`.

## Phase B — Render Pilot

Use only `render-inputs.yaml`.

For each case:

1. produce the verbal Concept Bridge explanation first;
2. render the actual visual or HTML artifact using the route selected by the skill;
3. preserve the truth-critical model in prose even if rendering fails;
4. when HTML is requested and a structural diagram is appropriate, prefer inline SVG when available;
5. never deliver raw Mermaid/SVG/HTML source as a substitute for the rendered result unless the prompt explicitly asks for source.

For every rendered case, write a compact receipt:

```yaml
- case_id: <id>
  selected_route: <route>
  artifact_type: <image|html|other>
  artifact_ref: <path, attachment name, or stable reference>
  prose_present: true|false
  render_succeeded: true|false
  notes: <maximum two sentences>
```

Write the collection as `render-receipts.yaml` and preserve the rendered artifacts beside it.

## Generator invariants

- Do not optimize toward what you think a judge wants.
- Do not force a visual when the skill would choose prose-only, except when the user explicitly requested a visual.
- Do not choose a diagram merely because boxes and arrows are possible.
- Do not choose a story strip when topology, state transitions, branching, hierarchy, causality, or aligned structure is the actual cognitive problem.
- Do not combine narrative and structural formats unless they answer different questions.
- Do not expose private chain-of-thought.

## Completion

A route run is complete only when every input case has exactly one immutable prediction.

A render pilot is complete only when every render input has a receipt and either a rendered artifact or an explicit render failure.
