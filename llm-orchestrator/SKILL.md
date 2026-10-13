---
name: llm-orchestrator
description: "Automatically route a task to the best available local coding LLM CLI (Codex, Claude Code, or Grok Build), ignore missing or unauthenticated providers, select an execution tier, fall back on failure, and optionally run independent review or multi-model synthesis. Use when a task should be delegated to the most suitable installed model instead of choosing a provider manually."
version: 1.2.0
---

# LLM Orchestrator

Route by task requirements, not by vendor. Detect only providers that are both installed and usable, classify the demand, rank candidates, then execute with fallback.

## Core rule

Run [router.mjs](scripts/router.mjs) instead of manually choosing Codex, Claude, or Grok whenever the user asks for model orchestration or when a substantial task benefits from provider selection.

Do not fail because one provider is absent. Missing or unauthenticated providers are excluded. Transient runtime failures such as quota exhaustion are caught at dispatch and fall through to the next ranked provider without blocking the task.

## Commands

```bash
llmo status
llmo route --task "Review this repository architecture and identify the three highest-risk gaps"
llmo run --task "Fix the failing auth tests and verify the suite" --cwd "$PWD"
```

For long tasks, prefer a file:

```bash
llmo run --task-file /tmp/task.md --cwd "$PWD"
```

Inspect or reset transient runtime health:

```bash
llmo health
llmo health reset grok
llmo health reset
```
## Routing behavior

1. **Preflight** — detect `codex`, `claude`, and `grok`; verify authentication/readiness without reading secrets.
2. **Classify** — infer code-write, debugging, review, architecture, research/current-info, writing/synthesis, security, complexity, and mutation risk.
3. **Rank** — score only ready providers against the task profile.
4. **Choose tier** — `fast`, `balanced`, or `strong`; exact model IDs remain adapter/config concerns so the skill survives model churn.
5. **Choose strategy**:
   - `single`: one provider is enough or only one is usable.
   - `reviewed`: implementation by the best executor, independent read-only review by another provider, one repair loop when needed.
   - `ensemble`: independent analyses from the top providers followed by synthesis.
6. **Fallback** — on provider failure, try the next ranked ready provider; never loop indefinitely.
7. **Circuit health** — temporarily skip providers with quota, rate-limit, auth-expiry, timeout, or service-outage failures; retry after cooldown with a single half-open probe.
8. **Report** — expose chosen provider, model/tier, strategy, circuit state, fallback history, and final result.

## Permission policy

Use safe noninteractive modes by default:

- Codex: workspace-write only for implementation; read-only for review/analysis; never use the dangerous bypass flag.
- Claude Code: `auto` for execution and `plan` for read-only review.
- Grok Build: `--sandbox workspace` always; headless `--always-approve` only for mutation, and a read-only tool allowlist with `dontAsk` for analysis/review.

Do not silently broaden filesystem or network authority. If a task genuinely requires broader access, let the host agent/user make that decision explicitly.

## Runtime health and portability

Circuit state is local, optional, and disposable. By default it lives at `~/.cache/llm-orchestrator/health.json` (or `$XDG_CACHE_HOME/llm-orchestrator/health.json`). No prompt, source code, secret, or raw provider error is stored.

A missing or corrupt health cache is treated as a fresh `CLOSED` state, so copied/cloned projects work immediately on another machine. The cache improves routing but is never required for routing. Set `LLM_ORCH_HEALTH_FILE` only for isolation/testing.
## Model policy

Model selection is intentionally future-proof:

- Codex inherits the user's configured model for `fast`/`balanced`; `strong` can be overridden with `LLM_ORCH_CODEX_STRONG_MODEL`.
- Claude uses stable aliases by tier (`haiku`, `sonnet`, `opus`) unless overridden.
- Grok discovers its current default from `grok models` and uses it unless overridden.
- Explicit model pins are soft only for model-resolution errors; quota, auth, permission, timeout, or execution failures fall through directly to the next provider.

Supported overrides:

```bash
LLM_ORCH_CODEX_FAST_MODEL=...
LLM_ORCH_CODEX_BALANCED_MODEL=...
LLM_ORCH_CODEX_STRONG_MODEL=...
LLM_ORCH_CLAUDE_FAST_MODEL=...
LLM_ORCH_CLAUDE_BALANCED_MODEL=...
LLM_ORCH_CLAUDE_STRONG_MODEL=...
LLM_ORCH_GROK_FAST_MODEL=...
LLM_ORCH_GROK_BALANCED_MODEL=...
LLM_ORCH_GROK_STRONG_MODEL=...
```

See [Routing Policy](references/routing-policy.md) for scoring and strategy details.
## Portable installation

Install a project-local copy for all three supported harnesses:

```bash
node ~/.agents/skills/llm-orchestrator/scripts/install-project.mjs /path/to/project
```

This writes the same skill into:

- `.agents/skills/llm-orchestrator/`
- `.claude/skills/llm-orchestrator/`
- `.grok/skills/llm-orchestrator/`
- `./.llmo` — project-local executable wrapper, so the router works even when no global launcher is on `PATH`.

Use copies rather than home-directory symlinks so a repository remains portable across machines. After installation, `./.llmo status`, `./.llmo route ...`, and `./.llmo run ...` work from the project root.

## Stress testing

Run the permanent routing and resilience suites after classifier, scoring, adapter, or fallback changes:

```bash
node scripts/health-test.mjs
node scripts/circuit-integration-test.mjs
node scripts/stress-test.mjs
node scripts/fault-test.mjs
```

`health-test.mjs` verifies circuit state transitions and privacy. `circuit-integration-test.mjs` verifies routing actually excludes/re-admits providers. `stress-test.mjs` exercises 32 routing demands plus paraphrase-invariance groups. `fault-test.mjs` injects 15 provider/readiness/quota/model/timeout/reviewer/ensemble failures using local stubs, without spending model quota. Keep real-provider canaries small and disposable; synthetic tests are the regression gate.

## Verification

After any change, run:

```bash
node scripts/router.mjs self-test
node scripts/health-test.mjs
node scripts/circuit-integration-test.mjs
node scripts/stress-test.mjs
node scripts/fault-test.mjs
node ~/.agents/skills/skill-creator/scripts/validate-skill.mjs ~/.agents/skills/llm-orchestrator
llmo status
llmo route --task "Implement a failing-test fix in this repository"
```

A valid installation must degrade cleanly to one ready provider and must never select an unavailable provider.

## Files

- [router.mjs](scripts/router.mjs) — detection, classification, ranking, execution, review, synthesis, fallback.
- [health.mjs](scripts/health.mjs) — portable local circuit-breaker state and health classification.
- [install-project.mjs](scripts/install-project.mjs) — portable project installation.
- [Routing Policy](references/routing-policy.md) — transparent scoring and extension points.
- [stress-test.mjs](scripts/stress-test.mjs) — 32-case routing and paraphrase regression suite.
- [fault-test.mjs](scripts/fault-test.mjs) — 15-case deterministic resilience/fallback suite.
- [health-test.mjs](scripts/health-test.mjs) — circuit state/privacy regression suite.
- [circuit-integration-test.mjs](scripts/circuit-integration-test.mjs) — router/circuit integration suite.
