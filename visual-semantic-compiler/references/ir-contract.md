# Visual Semantic IR v1 Contract

`visual-semantic-ir/v1` is a renderer-agnostic semantic contract. It captures meaning before layout.

## Required top-level fields

```json
{
  "schema_version": "visual-semantic-ir/v1",
  "source_skill": "concept-bridge",
  "intent": {},
  "representation": {},
  "entities": [],
  "relationships": [],
  "narrative_beats": [],
  "groups": [],
  "views": [],
  "constraints": {},
  "omissions": [],
  "text_equivalent": ""
}
```

Unknown top-level fields are rejected.

## Intent

`intent` records the cognitive contract, not style:

- `question` — the primary question being answered;
- `audience` — audience boundary;
- `depth` — upstream depth label when available;
- `language` — authored language such as `pt-BR`;
- `desired_outcome` — what the reader should be able to understand, predict, decide, or do.

## Representation

`representation.class`:

- `narrative-visual`;
- `structural-diagram`;
- `mixed`.

`representation.type` supports narrative and structural types. `mixed` uses type `mixed` plus explicit `views`.

Every representation records:

- `primary_question`;
- `reading_direction`: `left-to-right`, `top-to-bottom`, or `other`.

## Entities

Each entity contains:

```json
{
  "id": "retriever",
  "label": "Retriever",
  "kind": "component",
  "description": "optional",
  "provenance": {}
}
```

`kind` is semantic, not visual shape. Current kinds include actor, component, state, decision, data, concept, stage, outcome, storage, process, evidence, claim, and other.

## Relationships

Each relationship contains:

```json
{
  "id": "r2",
  "from": "app",
  "to": "retriever",
  "kind": "call",
  "semantic": "solicita contexto",
  "label": "optional reader label",
  "order": 2,
  "provenance": {}
}
```

`semantic` is mandatory. An edge without a named meaning is not a valid semantic relation.

Current relationship kinds include flow, transition, call, return, data, dependency, containment, causation, comparison, handoff, reads, writes, supports, attacks, feedback, and other.

## Narrative beats

Narrative visuals use ordered beats:

```json
{
  "id": "beat1",
  "title": "O usuário autoriza o acesso.",
  "action": "concede a permissão solicitada",
  "actor": "user",
  "order": 1,
  "provenance": {}
}
```

Titles should remain useful when read without the illustration.

## Groups

Groups express real semantic grouping such as boundaries, lanes, layers, comparison sides, or phases. They do not exist merely for decoration.

## Mixed views

Mixed artifacts use `views` to assign different cognitive questions to different representations. A valid mixed IR has at least one narrative and one structural view, and those views answer distinct questions.

## Provenance

Supported status values:

- `explicit` — directly supported by evidence;
- `inferred` — reasoned from evidence, not explicitly stated;
- `general-knowledge` — stable conceptual knowledge not tied to one supplied source;
- `unknown` — unresolved.

Optional fields:

- `source_ref`;
- `locator`;
- `confidence`: `high`, `medium`, `low`, `unknown`;
- `note`.

Do not use provenance as decoration. It exists to bound truth claims.

## Constraints

Current semantic constraints:

- `direct_labels`;
- `target_zero_crossings`;
- `max_primary_nodes`;
- `text_equivalent_required`.

`target_zero_crossings` is an authored downstream goal. R1 does not compute geometry, so layout remains deferred.

## Omissions

`omissions` records important complexity intentionally excluded at the selected depth. This is required for honest progressive disclosure when the first model is deliberately incomplete.

## Text equivalent

`text_equivalent` must preserve the truth-critical model independently of visual rendering.

## Versioning

R1 uses the exact schema identifier `visual-semantic-ir/v1`. Additive implementation behavior may improve without changing the schema identifier. Breaking field or semantic changes require `v2`.
