# Visual Representation Router

Use this reference only after the verbal explanation is conceptually correct and the main `SKILL.md` visual gate says a visual could materially reduce cognitive load.

The router separates two decisions that must not be collapsed:

1. **Does a visual help?**
2. **If it helps, is the concept best understood narratively, structurally, or with both?**

The objective is not to maximize visual richness. It is to choose the lowest-complexity representation that makes the mental model easier to predict, inspect, or remember.

## 1. Necessity gate

A visual earns its place when it makes at least one important relationship easier to understand than prose alone.

Prefer prose only when the concept is primarily a static definition and spatialization adds decoration rather than comprehension.

A visual is normally justified when the concept contains one or more of:

- meaningful sequence or lifecycle;
- state transitions;
- topology or component relationships;
- containment or hierarchy;
- branching decisions;
- causal structure;
- data or request movement;
- a transformation whose before/after difference matters;
- two structures whose difference is easier to see aligned.

Ask silently:

> If this visual disappeared, would the reader lose a useful relationship rather than merely lose decoration?

If no, skip it unless the user explicitly requested a visual.

## 2. Representation gate

When a visual is justified, classify the understanding problem.

### Narrative visual

Use when the reader mainly needs to follow **what happens over time** and the spatial topology is not itself the important lesson.

Typical signals:

- one dominant happy path;
- one actor performs one action after another;
- a before/after progression;
- request/response can be explained without meaningful branching;
- the main teaching problem is temporal ordering.

Default representation: **story strip**.

Examples:

- a basic pull request lifecycle;
- a webhook event delivered to an app;
- a simple browser request;
- a file moving through a processing pipeline.

### Structural diagram

Use when the reader must understand **where things are, what connects to what, what contains what, or which transitions are possible**.

Typical signals:

- topology is part of the concept;
- multiple components interact;
- branching changes the meaning;
- states and allowed events matter;
- containment or levels matter;
- the same sequence would be misleading if rendered as disconnected story scenes.

Apply the spatial-topology test:

> Removing spatial relationships from this visual would materially reduce understanding.

If true, prefer a diagram.

### Mixed composition

Use both narrative scenes and diagrams when the concept contains two genuinely different cognitive questions:

- **what happens when?** and
- **how are the actors or structures related?**

Do not mix formats merely for variety.

A mixed artifact is valid only when each representation owns a distinct explanatory job.

Example: OAuth can use a short narrative scene for the user granting access and a compact structural/flow diagram for browser → client → authorization server → resource server relationships.

## 3. Structural diagram router

If `structural-diagram` is selected, choose the archetype from the dominant relationship.

| Dominant relationship | Diagram archetype | Primary question |
|---|---|---|
| Ordered path with meaningful branches/decisions | `flow` | What path can this take? |
| States changed by events | `state` | What states exist and what can move between them? |
| Components and connections | `architecture` | What exists and who talks to whom? |
| Containment, ownership, or levels | `hierarchy` | What contains or belongs to what? |
| Cause → mechanism → effects | `causal` | Why does this outcome happen? |
| Same structural dimensions across alternatives | `structural-comparison` | Where do these systems differ structurally? |

### `flow`

Use only when decisions or alternative paths are meaningful.

Do not use a flowchart for a purely linear sequence that a story strip communicates more cheaply.

Good fit:

```text
request → authenticated?
             ├─ no → 401
             └─ yes → process
```

### `state`

Use for finite states, lifecycle constraints, retries, approvals, or event-driven status changes.

The labels on transitions should name the event or condition, not merely repeat the destination state.

Good fit:

```text
DRAFT --submit--> REVIEW --approve--> MERGED
  ^                  |
  └------reject------┘
```

### `architecture`

Use for system parts, ownership, boundaries, and communication paths.

Architecture diagrams answer **who exists and who connects to whom**, not the full runtime history of every component.

### `hierarchy`

Use for `contains`, `belongs-to`, `is-part-of`, or ordered levels.

Do not use hierarchy to imply temporal execution.

### `causal`

Use when the explanatory value is in an actual causal mechanism.

Prefer:

```text
cause → mechanism → effect → observable consequence
```

Allow branches only when multiple downstream effects are material to the user's question.

Never use causal arrows for mere correlation.

### `structural-comparison`

Use aligned structures with the same dimensions on both sides.

The reader should be able to compare equivalent layers without searching for correspondences.

Good fit: VM vs container stack.

## 4. Narrative router

When `narrative-visual` is selected, use the simplest story form that carries the temporal model.

Default to a vertical story strip:

- 3–6 scenes;
- one primary action per scene;
- one clear reading direction;
- recurring actors remain visually consistent;
- panel titles alone tell the sequence;
- captions add a new fact, never paraphrase the title.

Use before/after instead when the transformation itself matters more than intermediate steps.

## 5. Mixed-composition contract

A single rendered HTML artifact may contain explanatory prose, narrative scenes, and embedded diagrams.

Use this only when different sections answer different questions.

A valid mixed artifact commonly follows:

```text
verbal core
→ narrative beat
→ structural diagram
→ narrative consequence
→ closing truth
```

Rules:

1. Do not repeat the same fact in prose, scene, and diagram.
2. Narrative scenes own temporal comprehension.
3. Diagrams own topology, allowed transitions, containment, or structural comparison.
4. Use as few representation switches as necessary.
5. Keep terminology identical across prose and visuals.
6. The whole artifact still needs one obvious reading order.

## 6. Default routing examples

| Prompt | Expected route | Why |
|---|---|---|
| "Explain a pull request" | `narrative-visual/story-strip` | Main value is a short sequence. |
| "Explain the components of a RAG application" | `structural-diagram/architecture` | Component relationships are the lesson. |
| "Explain a GitHub issue lifecycle" | `structural-diagram/state` | Allowed states/transitions matter. |
| "Why can retries duplicate payments?" | `structural-diagram/causal` | The causal chain is the lesson. |
| "Docker vs VM" | `structural-diagram/structural-comparison` | Layer alignment reveals the core difference. |
| "What is JSON?" | `prose-only` | A diagram is normally decorative. |
| "Explain OAuth visually" | `mixed` | Temporal consent and multi-actor structure both matter. |

## 7. Anti-patterns

Reject these routes:

- `static definition → decorative infographic`;
- `simple linear process → dense flowchart`;
- `structural topology → disconnected comic panels`;
- `state machine → generic story strip that hides invalid transitions`;
- `causal question → architecture map with unlabeled arrows`;
- `comparison → two unrelated drawings with different dimensions`;
- `mixed → alternating formats for decoration rather than distinct cognitive jobs`.

## 8. Handoff to diagram contract

When this router selects any `structural-diagram/*` route, read `references/diagram-contract.md` before rendering.

When it selects `mixed`, read `references/diagram-contract.md` for the diagram sections and apply the story-strip rules in `SKILL.md` for narrative sections.
