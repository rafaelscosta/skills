# LLM Orchestrator

Skill portátil para rotear automaticamente uma demanda entre **Codex**, **Claude Code** e **Grok Build** conforme o tipo de trabalho, risco, complexidade e runtimes realmente disponíveis na máquina.

O pacote funciona sem serviço central, sem banco externo e sem exigir que os três providers estejam instalados. Providers ausentes, sem autenticação, em quota, rate limit, timeout ou outage são ignorados ou colocados temporariamente em circuit breaker.

## O que entrega

- detecção automática de Codex, Claude e Grok;
- classificação da task: código, debug, review, arquitetura, pesquisa, escrita e segurança;
- tier automático `fast`, `balanced` ou `strong`;
- estratégias `single`, `reviewed` e `ensemble`;
- fallback entre providers;
- circuit breaker `CLOSED / OPEN / HALF_OPEN`;
- review independente quando outro provider está disponível;
- instalação project-local para os três harnesses;
- stress tests e fault injection determinísticos.

## Uso rápido

```bash
llmo status
llmo route --task "Fix the failing auth tests and review the final diff"
llmo run --task "Fix the failing auth tests and review the final diff" --cwd "$PWD"
```

Para instalar dentro de qualquer projeto:

```bash
node scripts/install-project.mjs /path/to/project
```

Isso cria o mesmo contrato em `.agents/skills`, `.claude/skills` e `.grok/skills`, além de um wrapper `./.llmo` no projeto.

## Runtime health

O estado transitório fica fora do projeto, por padrão em `~/.cache/llm-orchestrator/health.json`. Ele não guarda prompts, código, secrets ou erro bruto e pode ser apagado sem quebrar o roteador.

```bash
llmo health
llmo health reset grok
llmo health reset
```

## Verificação

```bash
node scripts/router.mjs self-test
node scripts/health-test.mjs
node scripts/circuit-integration-test.mjs
node scripts/stress-test.mjs
node scripts/fault-test.mjs
```

Gate de publicação da v1.2.0: **32/32** casos de roteamento, **3/3** grupos de invariância semântica, **15/15** fault injections, **13/13** testes de health e **4/4** testes de integração do circuit breaker.

Veja [SKILL.md](./SKILL.md) para o contrato operacional e [references/routing-policy.md](./references/routing-policy.md) para a política de roteamento.
