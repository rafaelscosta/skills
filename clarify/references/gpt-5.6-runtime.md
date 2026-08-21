# GPT-5.6 Runtime Guidance

Use this reference when deploying the skill through the OpenAI API or tuning a host configuration. The skill itself does not force model parameters.

Aligned with the official GPT-5.6 model guidance reviewed on 2026-08-19:

- https://developers.openai.com/api/docs/guides/latest-model
- https://developers.openai.com/api/docs/models/gpt-5.6-sol

## Why this skill is structured this way

GPT-5.6 benefits from:

- lean prompts with each instruction stated once;
- domain context, hard constraints, approval boundaries, and success criteria;
- explicit conditions for when ambiguity should trigger a question;
- only relevant tools and examples;
- representative evals rather than intuition-only prompt growth.

Therefore:

- `SKILL.md` contains the invariant workflow and routing rules;
- large knowledge modules live in `references/` and load only when needed;
- scripts handle only deterministic lint, validation, and scoring;
- examples encode measured requirements and failure boundaries;
- trigger and regression evals protect activation and behavior.

## Suggested model selection

### GPT-5.6 Sol

Use for:

- high-risk clarification;
- complex multi-source audits;
- ambiguous causal or strategic models;
- large documents with many invariants;
- difficult visual/architecture synthesis;
- quality-first evaluation and skill maintenance.

### GPT-5.6 Terra

Use for:

- standard production explanations;
- documentation transformation at moderate volume;
- workflow normalization;
- terminology and structure audits with bounded complexity.

### GPT-5.6 Luna

Use only after evals demonstrate acceptable fidelity for:

- deterministic term bridging;
- quick low-risk explanations;
- lint-assisted batch transformations;
- classification or routing with structured inputs.

Do not select a cheaper tier solely because the final prose is short. Source complexity and fidelity risk determine model need.

## Suggested reasoning effort

| Clarify mode | Starting point | Increase when |
|---|---|---|
| `quick` | `low` | Source is ambiguous or precision-sensitive |
| `standard` | `medium` | Multiple hidden prerequisites or causal links exist |
| `compare` | `medium` | Categories overlap or evidence is disputed |
| `flow` | `medium` | Concurrency, state, failure recovery, or ownership is complex |
| `visual` | `medium` | Multiple notations or source inconsistencies must be reconciled |
| `deep` | `medium` | Increase to `high` for large, multi-source, or quality-first tasks |
| `audit` | `high` | Use `xhigh` when invariant tracking and contradictions remain difficult |
| `high-risk` | `high` | Compare `xhigh` or `max` only on representative safety/fidelity evals |

Use `max` for the hardest quality-first workloads only after comparing it with `xhigh`. More reasoning is not automatically better; measure task success, fidelity, latency, and cost.

## Pro mode

Consider `reasoning.mode: "pro"` when:

- a single final answer must integrate many constraints;
- source contradictions require deeper reconciliation;
- high-risk fidelity matters more than latency and token cost;
- ordinary high/xhigh settings miss critical invariants in evals.

Do not use pro mode as a substitute for complete source retrieval or qualified human review.

## Verbosity mapping

Use `text.verbosity` as the host default and task instructions for the exact contract.

| Clarify mode | Suggested verbosity |
|---|---|
| `quick` | `low` |
| `standard`, `compare` | `medium` |
| `flow`, `visual` | `medium` |
| `deep`, `audit`, `high-risk` | `high` only when required by the output contract |

Do not apply generic “be concise” instructions to every mode. Compress by removing repetition and background before conclusion, evidence, material caveat, or next action.

## Persisted reasoning

Use `reasoning.context: "all_turns"` or the GPT-5.6 default when:

- the same source, audience, invariants, and goals remain stable;
- the user iteratively revises one explanation;
- an audit spans several related sections.

Use `reasoning.context: "current_turn"` when:

- the task, source, or governing question changes materially;
- earlier assumptions should not influence the new explanation;
- stale reasoning creates terminology or scope drift.

Always preserve user inputs and relevant response items when managing state manually.

## Structured output

Use the schemas in `references/` when the output feeds another agent, UI, quality gate, or experiment.

Recommended mapping:

```text
Diagnosis stage → diagnosis.schema.json
Technique library → technique-record.schema.json
Final machine artifact → output.schema.json
```

Prefer strict structured output for routing, invariant records, term tables, flow models, and rubric scores. Use free text for the audience-facing explanation unless the consuming interface requires structure.

## Tool exposure

Expose only tools required by the task:

- file/source retrieval for source-dependent transformation;
- current authoritative web sources for unstable or high-risk claims;
- code execution for deterministic lint, validation, or data calculations;
- diagram/rendering tools only when a visual artifact is requested.

Do not expose write or destructive tools to an explanation-only workflow.

## Prompt caching

The stable reusable prefix should include:

- skill metadata;
- core `SKILL.md` contract;
- stable organization-specific terminology or policy.

Load task-specific references and source content after the stable prefix. Benchmark explicit caching on repeated production workloads; do not cache rapidly changing high-risk source material without governance.

## Optimization loop

```text
1. Establish a representative eval set.
2. Start with the current working prompt and medium reasoning.
3. Remove one repeated instruction, irrelevant example, or unused tool group.
4. Re-run trigger, fidelity, task-success, and cost evals.
5. Compare one reasoning level lower and one higher where useful.
6. Keep only changes that preserve or improve the governing metrics.
7. Add examples only when they encode a requirement or repair a measured failure.
```

## Runtime acceptance metrics

Track at least:

- trigger precision and recall;
- material invariant preservation;
- unsupported-claim rate;
- objective comprehension/action score;
- critical-gate pass rate;
- output tokens;
- total tokens and cached tokens;
- latency;
- tool calls;
- human-review correction rate;
- cost per accepted result.

A reduction in tokens, latency, or calls counts as an improvement only when final quality gates still pass.
