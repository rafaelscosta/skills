# Belief and Evidence Model

Use this reference when building a belief dependency graph, selecting proof, or auditing whether a claim is supported strongly enough.

## Canonical belief layers

A persuasive decision commonly depends on some subset of these layers:

1. **Problem recognition** — the current state is materially undesirable.
2. **Cost recognition** — the status quo has meaningful economic, emotional, temporal, strategic, or identity cost.
3. **Causal reframe** — the current explanation of the problem is incomplete or wrong.
4. **Mechanism plausibility** — the proposed cause/solution relationship makes sense.
5. **Solution plausibility** — the proposed intervention can affect the mechanism.
6. **Provider/product credibility** — this specific source or offer can deliver the intervention.
7. **Personal fit** — the prospect's context matches the conditions under which the intervention is relevant.
8. **Value superiority** — expected upside exceeds price, effort, switching cost, and opportunity cost.
9. **Risk acceptability** — downside is bounded and understandable.
10. **Timing preference** — acting now is better than acting later.
11. **Action readiness** — the next step is sufficiently clear and low-friction.

Do not force all layers into every task. Include only beliefs that are decision-relevant.

## Dependency rules

A belief may depend on one or more earlier beliefs. Examples:

```text
Mechanism plausibility
requires:
- problem definition understood
- causal terms understood

Product fit
requires:
- mechanism plausibility
- product actually contains or enables the mechanism

Value > price
requires:
- desired outcome valued
- expected mechanism credible
- price understood
- major costs and alternatives understood

Urgency
requires:
- value already credible
- timing claim independently grounded
```

A downstream block cannot repair an upstream missing prerequisite merely by becoming more forceful.

## Evidence taxonomy

### logical_proof
Use when the claim can be supported by transparent reasoning from accepted premises.

Best for:
- causal explanation;
- definitional distinctions;
- dependency logic.

Failure mode: valid-sounding rhetoric built on an unsupported premise.

### mechanism_proof
Shows why an intervention should produce an effect.

Best for:
- new mechanisms;
- technical or process claims;
- contrarian reframes.

Failure mode: naming a mechanism without showing its causal chain.

### demonstration
Shows the process or result directly.

Best for:
- tools;
- workflows;
- transformations;
- before/after behaviors.

Failure mode: staged demonstration presented as general proof.

### case_study
Documents one or more real implementations with context.

Best for:
- applied business outcomes;
- complex interventions.

Minimum useful fields:
- starting state;
- intervention;
- timeframe;
- measured outcome;
- relevant confounders or limits.

### testimonial
Reports a person's experience or judgment.

Best for:
- perceived quality;
- usability;
- subjective experience;
- trust support.

Weak for:
- proving general causal claims;
- proving exact expected outcomes.

### quantitative
Uses measured aggregate or individual data.

Best for:
- magnitude;
- frequency;
- benchmark comparisons.

Require denominator, timeframe, measurement definition, and source when material.

### authority
Uses expertise, track record, credentials, institutional role, or recognized competence.

Best for:
- source credibility.

Weak for:
- substituting authority for direct evidence of a specific claim.

### comparison
Shows differences against an alternative, baseline, control, or previous state.

Best for:
- differentiation;
- trade-off clarity;
- old-way/new-way architecture.

Failure mode: asymmetric comparison with selectively favorable dimensions.

### artifact
Shows that a claimed asset, system, product, or deliverable really exists.

Best for:
- implementation offers;
- templates;
- systems;
- named mechanisms.

### transparency
Explains incentives, limitations, pricing logic, trade-offs, or business model openly.

Best for:
- suspicion reduction;
- price anomalies;
- trust repair.

### guarantee
Bounds downside or transfers specific risk.

Best for:
- perceived risk reduction.

A guarantee is not evidence that the outcome will occur. It is evidence about downside allocation.

### self_evidence
Invites the prospect to verify the claim against their own observable experience.

Best for:
- recognition;
- symptom reinterpretation;
- diagnosis.

Failure mode: leading questions that manufacture false recognition.

## Evidence threshold

Use this heuristic:

```text
required_strength = claim_strength × perceived_improbability × decision_risk
```

Treat each factor qualitatively as low, medium, high, or extreme.

Examples:

| Claim | Improbability | Risk | Minimum evidence |
|---|---|---:|---|
| "Includes 25 chapters" | low | low | artifact/product detail |
| "Reduces no-shows" | medium | medium | mechanism + case/demo |
| "Doubles close rate" | high | medium-high | strong quantitative case evidence with context |
| "Works for almost everyone" | extreme | high | broad robust evidence; otherwise reject claim |

## Claim-evidence fit test

For every material claim ask:

1. What exactly is being asserted?
2. Is it descriptive, causal, comparative, predictive, or universal?
3. What evidence type can actually support that claim class?
4. Is the available evidence direct or merely adjacent?
5. What uncertainty remains?
6. Would a skeptical reader reasonably infer more than the evidence establishes?

Mark one result:

- `supported`
- `partially_supported`
- `unsupported`
- `unverifiable_from_available_inputs`

Never upgrade an evidence state through stronger wording.

## Proof ordering

Prefer:

```text
understand claim
→ understand causal logic
→ see appropriate evidence
→ infer consequence
```

Avoid leading with impressive proof when the reader cannot yet tell what the proof is supposed to establish.

## Self-evidence caution

Self-recognition can be powerful, but it must not replace objective evidence where the decision risk is material.

Use it to establish relevance, not to manufacture certainty.
