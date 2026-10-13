# Source review — 2026-10-13

CODE_READY candidate; NOT_CERTIFIED_CURRENT_CONTRACTS. Machine handoffs now require source_truth and nullable target_duration_seconds, an inspected/located AssetManifest, bound downstream versions, and a QA verdict that cannot pass failed or uncertified blocking gates. Human Markdown remains optional presentation.

Historical model outputs, manifests, judges and scores remain unchanged. They bind the earlier skill bytes. Current contract changes invalidate reuse as certification of the new bytes: default validate_v0_1.py continues to reject drift. --source-only labels its limited scope and does not certify behavior. validate_handoff.py validates actual JSON contracts and source relationships. New independent model holdouts must bind all relevant skill/fixture/output artifacts before promotion. No generated-media, provider, delivery or publication certificate is claimed.

Validation: seven actual handoff regressions passed (including unknown/uninspected/duplicate assets and failed/uncertified gates). Source routing/structure checks passed. Historical fixture EV-SVE-001 does not bind every current downstream contract artifact and cannot independently certify the repaired handoffs.

## Attention candidate integration

The attention route preserves the five existing source-handoff contracts, all historical evidence and the current catalog. Fourteen promotion-validator integrity tests pass with explicitly synthetic fixtures/traces, and seven prior handoff tests continue to pass. Source structure/route validation passes for six skills. The default full validator fails closed for missing original A–E contact sheets and original run provenance. Promotion requires those inputs; current integration is CODE_READY only.
