# skills

Catálogo pessoal de skills de Rafael Costa.

## Skills

| Skill | O que faz |
| --- | --- |
| [clarify](./clarify) | Diagnostica e reconstrói material complexo preservando invariantes; para visuais source-bound, pode provar cobertura, renderização e revisão perceptiva via Visual Semantic Compiler. |
| [concept-bridge](./concept-bridge) | Constrói o menor modelo mental correto para entender um conceito novo e, quando um visual ajuda, roteia entre narrativa, diagramas estruturais ou composição mista sem aumentar a carga cognitiva. |
| [visual-semantic-compiler](./visual-semantic-compiler) | Compila decisões visuais em IR semântico verificável, preserva regras/recovery, gera layout/HTML determinístico e separa browser evidence de revisão perceptiva hash-bound. |
| [youtube-fetcher](./youtube-fetcher) | Extrai evidência do YouTube com contexto mínimo: metadata, capítulos, transcript, ranges, chunks determinísticos, manifests e Markdown pronto para Obsidian/RAG. |

## Uso

Clone o repositório e aponte o runtime de skills para esta pasta, ou copie a skill desejada para o catálogo local do agente:

```bash
git clone https://github.com/rafaelscosta/skills.git
cp -R skills/clarify ~/.claude/skills/clarify
cp -R skills/concept-bridge ~/.claude/skills/concept-bridge
cp -R skills/visual-semantic-compiler ~/.claude/skills/visual-semantic-compiler
cp -R skills/youtube-fetcher ~/.claude/skills/youtube-fetcher
```

As skills seguem o mesmo molde de catálogo: `SKILL.md`, metadata do agente, contrato em `config.yaml` e, quando necessário, referências, evals, assets e scripts de validação/runtime.
