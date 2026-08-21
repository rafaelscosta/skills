# Technique Selector

Use this reference after diagnosis. Select the smallest sufficient intervention set.

## Selection rule

```text
WHEN [observable difficulty]
AND [audience/task conditions]
APPLY [primary technique]
WITH [bounded parameters]
PRESERVE [material invariants]
AVOID [known failure]
VALIDATE BY [observable test]
RECOVER WITH [repair technique]
```

Do not select a technique because it is familiar or fashionable. Select it because its information structure matches the diagnosed failure.

## Evidence labels

- **A — strong/authoritative:** official standard, systematic review, meta-analysis, or repeatedly supported mechanism.
- **B — moderate:** controlled studies or converging research with material boundary conditions.
- **C — institutional/practice-supported:** established professional method with strong operational rationale but limited direct comparative evidence.
- **D — heuristic:** useful practitioner pattern with sparse or indirect empirical validation.
- **Mixed:** results depend strongly on domain, implementation, prior knowledge, or outcome measure.

The label concerns the technique as used here, not every claim made about it.

## Audience and prerequisite techniques

### Operational audience definition

- **Use when:** “beginner,” “executive,” or “general public” is too vague to determine depth or action.
- **Procedure:** identify prior knowledge, context, desired observable behavior, unacceptable errors, and constraints.
- **Output:** one-sentence audience contract.
- **Avoid:** demographic personas without task evidence.
- **Validate:** a reviewer can tell what successful understanding looks like.
- **Evidence:** C; grounded in user-centered communication and instructional design.

### Prior-knowledge map

- **Use when:** explanations fail despite simple wording or experts disagree about what is “basic.”
- **Procedure:** list known, required-new, unnecessary-now, and likely-misconceived concepts; connect dependencies.
- **Output:** prerequisite map.
- **Avoid:** self-report as the only measure when stakes are high.
- **Validate:** a diagnostic task distinguishes familiarity from usable knowledge.
- **Evidence:** B; prior knowledge is a major moderator of instructional effectiveness.

### Minimum viable prerequisite

- **Use when:** the target concept depends on hidden foundations.
- **Procedure:** trace dependencies backward; retain only prerequisites necessary for the stated outcome; teach those first.
- **Output:** shortest safe learning path.
- **Avoid:** reducing prerequisites until prediction or execution becomes impossible.
- **Validate:** learner succeeds without unexplained intermediate terms.
- **Evidence:** B/C.

### Misconception map

- **Use when:** the audience has a plausible but incorrect model.
- **Procedure:** elicit prediction; identify rule causing the error; contrast with discriminating case; rebuild model.
- **Output:** misconception→evidence→replacement model.
- **Avoid:** merely stating “this is wrong” without replacing the mechanism.
- **Validate:** prediction changes on a novel case.
- **Evidence:** B/Mixed by domain.

## Decomposition and reasoning techniques

### Feynman-style explanation audit

- **Use when:** the explainer may be hiding gaps behind jargon.
- **Procedure:** explain from memory in plain terms; mark vague links; verify against source; reconstruct with explicit mechanism.
- **Output:** gap list and repaired explanation.
- **Avoid:** treating simplicity as proof of correctness.
- **Validate:** domain review plus transfer question.
- **Evidence:** D as a branded technique; supported indirectly by retrieval and self-explanation research.

### First-principles decomposition

- **Use when:** assumptions are being inherited without inspection.
- **Procedure:** separate observations, definitions, constraints, assumptions, and derived claims; rebuild only from justified elements.
- **Output:** foundation→derivation map.
- **Avoid:** ignoring mature domain knowledge or re-deriving facts without evidence.
- **Validate:** each conclusion traces to explicit premises.
- **Evidence:** D as a method; logical validity is case-specific.

### Concept inventory

- **Use when:** source material contains many implicit entities, rules, states, or dependencies.
- **Procedure:** extract actors, objects, actions, states, rules, decisions, inputs, outputs, failures, and uncertainties; deduplicate.
- **Output:** normalized model inventory.
- **Avoid:** treating every noun as an independent concept.
- **Validate:** all source claims map to inventory elements without orphan relations.
- **Evidence:** C.

### Dependency tree or graph

- **Use when:** concepts arrive before prerequisites or execution order is unclear.
- **Procedure:** connect “requires” relationships; identify roots, cycles, optional paths, and critical path; order accordingly.
- **Output:** prerequisite or dependency graph.
- **Avoid:** forcing cyclic systems into a tree.
- **Validate:** no term depends on an unexplained downstream term.
- **Evidence:** C.

### Issue tree

- **Use when:** a broad strategic or diagnostic question must be decomposed.
- **Procedure:** write the governing question; split into answer-relevant subquestions; test coverage and overlap; stop at actionable leaves.
- **Output:** question hierarchy.
- **Avoid:** branches that are topics rather than answerable questions.
- **Validate:** every leaf can change the final answer.
- **Evidence:** D/C.

### MECE grouping

- **Use when:** categories overlap or leave gaps that impair analysis.
- **Procedure:** define classification rule; test each item for unique placement; test total coverage; document justified overlaps.
- **Output:** bounded classification.
- **Avoid:** forcing naturally overlapping phenomena into artificial boxes.
- **Validate:** edge cases can be classified consistently.
- **Evidence:** D; professional reasoning heuristic.

### Abstraction ladder

- **Use when:** an explanation is too abstract or trapped in examples.
- **Procedure:** move among principle, operational meaning, and concrete case; show correspondences at each level.
- **Output:** abstract↔operational↔concrete ladder.
- **Avoid:** unrelated examples that share vocabulary but not structure.
- **Validate:** learner moves from example to principle and back to a new example.
- **Evidence:** B/C; consistent with concrete-to-abstract learning research.

### Cause→mechanism→effect chain

- **Use when:** causal claims skip the process that produces the outcome.
- **Procedure:** name cause, intermediate state changes, enabling conditions, effect, and downstream consequence; label uncertainty.
- **Output:** causal chain.
- **Avoid:** filling unknown links with plausible stories.
- **Validate:** counterfactual or intervention prediction.
- **Evidence:** C as explanatory structure; evidence for the actual causal claim must come from domain sources.

### Rule→example→exception

- **Use when:** a rule is precise but hard to apply.
- **Procedure:** state rule; instantiate a typical case; show a boundary or exception; explain why classification changes.
- **Output:** usable rule card.
- **Avoid:** presenting an exceptional case before the default model unless risk requires it.
- **Validate:** classify a new boundary case.
- **Evidence:** B/C.

## Information architecture techniques

### Main message

- **Use when:** the audience cannot state the point or action.
- **Procedure:** formulate one audience-relevant proposition containing conclusion and practical meaning.
- **Output:** one-sentence essence.
- **Avoid:** a topic label such as “About security.”
- **Validate:** a reader repeats the intended conclusion after brief exposure.
- **Evidence:** C; supported by clear-communication guidance.

### BLUF — Bottom Line Up Front

- **Use when:** the audience needs the conclusion before evidence or chronology.
- **Procedure:** lead with decision/result; follow with reasons, evidence, caveats, and next action.
- **Output:** conclusion-first message.
- **Avoid:** when premature disclosure would make the explanation incoherent or when discovery is pedagogically essential.
- **Validate:** user can act after the first block and inspect evidence as needed.
- **Evidence:** C/D; strong professional convention, limited isolated causal evidence.

### Inverted pyramid

- **Use when:** readers may stop early or scan for the most important information.
- **Procedure:** order by consequence and relevance; progressively add context and detail.
- **Output:** scan-resilient article or update.
- **Avoid:** procedures where chronology controls correctness.
- **Validate:** early truncation preserves the core message.
- **Evidence:** C.

### Pyramid Principle

- **Use when:** a conclusion requires grouped supporting reasons.
- **Procedure:** state governing answer; group mutually coherent supports; place evidence under each; test vertical logic and horizontal consistency.
- **Output:** answer→reasons→evidence hierarchy.
- **Avoid:** forcing evidence into a predetermined conclusion.
- **Validate:** each child supports its parent; siblings answer the same question.
- **Evidence:** D/C as professional method.

### SCQA

- **Use when:** a recommendation needs concise narrative tension.
- **Procedure:** establish situation; identify complication; frame governing question; deliver answer.
- **Output:** problem-oriented opening.
- **Avoid:** adding theatrical complication or delaying an urgent conclusion.
- **Validate:** the question follows logically from the complication and the answer resolves it.
- **Evidence:** D.

### Chunking

- **Use when:** too many elements must be processed at once.
- **Procedure:** group items by meaningful schema; label each group; keep dependent elements together; sequence chunks.
- **Output:** conceptually segmented content.
- **Avoid:** arbitrary short fragments that increase integration burden.
- **Validate:** audience recalls group structure and locates items faster.
- **Evidence:** A/B for cognitive constraints; optimal chunk size is context-dependent.

### Signaling

- **Use when:** relationships, hierarchy, or transitions are not perceptually obvious.
- **Procedure:** use informative headings, verbal cues, numbering, emphasis, and diagram labels to point to essential structure.
- **Output:** guided attention path.
- **Avoid:** highlighting everything or adding decorative markers.
- **Validate:** faster identification of organization and key relations.
- **Evidence:** A/B in multimedia-learning research; implementation dependent.

### Progressive disclosure

- **Use when:** beginners need a safe default while advanced detail remains available.
- **Procedure:** expose essential actions/information first; reveal secondary options at the point of need; keep paths discoverable.
- **Output:** layered interface or document.
- **Avoid:** hiding safety-critical, high-frequency, or decision-essential information.
- **Validate:** beginners succeed without preventing expert access.
- **Evidence:** C; established HCI pattern, highly context-dependent.

### Layered explanation

- **Use when:** one audience contains multiple depth needs or consumption times.
- **Procedure:** create essence, overview, mechanism, application, and technical layers; enforce consistency across levels.
- **Output:** zoomable explanation.
- **Avoid:** different layers that contradict or introduce unstated scope changes.
- **Validate:** each layer stands alone for its declared outcome.
- **Evidence:** C; combines progressive disclosure and hierarchical organization.

### Whole–part–whole

- **Use when:** details feel disconnected from the system.
- **Procedure:** show purpose and whole; inspect parts; reconstruct interactions and outcome.
- **Output:** coherent system model.
- **Avoid:** a vague opening overview that provides no orienting structure.
- **Validate:** learner explains both parts and their contribution to the whole.
- **Evidence:** C/B, domain-dependent.

### Known→new

- **Use when:** the target concept has a reliable anchor in prior knowledge.
- **Procedure:** activate known model; identify structural similarity; state differences; introduce target terminology.
- **Output:** conceptual bridge.
- **Avoid:** familiar anchors that encode the wrong mechanism.
- **Validate:** learner identifies both mapping and difference.
- **Evidence:** B.

### Diátaxis

- **Use when:** documentation mixes learning, task execution, explanation, and reference.
- **Procedure:** classify content as tutorial, how-to, explanation, or reference; separate goals and navigation; cross-link.
- **Output:** four-mode documentation architecture.
- **Avoid:** treating the categories as mutually isolated user journeys.
- **Validate:** users can choose the correct content type for their need.
- **Evidence:** C/D; strong practitioner framework, limited direct comparative research.

## Language and terminology techniques

### Plain language

- **Use when:** wording, organization, or navigation prevents the intended audience from finding, understanding, and using information.
- **Procedure:** prioritize audience need; lead with main message; use familiar words and clear structure; test with users.
- **Output:** audience-usable communication.
- **Avoid:** reducing plain language to word substitution or a reading-grade score.
- **Validate:** find, understand, and use tasks with the target audience.
- **Evidence:** A/C: international standard and institutional guidance; effects vary by implementation.

### Controlled technical language

- **Use when:** consistency, translatability, safety, or repeated procedural accuracy matters.
- **Procedure:** define approved vocabulary, meanings, grammar, sentence patterns, and review rules; govern exceptions.
- **Output:** constrained authoring system.
- **Avoid:** applying rigid rules to persuasive, literary, or relationship-sensitive prose without adaptation.
- **Validate:** ambiguity, terminology, translation, and task-error audits.
- **Evidence:** A/C through formal standards and long operational use; outcome evidence varies.

### One concept–one term

- **Use when:** synonyms make entities or states appear different.
- **Procedure:** choose canonical label; map aliases; replace uncontrolled variants; document necessary user-facing synonyms.
- **Output:** terminology map.
- **Avoid:** erasing distinctions that are materially real.
- **Validate:** entity references remain stable across sections.
- **Evidence:** C.

### One term–one meaning

- **Use when:** one label carries multiple operational meanings.
- **Procedure:** identify senses; assign distinct labels or qualify scope; update definitions and examples.
- **Output:** disambiguated vocabulary.
- **Avoid:** redefining established terms silently.
- **Validate:** readers classify every occurrence consistently.
- **Evidence:** C.

### Actor–action–object

- **Use when:** responsibility or action is obscured.
- **Procedure:** name actor; use concrete verb; name object/recipient; add condition and result.
- **Output:** executable proposition.
- **Avoid:** inventing an actor when genuinely unknown; state “the actor is not specified.”
- **Validate:** reader identifies ownership without inference.
- **Evidence:** C, supported by controlled-language guidance.

### One action per procedural step

- **Use when:** users skip or partially execute compound instructions.
- **Procedure:** split independent actions; preserve dependency; attach result or verification to each meaningful step.
- **Output:** inspectable procedure.
- **Avoid:** fragmenting atomic actions into noise.
- **Validate:** observe completion and missed-step rate.
- **Evidence:** C.

### Condition before action

- **Use when:** users may act before noticing a restriction.
- **Procedure:** state condition/scope; state action; state expected result; separate alternate branch.
- **Output:** safe conditional instruction.
- **Avoid:** deeply nested natural-language conditions; use a table/tree instead.
- **Validate:** correct branch selection.
- **Evidence:** C, controlled-language practice.

### Point-of-use definition

- **Use when:** a necessary term is unfamiliar at first encounter.
- **Procedure:** give plain meaning immediately before or after the term; add consequence or example if material.
- **Output:** self-contained passage.
- **Avoid:** defining every common word or repeating long definitions.
- **Validate:** no glossary detour is required for first-pass comprehension.
- **Evidence:** C; aligned with accessibility and clear-communication guidance.

### Terminology bridge

- **Use when:** the audience must both understand the concept and learn the professional term.
- **Procedure:** plain meaning → canonical term → example → why it matters.
- **Output:** four-part term card.
- **Avoid:** replacing the canonical term forever when future work requires it.
- **Validate:** learner recognizes and correctly uses the term in a new context.
- **Evidence:** C/B.

### Explicit logical connectors

- **Use when:** relation among sentences is implicit or ambiguous.
- **Procedure:** name cause, consequence, condition, contrast, example, exception, or sequence explicitly.
- **Output:** visible reasoning structure.
- **Avoid:** connector inflation where no real relation exists.
- **Validate:** readers reconstruct the same argument graph.
- **Evidence:** B/C.

### Numerical framing

- **Use when:** percentages, rates, probabilities, or scale are difficult to interpret.
- **Procedure:** add baseline, denominator, timeframe, unit, comparison, and uncertainty; use consistent natural frequencies when appropriate.
- **Output:** decision-ready quantity statement.
- **Avoid:** emotionally loaded comparisons or denominator switching.
- **Validate:** accurate absolute and relative interpretation.
- **Evidence:** A/B in risk and health communication, with context-sensitive effects.

## Concretization techniques

### Concrete example

- **Use when:** a correct rule remains inert or abstract.
- **Procedure:** choose representative inputs; show complete application; explain which details instantiate which rule.
- **Output:** rule-linked case.
- **Avoid:** entertaining but atypical examples.
- **Validate:** learner extracts the governing rule.
- **Evidence:** B.

### Non-example

- **Use when:** category boundaries are easily confused.
- **Procedure:** choose a near-miss; identify the missing or violating property; contrast with a valid example.
- **Output:** boundary clarification.
- **Avoid:** obviously unrelated negative cases.
- **Validate:** classify a second near-miss.
- **Evidence:** B/C.

### Counterexample

- **Use when:** a universal claim or decision rule must be tested.
- **Procedure:** identify the claim; present a valid case that violates it; revise the claim or expose the exception.
- **Output:** bounded rule.
- **Avoid:** calling an out-of-scope case a counterexample.
- **Validate:** revised rule handles both original and counterexample.
- **Evidence:** logical method; empirical applicability is domain-specific.

### Analogy with explicit limits

- **Use when:** a structurally similar familiar domain can bootstrap a new model.
- **Procedure:** define source and target; map elements and relations; state supported prediction; state breakdown points.
- **Output:** bounded analogy map.
- **Avoid:** surface similarity, culturally unfamiliar sources, or sole use in high-risk content.
- **Validate:** learner distinguishes mapped from unmapped properties.
- **Evidence:** Mixed/B; effectiveness depends on mapping quality and prior knowledge.

### Worked example

- **Use when:** novices must learn a multi-step solution or decision process.
- **Procedure:** show goal, each step, rationale, intermediate state, and result; gradually fade support across later examples.
- **Output:** complete solved case.
- **Avoid:** unexplained step sequences or excessive examples after expertise develops.
- **Validate:** solve a partially completed and then independent case.
- **Evidence:** A/B; strong novice benefit in many structured domains, moderated by design.

### Comparison matrix

- **Use when:** similar options must be discriminated on shared criteria.
- **Procedure:** define decision question; use common dimensions; normalize scale; expose trade-offs and missing evidence.
- **Output:** side-by-side matrix plus recommendation rule.
- **Avoid:** feature dumps, unequal criteria, or false equivalence.
- **Validate:** choose under a new priority profile.
- **Evidence:** C.

### Scenario

- **Use when:** context and consequences affect application.
- **Procedure:** set actor, goal, constraints, trigger, decision, action, and outcome; tie each to the rule.
- **Output:** situated case.
- **Avoid:** narrative details that do not affect reasoning.
- **Validate:** transfer to another scenario with changed surface features.
- **Evidence:** B/C.

### Contrafactual

- **Use when:** a component’s causal role or necessity is unclear.
- **Procedure:** change or remove one condition; hold others stable; predict and justify the outcome.
- **Output:** causal contrast.
- **Avoid:** impossible or underdetermined worlds presented as evidence.
- **Validate:** accurate intervention prediction.
- **Evidence:** B as reasoning support; factual validity depends on domain evidence.

### Error commentary

- **Use when:** recurring authentic mistakes reveal hidden distinctions.
- **Procedure:** show error; identify why it is tempting; locate violated rule; correct; add prevention cue.
- **Output:** error→cause→correction card.
- **Avoid:** exposing novices to errors without immediate correction or clear contrast.
- **Validate:** detect the same error in a new case.
- **Evidence:** Mixed/B; timing and learner expertise matter.

## Flow and decision techniques

### Happy path first

- **Use when:** exceptions obscure the default system model.
- **Procedure:** show trigger, normal sequence, completion; add alternate and failure paths in later layers.
- **Output:** primary flow plus overlays.
- **Avoid:** when the exception is common, safety-critical, or the user’s actual task.
- **Validate:** audience narrates default flow before troubleshooting.
- **Evidence:** C, aligned with progressive complexity management.

### Trigger→input→action→decision→output

- **Use when:** a process description lacks operational anatomy.
- **Procedure:** identify start event, prerequisites, data, actions, branches, completion evidence, and owner.
- **Output:** normalized flow model.
- **Avoid:** omitting states, concurrency, or recovery when material.
- **Validate:** trace a concrete case from trigger to output.
- **Evidence:** C.

### Swimlane

- **Use when:** handoffs and responsibility are the main question.
- **Procedure:** create one lane per accountable actor/system; place actions in order; label handoffs; expose waits and loops.
- **Output:** responsibility flow.
- **Avoid:** lanes for every minor participant or use as infrastructure architecture.
- **Validate:** identify owner and next handoff for any step.
- **Evidence:** C; notation value is task-dependent.

### BPMN

- **Use when:** business processes require formal events, tasks, gateways, messages, and exception semantics.
- **Procedure:** choose a bounded BPMN subset; model pools/lanes, events, tasks, gateways, message flows, and end states; validate syntax and semantics.
- **Output:** formal process model.
- **Avoid:** full notation for audiences that need only a simple operational view.
- **Validate:** token-flow walkthrough and domain-owner review.
- **Evidence:** A as an official standard; comprehension depends on notation literacy and diagram complexity.

### State model

- **Use when:** allowable changes over time matter more than action chronology.
- **Procedure:** define states, events, transitions, guards, actions, invalid transitions, and terminal states.
- **Output:** state-transition diagram/table.
- **Avoid:** using activities as states or omitting transition triggers.
- **Validate:** predict next valid state from a new event.
- **Evidence:** A/C through formal modeling practice.

### Decision tree

- **Use when:** sequential conditional questions lead to outcomes.
- **Procedure:** order discriminating questions; ensure branches are clear; attach outcome/action; prune redundant paths.
- **Output:** navigable decision path.
- **Avoid:** many interacting conditions better expressed as a table.
- **Validate:** route representative and boundary cases.
- **Evidence:** C.

### Decision table

- **Use when:** combinations of conditions determine actions.
- **Procedure:** enumerate conditions and actions; create rules; test completeness, overlap, impossibility, and conflict.
- **Output:** auditable rule matrix.
- **Avoid:** narrative prose for combinatorial logic.
- **Validate:** every valid condition combination maps to one intended action set.
- **Evidence:** A/C in requirements and testing practice.

### Sequence diagram

- **Use when:** message order among participants is the main question.
- **Procedure:** identify lifelines; place calls/messages over time; distinguish sync/async; add alternatives, loops, and failures selectively.
- **Output:** interaction timeline.
- **Avoid:** static structural relationships or user journey emotions.
- **Validate:** trace request, response, timeout, and retry behavior.
- **Evidence:** A/C through UML specification and engineering practice.

### Data-flow diagram

- **Use when:** movement and transformation of information matters.
- **Procedure:** identify external entities, processes, data stores, and labeled data flows; decompose levels consistently.
- **Output:** data movement model.
- **Avoid:** control-flow semantics or unlabeled arrows.
- **Validate:** every produced datum has a source, transformation, and destination.
- **Evidence:** C.

### SIPOC

- **Use when:** a process needs a macro boundary before detailed modeling.
- **Procedure:** identify suppliers, inputs, 4–7 macro process steps, outputs, and customers; define scope.
- **Output:** high-level process frame.
- **Avoid:** implementation detail or branch logic.
- **Validate:** stakeholders agree on start, end, input, output, and customer.
- **Evidence:** C/D; established quality-management tool.

### C4 Model

- **Use when:** software architecture needs audience-specific levels of zoom.
- **Procedure:** start with system context; add containers; add components only where useful; keep notation and relationships consistent.
- **Output:** context/container/component views.
- **Avoid:** one giant diagram or confusing runtime sequence with static structure.
- **Validate:** each view answers one architecture question and traces consistently to adjacent levels.
- **Evidence:** C/D; established practitioner model, not a causal learning claim.

### Event Storming

- **Use when:** a group must discover domain behavior, events, commands, actors, policies, aggregates, and hotspots.
- **Procedure:** elicit domain events in time order; add triggers and rules; mark uncertainty; cluster bounded contexts; refine collaboratively.
- **Output:** shared domain model and unresolved hotspots.
- **Avoid:** presenting a workshop artifact as a validated specification without refinement.
- **Validate:** domain experts recognize behavior and can resolve representative scenarios.
- **Evidence:** D/C; facilitation practice with limited controlled evidence.

## Teaching and validation techniques

### Segmenting

- **Use when:** a continuous explanation overloads processing.
- **Procedure:** divide into coherent, learner-controllable units; preserve dependencies; add transition cues.
- **Output:** paced sequence.
- **Avoid:** segmentation that breaks tightly integrated relations.
- **Validate:** lower error/effort without content loss.
- **Evidence:** A/B in multimedia-learning research.

### Scaffolding and fading

- **Use when:** learners cannot yet perform independently.
- **Procedure:** supply prompts, templates, partial solutions, or checklists; monitor success; withdraw support progressively.
- **Output:** graduated practice path.
- **Avoid:** permanent support that masks non-mastery or fading too early.
- **Validate:** independent performance after support removal.
- **Evidence:** B/Mixed.

### I do→we do→you do

- **Use when:** a demonstrable procedure or reasoning routine is being taught.
- **Procedure:** model; practice jointly; require independent application; give corrective feedback.
- **Output:** demonstration-to-independence sequence.
- **Avoid:** passive imitation without explanation or transfer.
- **Validate:** independent new case.
- **Evidence:** B/C.

### Concrete→representational→abstract

- **Use when:** abstract symbols lack meaning.
- **Procedure:** begin with concrete instance; externalize relations in a representation; introduce formal abstraction; connect all three.
- **Output:** three-level model.
- **Avoid:** concrete examples with irrelevant surface features that dominate attention.
- **Validate:** move bidirectionally across levels.
- **Evidence:** B/Mixed by domain.

### Retrieval practice

- **Use when:** durable recall is needed.
- **Procedure:** prompt active recall without the answer; provide feedback; repeat with spacing and varied cues.
- **Output:** retrieval schedule/questions.
- **Avoid:** recognition-only quizzes or high-stakes grading without learning feedback.
- **Validate:** delayed unaided recall.
- **Evidence:** A.

### Spacing

- **Use when:** retention beyond the immediate session matters.
- **Procedure:** distribute retrieval or practice over time; increase interval as performance stabilizes.
- **Output:** review schedule.
- **Avoid:** treating one optimal interval as universal.
- **Validate:** delayed retention versus massed practice.
- **Evidence:** A; optimal spacing depends on retention interval and material.

### Interleaving

- **Use when:** learners must discriminate which strategy applies across problem types.
- **Procedure:** mix related categories after minimal initial grounding; require strategy selection; provide feedback.
- **Output:** mixed practice set.
- **Avoid:** premature mixing before basic patterns are recognizable.
- **Validate:** category discrimination and transfer.
- **Evidence:** B/Mixed by domain.

### Teach-back

- **Use when:** verbal understanding must be demonstrated, especially in consequential communication.
- **Procedure:** normalize the check as a test of the explanation; ask for reconstruction in own words; diagnose gaps; re-explain and recheck.
- **Output:** demonstrated mental model.
- **Avoid:** “Did you understand?” or shaming memory tests.
- **Validate:** accurate reconstruction and application.
- **Evidence:** A/B in health communication; generalization beyond studied contexts should be bounded.

### Show-me

- **Use when:** procedural competence matters.
- **Procedure:** ask the person to perform or simulate the task; observe actions and branch choices; correct; repeat.
- **Output:** observable performance evidence.
- **Avoid:** accepting verbal description as equivalent to execution.
- **Validate:** completion under representative conditions.
- **Evidence:** C/B; direct performance assessment has strong face validity.

### Prediction test

- **Use when:** a system or causal model should support anticipation.
- **Procedure:** present a new initial state/event; ask for next state and reason; compare with model.
- **Output:** prediction plus justification.
- **Avoid:** cases requiring unstated facts.
- **Validate:** correct state and mechanism.
- **Evidence:** B/C as assessment of mental models.

### Transfer test

- **Use when:** genuine understanding must generalize beyond surface similarity.
- **Procedure:** preserve deep structure; alter context and surface features; require application and rationale.
- **Output:** generalization evidence.
- **Avoid:** calling a near-copy a transfer task.
- **Validate:** correct rule use in the new context.
- **Evidence:** A/B as a learning outcome; transfer is often difficult and domain-sensitive.

## Technique conflict rules

| Conflict | Resolution |
|---|---|
| BLUF vs pedagogical discovery | Prefer BLUF for action/decision; discovery only when it serves the learning objective |
| Plain language vs canonical terminology | Explain plainly, then retain the canonical term |
| Progressive disclosure vs safety | Keep safety-critical information visible in the first actionable layer |
| Happy path vs exception-first | Lead with the exception when it is frequent, central, or harmful |
| Analogy vs precision | Exact model governs; analogy supports and declares limits |
| One-action steps vs excessive fragmentation | Split at independent decisions or verification points, not every physical motion |
| MECE vs real overlap | Preserve meaningful overlap and state the classification rule |
| Concision vs completeness | Remove repetition and background before evidence, caveats, and next action |
| Diagram simplicity vs semantic completeness | Use multiple linked views rather than corrupting notation or omitting critical paths |

## Default combinations

```text
Technical concept:
prerequisite map → plain meaning → canonical term → mechanism → example/non-example → prediction

Operational process:
SIPOC or whole view → happy path → swimlane → decision/state model → failure/recovery → show-me

Strategic reasoning:
governing question → issue tree → criteria/causal chain → Pyramid/BLUF → scenario → transfer

High-risk explanation:
source verification → invariant lock → exact plain language → layered detail → explicit uncertainty → teach-back/show-me
```
