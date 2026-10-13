# skills

Catálogo pessoal de skills de Rafael Costa.

## Skills

| Skill | O que faz |
| --- | --- |
| [clarify](./clarify) | Diagnostica e reconstrói material complexo preservando invariantes; para visuais source-bound, pode provar cobertura, renderização e revisão perceptiva via Visual Semantic Compiler. |
| [concept-bridge](./concept-bridge) | Constrói o menor modelo mental correto para entender um conceito novo e, quando um visual ajuda, roteia entre narrativa, diagramas estruturais ou composição mista sem aumentar a carga cognitiva. |
| [llm-orchestrator](./llm-orchestrator) | Roteia automaticamente tasks entre Codex, Claude Code e Grok Build conforme demanda, disponibilidade e saúde do runtime, com fallback, review/ensemble e circuit breaker portátil. |
| [visual-semantic-compiler](./visual-semantic-compiler) | Compila decisões visuais em IR semântico verificável, preserva regras/recovery, gera layout/HTML determinístico e separa browser evidence de revisão perceptiva hash-bound. |
| [visualize-design-system](./visualize-design-system) | Audita design systems e bibliotecas de componentes e os transforma em guias visuais verificáveis, com proveniência, artefatos editáveis e QA. |
| [youtube-fetcher](./youtube-fetcher) | Extrai evidência do YouTube com contexto mínimo: metadata, capítulos, transcript, ranges, chunks determinísticos, manifests e Markdown pronto para Obsidian/RAG. |
| [persuasion-architect](./persuasion-architect) | Estrutura e audita decisões persuasivas com evidência e limites explícitos; candidato de código, certificação comportamental pendente de controle de idioma. |
| [video-edit-contract](./video-edit-contract) | Converte briefing e objetivo em contrato editorial com invariantes, prioridades e gates de aceite. |
| [footage-intelligence](./footage-intelligence) | Inspeciona material bruto e produz mapa semântico source-grounded para recuperação editorial. |
| [story-edit](./story-edit) | Constrói ou repara narrativa, seleção, progressão, setup/payoff e decisões estruturais. |
| [senior-video-editor](./senior-video-editor) | Orquestra o pipeline editorial, integra especialistas e declara gaps antes de supervisão independente. |
| [supervising-video-editor](./supervising-video-editor) | Avalia cortes de forma independente, com blockers antes de score e condições objetivas de revisão. |
| [attention-choreography](./attention-choreography) | Analisa competição de atenção entre rosto, texto, gráficos e produto; candidato, promoção depende dos fixtures visuais e proveniência originais. |

## Uso

Clone o repositório e aponte o runtime de skills para esta pasta, ou copie a skill desejada para o catálogo local do agente:

```bash
git clone https://github.com/rafaelscosta/skills.git
cp -R skills/clarify ~/.claude/skills/clarify
cp -R skills/concept-bridge ~/.claude/skills/concept-bridge
cp -R skills/llm-orchestrator ~/.claude/skills/llm-orchestrator
cp -R skills/visual-semantic-compiler ~/.claude/skills/visual-semantic-compiler
cp -R skills/visualize-design-system ~/.claude/skills/visualize-design-system
cp -R skills/youtube-fetcher ~/.claude/skills/youtube-fetcher
```

As skills seguem o mesmo molde de catálogo: `SKILL.md`, metadata do agente, contrato em `config.yaml` e, quando necessário, referências, evals, assets e scripts de validação/runtime.

## Senior Video Editor candidate

The five-skill editorial slice provides machine-bound source handoffs and independent supervision contracts. It is CODE_READY; current contract bytes are NOT_CERTIFIED_CURRENT_CONTRACTS. Historical evaluation artifacts remain available, and new independent holdouts are required before behavioral promotion. See senior-video-editor/VALIDATION.md.
