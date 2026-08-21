# Task-Family Pipelines

Use these pipelines as default sequences, not rigid templates. Skip steps that do not address a diagnosed difficulty. Stop when the audience can demonstrate the intended outcome without fidelity loss.

## Pipeline 1 — Simplify technical language

### Use when

The source is accurate but inaccessible because of jargon, terminology, syntax, abstraction, or hidden prerequisites.

### Sequence

```text
1. Define audience and observable outcome
2. Lock technical invariants
3. Extract concepts and prerequisite dependencies
4. Normalize terminology
5. Repair actor/action/condition syntax
6. Build plain meaning → canonical term bridges
7. Add mechanism and consequence
8. Add representative example and boundary
9. Layer advanced detail
10. Validate by teach-back and transfer
```

### Procedure

1. **Define outcome.** Decide whether the reader must only recognize the idea or use the terminology professionally.
2. **Lock invariants.** Preserve definitions, parameters, thresholds, causal links, exceptions, units, and uncertainty.
3. **Build a term table.** Record canonical term, aliases, simple meaning, example, consequence, and prohibited conflations.
4. **Map prerequisites.** Identify the smallest concepts that must be taught first.
5. **Repair propositions.** Make actors, actions, objects, conditions, and outcomes explicit.
6. **Explain the mechanism.** Avoid definitions that merely restate the label.
7. **Concretize.** Use one representative example and one near-miss when category boundaries matter.
8. **Layer.** Keep a plain first layer and a precise technical layer that refer to the same model.
9. **Validate.** Ask the reader to explain the term and apply it to a new case.

### Stop criteria

Stop when:

- every essential term is understandable at first use;
- canonical vocabulary remains available;
- no unexplained dependency blocks the target concept;
- the audience can classify or apply a new case;
- additional detail would serve reference rather than the stated outcome.

### Common conflicts

| Conflict | Resolution |
|---|---|
| Simple synonym loses technical scope | Keep the canonical term and explain it |
| Glossary interrupts the flow | Define at point of use; retain glossary for later lookup |
| Short sentence fragments the mechanism | Keep related cause/mechanism/effect together |
| Analogy feels clearer than exact model | Lead with exact plain model; analogy remains secondary |

### Default output

```markdown
## Ideia central
## Explicação simples
## Como funciona
## Termos indispensáveis
## Exemplo e limite
## Camada técnica
## Teste de compreensão
```

### Validation

- teach-back of the concept;
- classification of a non-example;
- transfer to a new domain-relevant case;
- terminology consistency audit.

---

## Pipeline 2 — Explain an operational process

### Use when

The reader must understand, execute, supervise, troubleshoot, or improve a workflow.

### Sequence

```text
1. Define purpose and scope
2. Normalize actors, trigger, inputs, outputs, and completion evidence
3. Show macro boundary or SIPOC
4. Explain happy path
5. Add responsibility view
6. Add decisions and states
7. Add failures and recovery
8. Add observability and human controls
9. Convert to executable procedure
10. Validate by trace and show-me
```

### Procedure

1. **Boundary.** State what starts and ends the process and what is excluded.
2. **Inventory.** Extract actors, systems, data, actions, decisions, states, failures, and outputs.
3. **Macro view.** Use a short whole-system narrative or SIPOC.
4. **Happy path.** Show the most common successful route first.
5. **Ownership.** Use a swimlane when handoffs matter.
6. **Logic.** Use a decision table for combinations and a state model for persistent lifecycle behavior.
7. **Recovery.** Distinguish retry, fallback, compensation, rollback, reconciliation, and escalation.
8. **Observability.** Identify logs, metrics, alerts, statuses, and evidence of success.
9. **Procedure.** Write one independently verifiable action per step, with conditions first.
10. **Validation.** Test normal execution, one branch, one common failure, and one escalation.

### Stop criteria

- a newcomer can trace a case from trigger to completion;
- every decision has required information and branch behavior;
- every critical failure has detection and recovery;
- every action has an owner or an explicit unresolved owner;
- completion is externally observable.

### Common conflicts

| Conflict | Resolution |
|---|---|
| Happy path hides a frequent failure | Promote the failure to the first actionable layer |
| Swimlane becomes too wide | Split macro responsibility from detailed subflow |
| Procedure mixes rules and steps | Move combinations to a decision table |
| Architecture appears inside workflow | Use a separate C4/data-flow view |

### Default output

```markdown
## Objetivo e limites
## Visão geral
## Caminho principal
## Responsáveis e transferências
## Decisões e estados
## Falhas e recuperação
## Procedimento operacional
## Como saber que terminou corretamente
```

### Validation

- trace test;
- branch selection;
- state prediction;
- show-me execution;
- failure recovery drill.

---

## Pipeline 3 — Explain software architecture

### Use when

Different audiences need to understand system boundaries, responsibilities, dependencies, data, and runtime interactions.

### Sequence

```text
1. Define architecture question and audience
2. Inventory people, systems, containers, data stores, responsibilities, and relationships
3. Lock source-of-truth status and unknowns
4. Build C4 system-context view
5. Build container view
6. Expand only selected components
7. Add runtime sequence for a representative use case
8. Add data-flow or state view when needed
9. Add failure, security, and observability boundaries
10. Validate through scenario trace and ownership questions
```

### Procedure

1. **Question first.** Separate “what exists?” from “what happens at runtime?”
2. **Inventory.** Record responsibility, technology, interfaces, direction, protocol, data, trust boundary, and owner.
3. **Context.** Show people and external systems around the target system.
4. **Containers.** Show applications and stores, not deployment trivia unless it affects the audience’s decision.
5. **Components.** Expand only the container relevant to the question.
6. **Runtime.** Use a sequence diagram for one important scenario, including timeout/failure where material.
7. **Data.** Use a data-flow view for sensitive or transformed data.
8. **State.** Add state model when lifecycle controls behavior.
9. **Risk.** Mark authentication, authorization, network, data, tenancy, and human approval boundaries.
10. **Unknowns.** Keep unverified relationships visually and textually distinct.

### Stop criteria

- each view answers one declared question;
- adjacent zoom levels are consistent;
- static structure is not confused with runtime order;
- every relationship is labeled with purpose or protocol;
- unknowns are not drawn as established facts;
- a representative request can be traced end to end.

### Common conflicts

| Conflict | Resolution |
|---|---|
| One giant architecture diagram | Split context, containers, components, and runtime |
| C4 container confused with Docker | Define container as deployable/runnable application or data store in the model |
| Sequence diagram implies guaranteed timing | Label sync/async, timeout, retry, and eventual behavior |
| Generated diagram looks plausible but source is incomplete | Mark unknowns and require owner review |

### Default output

```markdown
## Sistema em uma frase
## Contexto
## Containers e responsabilidades
## Cenário de execução
## Dados e estados
## Falhas, confiança e observabilidade
## O que ainda não está confirmado
```

### Validation

- identify owner for a capability;
- trace one request and one failure;
- locate data storage and trust boundaries;
- compare diagram with code/config/source documentation.

---

## Pipeline 4 — Explain strategic reasoning

### Use when

A thesis, recommendation, diagnosis, or business strategy contains many assumptions, causal links, options, and trade-offs.

### Sequence

```text
1. Formulate governing question
2. State provisional answer or decision
3. Build issue tree
4. Separate facts, assumptions, and unknowns
5. Build causal or criteria model
6. Compare alternatives on shared dimensions
7. Organize answer→reasons→evidence
8. Test scenarios and counterfactuals
9. State recommendation, conditions, risks, and next action
10. Validate through transfer or sensitivity test
```

### Procedure

1. **Governing question.** Make it decision-relevant and bounded.
2. **Provisional answer.** Use BLUF when the audience needs action; label it provisional when evidence is incomplete.
3. **Issue tree.** Decompose only into questions that can change the answer.
4. **Epistemic split.** Distinguish observed data, interpretation, assumption, uncertainty, and missing evidence.
5. **Mechanism.** Use causal chain when recommending an intervention; use criteria model when choosing among alternatives.
6. **Comparison.** Evaluate options on common, weighted criteria; expose trade-offs.
7. **Argument.** Structure conclusion, reasons, evidence, caveats, and objections.
8. **Scenarios.** Change key assumptions and observe whether the recommendation changes.
9. **Action.** State decision, owner, trigger, metric, review point, and stop condition.

### Stop criteria

- the recommendation answers the governing question;
- each reason is supported by evidence or labeled assumption;
- alternatives are compared fairly;
- the causal mechanism is explicit where intervention is proposed;
- the recommendation states conditions under which it changes;
- the next action is concrete and measurable.

### Common conflicts

| Conflict | Resolution |
|---|---|
| MECE erases overlapping causes | Preserve overlap and state classification logic |
| Pyramid structure becomes advocacy | Include contradicting evidence and uncertainty |
| Strong narrative outruns evidence | Split observation from interpretation and recommendation |
| Feature matrix hides strategic fit | Weight criteria by the audience’s actual objective |

### Default output

```markdown
## Decisão em uma frase
## Pergunta que está sendo respondida
## Lógica da recomendação
## Evidências e premissas
## Alternativas e trade-offs
## Quando a recomendação deixa de valer
## Próxima ação e métrica
```

### Validation

- counterfactual: which assumption changes the decision;
- transfer: apply criteria to a new option;
- objection test: strongest evidence against the recommendation;
- calibration: confidence compared with evidence quality.

---

## Pipeline 5 — Education and onboarding

### Use when

The audience must build a durable mental model and increasingly independent performance.

### Sequence

```text
1. Define terminal performance
2. Diagnose prior knowledge and misconceptions
3. Build prerequisite sequence
4. Show whole and relevance
5. Segment instruction
6. Model with worked examples
7. Practice jointly with scaffolds
8. Fade support
9. Mix retrieval, prediction, and transfer
10. Revisit with spacing
```

### Procedure

1. **Terminal performance.** Describe what the learner must do without assistance.
2. **Diagnostic.** Use prediction or classification, not confidence alone.
3. **Prerequisites.** Teach the shortest safe foundation.
4. **Orientation.** Explain purpose and the whole before parts.
5. **Segmenting.** Create coherent units with visible progress and transitions.
6. **Modeling.** Show a worked example including decisions and rationale.
7. **Guided practice.** Use “eu faço → fazemos → você faz.”
8. **Fading.** Remove prompts and partial solutions as performance stabilizes.
9. **Discrimination.** Add non-examples and interleaved problem types after basic grounding.
10. **Durability.** Use retrieval and spaced review.

### Stop criteria

- learner performs independently;
- success persists after supports are removed;
- learner predicts and transfers, not only repeats;
- delayed retrieval reaches the required threshold;
- common misconceptions no longer control decisions.

### Common conflicts

| Conflict | Resolution |
|---|---|
| More examples increase passive familiarity | Fade examples and require unaided retrieval |
| Interleaving begins too early | Establish basic category recognition first |
| Immediate success masks non-retention | Add delayed retrieval |
| Tutorial becomes reference manual | Separate modes using Diátaxis |

### Default output

```markdown
## O que você será capaz de fazer
## O mapa do assunto
## Conceitos prévios
## Demonstração guiada
## Prática
## Erros comuns
## Teste de independência
## Revisão futura
```

### Validation

- immediate independent performance;
- delayed retrieval;
- transfer to changed surface context;
- error detection and correction;
- confidence calibration.

---

## Pipeline 6 — Communicate data and numbers

### Use when

The audience must correctly interpret magnitude, comparison, uncertainty, trend, distribution, or risk.

### Sequence

```text
1. Define the decision or question
2. Verify source, population, unit, timeframe, and denominator
3. Choose absolute and relative framing
4. Establish baseline and comparison
5. Expose uncertainty and data limitations
6. Select chart by analytical question
7. Write conclusion-first narrative
8. Add representative numerical example
9. Test interpretation and decision
```

### Procedure

1. **Question.** State what the number is meant to answer.
2. **Provenance.** Record source, scope, collection period, sample, and transformations.
3. **Magnitude.** Show absolute and relative change when both matter.
4. **Denominator.** Keep comparison bases consistent.
5. **Distribution.** Do not use an average alone when variation changes the decision.
6. **Uncertainty.** Include interval, scenario range, sensitivity, missingness, or confidence label.
7. **Chart.** Select comparison, trend, distribution, relationship, composition, or uncertainty view.
8. **Narrative.** State result, context, consequence, caveat, and next question.
9. **Validation.** Ask the audience to restate “how much, compared with what, and with what uncertainty.”

### Stop criteria

- unit, denominator, timeframe, and population are explicit;
- baseline supports the comparison;
- absolute and relative framing cannot mislead;
- uncertainty is visible;
- chart geometry preserves magnitude;
- the audience interprets the number correctly in a new decision.

### Common conflicts

| Conflict | Resolution |
|---|---|
| Simple headline hides uncertainty | Keep uncertainty in the same actionable layer |
| Natural frequency becomes unwieldy | Use consistent percentages plus absolute counts |
| Chart simplifies by deleting distribution | Add distribution or interval view |
| Exact decimals imply confidence | Round according to measurement precision |

### Default output

```markdown
## Principal conclusão
## O número em contexto
## Comparação correta
## Incerteza e limitações
## Representação visual recomendada
## O que esse dado permite — e não permite — concluir
```

### Validation

- absolute versus relative interpretation;
- baseline identification;
- uncertainty-aware choice;
- chart reading task;
- detect a misleading alternative framing.

---

## Pipeline 7 — High-risk explanation

### Use when

Misunderstanding may create health, legal, financial, safety, security, compliance, or materially irreversible harm.

### Sequence

```text
1. Classify risk and decision boundary
2. Verify current authoritative sources
3. Lock exact constraints, thresholds, dates, units, warnings, and uncertainty
4. Separate information from professional decision authority
5. State the critical action or prohibition first
6. Explain mechanism and rationale plainly
7. Layer supporting detail without hiding caveats
8. Add red flags, escalation, and recovery
9. Use teach-back and show-me
10. Require qualified review where appropriate
```

### Procedure

Follow `high-risk-protocol.md` in full.

### Stop criteria

- current authoritative basis is identified;
- exact constraints are visible before action;
- no material caveat is buried;
- uncertainty and limits of authority are explicit;
- emergency/red-flag escalation is unambiguous;
- audience demonstrates correct action, not only recall;
- qualified human review is included when the system cannot safely decide.

### Common conflicts

| Conflict | Resolution |
|---|---|
| Friendly tone softens mandatory action | Use direct requirement/prohibition and consequence |
| Concision removes a caveat | Remove background and repetition first |
| Analogy improves recall but distorts dose/threshold | Keep exact value primary and analogy secondary |
| User asks for certainty unsupported by evidence | State uncertainty and decision limits explicitly |

### Default output

```markdown
## Ação principal
## Condições exatas
## Por que isso importa
## O que fazer agora
## Sinais de alerta e escalonamento
## Incertezas e limites
## Confirmação de compreensão
```

### Validation

- teach-back of condition and action;
- show-me or simulated decision;
- red-flag recognition;
- exact number/unit recall when action depends on it;
- qualified review for material decisions.

## Global stop rule

Do not continue adding explanatory layers merely because they are available.

Stop when:

```text
Fidelity is intact
AND the audience can demonstrate the target outcome
AND remaining detail does not alter the target decision or action
AND the user can access deeper reference detail when needed.
```
