# Flow Explanation Protocol

Use this reference for workflows, lifecycles, procedures, automations, APIs, business processes, operational routines, and systems with states or handoffs.

## First determine the primary flow question

Choose one:

```text
What happens and in what order?
Who is responsible for each step?
What data moves where?
What messages are exchanged over time?
Which state changes are allowed?
Which conditions select each action?
What can fail and how does recovery work?
Where are delays, bottlenecks, or control points?
```

Do not force all questions into one representation.

## Normalize the flow model

Extract these fields before writing or diagramming:

```yaml
flow:
  purpose: ""
  scope:
    starts_when: ""
    ends_when: ""
    exclusions: []
  preconditions: []
  trigger: ""
  actors: []
  systems: []
  inputs: []
  happy_path: []
  decisions: []
  parallel_branches: []
  states: []
  outputs: []
  completion_evidence: []
  failures: []
  recovery: []
  human_interventions: []
  observability: []
```

If a field is unknown, mark it unknown. Do not manufacture it.

## Explain in progressive views

### View 1 — Purpose and boundary

Answer:

- Why does this flow exist?
- What starts it?
- What result proves completion?
- What is outside scope?

Use 2–5 sentences or a SIPOC when stakeholder boundaries are disputed.

### View 2 — Happy path

Show only the normal successful route:

```text
Trigger → validate → process → confirm → complete
```

For each step, name actor, action, object, and observable result.

### View 3 — Decisions and alternate paths

For every decision, record:

```yaml
- question: ""
  evaluated_by: ""
  required_data: []
  branch_yes: ""
  branch_no: ""
  other_branches: []
  default_or_unknown_behavior: ""
```

Use a decision table when multiple conditions interact. Use a tree when decisions are sequential and mutually discriminating.

### View 4 — States

Use states when the system persists a meaningful condition over time.

For each state:

```yaml
- state: ""
  entered_by: ""
  allowed_events: []
  resulting_states: []
  invalid_events: []
  exit_condition: ""
```

Name states as stable conditions, not activities:

```text
Good: aguardando aprovação
Weak: aprovar documento
```

### View 5 — Failures and recovery

For each failure, explain:

```text
Failure condition
→ how it is detected
→ immediate state
→ automatic recovery
→ retry policy
→ fallback or compensation
→ escalation threshold
→ human intervention
→ terminal outcome
```

Do not write “o sistema trata o erro” without the behavior.

### View 6 — Observability and control

Identify:

- logs and events;
- status visible to users;
- metrics and service levels;
- alerts;
- correlation or trace identifiers;
- audit trail;
- manual pause/cancel/override;
- evidence that recovery succeeded.

A flow cannot be operationally managed if failure is invisible.

## Failure taxonomy

### Validation failure

Input violates a rule before processing.

Preserve:

- failed field/rule;
- user-visible correction;
- whether partial data is saved;
- retry conditions.

### Authentication or authorization failure

Identity cannot be confirmed or permission is absent.

Preserve:

- distinction between unauthenticated and unauthorized;
- token/key scope;
- retry versus escalation;
- security-sensitive disclosure limits.

### Timeout

Expected response does not arrive before a defined limit.

Preserve:

- timeout threshold;
- whether work may still finish remotely;
- duplicate-risk on retry;
- status reconciliation.

### Transient dependency failure

An external service is temporarily unavailable.

Preserve:

- retry count;
- backoff strategy;
- jitter if relevant;
- retryable status classes;
- terminal queue/dead-letter behavior.

### Permanent business failure

The request is valid structurally but violates a business rule.

Preserve:

- reason code;
- corrective action;
- non-retryability unless data changes.

### Partial failure

Some parallel or composite operations succeed and others fail.

Preserve:

- committed effects;
- compensation/rollback behavior;
- reconciliation state;
- user-visible truth.

### Duplicate or replay

The same logical operation arrives more than once.

Preserve:

- identity key;
- idempotency window;
- response replay behavior;
- side-effect guarantees.

### Concurrency conflict

Multiple operations compete to change the same state.

Preserve:

- locking/version rule;
- winner/loser behavior;
- retry or merge policy;
- conflict visibility.

### Human delay or rejection

The flow waits for a person or receives a negative decision.

Preserve:

- owner;
- service-level target;
- reminders;
- escalation;
- rejection reason;
- resubmission path.

## Retry, fallback, compensation, and rollback

Do not treat these as synonyms.

| Mechanism | Meaning | Use when |
|---|---|---|
| Retry | Repeat the same operation | Failure may be transient and repetition is safe |
| Fallback | Use an alternate method or dependency | Primary path is unavailable but a degraded path is acceptable |
| Compensation | Apply a new action that semantically reverses a prior effect | Distributed effects cannot be atomically rolled back |
| Rollback | Restore a previous transaction/state | The system supports safe reversal of the committed unit |
| Reconciliation | Compare records and repair divergence | Completion status is uncertain or systems disagree |
| Escalation | Transfer unresolved control to a higher authority or human | Automated policy reaches a limit |

Always explain what has already happened before recovery begins.

## Parallelism

When branches run concurrently, identify:

```text
fork condition
branch owners
shared resources
independent vs dependent completion
join condition
timeout behavior
partial success policy
ordering guarantees
```

Use explicit fork/join notation or separate branch tables. Do not imply sequence merely through vertical placement.

## Loops

For every loop, state:

- what repeats;
- why it repeats;
- who controls repetition;
- maximum attempts or stop condition;
- state carried between attempts;
- what happens after exhaustion.

Avoid diagrams with unlabeled backward arrows.

## Human-in-the-loop points

For each human checkpoint, state:

```yaml
human_gate:
  purpose: "approve | review | correct | choose | override | investigate"
  assigned_role: ""
  evidence_available: []
  allowed_actions: []
  deadline: ""
  escalation: ""
  audit_record: ""
  automation_boundary: ""
```

Do not use “human review” as a vague assurance. Define authority and effect.

## Textual flow format

Use this when a visual is unnecessary or must have an accessible equivalent:

```markdown
### Gatilho

### Pré-condições

### Caminho principal
1. **[Ator]** executa **[ação]** sobre **[objeto]**.
   - Resultado esperado: ...

### Decisões
- **Se [condição]:** ...
- **Caso contrário:** ...

### Saída e evidência de conclusão

### Falhas e recuperação

### Intervenções humanas

### Observabilidade
```

## Flow quality gate

```text
[ ] Start and end conditions are explicit.
[ ] Preconditions are distinct from the trigger.
[ ] Every action has an accountable actor or an explicit unknown.
[ ] Inputs and outputs are named.
[ ] Decision questions and branch conditions are complete.
[ ] Persistent states are distinguishable from activities.
[ ] Parallelism and joins are explicit.
[ ] Loops have termination conditions.
[ ] Failures include detection and resulting state.
[ ] Retry, fallback, compensation, rollback, and escalation are not conflated.
[ ] Human checkpoints define authority and deadlines.
[ ] Completion has observable evidence.
[ ] The visual and textual versions describe the same behavior.
```

## Flow validation tasks

Use at least one:

- **Trace:** Given input X, narrate the path to completion.
- **Branch:** Given condition Y, identify which path applies and why.
- **State:** Given event Z in state S, predict the next valid state.
- **Failure:** Given timeout after step N, identify prior effects and recovery.
- **Ownership:** Identify who owns the next action and escalation.
- **Replay:** Predict what happens if the same request arrives twice.
- **Partial success:** Explain user-visible state when one parallel branch fails.
