# Persuasion Architect Behavioral Certification

This directory records blind behavioral evidence for the skill. It is not business-outcome proof.

## Protocol

Each run uses three independent model contexts:

1. **Control generator** — receives only the fixture briefs and ordinary model capability.
2. **Treatment generator** — receives the same briefs plus the allowed generator surface of `persuasion-architect`.
3. **Blind judge** — receives the rubric, judge-only oracle, and randomized Candidate A/B outputs.

The A/B mapping is generated after both outputs exist and is withheld from the judge until the judgment file is written.

The judge scores architecture separately from mode-aware behavioral correctness. A truthful `BLOCKED` or conditional state can be a behavioral success when the inputs cannot support a stronger action.

## Fixed rules

- same model and reasoning effort for control and treatment;
- no web or external evidence during generation;
- no oracle or rubric access for generators;
- no skill access for the control condition;
- invented evidence, guarantees, or scarcity are hard failures;
- average score cannot hide a broken critical gate;
- results are unblinded only after the judge output exists;
- post-result fixes require a new holdout before promotion.

## Run 1 — diagnostic certification

Source skill commit: `72d568bae2bb00a929f27e3c3c09457ca421c875` (`0.1.0`).

Model: `gpt-6-astra`, reasoning effort `high`.

Results after unblinding:

- treatment won 5/5 cases;
- average score: treatment `30.6/40`, control `27.0/40`;
- treatment architecture certification: `2/5`; control: `0/5`;
- no generated candidate triggered an invented-evidence or invented-scarcity hard fail;
- strongest gains were belief continuity and transition integrity;
- causal clarity remained a real bottleneck in cases with incomplete mechanism information.

The run was treated as diagnostic rather than promotional evidence. The skill was revised instead of averaging away the failed causal gates.

See `run-2026-09-13/` for the complete control, treatment, randomized pairs, mapping, judgment, and validator receipt.

## Corrective change

Version `0.2.0` adds a mandatory mechanism contract for material outcome claims:

```text
starting condition
→ intervention
→ immediate change
→ intermediate behavior/state
→ bounded expected outcome
```

It also requires scope, prerequisites, alternative causes/confounders, a falsifier, and explicit evidence state. Unknown causal arrows must remain unknown, and the CTA must downgrade or block when the mechanism gate cannot pass.

## Run 2 — fresh holdout after corrective change

The second run uses five new cases not used to derive the causal-clarity fix: legitimate service-capacity scarcity, an AI inbox free trial, an unsupported performance guarantee, a multi-stakeholder onboarding platform, and a vague premium membership.

Model: `gpt-6-astra`, reasoning effort `high`.

Results after unblinding:

- treatment: **4 wins, 1 tie, 0 losses**;
- average score: treatment `35.0/40`, control `32.8/40`;
- architecture certification: treatment `5/5`, control `4/5`;
- behavioral pass: treatment `5/5`, control `5/5`;
- correct terminal state: treatment `5/5`, control `5/5`;
- causal clarity: treatment `3.6`, control `3.2`;
- belief continuity: treatment `4.0`, control `3.2`;
- transition integrity: treatment `4.0`, control `2.8`;
- no hard failures in either condition.

Treatment also retained `4.0` claim/evidence fit. It did not dominate every non-critical dimension: risk asymmetry averaged `2.8` versus control `3.0`, and action readiness `3.2` versus `3.6`. Those remain useful optimization targets rather than hidden by the aggregate score.

See `run-2026-09-13-v2/` for complete evidence.

## Certification verdict

`persuasion-architect` version `0.2.0` passes this behavioral certification protocol for promotion to release-candidate/review status.

This verdict means the skill materially improves the tested persuasion-architecture behavior while preserving truth boundaries. It does **not** establish that pages generated with the skill will increase real-world conversion rates.

## Limits

- one primary model family was used for this certification;
- fixtures are synthetic, although adversarial and mode-diverse;
- the benchmark authors also designed the skill, so the blind judge reduces but does not eliminate benchmark-author bias;
- no live user study or conversion experiment is included;
- future material skill changes should rerun a fresh holdout rather than only these fixtures.
