# Diagnostic Taxonomy

Use this reference to identify why material is difficult before selecting an intervention.

## Diagnostic principle

Do not label content “complex” as a single problem. Complexity is an interaction among:

```text
Audience gap × content structure × representation × task demand × consequence of error
```

Diagnose observable failures, not stylistic preferences.

## Operational audience contract

Complete internally or expose in audit mode:

```yaml
audience:
  identity: ""
  prior_knowledge: "none | low | working | advanced"
  familiar_terms: []
  likely_misconceptions: []
  accessibility_needs: []
  context_of_use: ""
outcome:
  verb: "recognize | locate | understand | remember | explain | compare | decide | execute | predict | detect | transfer"
  observable_behavior: ""
  conditions: ""
  unacceptable_errors: []
constraints:
  format: ""
  time_budget: ""
  risk_level: "low | medium | high | critical"
```

A useful outcome is observable. “Understand APIs” is weak. “Given a webhook failure, identify the sender, receiver, expected payload, status, and next recovery action” is operational.

## Difficulty taxonomy

### 1. Lexical difficulty

**Definition:** Individual words are unfamiliar, rare, bureaucratic, archaic, or needlessly abstract.

**Symptoms**

- the audience stops at individual words;
- frequent dictionary dependence;
- many nominalizations and Latinate constructions;
- simpler synonyms preserve the same meaning.

**Diagnostic question:** Would replacing a few words substantially repair comprehension without changing the structure?

**Primary interventions:** familiar vocabulary, concrete verbs, point-of-use definitions.

**Do not confuse with:** terminological difficulty, where the technical term itself is necessary and must be learned.

**Validation:** recognition of the idea without needing to paraphrase the difficult word.

### 2. Terminological difficulty

**Definition:** Domain terms are undefined, inconsistent, overloaded, or used with unstable meanings.

**Symptoms**

- several names refer to the same entity;
- the same term refers to multiple entities;
- acronyms appear before expansion;
- local jargon conflicts with industry terminology;
- the audience can read the sentence but cannot identify the concept.

**Diagnostic question:** Can every essential term be mapped to exactly one concept in this context?

**Primary interventions:** controlled vocabulary, one concept–one term, one term–one meaning, term bridge, glossary.

**Validation:** correct classification of new examples using the terms.

### 3. Syntactic difficulty

**Definition:** Sentence structure hides actors, actions, conditions, references, or logical relations.

**Symptoms**

- long nested clauses;
- ambiguous pronouns;
- passive constructions hide responsibility;
- conditions appear after actions;
- one sentence contains multiple independent instructions;
- connectors do not match the logical relation.

**Diagnostic question:** Can the reader identify who does what, to which object, under which condition, and with what consequence?

**Primary interventions:** actor–action–object, condition before action, one action per instruction, explicit connectors, pronoun repair.

**Validation:** the audience can reconstruct the proposition or perform the instruction without asking who or when.

### 4. Semantic difficulty

**Definition:** The wording permits multiple interpretations or relies on unstated distinctions.

**Symptoms**

- two competent readers infer different meanings;
- vague quantifiers such as “often,” “adequate,” or “soon” govern decisions;
- category boundaries are implicit;
- key verbs lack operational definitions.

**Diagnostic question:** What alternative interpretations remain compatible with the sentence?

**Primary interventions:** operational definitions, explicit scope, quantified thresholds, examples and non-examples.

**Validation:** independent readers make the same classification or decision.

### 5. Conceptual difficulty

**Definition:** The audience lacks the mental model needed to integrate the claims.

**Symptoms**

- every sentence is understandable, but the whole is not;
- the audience memorizes labels without predicting behavior;
- new concepts depend on missing prerequisites;
- abstract categories have no concrete instantiation.

**Diagnostic question:** What model must exist in the reader’s mind for these facts to cohere?

**Primary interventions:** prerequisite map, known-to-new, whole–part–whole, abstraction ladder, examples/non-examples, concept map.

**Validation:** prediction or transfer to a structurally new case.

### 6. Causal difficulty

**Definition:** The material states that events are related but does not reveal why, through which mechanism, or under which conditions.

**Symptoms**

- “A causes B” skips intermediate steps;
- correlation is presented as causation;
- feedback loops are flattened into linear sequences;
- necessary and sufficient conditions are confused;
- interventions are recommended without a mechanism.

**Diagnostic question:** What changes between cause and effect, and what would happen if a proposed link were absent?

**Primary interventions:** cause→mechanism→effect chain, causal graph, counterfactual, boundary conditions.

**Validation:** justified prediction after changing one causal input.

### 7. Structural difficulty

**Definition:** Important information exists but is ordered, grouped, or prioritized poorly.

**Symptoms**

- the conclusion appears late;
- details arrive before the whole;
- related information is scattered;
- headings name topics rather than answer questions;
- the reader cannot tell what is primary versus supporting.

**Diagnostic question:** Is the reader forced to reconstruct the architecture of the message?

**Primary interventions:** main message, BLUF, Pyramid Principle, chunking, signaling, progressive disclosure, layered explanation.

**Validation:** rapid retrieval of the main point and supporting reasons.

### 8. Procedural difficulty

**Definition:** A task or process lacks an executable sequence, decision logic, ownership, or recovery behavior.

**Symptoms**

- verbs are descriptive rather than executable;
- steps mix actions and explanations;
- prerequisites are missing;
- branches and stop conditions are unclear;
- failures have no recovery path;
- users know what the system is but cannot operate it.

**Diagnostic question:** Can a competent newcomer complete the task and recover from a common failure using only the material?

**Primary interventions:** trigger→input→step→decision→output model, one action per step, happy path, decision table, swimlane, state model, failure/recovery protocol.

**Validation:** show-me task with observed completion and error recovery.

### 9. Decisional difficulty

**Definition:** The reader must choose among options but criteria, trade-offs, evidence, or branch rules are unclear.

**Symptoms**

- comparisons list features without decision relevance;
- options are not evaluated on common dimensions;
- criteria conflict without weights;
- exceptions overwhelm a narrative explanation;
- the recommendation is detached from constraints.

**Diagnostic question:** What evidence changes the choice, and how?

**Primary interventions:** issue tree, MECE decomposition, criteria matrix, decision tree/table, scenarios, sensitivity analysis.

**Validation:** consistent choice in a new case with explicit rationale.

### 10. Numerical difficulty

**Definition:** Quantities are mathematically correct but hard to interpret, compare, or act on.

**Symptoms**

- changing denominators;
- percentages without baselines;
- averages hide distributions;
- units or timeframes are omitted;
- false precision;
- uncertainty is invisible;
- chart choice obscures comparison.

**Diagnostic question:** Can the audience say “how much, compared with what, over which period, and with what uncertainty?”

**Primary interventions:** natural frequencies, consistent denominators, familiar units, baseline and timeframe, uncertainty interval, suitable chart.

**Validation:** accurate comparison and consequence estimation.

### 11. Visual-relational difficulty

**Definition:** Relationships are hard to perceive in prose or are distorted by an unsuitable visual representation.

**Symptoms**

- the reader repeatedly traces relationships manually;
- one diagram mixes sequence, architecture, responsibility, and state;
- crossing lines dominate;
- color carries meaning without labels;
- symbols are visually distinct but semantically undefined.

**Diagnostic question:** Which relationship must become perceptually obvious: order, responsibility, dependency, state, causality, hierarchy, comparison, or quantity?

**Primary interventions:** select one-question visual, progressive zoom, semantic labels, accessible text equivalent.

**Validation:** relationship identification without explanatory rescue.

### 12. Epistemic difficulty

**Definition:** The material hides what is known, inferred, uncertain, disputed, or outside scope.

**Symptoms**

- claims have uniform confidence despite unequal evidence;
- assumptions are stated as facts;
- competing explanations are collapsed;
- missing evidence is filled with plausible language;
- the audience cannot judge what to trust.

**Diagnostic question:** What is the status and evidential basis of each material claim?

**Primary interventions:** known/assumed/uncertain/out-of-scope split, evidence labels, confidence calibration, competing-model comparison.

**Validation:** audience distinguishes fact, inference, uncertainty, and open question.

### 13. Contextual or pragmatic difficulty

**Definition:** The explanation is technically correct but not fitted to the audience’s purpose, situation, culture, or decision.

**Symptoms**

- examples are unfamiliar or culturally narrow;
- detail level mismatches time available;
- the answer addresses “what is it?” when the user needs “what do I do?”;
- formality, channel, or accessibility is wrong;
- implications for the audience are absent.

**Diagnostic question:** What must this audience do with the information here and now?

**Primary interventions:** audience contract, task-centered framing, localization, use-case scenarios, adaptive depth.

**Validation:** successful action in the actual context of use.

### 14. Cognitive-load difficulty

**Definition:** Too many interacting elements must be held or integrated at once, including avoidable presentation burden.

**Symptoms**

- overloaded slides or diagrams;
- split attention between distant text and labels;
- decorative material competes with essential content;
- all exceptions appear before the default model;
- long sequences have no chunking or external memory support.

**Diagnostic question:** Which simultaneous mental operations are necessary, and which are imposed by presentation?

**Primary interventions:** segmenting, signaling, spatial contiguity, worked examples, externalized checklists, progressive disclosure.

**Validation:** lower error and completion time at equal content fidelity.

### 15. Motivational or relevance difficulty

**Definition:** The audience can understand the content but does not see why it matters, when to use it, or what problem it solves.

**Symptoms**

- correct explanation is ignored or abandoned;
- purpose appears after detailed theory;
- examples do not resemble real tasks;
- no consequence or payoff is visible.

**Diagnostic question:** What practical tension, decision, or outcome makes this knowledge worth processing?

**Primary interventions:** problem-first framing, concrete consequence, authentic scenario, action relevance.

**Validation:** audience can state when and why the concept is useful.

### 16. Accessibility difficulty

**Definition:** The representation excludes or burdens people because of sensory, cognitive, linguistic, motor, or device constraints.

**Symptoms**

- meaning depends on color, hover, sound, or visual position alone;
- labels are missing;
- dense paragraphs or tables break on mobile;
- acronyms are not expanded;
- no text alternative exists;
- timing cannot be controlled.

**Diagnostic question:** Can the intended outcome be reached through more than one perceivable and operable path?

**Primary interventions:** text alternatives, semantic structure, redundant cues, controllable pacing, plain labels, accessible tables and diagrams.

**Validation:** task completion with relevant assistive conditions and devices.

## Complexity interaction patterns

Some combinations require specific handling.

| Pattern | Typical failure | Correct response |
|---|---|---|
| Lexical + conceptual | Word replacement creates an illusion of clarity | Teach the missing model, then simplify terms |
| Structural + cognitive-load | Shorter text remains disorienting | Reorder and chunk before compressing |
| Procedural + decisional | Narrative steps hide branches | Use a decision table/tree plus procedure |
| Causal + epistemic | Confident mechanism is invented | Separate evidence from inference before explaining |
| Visual + accessibility | Elegant diagram excludes part of the audience | Add semantic labels and a text-equivalent path |
| High-risk + analogy | Memorable analogy erases constraints | Lead with exact model; use analogy only as support |
| Numerical + decisional | Correct numbers do not guide a choice | Add baseline, thresholds, weights, and uncertainty |
| Terminological + organizational | Teams use different words for the same object | Establish a controlled vocabulary before rewriting |

## Severity and priority

Score each diagnosed difficulty from 0–3:

```text
0 = absent
1 = friction: slows comprehension but rarely changes meaning
2 = material: causes recurring misunderstanding or action errors
3 = critical: can reverse meaning, ownership, decision, or safety outcome
```

Prioritize by:

```text
Priority = severity × consequence × dependency
```

Repair prerequisite and fidelity-critical defects before readability defects.

## Diagnostic decision sequence

```text
1. What must the audience be able to do?
2. What must remain exactly true?
3. Where does current performance fail?
4. Is the failure primarily in source logic, audience knowledge, wording, structure, representation, or validation?
5. Which single repair would remove the largest blocking dependency?
6. Which secondary repair prevents distortion?
7. What observable task will demonstrate success?
```

## Minimum diagnostic output

Use this only in audit mode or machine-readable output:

```yaml
diagnosis:
  audience_outcome: ""
  primary_difficulty:
    type: ""
    severity: 0
    evidence: []
  secondary_difficulties: []
  missing_prerequisites: []
  fidelity_risks: []
  recommended_mode: "quick | standard | deep | flow | compare | audit | visual | high-risk"
  success_test: ""
```
