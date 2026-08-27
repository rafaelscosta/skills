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

The executable logic was exercised in an isolated local Python harness using the same contracts implemented in this directory, followed by code review of the final fail-closed matching and post-unblind guards.

Observed checks:

1. **Harness firewall — PASS**
   - three self-contained blind input cases detected;
   - three oracle cases detected;
   - blind inputs contain no critical invariants, judge dimensions, expected fields, promotion criteria, or external `source_file` dependency;
   - exact frozen control/treatment commits are distinct and bound in both baselines and sealer;
   - generator protocols explicitly forbid oracle access;
   - Judge protocol explicitly forbids condition-map access before scoring.

2. **Injected oracle leakage — correctly rejected**
   - adding `critical_invariants` to the blind input surface changes harness validation to failed.

3. **Matched-condition sealer — fail closed**
   - verifies exact control and treatment repository commits;
   - requires exactly the expected 3/3 case directories;
   - requires `oracle_seen`, `opposite_condition_seen`, and `prior_judgment_seen` to be false;
   - requires non-empty model, surface, reasoning effort, and tool-budget profile;
   - rejects model/surface/reasoning/tool-budget mismatch before creating the Judge package;
   - verifies `hashes.sha256` for `run-metadata.json` and every file under `cases/`;
   - requires hash paths to be canonical run-relative paths such as `cases/...` without leading `./`.

4. **Blinding sanitizer — PASS**
   - condition identity removed from Judge receipt;
   - repository commit/version identity removed;
   - internal notes/evidence filenames excluded by whitelist;
   - internal renderer artifact names rewritten to generic `artifact-001.ext` names;
   - private map retains control/treatment identity outside the Judge package;
   - public manifest retains only matched experimental metadata plus blinded candidate evidence.

5. **Post-unblind judgment validation — fail closed**
   - condition map and judgment must bind to the exact blinded manifest SHA-256;
   - Judge must be identified and attest `condition_mapping_seen: false`;
   - case IDs must be exactly the expected three;
   - each candidate must score at least one critical invariant;
   - score values must be integers 0–2;
   - each candidate total must equal the sum of its scores;
   - malformed or substituted case sets are invalid rather than merely losing the A/B.

6. **Valid promotion path — PASS**
   - simulated treatment result: 2 case wins, 0 losses, 1 tie;
   - no critical regression;
   - no automatic failure;
   - no fidelity loss;
   - non-catastrophic comparable cost;
   - promotion gate returns passing semantics.

7. **Critical regression — correctly blocked**
   - changing one treatment critical invariant from `passed` to `partial` while control remains `passed` blocks promotion even with 2 case wins.

8. **Catastrophic execution-cost guard — correctly blocked**
   - treatment at 2.5× median elapsed time and 2.5× median tool calls with only 2 case wins triggers the cost guard;
   - a 3/3 treatment sweep may override that cost gate while still reporting the cost ratios.

## Security / validity properties

The harness now enforces:

```text
oracle != generator surface
control baseline != current-main approximation
control context != treatment context
matched execution configuration required before pairing
condition outputs hash-sealed before pairing
condition identity != Judge package
Judge verdict sealed before unblinding
promotion != Judge discretion
```

`seal_pair.py` performs validity and byte-integrity checks **before** producing a blinded package, then uses a private seed-derived A/B mapping and publishes only whitelisted receipts plus generically named artifacts.

`score_ab.py` accepts the private mapping only after the blind judgment exists and verifies judgment structure, expected case IDs, score totals, and exact manifest bindings before applying the promotion policy.

## What remains

A real certification still requires fresh contexts executing the frozen commits declared in `baselines.yaml` under the same model/surface/reasoning/tool-budget configuration.

No result from this implementation session may be substituted for those fresh runs.
