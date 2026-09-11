# skills

Catálogo pessoal de skills de Rafael Costa.

## Skills

| Skill | O que faz |
| --- | --- |
| [clarify](./clarify) | Diagnostica e reconstrói material complexo preservando invariantes; para visuais source-bound, pode provar cobertura, renderização e revisão perceptiva via Visual Semantic Compiler. |
| [concept-bridge](./concept-bridge) | Constrói o menor modelo mental correto para entender um conceito novo e, quando um visual ajuda, roteia entre narrativa, diagramas estruturais ou composição mista sem aumentar a carga cognitiva. |
| [visual-semantic-compiler](./visual-semantic-compiler) | Compila decisões visuais em IR semântico verificável, preserva regras/recovery, gera layout/HTML determinístico e separa browser evidence de revisão perceptiva hash-bound. |
| [youtube-fetcher](./youtube-fetcher) | Extrai evidência do YouTube com contexto mínimo: metadata, capítulos, transcript, ranges, chunks determinísticos, manifests e Markdown pronto para Obsidian/RAG. |
| [video-edit-contract](./video-edit-contract) | Converte briefing e objetivo em contrato editorial com invariantes, prioridades e gates de aceite. |
| [footage-intelligence](./footage-intelligence) | Inspeciona material bruto e produz mapa semântico source-grounded para recuperação editorial. |
| [story-edit](./story-edit) | Constrói ou repara narrativa, seleção, progressão, setup/payoff e decisões estruturais. |
| [senior-video-editor](./senior-video-editor) | Orquestra o pipeline editorial, integra especialistas e declara gaps antes de supervisão independente. |
| [supervising-video-editor](./supervising-video-editor) | Avalia cortes de forma independente, com blockers antes de score e condições objetivas de revisão. |

## Uso

Clone o repositório e aponte o runtime de skills para esta pasta, ou copie a skill desejada para o catálogo local do agente.

As skills seguem o mesmo molde de catálogo: `SKILL.md`, metadata do agente, contrato em `config.yaml` e, quando necessário, referências, evals, assets e scripts de validação/runtime.

## Senior Video Editor v0.1

O primeiro vertical slice de edição sênior é propositalmente pequeno:

```text
video-edit-contract
→ footage-intelligence
→ story-edit
→ senior-video-editor
→ supervising-video-editor
```

Ele certifica julgamento editorial e separação generator/judge antes de expandir para timing, atenção, continuidade, motion, sound, color, VFX, captions, media engineering, AI-assisted post e delivery QC.
