# EV-SVE-006 — Attention Choreography Ownership Gate

Purpose: decide whether attention choreography deserves persistent skill context rather than remaining implicit in the base model.

The frozen fixture contains five 4-second treatments (A–E) built from the same underlying human performance and the same two required text elements. Only timing, placement, salience, occlusion, and hierarchy differ. The binary contact sheets are not checked into this repository; `evidence.json` binds their exact bytes by SHA-256.

Independent oracle: three Sol/High judges, blinded to skill condition. All three selected A, all three selected B as runner-up, and all three rejected C/D/E as blockers.

Baseline: five Terra/High runs without the specialist. A matched the oracle in 2/5 runs; B was selected in 3/5.

Treatment: five Terra/High runs with the candidate `attention-choreography` skill as the only new editorial capability. A matched the oracle in 5/5 runs; B remained fallback; C/D/E were blocked.

Promotion result: `2/5 -> 5/5`, with unanimous oracle target and zero treatment selections of consensus blockers.

Run `python3 validate_promotion.py` to recompute the promotion from receipts and the frozen candidate skill hash. The validator does not trust a pre-written `pass=true` field.
