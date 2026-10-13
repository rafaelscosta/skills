# Persuasion Failure Catalog

Use this reference during audit, reconstruction, and adversarial review.

## F01 — Product-before-problem

**Symptom:** The offer appears before the reader has enough context to understand why it should exist.

**Why it fails:** The prospect evaluates features before accepting the problem model.

**Repair:** Establish problem relevance and causal context first, unless traffic is already product-aware and explicitly seeking the offer.

## F02 — Mechanism naming without mechanism explanation

**Symptom:** A branded term is introduced as though naming it proves it works.

**Why it fails:** Category creation is mistaken for causality.

**Repair:** Explain cause → mechanism → effect and then use the name as compression.

## F03 — Testimonial substitution

**Symptom:** Testimonials carry claims that require causal or quantitative evidence.

**Why it fails:** Experience reports do not establish general causality.

**Repair:** Pair testimonials with mechanism, direct evidence, or scoped claims.

## F04 — Claim/evidence mismatch

**Symptom:** Evidence is adjacent to the claim but cannot support the exact claim class.

**Examples:**
- authority used to prove outcome magnitude;
- guarantee used to imply efficacy;
- one case used to imply universality.

**Repair:** Narrow the claim or strengthen the evidence.

## F05 — Generic benefit field

**Symptom:** Benefits could be pasted onto a competitor's page unchanged.

**Repair:** Tie outcome to audience condition, unique mechanism, named artifact, or causal path.

## F06 — Feature dump

**Symptom:** A list of modules, deliverables, or features without a belief or decision job.

**Repair:** For each item identify the implementation gap or decision uncertainty it resolves.

## F07 — Urgency-before-belief

**Symptom:** Countdown, scarcity, or time pressure appears before sufficient value and credibility exist.

**Why it fails:** Pressure substitutes for proof.

**Repair:** Move urgency downstream or remove it.

## F08 — Invented scarcity

**Symptom:** Deadline, stock, cohort size, disappearing bonus, or price rise lacks a real operational basis.

**Repair:** Remove. Never fabricate urgency.

## F09 — Identity coercion

**Symptom:** The page implies that a good/smart/serious person must buy.

**Why it fails:** Identity is used to shame rather than clarify fit.

**Repair:** Use identity to reflect genuine self-selection and implementation readiness, never moral worth.

## F10 — Objection warehouse

**Symptom:** Important objections are dumped into a late FAQ even though they block earlier beliefs.

**Repair:** Resolve objections where they become cognitively relevant.

## F11 — Decorative repetition

**Symptom:** The same claim is restated without adding causal depth, proof, specificity, consequence, contrast, or applicability.

**Repair:** Deepen or delete.

## F12 — Proof-before-meaning

**Symptom:** Impressive statistics or testimonials appear before the reader understands what they prove.

**Repair:** Establish the proposition and causal model first.

## F13 — Unbounded promise

**Symptom:** Outcome is stated without conditions, timeframe, audience fit, or limitations where these are material.

**Repair:** Add scope and evidence boundaries.

## F14 — False binary

**Symptom:** The page frames the offer as the only alternative to failure when legitimate alternatives exist.

**Repair:** Compare honestly against real alternatives and trade-offs.

## F15 — Risk laundering

**Symptom:** Low purchase price is used to imply low total risk despite implementation time, switching cost, privacy, legal, financial, or operational downside.

**Repair:** Model total decision risk, not price alone.

## F16 — Bonus landfill

**Symptom:** Bonuses are added only to inflate nominal value.

**Repair:** Require each bonus to close an implementation, uncertainty, speed, or effort gap.

## F17 — Price anchor theater

**Symptom:** Artificial reference prices or unverifiable value totals are used to make the real price look cheap.

**Repair:** Anchor against genuine alternatives, time, access, replacement cost, or actual tiers.

## F18 — CTA overreach

**Symptom:** The requested action demands more commitment than the current belief state supports.

**Repair:** Lower the commitment or strengthen missing upstream beliefs.

## F19 — Friction after conviction

**Symptom:** The page persuades successfully but introduces unnecessary fields, navigation changes, hidden steps, or uncertainty at conversion.

**Repair:** Remove transaction ambiguity and unnecessary interaction cost.

## F20 — Causal monoculture

**Symptom:** A complex business result is attributed to one mechanism with no consideration of confounders.

**Repair:** Scope the claim and acknowledge material alternative causes.

## F21 — Self-evidence overreach

**Symptom:** Reader recognition is treated as objective proof of the solution.

**Repair:** Use self-evidence for relevance, not universal efficacy.

## F22 — Category without contrast

**Symptom:** A new category is named but the reader cannot distinguish it from known alternatives.

**Repair:** Explain old model, new model, boundary, and practical consequence.

## F23 — Open-loop debt

**Symptom:** Curiosity loops are opened repeatedly and not paid off.

**Repair:** Track each open loop and close it before adding unrelated tension.

## F24 — Transition jump

**Symptom:** The page asks the reader to accept a downstream belief whose prerequisites were never established.

**Repair:** Restore missing dependency nodes.

## F25 — Average-score masking

**Symptom:** A strong total QA score hides a critical dimension below acceptable quality.

**Repair:** Use floor gates. Any critical score below 3/4 blocks certification.

## Audit severity

- `critical` — breaks a prerequisite belief, fabricates evidence/scarcity, or creates materially misleading persuasion.
- `major` — meaningfully reduces credibility, relevance, or action readiness.
- `minor` — local inefficiency, redundancy, or friction that does not break the architecture.

## Repair priority

Repair in dependency order:

```text
truth/evidence
→ problem model
→ causality/mechanism
→ relevance
→ product/offer fit
→ value
→ risk
→ timing
→ transaction friction
→ cosmetic optimization
```

Never optimize button copy while upstream belief gates are broken.
