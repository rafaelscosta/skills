# Validation and Evaluation

Use this reference to verify that a clarification changed understanding or performance rather than only style preference.

## Core distinction

```text
Clarity perceived ≠ comprehension demonstrated ≠ action performed ≠ retention ≠ transfer
```

Measure the outcome the explanation is intended to produce.

## Outcome-to-test matrix

| Intended outcome | Primary test | Secondary test |
|---|---|---|
| Recognize | Identify valid instance | Reject near-miss |
| Locate | Find required information under time limit | Explain navigation choice |
| Understand | Teach-back | Prediction |
| Remember | Delayed free recall | Cued recall |
| Explain | Reconstruct mechanism in own words | Answer challenge question |
| Compare | Apply common criteria | Explain trade-off |
| Decide | Choose in a new scenario | Sensitivity to changed assumption |
| Execute | Show-me task | Recovery from common error |
| Predict | Next-state or consequence prediction | Justify mechanism |
| Detect errors | Diagnose flawed case | Correct and prevent recurrence |
| Transfer | Structurally new case | Farther-domain application when appropriate |

## Validation techniques

### Teach-back

Prompt:

> Quero verificar se a explicação ficou clara. Com suas próprias palavras, o que acontece e por que?

Evaluate:

- central idea;
- causal mechanism;
- essential condition;
- consequence;
- uncertainty or limitation when material.

Do not grade stylistic similarity. Grade model fidelity.

### Show-me

Prompt:

> Mostre como você executaria esta tarefa a partir do estado inicial apresentado.

Observe:

- prerequisite checks;
- correct order;
- branch selection;
- verification of result;
- failure recognition;
- recovery/escalation.

### Chunk-and-check

After each prerequisite block:

1. ask one reconstruction or prediction question;
2. diagnose the specific gap;
3. re-explain using a different representation;
4. recheck before adding dependencies.

Do not turn every paragraph into a quiz. Place checks at dependency boundaries.

### Prediction

Provide a new initial state and event. Require both result and mechanism.

Weak:

> O que acontece depois?

Strong:

> O pedido está em “aguardando pagamento”. O mesmo evento de pagamento chega duas vezes com a mesma chave de idempotência. Qual deve ser o estado final e por quê?

### Transfer

Preserve deep structure and alter surface details.

A transfer case should not be solvable by copying nouns or numbers from the example.

### Error detection

Create a plausible error that reflects a known misconception. Ask the learner to:

1. locate the error;
2. name the violated rule;
3. explain the consequence;
4. repair the example;
5. propose a prevention cue.

### Retrieval and retention

For durable knowledge:

- test without showing the answer;
- provide corrective feedback;
- repeat after a meaningful delay;
- vary cues and contexts;
- distinguish recognition from recall.

## Quality rubric: 0–2

Score every dimension:

```text
0 = absent, wrong, or materially unsafe
1 = present but incomplete, ambiguous, or weakly fitted
2 = complete, correct, and fitted to the audience/task
```

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Audience fit | Generic or wrong audience | Partial fit | Operationally fitted |
| Main message | Missing/wrong | Present but buried | Immediate and accurate |
| Logical order | Dependencies violated | Mostly coherent | Prerequisite-correct |
| Terminology | Undefined/inconsistent | Minor drift | Stable and defined |
| Sentence clarity | Actors/conditions hidden | Occasional ambiguity | Explicit and executable |
| Causal completeness | Invented/missing | Partial mechanism | Accurate bounded mechanism |
| Fidelity | Invariants changed/lost | Minor risk | All material invariants preserved |
| Example quality | Misleading/irrelevant | Helpful but narrow | Representative plus boundary |
| Visual fit | Wrong semantics/overload | Usable with friction | One-question, semantically correct |
| Actionability | No usable next action | Partial guidance | Correct action and completion evidence |
| Exceptions/recovery | Critical omissions | Some coverage | Material paths explicit |
| Epistemic clarity | Assumptions as facts | Mixed status | Known/inferred/uncertain separated |
| Accessibility | Exclusionary | Partial alternative | Equivalent usable path |
| Validation | “Entendeu?” only | Recall check | Outcome-matched demonstration |

Maximum: 28.

### Critical gates

The following must score `2` for high-risk or operationally consequential material:

- fidelity;
- causal completeness where a causal claim guides action;
- exceptions/recovery;
- epistemic clarity;
- actionability;
- validation.

A high total cannot compensate for failure in a critical gate.

### Suggested thresholds

| Use | Minimum | Additional rule |
|---|---:|---|
| Low-risk quick explanation | 20/28 | No zero in fidelity or main message |
| Standard reusable explanation | 24/28 | No zero; validation at least 1 |
| Operational procedure | 25/28 | Actionability and recovery = 2 |
| High-risk explanation | 27/28 | All critical gates = 2 |

These are governance defaults, not empirical universal constants. Adapt only with explicit rationale.

## Fidelity diff

For source transformations, create an internal invariant table:

```yaml
- invariant: ""
  source_evidence: ""
  transformed_location: ""
  status: "preserved | clarified | intentionally omitted | unresolved"
  risk: ""
```

Any intentionally omitted invariant must be outside the audience outcome and available in a deeper layer or source reference.

## A/B evaluation design

### Basic design

```text
A = original or current explanation
B = clarified explanation
Same audience definition
Same source truth
Same task
Same testing conditions
```

Randomize assignment when practical. Prevent participants from seeing both versions before objective testing unless the design explicitly studies preference.

### Minimum metrics

1. **Comprehension accuracy:** correct model questions.
2. **Fidelity errors:** claims that contradict or omit source truth.
3. **Information location:** time and success finding a rule or answer.
4. **Execution:** task completion, error count, assistance, and recovery.
5. **Retention:** delayed unaided recall.
6. **Transfer:** new-structure application.
7. **Cognitive effort:** self-report plus behavioral proxies such as rereads and time.
8. **Confidence calibration:** confidence minus actual performance.
9. **Preference:** perceived clarity and trust.
10. **Accessibility:** performance under relevant assistive conditions.

### Pre-register the primary outcome

Do not choose whichever metric improved after seeing results.

Example:

```yaml
primary_outcome: "successful recovery from a webhook timeout without assistance"
secondary_outcomes:
  - "time to locate retry policy"
  - "accurate teach-back of idempotency"
  - "perceived clarity"
```

### Separate immediate and delayed measures

```text
Immediate test: comprehension and execution
Delayed test: retention and transfer
```

A version may improve immediate performance without durable learning.

### Control content fidelity

Before user testing, have a domain reviewer compare A and B against the same invariant set. A clearer but inaccurate version is not a success.

### Avoid demand effects

Do not tell participants which version is “simplified.” Use neutral labels and equivalent visual polish when testing the effect of information architecture rather than aesthetics.

## Experiment patterns

### Plain-language test

- **A:** current technical text.
- **B:** same content with terminology bridges, explicit actors, and layered structure.
- **Primary:** correct answers and task action.
- **Secondary:** time, preference, canonical-term retention.
- **Guardrail:** no increase in domain-fidelity errors.

### Diagram-selection test

- **A:** generic flowchart.
- **B:** notation matched to the question, such as swimlane for ownership.
- **Primary:** relationship identification.
- **Secondary:** time and confidence.
- **Guardrail:** equivalent content and labels.

### Progressive-disclosure test

- **A:** all options/details visible.
- **B:** essential layer plus discoverable advanced layer.
- **Primary:** beginner task success.
- **Secondary:** expert task time and hidden-information failures.
- **Guardrail:** safety-critical information visible in both.

### Worked-example test

- **A:** rule plus independent exercises.
- **B:** worked example, faded example, independent exercise.
- **Primary:** independent solution accuracy.
- **Secondary:** transfer and time.
- **Guardrail:** same total content and feedback where possible.

### Teach-back implementation test

- **A:** “Você entendeu?”
- **B:** normalized teach-back with re-explanation and recheck.
- **Primary:** undiscovered misunderstanding rate.
- **Secondary:** task error and user comfort.

### High-risk warning test

- **A:** caveat buried in background text.
- **B:** condition→required action→consequence→escalation first.
- **Primary:** correct action under scenario.
- **Guardrails:** anxiety, false alarm, and overgeneralization.

## Confidence calibration

Ask for confidence after the answer, not before:

```text
0% = puro palpite
50% = vejo duas respostas plausíveis
100% = consigo justificar e aplicar sem ajuda
```

Compute conceptually:

```text
Calibration gap = stated confidence − actual performance
```

High confidence with low performance indicates an explanation that may feel clear but creates illusion of understanding.

## Cognitive-effort measures

Use multiple signals:

- subjective mental effort scale;
- time on task;
- rereads or backtracking;
- requests for clarification;
- abandoned steps;
- working-memory errors;
- eye-tracking only when justified and available.

Do not interpret longer time alone as worse. Deeper processing may improve learning.

## Accessibility evaluation

Select conditions relevant to the medium:

- screen reader navigation;
- keyboard-only operation;
- color-blind-safe interpretation;
- low vision or zoom;
- mobile width;
- captions/transcript;
- low technical literacy;
- second-language readers;
- cognitive pacing control.

Measure the same task outcome, not only standards conformance.

## Evaluation case format

```yaml
id: ""
title: ""
audience: ""
source: ""
intended_outcome: ""
risk_level: ""
known_misconceptions: []
required_invariants: []
expected_mode: ""
required_techniques: []
forbidden_failures: []
tests:
  teach_back: []
  prediction: []
  transfer: []
  show_me: []
acceptance:
  rubric_minimum: 0
  critical_dimensions: []
```

## Self-correction loop

```text
1. Run outcome-matched test.
2. Identify the smallest failed proposition, decision, or action.
3. Diagnose failure type.
4. Select a different representation or technique.
5. Re-explain only the failed dependency and its bridge.
6. Re-test with a new case.
7. Stop when threshold is met or expose unresolved uncertainty.
```

Do not respond to failure by repeating the same explanation more slowly or adding indiscriminate detail.
