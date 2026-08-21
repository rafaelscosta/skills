# High-Risk Clarity Protocol

Use this protocol when misunderstanding may cause material medical, legal, financial, safety, security, privacy, compliance, or irreversible operational harm.

## Core rule

```text
Clarity must increase safe action without increasing unsupported certainty.
```

Do not optimize only for reassurance, brevity, memorability, or confidence.

## Risk classification

### High risk

A misunderstanding can materially affect health, rights, money, security, compliance, or critical operations, but qualified review or recovery remains available.

### Critical risk

A misunderstanding can create immediate severe harm, irreversible loss, unauthorized access, major legal exposure, or an emergency condition.

When uncertain, classify upward until the consequence is understood.

## Source protocol

1. Verify temporally unstable claims using current authoritative sources.
2. Prefer official regulation, standards, clinical guidance, product documentation, and primary research as appropriate.
3. Record jurisdiction, version, effective date, population, and scope.
4. Separate direct source claims from inference.
5. Represent disagreement among reliable sources when it changes action.
6. Do not use a summary source to override an applicable official source.
7. State when source verification is incomplete.

## Invariants that require exact preservation

- mandatory and prohibited actions;
- eligibility and contraindications;
- dose, threshold, unit, range, date, deadline, duration, and frequency;
- jurisdiction and applicability;
- prerequisites and required approvals;
- red flags and emergency escalation;
- authentication, authorization, and data-sensitivity boundaries;
- uncertainty and evidence limitations;
- failure and recovery behavior;
- distinction between information and professional decision authority.

Never convert exact constraints into vague approximations merely to sound simpler.

## Output order

Use this order unless another order is demonstrably safer:

```text
1. Critical action or prohibition
2. Exact condition and scope
3. Immediate consequence
4. What to do now
5. Red flags and escalation
6. Explanation and mechanism
7. Alternatives and recovery
8. Uncertainty, evidence, and authority limits
9. Teach-back or show-me
```

## Language controls

- Use direct verbs for mandatory action: “faça,” “não faça,” “interrompa,” “procure.”
- Do not soften requirements with “talvez,” “pode ser interessante,” or “de preferência.”
- Use “pode” carefully: distinguish possibility from permission.
- Keep numbers beside their units and conditions.
- State absolute risk or baseline when communicating relative risk.
- Avoid euphemism that hides severity.
- Avoid alarmist language unsupported by the actual risk.
- Distinguish symptom/condition, diagnosis, and action.

## Analogy limits

In high-risk content:

- never use an analogy as the sole model;
- place the exact rule before the analogy;
- preserve exact values outside the analogy;
- state where the mapping fails;
- remove the analogy if it changes action or confidence incorrectly.

## Medical communication

Preserve:

- population and condition to which guidance applies;
- dose, route, frequency, duration, and contraindications when present;
- red flags requiring urgent or emergency care;
- difference between general information and individualized diagnosis/treatment;
- uncertainty and differential possibilities;
- interaction and allergy constraints;
- current authoritative guidance.

Do not diagnose from insufficient information or imply professional evaluation is unnecessary when it is material.

## Legal and compliance communication

Preserve:

- jurisdiction;
- effective date;
- binding source versus interpretation;
- definitions and thresholds;
- filing/response deadlines;
- exceptions and procedural rights;
- facts that require counsel or authority review.

Do not present general information as a definitive legal conclusion for facts not established.

## Financial communication

Preserve:

- assumptions;
- fees, taxes, liquidity, leverage, and downside;
- time horizon;
- nominal versus real values;
- base rate and uncertainty;
- distinction between education, analysis, and personalized recommendation.

Do not use a favorable scenario as the default without sensitivity or downside context.

## Security and privacy communication

Preserve:

- threat model;
- authentication versus authorization;
- privilege and trust boundaries;
- data classification;
- credential handling;
- destructive or irreversible actions;
- rollback and recovery;
- disclosure limits that prevent enabling abuse.

Do not reveal sensitive operational detail merely to make a threat explanation complete.

## Critical operations

Preserve:

- preconditions;
- checkpoint/approval authority;
- irreversible boundary;
- backup and recovery state;
- rollback feasibility;
- observability;
- stop conditions;
- escalation owner.

Use a pre-flight checklist and show-me validation before execution when feasible.

## Teach-back protocol

Frame teach-back as a test of the explanation:

> Quero confirmar que expliquei de forma clara. Em quais condições você deve executar essa ação, e quando não deve executá-la?

Then test:

- exact condition;
- exact action;
- prohibited alternative;
- red flag;
- escalation path;
- uncertainty or limit.

Re-explain failed elements using a different representation and recheck.

## Show-me protocol

For procedures, use a safe simulation or non-destructive environment when possible.

Observe:

- prerequisite verification;
- correct target selection;
- branch selection;
- confirmation before irreversible action;
- result verification;
- rollback/escalation.

## Human review boundary

Require qualified human review when:

- source applicability depends on facts not established;
- reliable sources conflict materially;
- the decision is individualized and consequential;
- legal/clinical authority is required;
- the action is irreversible or difficult to recover;
- the explanation exposes an unresolved critical ambiguity;
- automated interpretation cannot be safely validated.

Do not use “human review” as a ritual phrase. Name the required role, decision, evidence, and authority when known.

## High-risk acceptance gate

```text
[ ] Current authoritative basis is verified or verification limits are explicit.
[ ] Jurisdiction/population/version/scope are visible.
[ ] Mandatory and prohibited actions are unambiguous.
[ ] Numbers, dates, thresholds, and units are exact.
[ ] Critical caveats appear before governed action.
[ ] Red flags and escalation are explicit.
[ ] Uncertainty is calibrated rather than erased.
[ ] The explanation does not exceed its authority.
[ ] Recovery or rollback is specified where relevant.
[ ] Teach-back or show-me demonstrates safe action.
[ ] Qualified review is required at the correct boundary.
```
