# Technique Scoring and Contextual Weighting

Use this reference only when comparing multiple plausible techniques, designing a reusable system, or producing an explicit selection audit. Do not turn the score into a universal ranking.

## Scoring scale

Score each technique from 0–5 on every dimension for the specific task.

```text
0 = unusable or actively harmful in this context
1 = weak fit; major support or repair required
2 = limited fit; useful only for a narrow subproblem
3 = adequate fit; meaningful benefit with known limitations
4 = strong fit; high expected value and manageable risk
5 = exceptional fit; directly matches the dominant problem and outcome
```

For `misuse_risk`, a higher score means **greater risk**, so it is subtracted rather than added.

## Dimensions

| Dimension | Operational question |
|---|---|
| `clarity_gain` | How much should this technique reduce the diagnosed difficulty? |
| `precision_preservation` | How well can it preserve definitions, conditions, causality, uncertainty, and exceptions? |
| `ease` | Can the intended operator apply it correctly with available expertise? |
| `speed` | Can it produce value within the available time? |
| `scalability` | Can it be reused, governed, templated, or automated at the required volume? |
| `versatility` | Does it work across the relevant audiences, domains, and media? |
| `accessibility` | Can it support equivalent understanding across relevant access conditions? |
| `validatability` | Does it produce observable outputs that can be tested? |
| `empirical_support` | How strong and applicable is the evidence for the intended outcome? |
| `misuse_risk` | How likely is incorrect application to distort meaning or create false confidence? |

## Weighted score

Normalize weights so positive dimensions sum to 1.0. Apply a separate misuse penalty.

```text
Positive score = Σ(dimension score × dimension weight)
Risk penalty = misuse_risk × misuse_weight
Context score = Positive score − Risk penalty
```

Do not compare context scores created with different weights without showing the weights.

## Default weights by context

### Quick low-risk explanation

```yaml
weights:
  clarity_gain: 0.24
  precision_preservation: 0.15
  ease: 0.13
  speed: 0.18
  scalability: 0.05
  versatility: 0.08
  accessibility: 0.05
  validatability: 0.06
  empirical_support: 0.06
misuse_weight: 0.08
```

### Reusable documentation

```yaml
weights:
  clarity_gain: 0.17
  precision_preservation: 0.17
  ease: 0.08
  speed: 0.06
  scalability: 0.14
  versatility: 0.10
  accessibility: 0.10
  validatability: 0.10
  empirical_support: 0.08
misuse_weight: 0.10
```

### Education and onboarding

```yaml
weights:
  clarity_gain: 0.16
  precision_preservation: 0.12
  ease: 0.07
  speed: 0.04
  scalability: 0.08
  versatility: 0.07
  accessibility: 0.12
  validatability: 0.15
  empirical_support: 0.19
misuse_weight: 0.10
```

### Operational workflow

```yaml
weights:
  clarity_gain: 0.15
  precision_preservation: 0.21
  ease: 0.07
  speed: 0.05
  scalability: 0.10
  versatility: 0.06
  accessibility: 0.07
  validatability: 0.18
  empirical_support: 0.11
misuse_weight: 0.14
```

### High-risk explanation

```yaml
weights:
  clarity_gain: 0.11
  precision_preservation: 0.27
  ease: 0.04
  speed: 0.03
  scalability: 0.04
  versatility: 0.03
  accessibility: 0.12
  validatability: 0.18
  empirical_support: 0.18
misuse_weight: 0.24
```

A high-risk technique is ineligible regardless of score if it cannot preserve critical invariants or support an outcome-matched validation.

## Eligibility gates before scoring

Reject a technique before scoring when any condition applies:

- its information structure does not represent the primary relationship;
- required source facts are absent and the technique would invent them;
- the audience lacks notation literacy and no bridge can be provided;
- a safety-critical invariant would be hidden;
- the technique cannot produce the intended observable outcome;
- a simpler technique fully solves the same problem with lower misuse risk.

## Suggested baseline profiles

These are starting priors, not final context scores. Re-score when audience, medium, or risk changes.

| Technique | Clarity | Precision | Ease | Speed | Scale | Versatility | Access | Validate | Evidence | Misuse risk |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Plain language | 4 | 4 | 4 | 4 | 5 | 5 | 4 | 4 | 4 | 2 |
| Controlled technical language | 3 | 5 | 2 | 2 | 5 | 2 | 3 | 4 | 3 | 3 |
| Point-of-use definition | 4 | 5 | 5 | 5 | 5 | 5 | 4 | 4 | 3 | 1 |
| Terminology bridge | 5 | 5 | 4 | 4 | 5 | 5 | 4 | 5 | 3 | 1 |
| Actor–action–object | 4 | 5 | 4 | 5 | 5 | 4 | 4 | 4 | 3 | 1 |
| BLUF | 4 | 4 | 5 | 5 | 5 | 4 | 4 | 3 | 2 | 2 |
| Pyramid Principle | 4 | 4 | 3 | 3 | 4 | 4 | 3 | 4 | 2 | 2 |
| SCQA | 3 | 3 | 4 | 4 | 4 | 3 | 3 | 2 | 1 | 3 |
| Chunking | 4 | 4 | 4 | 4 | 5 | 5 | 4 | 4 | 5 | 2 |
| Signaling | 4 | 4 | 4 | 4 | 5 | 5 | 4 | 4 | 5 | 2 |
| Progressive disclosure | 4 | 3 | 3 | 3 | 5 | 4 | 3 | 4 | 3 | 4 |
| Layered explanation | 5 | 5 | 3 | 3 | 5 | 5 | 4 | 5 | 3 | 2 |
| Whole–part–whole | 4 | 5 | 4 | 3 | 4 | 5 | 4 | 4 | 3 | 1 |
| Analogy with limits | 4 | 2 | 4 | 4 | 4 | 4 | 3 | 3 | 3 | 5 |
| Concrete example | 4 | 4 | 5 | 4 | 5 | 5 | 4 | 4 | 4 | 2 |
| Non-example | 4 | 5 | 4 | 4 | 5 | 4 | 4 | 5 | 4 | 2 |
| Worked example | 5 | 5 | 3 | 2 | 4 | 4 | 4 | 5 | 5 | 2 |
| Concept map | 4 | 4 | 3 | 3 | 4 | 4 | 3 | 4 | 4 | 3 |
| Flowchart | 4 | 3 | 4 | 4 | 5 | 3 | 3 | 4 | 3 | 3 |
| Swimlane | 5 | 4 | 4 | 3 | 5 | 3 | 3 | 5 | 3 | 2 |
| BPMN | 4 | 5 | 1 | 1 | 4 | 2 | 2 | 5 | 3 | 4 |
| Decision table | 5 | 5 | 3 | 3 | 5 | 3 | 4 | 5 | 4 | 2 |
| State model | 5 | 5 | 3 | 3 | 5 | 3 | 3 | 5 | 4 | 3 |
| Sequence diagram | 5 | 4 | 3 | 3 | 5 | 3 | 3 | 5 | 3 | 3 |
| C4 Model | 4 | 4 | 3 | 3 | 5 | 3 | 3 | 4 | 2 | 3 |
| Event Storming | 4 | 4 | 2 | 1 | 3 | 3 | 3 | 4 | 2 | 3 |
| Teach-back | 4 | 5 | 4 | 3 | 3 | 4 | 4 | 5 | 4 | 1 |
| Show-me | 4 | 5 | 3 | 2 | 2 | 4 | 4 | 5 | 3 | 1 |
| Retrieval practice | 3 | 4 | 4 | 3 | 5 | 5 | 4 | 5 | 5 | 2 |
| Transfer test | 3 | 5 | 2 | 2 | 3 | 4 | 4 | 5 | 5 | 2 |
| Readability metric | 2 | 1 | 5 | 5 | 5 | 4 | 2 | 2 | 2 | 5 |

### Interpreting the baseline table

- A low evidence score does not make a formal notation useless. It means claims about audience comprehension require validation.
- A high misuse score does not prohibit a technique. It raises review and validation requirements.
- Readability metrics score well on speed and scale but poorly on precision and proof of comprehension; use them as lint only.
- Analogy can produce high clarity but also high misuse risk; explicit mapping and boundaries are mandatory.
- BPMN provides high semantic precision but low ease for audiences without notation literacy.

## Pair selection

When two techniques solve different stages, do not force a winner. Select a pipeline.

Example:

```text
Plain language repairs wording.
A state model externalizes lifecycle behavior.
Teach-back verifies the mental model.
```

Score each technique against its assigned stage, then score the pipeline for gaps, redundancy, and cost.

## Pipeline score

A pipeline is only as safe as its weakest critical stage.

```text
Pipeline fidelity = minimum fidelity score among critical stages
Pipeline validation = maximum applicable validation strength only if it tests the final outcome
Pipeline cost = sum of stage costs minus reusable assets
Pipeline misuse risk = maximum critical misuse risk plus interaction penalties
```

Interaction penalties include:

- analogy contradicts diagram;
- summary changes terminology used in procedure;
- progressive disclosure hides a warning;
- visual and text describe different branches;
- worked example uses a rule not present in the reference layer.

## Selection explanation template

Use only when the user requests rationale:

```markdown
### Técnica principal

**[Technique]** was selected because the dominant difficulty is **[difficulty]** and the target outcome is **[outcome]**.

### Why not the nearest alternatives

- **[Alternative A]:** rejected because ...
- **[Alternative B]:** reserved for ...

### Critical preservation rule

...

### Validation

...
```
