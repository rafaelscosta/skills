# EV-SVE-006 — Attention Choreography Ownership Gate

Purpose: decide whether attention choreography deserves persistent skill context rather than remaining implicit in the base model.

The frozen fixture contains five 4-second treatments (A–E) built from the same underlying human performance and the same two required text elements. Only timing, placement, salience, occlusion, and hierarchy differ. The binary contact sheets are not checked into this repository; `evidence.json` binds their exact bytes by SHA-256.

Independent oracle: three Sol/High judges, blinded to skill condition. All three selected A, all three selected B as runner-up, and all three rejected C/D/E as blockers.

Baseline: five Terra/High runs without the specialist. A matched the oracle in 2/5 runs; B was selected in 3/5.

Treatment: five Terra/High runs with the candidate `attention-choreography` skill as the only new editorial capability. A matched the oracle in 5/5 runs; B remained fallback; C/D/E were blocked.

Historical reported promotion result: `2/5 -> 5/5`, with unanimous oracle target and zero treatment selections of consensus blockers.

Install the validator dependency with `python3 -m pip install -r requirements.txt`.

To recompute promotion, supply all five original contact sheets:

```bash
python3 validate_promotion.py \
  --fixture A=/path/to/A.png --fixture B=/path/to/B.png \
  --fixture C=/path/to/C.png --fixture D=/path/to/D.png \
  --fixture E=/path/to/E.png \
  --provenance /path/to/original-runs.json
```

The paths may use any extension; each file must match its recorded SHA-256 in
`evidence.json`. Missing, duplicate, unreadable or changed fixtures fail validation.
Each oracle and selection receipt must satisfy its JSON Schema before aggregation;
incomplete receipts and duplicate candidate rankings fail validation.

The recorded `2/5 -> 5/5` result remains historical evidence. Without the external
fixture bytes, fresh promotion and the bundle validator are blocked; a receipts-only
run cannot certify promotion. The validator does not trust a pre-written `pass=true`
field.

The bundle validator accepts the same repeated `--fixture` arguments. Run the
integrity regression tests from the repository root with:

```bash
python3 -m unittest discover -s attention-choreography/evals/EV-SVE-006 -p 'test_*.py' -v
```

These tests use explicitly synthetic fixture bytes and temporary evidence bindings;
they test the validator and do not recertify the historical visual experiment.


Current source integration status: NOT_CERTIFIED_MISSING_ORIGINAL_EVIDENCE. Original visual fixture bytes and original run traces/provenance are absent from this portable bundle. Run counts and similar/different outputs cannot establish independent contexts. The provenance manifest must bind each original receipt, unique run_id/context_id, and a distinct sealed trace file. Both fixture bytes and provenance are required; synthetic integrity-test inputs do not replace them. Historical receipts remain byte-identical.
