# EV-SVE-004 — Multimodal timing specialist promotion gate

## Outcome

**Verdict: NO_PROMOTION.** The candidate `timing-rhythm` specialist did not outperform the control reliably enough to justify persistent instruction/context cost.

## Evidence sequence

1. Initial multimodal fixture exposed a real regression: control beat treatment 3–0 because treatment hid 0.5 s more decisive human performance without repair benefit.
2. A general `timing-rhythm` candidate was created around the policy “use the shortest intervention that fully solves the temporal problem.” It contained no fixture timestamps or answer leakage.
3. On the first rerun, the candidate shortened the cutaway, but the source fixture contained native ghosting immediately after the synthetic defect. Two judges interpreted that native artifact as unresolved defect. That run was marked **confounded**, not a skill failure.
4. A clean fixture was rebuilt from a continuous performance take with one isolated 0.5 s synthetic 1.5× reframing pop. With exact defect bounds visible, control and treatment produced identical 0.5 s repairs.
5. The final hidden-boundary consistency gate ran five independent control and five independent treatment generations. The exact in/out was hidden from the generator and retained only in the oracle.

## Deterministic gate

A run passes only when it:

- uses the contextually valid `mechanical_detail` cutaway;
- fully covers the hidden defect interval;
- keeps cutaway duration at or below 0.75 s;
- preserves the underlying performance outside the repair.

## Final score

- Control: **2 / 5 PASS**
- Treatment (`timing-rhythm`): **2 / 5 PASS**

Treatment therefore produced **0 incremental accepted outcomes**. Its common failure was under-covering the true defect by one 0.125 s sample.

## Architecture decision

Do not add `timing-rhythm` as a standalone skill in v0.1. Keep timing/rhythm as an explicit specialist gap until a future candidate demonstrates a distinct policy with repeatable lift over the frontier-model baseline. The media fixture is intentionally not committed; hashes, task, hidden oracle, and scored outcomes are preserved here.
