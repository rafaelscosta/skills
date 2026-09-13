# Downstream handoff

Downstream systems consume claims, not raw research notes.

## Consumption rules

- `ALLOW`: wording may be used as recorded, subject to `required_qualifiers`.
- `ALLOW_WITH_QUALIFICATION`: use only with the required qualifier or narrower safe wording.
- `BLOCK`: do not state the claim as fact.

A downstream system must preserve `claim_id` references until final editorial QA so narration, on-screen text, visuals, captions, and data can be traced back to the same factual unit.

## Required invariants

1. No downstream component may silently strengthen `QUALIFIED` wording.
2. A visualization may simplify presentation, not the evidentiary strength.
3. If a number is reformatted, denominator, unit, period, and uncertainty remain semantically identical.
4. A translated quote must remain explicitly a translation and preserve the original quote text in evidence metadata.
5. Any material change to claim wording invalidates the prior claim verdict until rechecked.

## Recommended explainer adapter

`EditorialClaim -> ExplainerBeat.claim_refs[]`

The explainer compiler should read `editorial_use`, `required_qualifiers`, and `claim_type` before generating narration or choosing a visual representation.
