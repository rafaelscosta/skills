# Diagram Contract

Use this reference only when the visual router selects `structural-diagram/*` or a mixed artifact containing a structural diagram.

A Concept Bridge diagram is an explanatory instrument, not decoration and not an architecture poster.

The governing requirement is:

> **The diagram must make one important relationship easier to understand than prose alone.**

## 1. One-question rule

Every diagram answers one primary question.

Examples:

- `flow`: What path can this request take?
- `state`: What states exist and what events move between them?
- `architecture`: What components exist and who talks to whom?
- `hierarchy`: What contains or belongs to what?
- `causal`: What mechanism creates this outcome?
- `structural-comparison`: Where do these systems differ structurally?

If a diagram simultaneously tries to explain architecture, runtime sequence, ownership, errors, deployment, and metrics, split it.

## 2. Minimal semantic model

Before drawing, identify only:

1. required nodes;
2. required relationships;
3. required direction;
4. required labels;
5. one material boundary or exception if needed for truth.

A node or edge survives only when removing it would make the reader's mental model materially worse.

Do not draw implementation detail merely because it exists.

## 3. Direct-label rule

Prefer direct labels on nodes and relationships.

Good:

```text
Browser → API → Database
```

Avoid numbered or color-coded legends when the same information can be written directly.

A legend is cognitive tax. Use one only when repeated visual encoding genuinely reduces more complexity than it introduces.

## 4. Explicit reading direction

The starting point and reading direction must be obvious within about two seconds.

Prefer one dominant direction:

- left → right; or
- top → bottom.

Do not combine several directional systems unless the topology genuinely requires it.

For cycles, clearly mark the cycle entry and repeated transition.

## 5. Node budget

Use the minimum node set required for the selected depth.

Default target for a first mental model: **3–7 primary nodes**.

More nodes are allowed only when the relationship cannot remain truthful without them.

When node count grows, first consider:

- grouping implementation details into one conceptual component;
- progressive disclosure;
- splitting the diagram;
- moving advanced detail to prose.

## 6. Edge budget

Use the minimum relationship set required to answer the diagram's primary question.

Do not connect components merely because they can communicate.

Each edge should carry semantic meaning such as:

- sends request;
- contains;
- transitions on event;
- causes;
- reads/writes;
- delegates;
- depends on.

When ambiguity is possible, label the edge with a short verb or event.

## 7. Crossing-edge rule

Target **zero crossing edges**.

If crossings appear:

1. reorder nodes;
2. change orientation;
3. group components;
4. split independent concerns;
5. only then tolerate a crossing if the real topology requires it.

Several crossings are a strong signal that the diagram is trying to explain too much at once.

## 8. Semantic consistency

Visual grammar must remain stable inside one artifact.

Examples:

- component shape = component throughout;
- state shape = state throughout;
- solid arrow = the same relationship class throughout;
- accent color = active/current/emphasized concept throughout.

Do not change shape or arrow meaning for decoration.

Do not encode meaning by color alone when text or shape can make it explicit.

## 9. Canonical terminology

Visual labels must use the same canonical vocabulary as the verbal explanation.

If the prose says `queue`, do not rename the same object `message buffer` in the visual unless the equivalence is explicitly taught.

Keep vendor/product names exact when they matter.

All visible text uses the language of the explanation; canonical technical names may remain in their conventional language.

For Brazilian Portuguese responses, all explanatory labels, titles, captions, and annotations must be PT-BR.

## 10. Diagram-type contracts

### Flow

Use when branching or decision logic matters.

Required:

- obvious entry;
- explicit decision labels;
- branches labeled by conditions/outcomes;
- terminal paths clear.

Avoid:

- flowcharts for purely linear stories;
- unlabeled yes/no ambiguity;
- multiple independent workflows in one chart.

### State

Use when allowed states and transitions are the concept.

Required:

- states are nouns/statuses;
- transitions are events/actions/conditions;
- invalid transitions are not accidentally implied;
- initial state is clear when relevant.

Avoid using arrows merely to show chronological prose.

### Architecture

Use when system parts and connections matter.

Required:

- conceptual boundaries are clear;
- connections reflect relevant communication/dependency;
- sequence is not falsely implied when the diagram is structural.

If runtime order matters too, pair the architecture diagram with a short narrative or flow rather than overloading the architecture view.

### Hierarchy

Use when containment, ownership, or levels matter.

Required:

- parent/child direction is obvious;
- siblings use comparable abstraction levels;
- hierarchy does not imply execution order.

### Causal

Use when one condition produces an outcome through a mechanism.

Required:

- causal direction is explicit;
- mechanism is named rather than skipped;
- correlation is not drawn as causation;
- branches only show material downstream effects.

### Structural comparison

Use two or more aligned views sharing the same dimensions.

Required:

- equivalent layers align;
- labels use parallel wording;
- missing layers remain visibly absent rather than being silently shifted;
- differences that matter are emphasized without hiding common structure.

## 11. HTML/SVG artifact policy

A rendered HTML artifact may contain one or more embedded diagrams.

Preferred implementation order:

1. **inline SVG** for deterministic diagrams;
2. deterministic HTML/CSS for simple stacks or comparisons;
3. rendered Mermaid only when it materially simplifies implementation and the final result is actually rendered.

Prefer inline SVG because it supports:

- deterministic layout;
- crisp scaling;
- precise typography;
- reusable symbols;
- responsive composition;
- direct labels;
- no external runtime dependency.

The final deliverable is the rendered artifact, not the source.

Never expose raw Mermaid, Graphviz, SVG, HTML, or other diagram code unless the user explicitly asks for source.

## 12. Mixed HTML composition

A single HTML artifact may contain:

```text
HTML artifact
├── explanatory text
├── narrative scenes
└── structural diagrams
```

Use mixed composition only when the parts answer different cognitive questions.

Example for OAuth:

- narrative scene: user clicks "Entrar com Google";
- architecture/flow: browser/client ↔ authorization server ↔ resource server;
- narrative scene: user grants access;
- compact flow: authorization code → token exchange;
- closing truth: delegated access, not password sharing.

Do not duplicate the same fact across all layers.

## 13. Accessibility and textual equivalence

The user must not need the diagram to recover a critical fact that has no textual equivalent.

For HTML/SVG artifacts:

- use meaningful headings;
- preserve logical DOM reading order;
- add concise accessible text/ARIA labeling where the rendering environment supports it;
- avoid meaning encoded only through color;
- keep labels readable on narrow/mobile surfaces.

The diagram augments the verbal bridge; it does not replace truth-critical prose.

## 14. Visual quality gate

Before rendering, silently verify:

### Necessity

Does the diagram reduce cognitive load rather than decorate?

### Representation fit

Would story, diagram, or mixed composition better answer the user's actual question?

### Topology

Are all material relationships represented correctly, without invented edges or missing boundaries?

### Scanability

Can the reader identify the starting point, actors, and reading direction in about two seconds?

### Semantic consistency

Do terms, shapes, arrows, and accents keep stable meanings?

### Prose independence

Does the verbal explanation still contain the truth-critical model if the visual fails to render?

Fix any failure before delivery.

## 15. Automatic failures

Treat these as representation failures:

- a static concept receives a decorative diagram without explicit user request;
- a simple narrative process becomes a dense flowchart;
- meaningful topology is hidden inside disconnected comic scenes;
- a state problem is rendered without showing allowed transitions;
- a causal diagram invents or implies unsupported causal links;
- several crossing edges remain when re-layout or decomposition could remove them;
- a legend replaces straightforward direct labeling;
- visual terminology diverges from prose;
- multiple cognitive questions are collapsed into one dense diagram;
- the visual lacks an obvious reading direction;
- raw diagram source is delivered as the finished visual;
- the diagram is harder to parse than the prose it is supposed to help.
