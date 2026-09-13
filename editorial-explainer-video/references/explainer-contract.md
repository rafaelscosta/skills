# Explainer Contract

## One question, one bounded answer

The plan must define one `question_pt_br` and one `answer_pt_br`. A broad subject such as “IA no trabalho” is not an explanatory question.

## Thesis strength

The thesis may be no stronger than the evidence used to prove it. If a load-bearing claim is qualified, the thesis must preserve the same uncertainty or narrow its scope.

## Mechanism

`central_mechanism_pt_br` explains how the evidence connects to the answer. Use the weakest sufficient relation: definition, chronology, comparison, structural relationship, correlation, plausible cause, or supported cause.

## Claim economy

Use only claims that advance the explanation. Evidence density is not evidence quality. A smaller set of load-bearing claims with clean provenance is preferable to a script padded with facts.

## Script discipline

A factual block carries `fact_bearing: true`, non-empty `claim_refs`, and any required qualifier acknowledgements. A transition or rhetorical question may be `fact_bearing: false` and have no claims.

## Information dependency

Order concepts so a beat never depends on a term, actor, metric, or mechanism the viewer has not yet been given enough context to understand.

## Locks

- `QUESTION_LOCKED`: the video question is stable.
- `THESIS_LOCKED`: answer + must-prove claims are stable.
- `SCRIPT_LOCKED`: wording may move only if claim bindings remain valid.
- `BEATS_COMPILED`: downstream representation can begin.

A change to evidence bytes invalidates all downstream locks that depended on that ledger.
