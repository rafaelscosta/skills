# Clarify Visual A/B Certification Harness — Validation

## Scope

This report validates the **certification harness**, not Clarify behavioral superiority.

The implementation session is contaminated for generation/judging and therefore did not execute the real control/treatment A/B.

Correct status:

```text
HARNESS IMPLEMENTATION: VALIDATED
FRESH CONTROL RUN: PENDING
FRESH TREATMENT RUN: PENDING
BLIND JUDGE: PENDING
BEHAVIORAL SUPERIORITY CLAIM: NOT YET PERMITTED
```

## Contract checks executed

The executable logic was exercised in an isolated local Python harness using the same contracts implemented in this directory.

Observed checks:

1. **Harness firewall — PASS**
   - three blind input cases detected;
   - three oracle cases detected;
   - control/treatment commits are distinct;
   - generator protocols explicitly forbid oracle access;
   - Judge protocol explicitly forbids condition-map access before scoring.

2. **Injected oracle leakage — correctly rejected**
   - adding `critical_invariants` to the blind input surface changed harness validation to failed.

3. **Blinding sanitizer — PASS**
   - condition identity removed from Judge receipt;
   - repository commit/version identity removed;
   - internal notes/evidence filenames excluded by whitelist;
   - internal renderer artifact name rewritten to generic `artifact-001.html`;
   - private map retained control/treatment identity outside the Judge package.

4. **Valid promotion path — PASS**
   - simulated treatment result: 2 case wins, 0 losses, 1 tie;
   - no critical regression;
   - no automatic failure;
   - no fidelity loss;
   - non-catastrophic comparable cost;
   - promotion gate returned passing semantics.

5. **Critical regression — correctly blocked**
   - changing one treatment critical invariant from `passed` to `partial` while control remained `passed` blocked promotion even with 2 case wins.

6. **Catastrophic execution-cost guard — correctly blocked**
   - treatment at 2.5× median elapsed time and 2.5× median tool calls with only 2 case wins triggers the cost guard;
   - a 3/3 treatment sweep is allowed to override that cost gate while still reporting the cost ratios.

## Security / validity properties

The harness now enforces:

```text
oracle != generator surface
control context != treatment context
condition outputs immutable before pairing
condition identity != Judge package
Judge verdict sealed before unblinding
promotion != Judge discretion
```

`seal_pair.py` uses a private seed-derived A/B mapping and publishes only sanitized receipts plus generically named artifacts.

`score_ab.py` accepts the private mapping only after the blind judgment exists and verifies that both the condition map and judgment bind to the exact blinded manifest SHA-256.

## What remains

A real certification still requires fresh contexts executing the frozen commits declared in `baselines.yaml`.

No result from this implementation session may be substituted for those fresh runs.
