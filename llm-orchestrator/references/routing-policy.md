# Routing Policy

The router optimizes for task fit while remaining provider-agnostic. Scores are heuristics, not claims that one vendor is universally better.

## Task dimensions

- `code`: implementation, repository edits, refactors, tests, build/deploy work.
- `debug`: failures, regressions, diagnosis, root-cause analysis.
- `review`: audits, verification, critique, risk and quality review.
- `architecture`: system design, roadmaps, migrations, decomposition, workflows.
- `research`: current information, web evidence, benchmarks, competitive research.
- `writing`: synthesis, documentation, proposals, editorial output.
- `security`: auth, permissions, secrets, vulnerabilities, compliance.

The classifier also computes:

- `mutation`: whether the task is likely to change the workspace.
- `complexity`: 1–5 based on breadth, length, multi-domain signals, and end-to-end scope.
- `risk`: low / medium / high.
- `tier`: fast / balanced / strong.

## Default capability matrix

| Provider | Code | Debug | Review | Architecture | Research | Writing | Security |
|---|---:|---:|---:|---:|---:|---:|---:|
| Codex | 100 | 100 | 90 | 88 | 74 | 80 | 90 |
| Claude | 88 | 88 | 100 | 100 | 90 | 100 | 96 |
| Grok | 92 | 90 | 88 | 90 | 100 | 86 | 88 |

Bonuses are small and task-specific: Codex for mutation, Grok for research, Claude for architecture/review.
## Strategy selection

- One ready provider → always `single`.
- Mutable task with complexity ≥ 3, or a mutable task that explicitly asks for review/verification, with two or more providers → `reviewed`.
- Research/architecture/review task, complexity ≥ 4, two or more providers → `ensemble`.
- Everything else → `single`.

`reviewed` uses a different provider for review when possible. The reviewer is read-only. A `VERDICT: FIX` permits one repair pass and one final review; there is no unbounded agent loop.

`ensemble` asks up to three providers for independent read-only analyses, then asks the highest-ranked available provider to synthesize them.

## Readiness, not installation

A binary on PATH is insufficient. The adapter excludes providers that cannot actually run:

- Codex: `codex login status` must pass.
- Claude: authenticated session or supported API/provider environment configuration.
- Grok: authenticated `grok models` or `XAI_API_KEY`.

This distinction prevents a missing login from breaking orchestration.

## Model churn

The routing contract selects a tier first. Exact model IDs are deliberately soft:

- inherit/discover defaults where possible;
- use stable aliases where supported;
- permit environment overrides;
- if an explicit model pin fails, retry that provider once without the pin;
- if the provider still fails, move to the next ranked provider.

## Calibration path

The next maturity step is empirical routing: log anonymized task profile, selected provider/model, latency, exit status, verification verdict, and retries; then periodically update the capability matrix from observed outcomes. Keep this opt-in and never log prompts, secrets, or source code by default.

## Runtime execution notes

Mutation tasks never use the `fast` tier: even a small edit routes at least as `balanced`. Complexity >= 4 or high-risk work routes to `strong`.

Authentication is an eligibility check, not a guarantee that a provider can serve the next request. Quota, rate-limit, timeout, permission, and runtime errors are dispatch failures and immediately advance to the next ranked provider.

For Grok mutation, use headless tool execution with `--sandbox workspace` and `--always-approve`; the sandbox bounds writes to the workspace. For Grok analysis/review, keep the workspace sandbox and expose only read-oriented tools (plus web tools when research is requested).

A model-pin retry is allowed only when the error itself indicates an unknown, unsupported, missing, or unavailable model. Do not retry quota/auth/runtime failures with a different pin before falling back providers.

## Regression gates

Routing policy changes must preserve the deterministic stress suites unless a benchmark expectation is deliberately revised with a documented reason. The routing suite covers task semantics and paraphrase stability; the fault suite covers provider absence, zero providers, quota, runtime failure, invalid model pins, incomplete mutation responses, reviewer failure, ensemble degradation, and timeout fallback.

Provider discovery checks the active `PATH` first, then common machine-level locations (`~/.local/bin`, `/opt/homebrew/bin`, `/usr/local/bin`) so routing reflects installed CLIs rather than shell-specific PATH differences.

## Runtime circuit breaker

Runtime health is progressive enhancement, not a prerequisite. A provider is `CLOSED` by default, `OPEN` during a cooldown after a provider-level transient failure, and `HALF_OPEN` after cooldown so one probe can test recovery. A successful probe closes the circuit.

Default cooldowns: quota 60 minutes; rate limit 5 minutes; auth-expiry 15 minutes; timeout 2 minutes; service outage 1 minute. Timeout and rate-limit cooldowns back off on repeated failures. Environment overrides use `LLM_ORCH_COOLDOWN_<REASON>_MS`.

Only provider-health failures open a circuit. Model-resolution errors, task failures, verification failures, permission constraints, and incomplete model output do not globally penalize a provider. The cache stores categories and timestamps only, never prompts, source code, secrets, or raw errors.

The cache is machine-local and disposable. Missing/corrupt cache means `CLOSED`; portability therefore does not depend on copying runtime state. `llmo health reset [provider]` clears stale state manually.
