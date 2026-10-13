# Validation — LLM Orchestrator v1.2.0

Publication gate executed on 2026-09-16.

## Deterministic suites

- Routing stress: **32/32**
- Semantic paraphrase invariance: **3/3**
- Fault injection: **15/15**
- Runtime health / circuit breaker: **13/13**
- Router ↔ circuit integration: **4/4**
- Skill validator: **PASS**
- Fresh project installation: **PASS**

## Real-provider canaries

A disposable mutation task was routed to Codex, fixed the failing test, verified it, attempted independent review with Grok, detected real Grok quota exhaustion, and degraded truthfully to Codex self-review.

A research canary selected Grok first, detected the same quota condition, fell back to Codex, and completed successfully. The subsequent route skipped Grok because the quota circuit was `OPEN`.

## Portability invariant

The package does not ship runtime health state or historical outputs. A missing or corrupt health cache starts from a clean `CLOSED` circuit state and does not block execution.
