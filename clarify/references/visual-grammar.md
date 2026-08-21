# Visual Grammar and Diagram Selection

Use this reference to select and specify a visual representation. Choose by relationship and question, not by style.

## Selection map

| Primary question | Recommended representation |
|---|---|
| What happens in order? | Flowchart |
| Who performs each action? | Swimlane |
| What formal events, gateways, and messages govern the business process? | BPMN |
| What are the macro boundaries, suppliers, inputs, outputs, and customers? | SIPOC |
| Which state changes are allowed? | State diagram/table |
| Which sequential questions lead to an outcome? | Decision tree |
| Which combinations of conditions select actions? | Decision table |
| Which participant sends which message over time? | Sequence diagram |
| How does data move and transform? | Data-flow diagram |
| What depends on what? | Directed graph or DAG |
| How are concepts propositionally related? | Concept map |
| Which evidence supports or attacks which claim? | Argument map |
| Which variables cause feedback over time? | Causal-loop diagram |
| What does a user experience across stages? | Journey map |
| How do visible and backstage services interact? | Service blueprint |
| What is the software architecture at different zoom levels? | C4 Model |
| Which domain events and rules define behavior? | Event Storming |
| What changed over time? | Timeline |
| How does an experience unfold frame by frame? | Storyboard |
| What pattern, comparison, distribution, or uncertainty exists in data? | Statistical chart |

## Universal diagram contract

Every diagram specification should include:

```yaml
diagram:
  question_answered: ""
  audience: ""
  notation: ""
  scope: ""
  reading_direction: "left-to-right | top-to-bottom"
  entities: []
  relationships: []
  legend: []
  visual_hierarchy: []
  accessibility_text: ""
  excluded_questions: []
```

## Universal rules

1. One diagram answers one primary question.
2. Title the conclusion or question, not only the topic.
3. Make start, end, scope, and direction explicit.
4. Label arrows with verbs or relationship semantics.
5. Use shape for type and color only as a redundant cue.
6. Keep labels close to the element they explain.
7. Use consistent symbols and terminology across views.
8. Avoid line crossings; group or split when crossings dominate.
9. Use progressive zoom instead of microscopic detail on a macro view.
10. Provide a text-equivalent explanation.
11. State what the diagram intentionally omits.
12. Validate semantics before visual polish.

## Complexity limits

No universal node limit exists. Split a view when one or more symptoms appear:

- labels require shrinking below normal reading size;
- the reader must trace more than one unrelated relationship type;
- crossing lines obscure direction;
- exceptions outnumber the main path;
- more than one legend is needed to understand basic meaning;
- the same node means different things in different regions;
- the diagram cannot be summarized in one sentence;
- accessibility text becomes a second full specification rather than an equivalent description.

## Flowchart

**Answers:** What happens and in what order?

**Represents well:** actions, simple decisions, loops, start/end.

**Represents poorly:** complex concurrency, formal message semantics, architecture, rich state behavior.

**Core grammar:**

- rounded terminal: start/end;
- rectangle: action/process;
- diamond: decision question;
- arrow: control flow, labeled on decision branches;
- document/data/storage symbols only when needed and defined.

**Frequent errors:**

- diamond contains an action rather than a question;
- yes/no branches are unlabeled;
- multiple starts or ends are unexplained;
- backward arrows have no loop condition;
- actors are inferred from color only.

**Automation suitability:** high for structured linear flows; validate branch completeness and direction.

## Swimlane

**Answers:** Who owns each action and handoff?

**Represents well:** responsibility, sequence, waits, cross-team/system handoffs.

**Represents poorly:** static architecture, detailed data models, complex state transitions.

**Core grammar:**

- one lane per accountable role, team, or system;
- action placed inside owner’s lane;
- arrow crossing a lane boundary represents a handoff or interaction;
- decisions belong to the actor that evaluates them.

**Frequent errors:**

- lanes represent phases rather than owners without saying so;
- shared ownership hides accountability;
- too many lanes for minor actors;
- message and responsibility semantics are mixed.

**Automation suitability:** medium-high after actor normalization.

## BPMN

**Answers:** How does a formal business process respond to events, tasks, decisions, messages, and exceptions?

**Represents well:** start/intermediate/end events, activities, gateways, pools/lanes, message flow, boundary events, subprocesses.

**Represents poorly:** informal audiences without notation support, static architecture, conceptual relationships.

**Core grammar:** use the smallest necessary official subset. Distinguish:

- sequence flow inside a process;
- message flow between pools;
- exclusive, parallel, and inclusive gateways;
- catching versus throwing events;
- normal versus interrupting boundary events.

**Frequent errors:**

- sequence flow crosses pools;
- gateways are used as decorative branch points;
- event types are semantically wrong;
- pools, lanes, and systems are conflated;
- diagram is syntactically valid but operationally incomplete.

**Automation suitability:** medium; syntax can be generated, but domain and exception semantics require review.

## SIPOC

**Answers:** What is the high-level boundary of the process?

**Represents well:** suppliers, inputs, 4–7 macro steps, outputs, customers.

**Represents poorly:** decisions, exceptions, detailed responsibilities, technical implementation.

**Core grammar:**

```text
Supplier → Input → Process → Output → Customer
```

**Frequent errors:**

- “customer” is confused with only an external buyer;
- outputs are activities rather than deliverables;
- process column contains dozens of steps;
- scope start/end is absent.

**Automation suitability:** high when source boundaries are explicit.

## State diagram or state table

**Answers:** What stable condition is the entity in, and which events can change it?

**Represents well:** lifecycle, valid/invalid transitions, guards, terminal states.

**Represents poorly:** actor responsibility and message chronology.

**Core grammar:**

```text
State --event [guard] / action--> State
```

**Frequent errors:**

- activities are modeled as states;
- transition labels omit triggers;
- error states have no exit;
- impossible transitions are implied by visual proximity.

**Automation suitability:** high if states and transition rules are structured.

## Decision tree

**Answers:** Which sequential condition leads to which outcome?

**Represents well:** hierarchical discrimination, triage, simple policy routing.

**Represents poorly:** combinatorial conditions, weighted trade-offs, feedback loops.

**Core grammar:**

- internal node: explicit question or test;
- branch: mutually interpretable answer;
- leaf: action/outcome;
- branch order reflects diagnostic efficiency or dependency.

**Frequent errors:**

- branches overlap;
- a condition appears after an action it governs;
- “other” hides important outcomes;
- deep trees become unscannable.

**Automation suitability:** high after rule validation.

## Decision table

**Answers:** Which action applies to each combination of conditions?

**Represents well:** completeness, overlap, conflict, test-case derivation.

**Represents poorly:** time, ownership, long narrative explanation.

**Core grammar:** rows or columns must consistently separate conditions, rules, and actions.

**Validation checks:**

- every valid combination covered;
- impossible combinations marked;
- overlapping rules resolved;
- default behavior explicit;
- actions consistent.

**Automation suitability:** very high for structured rules.

## Sequence diagram

**Answers:** Which participant sends which message, in what order, and with which alternatives?

**Represents well:** request/response, synchronous/asynchronous calls, loops, alternatives, timeouts.

**Represents poorly:** static dependencies, business ownership, data transformations.

**Core grammar:**

- lifelines represent participants;
- vertical direction represents time;
- arrows represent messages/calls;
- combined fragments represent `alt`, `opt`, `loop`, `par`;
- activation bars are optional when they add meaning.

**Frequent errors:**

- return arrows imply behavior that is not guaranteed;
- sequence is confused with causation;
- asynchronous behavior is drawn synchronously;
- failure and timeout behavior is omitted.

**Automation suitability:** medium-high; runtime truth must be verified.

## Data-flow diagram

**Answers:** Where does information originate, how is it transformed, where is it stored, and where does it go?

**Represents well:** entities, processes, stores, labeled data flows, decomposition levels.

**Represents poorly:** control sequence, timing, UI navigation.

**Core grammar:**

- external entity;
- process that transforms data;
- data store;
- arrow labeled with data, not action.

**Frequent errors:**

- unlabeled arrows;
- direct external-entity-to-store flows without a process;
- control messages treated as data without distinction;
- inconsistent decomposition between levels.

**Automation suitability:** medium-high.

## Dependency graph or DAG

**Answers:** What requires, blocks, enables, or precedes what?

**Represents well:** prerequisites, build dependencies, critical path, lineage.

**Represents poorly:** responsibility, state, rich decision logic.

**Core grammar:** define arrow meaning explicitly:

```text
A → B means “B depends on A”
```

Do not assume readers infer direction.

**Frequent errors:** mixed arrow semantics, hidden cycles, transitive edges cluttering the view.

**Automation suitability:** high; cycle and topology checks are deterministic.

## Concept map

**Answers:** Which concepts form meaningful propositions together?

**Represents well:** hierarchical and cross-domain conceptual relations.

**Represents poorly:** exact procedure and time.

**Core grammar:**

```text
Concept --linking phrase--> Concept
```

A valid edge should read as a proposition.

**Frequent errors:** unlabeled lines, mind-map branches mistaken for propositions, decorative association without semantic relation.

**Automation suitability:** medium; relation labels require semantic review.

## Argument map

**Answers:** Which premises support, challenge, or rebut which claims?

**Represents well:** evidence structure, objections, assumptions, inference gaps.

**Represents poorly:** chronological process and architecture.

**Core grammar:** distinguish claim, evidence/premise, objection, rebuttal, and inference.

**Frequent errors:** evidence source omitted, correlation treated as support for causation, multiple claims inside one node.

**Automation suitability:** medium; claim decomposition and evidential status require review.

## Causal-loop diagram

**Answers:** How do variables influence one another through reinforcing or balancing feedback over time?

**Represents well:** feedback, delays, systemic dynamics.

**Represents poorly:** exact sequence, actor responsibility, unverified causal claims.

**Core grammar:**

- variables, not events, as nodes;
- signed links indicate same/opposite direction of change;
- loops labeled reinforcing or balancing;
- delays marked explicitly.

**Frequent errors:** causal claims inferred from sequence; polarity inconsistent; missing delay creates false immediacy.

**Automation suitability:** low-medium unless causal model is supplied.

## Journey map

**Answers:** What does a person do, think, feel, and encounter across stages?

**Represents well:** stages, goals, touchpoints, pain points, evidence, opportunities.

**Represents poorly:** backstage dependencies and formal process rules.

**Core grammar:** distinguish observed evidence from assumed emotion.

**Frequent errors:** fictional feelings presented as research, stages based on internal departments, opportunities mixed with observed facts.

**Automation suitability:** medium for synthesis; low for inventing user evidence.

## Service blueprint

**Answers:** How does the customer-visible experience connect to frontstage, backstage, support processes, and evidence?

**Represents well:** lines of interaction/visibility, handoffs, dependencies, failure points.

**Represents poorly:** detailed technical architecture or rules.

**Frequent errors:** no line of visibility, backstage work mixed with user actions, unsupported internal assumptions.

**Automation suitability:** medium after evidence collection.

## C4 Model

**Answers by level:**

1. **System context:** Who uses the system and what external systems interact with it?
2. **Container:** What applications/data stores make up the system and how do they communicate?
3. **Component:** What major components exist inside a selected container?
4. **Code:** What implementation detail is needed for a narrow technical audience?

**Core grammar:** people, software systems, containers/components, and labeled relationships. Technology and responsibility labels should be visible where relevant.

**Frequent errors:** “container” confused with Docker only, mixed zoom levels, unlabeled arrows, dynamic request flow placed into a static view.

**Automation suitability:** medium-high when architecture inventory is trustworthy.

## Event Storming

**Answers:** What domain events occur, what triggers them, which rules react, and where are uncertainties or boundaries?

**Represents well:** collaborative discovery, chronology of domain events, policies, commands, actors, aggregates, hotspots.

**Represents poorly:** finished visual documentation without cleanup, infrastructure topology.

**Core grammar:** follow the local workshop legend consistently. Common elements include domain events, commands, actors, policies, aggregates, external systems, and hotspots.

**Frequent errors:** implementation events dominate domain language, unvalidated assumptions look final, chronology is confused with causality.

**Automation suitability:** low for discovery, medium for normalizing an existing workshop artifact.

## Timeline

**Answers:** What happened or will happen over time?

**Represents well:** dates, durations, overlap, milestones, eras.

**Represents poorly:** causality without explicit links, decision rules.

**Frequent errors:** uneven scale without disclosure, events and durations rendered identically, visual proximity implies causality.

**Automation suitability:** high with structured dates.

## Storyboard

**Answers:** How does a person or system experience unfold frame by frame?

**Represents well:** interaction context, screen/state change, narrative sequence, moments of confusion.

**Represents poorly:** exhaustive rule systems and data architecture.

**Frequent errors:** decorative scenes without state change, missing user goal, captions describe visuals rather than actions/consequences.

**Automation suitability:** medium; scenario fidelity requires review.

## Statistical chart selector

| Analytical question | Preferred chart | Avoid |
|---|---|---|
| Compare categories | Bar/dot plot | Pie with many categories |
| Show change over time | Line chart | Unordered bars for dense time series |
| Show distribution | Histogram, box plot, violin, ECDF | Mean-only bar |
| Show relationship | Scatter plot | Dual-axis chart without strong justification |
| Show composition | Stacked bar/area when totals matter | Many-slice pie |
| Show ranking | Ordered bar/dot plot | Alphabetical order |
| Show deviation from baseline | Diverging bar | Arbitrary zero suppression |
| Show uncertainty | Error bars, interval plot, fan chart | Point estimate alone |
| Show part-to-whole with few parts | Stacked bar or carefully limited pie | 3D pie |
| Show flow magnitude | Sankey when magnitude and path both matter | Sankey for precise comparisons |

Always preserve scale, unit, denominator, time, source, and uncertainty. Do not truncate axes in ways that materially distort magnitude.

## Progressive zoom patterns

### Process

```text
SIPOC → happy-path flowchart → swimlane → decision/state/failure views
```

### Software architecture

```text
C4 context → container → selected component → sequence diagram for runtime behavior
```

### Strategy

```text
governing question → issue tree → causal/criteria view → evidence details
```

### Data

```text
headline finding → overview chart → subgroup view → methodology/uncertainty
```

## Accessible text-equivalent template

```markdown
### O que o diagrama responde

### Como ler

### Elementos

### Relações principais

### Caminho ou conclusão

### Exceções e limites

### O que o diagrama não mostra
```

## Visual semantic audit

```text
[ ] The diagram has one primary question.
[ ] Symbols have defined semantics.
[ ] Arrow meaning is explicit and consistent.
[ ] Reading direction is obvious.
[ ] Color is redundant, not exclusive.
[ ] Labels are close to their referents.
[ ] Different relationship types are not silently mixed.
[ ] Macro and micro levels are separated.
[ ] Exceptions do not obscure the default view.
[ ] A text equivalent preserves the same meaning.
[ ] The diagram omits no safety- or decision-critical relation.
[ ] The notation is appropriate for the audience’s literacy.
```
