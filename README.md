# skills

Catálogo pessoal de skills de Rafael Costa.

## Skills

| Skill | O que faz |
| --- | --- |
| [clarify](./clarify) | Diagnostica por que um material é difícil de entender e transforma em explicações, fluxos, procedimentos ou auditorias de clareza em português brasileiro. |
| [youtube-fetcher](./youtube-fetcher) | Extrai evidência do YouTube com contexto mínimo: metadata, capítulos, transcript, ranges, chunks determinísticos, manifests e Markdown pronto para Obsidian/RAG. |

## Uso

Clone o repositório e aponte o runtime de skills para esta pasta, ou copie a skill desejada para o catálogo local do agente:

```bash
git clone https://github.com/rafaelscosta/skills.git
cp -R skills/clarify ~/.claude/skills/clarify
cp -R skills/youtube-fetcher ~/.claude/skills/youtube-fetcher
```

As skills seguem o mesmo molde de catálogo: `SKILL.md`, metadata do agente, contrato em `config.yaml` e, quando necessário, referências, evals, assets e scripts de validação/runtime.
