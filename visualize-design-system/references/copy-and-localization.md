# Copy and localization

The visible guide must be scannable before it is comprehensive. Put technical traceability in the source package, not inside every card.

## Default language behavior

- Visible instructional copy: Brazilian Portuguese.
- Image-generation and art-direction prompts: English.
- Token paths, prop names, component exports, CSS variables, and code literals: preserve exactly.
- Established English design-system terms may remain in English when they match the codebase. Add a short explanation rather than inventing a translation that breaks shared vocabulary.

## Copy hierarchy

### Eyebrow

Purpose: collection, layer, or system context.

Examples:

```text
DESIGN SYSTEM / COMPONENTES
FOUNDATIONS / COLOR
PADRÕES DE INTERAÇÃO
```

Budget: approximately 12–32 characters.

### Title

Purpose: name the governed subject.

Examples:

```text
SISTEMA DE BOTÕES
CORES SEMÂNTICAS
ESCOLHA DO COMPONENTE
```

Budget: approximately 18–44 characters, preferably one or two lines.

### Subtitle

Purpose: state what the reader will learn or decide.

Examples:

```text
Variantes, estados e regras de uso.
Do valor primitivo ao estado do componente.
Escolha o padrão certo para cada tipo de feedback.
```

Budget: one concise sentence, usually 45–95 characters.

## Card microcopy

Use parallel grammar across peer entries.

Recommended structure:

- **Name:** 1–5 words.
- **Definition or role:** 6–18 words.
- **Use when:** 4–12 words.
- **Avoid when:** 4–12 words.
- **Technical note:** exact token/prop/value, separate from prose.

Prefer:

```text
Primary
Use para a ação principal da etapa.
```

Avoid:

```text
This is the primary style and it is generally used whenever the user needs to perform the main action on a screen.
```

## Decision-writing pattern

Use observable conditions.

```text
Quando há 2–4 opções mutuamente exclusivas e todas devem permanecer visíveis, use Radio Group.
```

Avoid taste-based wording:

```text
Use Radio Group quando parecer mais elegante.
```

## Do/don't writing pattern

A rationale should name the consequence, not merely repeat the visual.

Good:

```text
DO — Use uma única ação primária por área.
Reduz competição visual e deixa a próxima ação inequívoca.
```

Weak:

```text
DO — Use o botão correto.
Fica melhor.
```

## State labels

Use consistent labels across the guide:

```text
Default
Hover
Focus
Pressed
Selected
Disabled
Loading
Error
Success
Read-only
```

Translate explanatory copy, but keep state names aligned with the repository when they are public API or test identifiers.

## Provenance labels

Recommended visible shorthand only when the status matters to interpretation:

```text
IMPLEMENTADO
DOCUMENTADO
INFERIDO
PROPOSTO
AUSENTE
DEPRECADO
```

Do not clutter every cell with provenance. Use a legend, section badge, or source report.

## Error and uncertainty language

State uncertainty plainly:

```text
O estado de loading foi documentado, mas não foi encontrado na API pública.
```

Do not mask uncertainty:

```text
Provavelmente existe um loading state robusto.
```

## Copy budgets by architecture

| Architecture | Typical visible body copy |
|---|---:|
| Token sheet | 120–260 words |
| Anatomy | 80–180 words |
| State matrix | 60–160 words |
| Do/don't board | 120–260 words |
| Decision table | 140–320 words |
| Responsive strip | 90–200 words |
| Master cheat sheet | 180–360 words |

If the copy exceeds the range, shorten, split, or move details to the companion documentation. Do not solve overflow by shrinking the type below practical reading size.

## Prompt format for generated visuals

When an image or illustration prompt is required, use this structure:

```markdown
## ART DIRECTION PROMPT — ENGLISH

[English instructions describing composition, subject consistency, lighting, camera, style, exclusions, and production constraints.]

## VISIBLE TEXT — PT-BR

- "Exact visible string 1"
- "Exact visible string 2"

## NEGATIVE CONSTRAINTS — ENGLISH

- No embedded text beyond the exact visible-text block.
- No watermark, signature, logo imitation, or placeholder copy.
- Do not alter the documented component geometry.
```

For core UI samples, prefer actual rendered components rather than image-generation prompts.
