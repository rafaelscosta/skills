# Evidence contract

## Source

Required fields: `source_id`, `title`, `locator`, `source_type`, `authority`, `freshness`.

Recommended source types:

`PRIMARY | OFFICIAL | DATASET | PAPER | FILING | TRANSCRIPT | SOURCE_CODE | SECONDARY | EXPERT | USER_PROVIDED`

`authority` is an editorial assessment (`HIGH | MEDIUM | LOW | UNKNOWN`), not a claim that the source is infallible.

`freshness`: `CURRENT | AGING | STALE | UNKNOWN` relative to the intended editorial use.

## Binding

Each claim binding records:

- `source_id`;
- `relation`: `SUPPORTS | REFUTES | CONTEXTUALIZES`;
- `locator`: the exact evidence location for this claim;
- optional `excerpt` or compact evidence note.

A source-level URL without a claim-level locator is insufficient for a high-materiality claim.

## Claim

Required fields: `claim_id`, `statement`, `language`, `claim_type`, `materiality`, `epistemic_status`, `editorial_use`, `source_bindings`, `required_qualifiers`, and `time_sensitive`.

### Quantitative

Preserve the full numeric context in `numeric_context`: metric, unit, denominator when applicable, period, comparison basis, and uncertainty when material.

### Quote

Use a `quote` object with `original_text` and `source_language`. If the audience-facing wording is translated, add `translation_pt_br` and never replace the original evidence text.

### Causal

Use a `causal_review` object with `basis`, `contradiction_search: true|false`, and an optional `alternative_explanations` list. A causal claim cannot be certified as `VERIFIED` without an affirmative contradiction search.
