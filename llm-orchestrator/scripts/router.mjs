#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { accessSync, constants, existsSync, readFileSync, writeFileSync, mkdtempSync, rmSync } from 'node:fs';
import { homedir, tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import assert from 'node:assert/strict';
import { beginDispatch, healthSnapshot, previewCircuit, recordFailure, recordSuccess, resetHealth } from './health.mjs';

const PROVIDERS = ['codex', 'claude', 'grok'];
const CAPS = {
  codex:  { code: 100, debug: 100, review: 90, architecture: 88, research: 74, writing: 80, security: 90 },
  claude: { code: 88,  debug: 88,  review: 100, architecture: 100, research: 90, writing: 100, security: 96 },
  grok:   { code: 92,  debug: 90,  review: 88, architecture: 90, research: 100, writing: 86, security: 88 },
};

function parseArgs(argv) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) out._.push(a);
    else {
      const key = a.slice(2);
      const next = argv[i + 1];
      if (!next || next.startsWith('--')) out[key] = true;
      else { out[key] = next; i++; }
    }
  }
  return out;
}
function run(bin, args = [], opts = {}) {
  return spawnSync(bin, args, {
    encoding: 'utf8',
    timeout: opts.timeout ?? 15000,
    maxBuffer: 50 * 1024 * 1024,
    input: opts.input,
    cwd: opts.cwd,
    env: { ...process.env, ...(opts.env || {}) },
  });
}

function commandPath(name) {
  const r = run('/bin/sh', ['-c', `command -v ${name}`]);
  if (r.status === 0 && r.stdout.trim()) return r.stdout.trim();
  const candidates = [
    join(homedir(), '.local', 'bin', name),
    join('/opt/homebrew/bin', name),
    join('/usr/local/bin', name),
  ];
  for (const candidate of candidates) {
    try { accessSync(candidate, constants.X_OK); return candidate; } catch {}
  }
  return null;
}

function codexConfiguredModel() {
  try {
    const p = join(homedir(), '.codex', 'config.toml');
    const m = readFileSync(p, 'utf8').match(/^model\s*=\s*"([^"]+)"/m);
    return m?.[1] || null;
  } catch { return null; }
}

function probeProviders() {
  const hasMockReady = Object.prototype.hasOwnProperty.call(process.env, 'LLM_ORCH_MOCK_READY');
  const mocked = process.env.LLM_ORCH_MOCK_READY || '';
  if (hasMockReady) {
    const ready = new Set(mocked.split(',').map(s => s.trim()).filter(Boolean));
    return PROVIDERS.map(name => ({ name, installed: ready.has(name), ready: ready.has(name), reason: ready.has(name) ? 'mock-ready' : 'mock-unavailable' }));
  }
  const states = [];
  for (const name of PROVIDERS) {
    const path = commandPath(name);
    if (!path) { states.push({ name, installed: false, ready: false, reason: 'not-installed' }); continue; }
    if (name === 'codex') {
      const r = run(path, ['login', 'status']);
      states.push({ name, installed: true, ready: r.status === 0, reason: r.status === 0 ? 'authenticated' : 'auth-required', model: codexConfiguredModel() });
    } else if (name === 'claude') {
      const r = run(path, ['auth', 'status']);
      const keyReady = Boolean(process.env.ANTHROPIC_API_KEY || process.env.CLAUDE_CODE_USE_BEDROCK || process.env.CLAUDE_CODE_USE_VERTEX);
      let loggedIn = false;
      try { loggedIn = JSON.parse(r.stdout || '{}').loggedIn === true; } catch {}
      states.push({ name, installed: true, ready: loggedIn || keyReady, reason: loggedIn || keyReady ? 'authenticated' : 'auth-required' });
    } else {
      const r = run(path, ['models']);
      const text = `${r.stdout || ''}\n${r.stderr || ''}`;
      const keyReady = Boolean(process.env.XAI_API_KEY);
      const ready = keyReady || (r.status === 0 && !/not authenticated/i.test(text));
      const model = text.match(/Default model:\s*([^\s]+)/i)?.[1] || null;
      states.push({ name, installed: true, ready, reason: ready ? 'authenticated' : 'auth-required', model });
    }
  }
  return states;
}

const has = (text, re) => re.test(text);
function classify(task) {
  const t = task.toLowerCase();
  const flags = {
    code: has(t, /\b(code|coding|implement\w*|fix\w*|bug\w*|refactor\w*|repo\w*|test\w*|typescript|javascript|python|rust|golang|compile|lint|deploy\w*|dependenc\w*|package|framework|function|module|variable|diff|patch|git|files?)\b/i),
    debug: has(t, /\b(debug\w*|fail\w*|error\w*|broken|regression\w*|root cause|diagnos\w*|intermittent|wrong|problem|investigat\w*|performance|faster|slow\w*|latency|bottleneck|optimi[sz]\w*)\b/i),
    review: has(t, /\b(review\w*|audit\w*|critique\w*|evaluat\w*|assess\w*|second opinion|verif\w*|validat\w*|prove|quality|risk\w*|acceptance|challenge\w*|tradeoffs?|contradiction\w*|canonical|conflict\w*|best supported)\b/i),
    architecture: has(t, /\b(architect\w*|system design|roadmap|plans?|strategy|decompos\w*|migration\w*|topology|workflow\w*|monolith|modular\w*|coupling|services?|canonical)\b/i),
    research: has(t, /\b(research\w*|latest|current|today|news|web|internet|benchmark\w*|compar\w*|competitor\w*|market|sources?|evidence|official docs?|official documentation|primary sources?|up[- ]to[- ]date|best practices?)\b/i),
    writing: has(t, /\b(write|rewrite|copy|article|documents?|documentation|proposal|summar\w*|synthesi[sz]\w*|narrative|content|specification|decision record|adr|stakeholder|notes?)\b/i),
    security: has(t, /\b(security|vulnerabilit\w*|auth\w*|permission\w*|secrets?|credentials?|threat\w*|exploit\w*|compliance)\b/i),
  };
  const explicitEnsemble = has(t, /\b(every|all) available models?\b|\bevery model\b|\ball models\b|\bensemble\b|independent approaches?.*models?|models?.*independent approaches?/i);
  const independentComparison = has(t, /\bindependently\b/i) && has(t, /\b(competing|approaches?|plans?|alternatives?|contradictions?)\b/i);
  const explicitReadOnly = has(t, /do not (?:modify|change|edit) (?:files?|anything|code|the workspace)|without (?:modifying|changing|editing) (?:files?|code|the workspace)|\bread[- ]only\b/i);
  const broadScope = has(t, /\b(end[- ]to[- ]end|multiple|across|entire|complete|deep|comprehensive|production|system[- ]wide|everything|all files?|as much as possible)\b/i);
  const performance = has(t, /\b(performance|faster|slow\w*|latency|bottleneck|optimi[sz]\w*)\b/i);
  if (performance) { flags.code = true; flags.debug = true; }
  if (has(t, /\bfix\w*\b/i)) flags.debug = true;
  if (!Object.values(flags).some(Boolean)) flags.writing = true;

  const mutationVerb = has(t, /\b(implement|fix\w*|edit\w*|create\w*|remove\w*|delete\w*|migrat\w*|refactor\w*|build|deploy\w*|update\w*|upgrade\w*|patch\w*|rename\w*|correct|resolve)\b/i);
  const mutation = flags.code && mutationVerb && !explicitReadOnly;
  const substantiveCount = ['code','debug','review','architecture','research','security'].filter(k => flags[k]).length;
  let complexity = 1;
  if (task.length > 350) complexity++;
  if (task.length > 1000) complexity++;
  if (broadScope) {
    complexity += 1;
    if (has(t, /\b(everything|entire|system[- ]wide|comprehensive)\b/i)) complexity = Math.max(complexity, 4);
  }
  if (substantiveCount >= 3) complexity++;
  if (has(t, /best practices?.*(repo|repository)|compar\w*.*(repo|repository)|(repo|repository).*compar\w*/i)) complexity = Math.max(complexity, 2);
  if (flags.debug && has(t, /\b(intermittent|root cause|regression\w*)\b/i)) complexity = Math.max(complexity, 2);
  complexity = Math.min(5, complexity);

  const risk = flags.security || has(t, /\b(high[- ]risk|production|database|data loss|payment|billing|permission\w*|deploy\w*|migration\w*)\b/i) ? 'high' : mutation ? 'medium' : 'low';
  let tier = complexity >= 4 || risk === 'high' ? 'strong' : mutation ? 'balanced' : complexity <= 1 ? 'fast' : 'balanced';
  if (!mutation && (flags.debug || flags.review || flags.architecture) && tier === 'fast') tier = 'balanced';
  return { flags, mutation, complexity, risk, tier, signals: { explicitEnsemble, independentComparison, explicitReadOnly, broadScope, performance } };
}

function scoreProvider(name, profile) {
  const active = Object.entries(profile.flags).filter(([, on]) => on).map(([k]) => k);
  const base = active.reduce((sum, k) => sum + CAPS[name][k], 0) / Math.max(1, active.length);
  let bonus = 0;
  if (profile.mutation && name === 'codex') bonus += 20;
  if (profile.flags.research && name === 'grok') bonus += 8;
  if ((profile.flags.review || profile.flags.architecture) && name === 'claude') bonus += 8;
  return Math.round((base + bonus) * 10) / 10;
}
function chooseModel(provider, tier, state) {
  const key = `LLM_ORCH_${provider.toUpperCase()}_${tier.toUpperCase()}_MODEL`;
  if (process.env[key]) return { id: process.env[key], source: 'env' };
  if (provider === 'claude') return { id: tier === 'fast' ? 'haiku' : tier === 'strong' ? 'opus' : 'sonnet', source: 'alias' };
  if (provider === 'grok') return { id: state?.model || null, source: state?.model ? 'discovered-default' : 'inherit' };
  if (provider === 'codex' && tier === 'strong') return { id: 'gpt-6-astra', source: 'strong-default' };
  return { id: state?.model || null, source: state?.model ? 'configured-default' : 'inherit' };
}

function planTask(task, states = probeProviders(), overrides = {}) {
  const profile = classify(task);
  const circuitStates = states.map(s => ({
    ...s,
    circuit: overrides.ignoreHealth ? { state: 'CLOSED', eligible: true, reason: null, retryAt: null } : previewCircuit(s.name),
  }));
  const ready = circuitStates.filter(s => s.ready && s.circuit.eligible);
  const circuitBlocked = circuitStates.filter(s => s.ready && !s.circuit.eligible).map(s => ({ name: s.name, ...s.circuit }));
  if (!ready.length) {
    const reason = circuitBlocked.length ? 'All authenticated providers are temporarily circuit-open.' : 'No authenticated provider is available.';
    return { task, profile, ready: [], ranking: [], strategy: 'blocked', reason, circuitBlocked };
  }
  let ranking = ready.map(s => ({ ...s, score: scoreProvider(s.name, profile) })).sort((a, b) => b.score - a.score || PROVIDERS.indexOf(a.name) - PROVIDERS.indexOf(b.name));
  if (overrides.provider) {
    const i = ranking.findIndex(x => x.name === overrides.provider);
    if (i >= 0) ranking = [ranking[i], ...ranking.filter((_, j) => j !== i)];
  }
  let strategy = 'single';
  const analyticCount = ['review','architecture','research'].filter(k => profile.flags[k]).length;
  const explicitEnsemble = profile.signals?.explicitEnsemble || profile.signals?.independentComparison;
  if (ranking.length > 1 && !profile.mutation && explicitEnsemble) strategy = 'ensemble';
  else if (ranking.length > 1 && profile.mutation && (profile.flags.review || profile.complexity >= 3 || Object.values(profile.flags).filter(Boolean).length >= 3)) strategy = 'reviewed';
  else if (ranking.length > 1 && !profile.mutation && analyticCount >= 3 && (profile.risk === 'high' || profile.complexity >= 2)) strategy = 'ensemble';
  else if (ranking.length > 1 && !profile.mutation && analyticCount >= 2 && profile.complexity >= 3) strategy = 'ensemble';
  if (overrides.strategy && ['single', 'reviewed', 'ensemble'].includes(overrides.strategy)) strategy = overrides.strategy;
  const primary = ranking[0];
  const models = Object.fromEntries(ranking.map(s => [s.name, chooseModel(s.name, profile.tier, s)]));
  return {
    task, profile, ready: ready.map(s => s.name),
    ranking: ranking.map(({ name, score, reason, circuit }) => ({ name, score, reason, circuit: circuit?.state || 'CLOSED' })),
    primary: primary.name, strategy, models, circuitBlocked,
  };
}

function reasoningEffort(tier) {
  return tier === 'strong' ? 'high' : tier === 'fast' ? 'low' : 'medium';
}
function rolePrompt(task, role, profile, extra = '') {
  const common = `You are one worker in a local multi-model orchestration system.\nOriginal task:\n${task}\n\n`;
  if (role === 'execute') return common + `Execute the task in the current workspace. Inspect before changing anything, make only task-relevant changes, run meaningful verification, and report what changed plus evidence. Do not ask for routine confirmations. End the final response with ORCH_DONE: <one-line summary> only after the requested verification has actually passed.\n${extra}`;
  if (role === 'review') return common + `Review the current workspace and the executor report independently. Do not modify files. Check correctness, regressions, missing verification, scope, and risk. End with exactly one line: VERDICT: PASS or VERDICT: FIX.\n${extra}`;
  if (role === 'synthesize') return common + `Synthesize the independent analyses below. Resolve disagreements using evidence; do not average opinions. Return one actionable answer in the user's language.\n${extra}`;
  return common + `Analyze independently and produce evidence-backed recommendations. Do not modify files.\n${extra}`;
}

function invoke(provider, prompt, { cwd, mutation, model, tier, research }) {
  const temp = mkdtempSync(join(tmpdir(), 'llmo-'));
  const promptFile = join(temp, 'prompt.md');
  const outFile = join(temp, 'last.txt');
  writeFileSync(promptFile, prompt);
  let args = [];
  if (provider === 'codex') {
    args.push('--ask-for-approval', 'never');
    if (research) args.push('--search');
    args.push('exec', '--ephemeral', '--skip-git-repo-check', '-C', cwd, '--sandbox', mutation ? 'workspace-write' : 'read-only');
    args.push('-c', `model_reasoning_effort="${reasoningEffort(tier)}"`);
    if (model) args.push('--model', model);
    args.push('--output-last-message', outFile, '-');
  } else if (provider === 'claude') {
    args = ['-p', '--output-format', 'text', '--permission-mode', mutation ? 'auto' : 'plan', '--max-turns', '30'];
    if (model) args.push('--model', model);
  } else {
    args = ['--cwd', cwd, '--sandbox', 'workspace', '--output-format', 'plain', '--max-turns', '30'];
    if (mutation) args.push('--always-approve');
    else {
      args.push('--permission-mode', 'dontAsk');
      args.push('--tools', research ? 'read_file,grep,list_dir,web_search,web_fetch' : 'read_file,grep,list_dir');
    }
    args.push('--prompt-file', promptFile);
    if (model) args.push('--model', model);
  }
  const executable = commandPath(provider) || provider;
  const result = run(executable, args, { cwd, input: provider === 'grok' ? undefined : prompt, timeout: Number(process.env.LLM_ORCH_TIMEOUT_MS || 1800000) });
  let text = '';
  if (provider === 'codex' && existsSync(outFile)) text = readFileSync(outFile, 'utf8').trim();
  if (!text) text = (result.stdout || '').trim();
  const stderr = (result.stderr || '').trim();
  const ok = result.status === 0 && Boolean(text) && (!mutation || /ORCH_DONE:/i.test(text));
  const failure = stderr || text || result.error?.message || (result.signal ? `signal ${result.signal}` : `exit ${result.status}`);
  rmSync(temp, { recursive: true, force: true });
  return { ok, provider, model: model || null, output: text, error: ok ? null : failure, status: result.status, signal: result.signal || null };
}

function invokeSoft(provider, prompt, opts) {
  const first = invoke(provider, prompt, opts);
  if (first.ok || !opts.model) return first;
  const modelError = /(?:unknown|invalid|unsupported|not found|does not exist|not available|unavailable).*model|model.*(?:unknown|invalid|unsupported|not found|does not exist|not available|unavailable)/i.test(first.error || '');
  if (!modelError) return first;
  const second = invoke(provider, prompt, { ...opts, model: null });
  return { ...second, modelFallbackFrom: opts.model, initialModelError: first.error };
}

function executeWithFallback(plan, prompt, role, mutation, exclude = []) {
  const states = probeProviders();
  const byName = Object.fromEntries(states.map(s => [s.name, s]));
  const ordered = plan.ranking.map(r => r.name).filter(n => !exclude.includes(n));
  const attempts = [];
  for (const provider of ordered) {
    const gate = beginDispatch(provider);
    if (!gate.allowed) {
      attempts.push({ role, provider, ok: false, skipped: true, circuit: gate.state, error: `circuit-${String(gate.state).toLowerCase()}` });
      continue;
    }
    const model = plan.models[provider]?.id || chooseModel(provider, plan.profile.tier, byName[provider]).id;
    const res = invokeSoft(provider, prompt, {
      cwd: plan.cwd, mutation, model, tier: plan.profile.tier, research: plan.profile.flags.research,
    });
    const health = res.ok ? (recordSuccess(provider), null) : recordFailure(provider, res.error, { status: res.status, signal: res.signal });
    attempts.push({ role, provider, ok: res.ok, model: res.model, error: res.error, modelFallbackFrom: res.modelFallbackFrom, circuitOpened: Boolean(health?.opened), healthReason: health?.reason || null });
    if (res.ok) return { ...res, attempts };
  }
  return { ok: false, attempts, error: 'All eligible providers failed.' };
}
const clip = (s, n = 24000) => (s || '').length > n ? `${s.slice(0, n)}\n...[truncated]` : (s || '');

function executePlan(plan) {
  const task = plan.task;
  if (plan.strategy === 'single') {
    const role = plan.profile.mutation ? 'execute' : 'analyze';
    const res = executeWithFallback(plan, rolePrompt(task, role, plan.profile), role, plan.profile.mutation);
    if (!res.ok) return { ok: false, error: res.error, attempts: res.attempts };
    return { ok: true, final: res.output, primary: res.provider, attempts: res.attempts };
  }

  if (plan.strategy === 'reviewed') {
    const first = executeWithFallback(plan, rolePrompt(task, 'execute', plan.profile), 'execute', true);
    if (!first.ok) return { ok: false, error: first.error, attempts: first.attempts };
    const reviewExtra = `\nExecutor: ${first.provider}\nExecutor report:\n${clip(first.output)}\n`;
    let review = executeWithFallback(plan, rolePrompt(task, 'review', plan.profile, reviewExtra), 'review', false, [first.provider]);
    const reviewAttempts = [...(review.attempts || [])];
    if (!review.ok) {
      review = executeWithFallback(plan, rolePrompt(task, 'review', plan.profile, reviewExtra), 'review', false);
      reviewAttempts.push(...(review.attempts || []));
    }
    if (!review.ok) return { ok: true, final: first.output, primary: first.provider, warning: 'Execution succeeded but review failed.', attempts: [...first.attempts, ...reviewAttempts] };
    const reviewIndependent = review.provider !== first.provider;
    const reviewLabel = reviewIndependent ? 'Independent review' : 'Fallback self-review';
    if (!/VERDICT:\s*FIX/i.test(review.output)) {
      return { ok: true, final: `${first.output}\n\n--- ${reviewLabel} (${review.provider}) ---\n${review.output}`, primary: first.provider, reviewer: review.provider, reviewerIndependent: reviewIndependent, attempts: [...first.attempts, ...reviewAttempts] };
    }
    const repairExtra = `\nReview found issues:\n${clip(review.output)}\nFix the verified issues, rerun relevant checks, and report evidence.`;
    const repair = executeWithFallback(plan, rolePrompt(task, 'execute', plan.profile, repairExtra), 'execute', true);
    if (!repair.ok) return { ok: false, error: 'Review requested fixes, but repair failed.', attempts: [...first.attempts, ...reviewAttempts, ...(repair.attempts || [])] };
    const finalReviewExtra = `\nRepair executor: ${repair.provider}\nRepair report:\n${clip(repair.output)}\n`;
    let finalReview = executeWithFallback(plan, rolePrompt(task, 'review', plan.profile, finalReviewExtra), 'review', false, [repair.provider]);
    const finalReviewAttempts = [...(finalReview.attempts || [])];
    if (!finalReview.ok) {
      finalReview = executeWithFallback(plan, rolePrompt(task, 'review', plan.profile, finalReviewExtra), 'review', false);
      finalReviewAttempts.push(...(finalReview.attempts || []));
    }
    const finalIndependent = finalReview.ok && finalReview.provider !== repair.provider;
    const finalLabel = finalIndependent ? 'Final independent review' : 'Final fallback self-review';
    const finalText = finalReview.ok
      ? `${repair.output}\n\n--- ${finalLabel} (${finalReview.provider}) ---\n${finalReview.output}`
      : `${repair.output}\n\n[warning] Final review could not run.`;
    return { ok: true, final: finalText, primary: repair.provider, reviewer: finalReview.provider || review.provider, reviewerIndependent: Boolean(finalIndependent), attempts: [...first.attempts, ...reviewAttempts, ...repair.attempts, ...finalReviewAttempts] };
  }

  const states = Object.fromEntries(probeProviders().map(s => [s.name, s]));
  const members = plan.ranking.slice(0, Math.min(3, plan.ranking.length));
  const outputs = [];
  const ensembleAttempts = [];
  for (const member of members) {
    const gate = beginDispatch(member.name);
    if (!gate.allowed) {
      ensembleAttempts.push({ role: 'analyze', provider: member.name, ok: false, skipped: true, circuit: gate.state, error: `circuit-${String(gate.state).toLowerCase()}` });
      continue;
    }
    const model = plan.models[member.name]?.id || chooseModel(member.name, plan.profile.tier, states[member.name]).id;
    const res = invokeSoft(member.name, rolePrompt(task, 'analyze', plan.profile), {
      cwd: plan.cwd, mutation: false, model, tier: plan.profile.tier, research: plan.profile.flags.research,
    });
    const health = res.ok ? (recordSuccess(member.name), null) : recordFailure(member.name, res.error, { status: res.status, signal: res.signal });
    ensembleAttempts.push({ role: 'analyze', provider: member.name, ok: res.ok, model: res.model, error: res.error, modelFallbackFrom: res.modelFallbackFrom, circuitOpened: Boolean(health?.opened), healthReason: health?.reason || null });
    if (res.ok) outputs.push({ provider: member.name, output: res.output });
  }
  if (!outputs.length) return { ok: false, error: 'Every ensemble member failed.', attempts: ensembleAttempts };
  if (outputs.length === 1) return { ok: true, final: outputs[0].output, primary: outputs[0].provider, warning: 'Ensemble degraded to one provider.', attempts: ensembleAttempts };
  const evidence = outputs.map(o => `## ${o.provider}\n${clip(o.output, 18000)}`).join('\n\n');
  const synth = executeWithFallback(plan, rolePrompt(task, 'synthesize', plan.profile, `\nIndependent outputs:\n${evidence}`), 'synthesize', false);
  if (!synth.ok) return { ok: true, final: evidence, warning: 'Synthesis failed; returning independent outputs.', attempts: [...ensembleAttempts, ...(synth.attempts || [])] };
  return { ok: true, final: synth.output, primary: synth.provider, ensemble: outputs.map(o => o.provider), attempts: [...ensembleAttempts, ...(synth.attempts || [])] };
}
function loadTask(args) {
  if (args['task-file']) return readFileSync(resolve(args['task-file']), 'utf8').trim();
  if (args.task) return String(args.task).trim();
  if (args._.length > 1) return args._.slice(1).join(' ').trim();
  return '';
}

function printStatus(states) {
  console.log('provider\tinstalled\tauth_ready\tcircuit\tdispatch_ready\tmodel\treason');
  for (const s of states) {
    const circuit = previewCircuit(s.name);
    console.log(`${s.name}\t${s.installed}\t${s.ready}\t${circuit.state}\t${Boolean(s.ready && circuit.eligible)}\t${s.model || '-'}\t${s.reason}`);
  }
}

function printHealth() {
  const snapshot = healthSnapshot();
  console.log(`health_file: ${snapshot.file}`);
  console.log('provider\tcircuit\teligible\treason\tretry_at');
  for (const [provider, h] of Object.entries(snapshot.providers)) {
    console.log(`${provider}\t${h.state}\t${h.eligible}\t${h.reason || '-'}\t${h.retryAt ? new Date(h.retryAt).toISOString() : '-'}`);
  }
}

function printRoute(plan) {
  console.log(`strategy: ${plan.strategy}`);
  if (plan.primary) console.log(`primary: ${plan.primary}`);
  console.log(`tier: ${plan.profile.tier} | complexity: ${plan.profile.complexity}/5 | risk: ${plan.profile.risk} | mutation: ${plan.profile.mutation}`);
  console.log(`ready: ${plan.ready.join(', ') || 'none'}`);
  if (plan.ranking.length) console.log(`ranking: ${plan.ranking.map(r => `${r.name}(${r.score})`).join(' > ')}`);
  if (plan.models) console.log(`models: ${Object.entries(plan.models).map(([p, m]) => `${p}=${m.id || 'inherit'}[${m.source}]`).join(', ')}`);
  if (plan.circuitBlocked?.length) console.log(`circuit-blocked: ${plan.circuitBlocked.map(x => `${x.name}[${x.state}:${x.reason || 'unknown'}]`).join(', ')}`);
  if (plan.reason) console.log(`reason: ${plan.reason}`);
}

function selfTest() {
  const all = PROVIDERS.map(name => ({ name, installed: true, ready: true, reason: 'test', model: name === 'grok' ? 'grok-current' : null }));
  const code = planTask('Implement and test a repository bug fix across multiple files.', all, { ignoreHealth: true });
  assert.equal(code.primary, 'codex');
  const research = planTask('Deep comprehensive research on the latest market evidence and current sources.', all, { ignoreHealth: true });
  assert.equal(research.primary, 'grok');
  const architecture = planTask('Design a complete system architecture, migration roadmap, risks, and review criteria.', all, { ignoreHealth: true });
  assert.equal(architecture.primary, 'claude');
  const codexOnly = [{ name: 'codex', installed: true, ready: true, reason: 'test' }, { name: 'claude', installed: false, ready: false }, { name: 'grok', installed: false, ready: false }];
  const degraded = planTask('Deep architecture review and current research.', codexOnly, { ignoreHealth: true });
  assert.equal(degraded.primary, 'codex');
  assert.equal(degraded.strategy, 'single');
  const none = PROVIDERS.map(name => ({ name, installed: false, ready: false, reason: 'test-unavailable' }));
  const blocked = planTask('Implement a fix.', none, { ignoreHealth: true });
  assert.equal(blocked.strategy, 'blocked');
  assert.equal(blocked.ranking.length, 0);
  console.log('PASS: routing self-test');
}

const args = parseArgs(process.argv.slice(2));
const command = args._[0] || 'status';

if (command === 'self-test') {
  selfTest();
} else if (command === 'health') {
  const sub = args._[1] || 'status';
  const provider = args._[2] || null;
  if (sub === 'reset') {
    if (provider && !PROVIDERS.includes(provider)) { console.error(`Unknown provider: ${provider}`); process.exit(2); }
    resetHealth(provider);
    if (args.json) console.log(JSON.stringify(healthSnapshot(), null, 2));
    else { console.log(provider ? `reset: ${provider}` : 'reset: all'); printHealth(); }
  } else if (sub === 'status') {
    if (args.json) console.log(JSON.stringify(healthSnapshot(), null, 2));
    else printHealth();
  } else { console.error('Usage: llmo health [status] | health reset [codex|claude|grok]'); process.exit(2); }
} else if (command === 'status') {
  const states = probeProviders();
  if (args.json) {
    const decorated = states.map(s => {
      const circuit = previewCircuit(s.name);
      return { ...s, circuit, dispatchReady: Boolean(s.ready && circuit.eligible) };
    });
    console.log(JSON.stringify(decorated, null, 2));
  } else printStatus(states);
} else if (command === 'route' || command === 'run') {
  const task = loadTask(args);
  if (!task) { console.error('Missing task. Use --task "..." or --task-file path.'); process.exit(2); }
  const plan = planTask(task, probeProviders(), { provider: args.provider, strategy: args.strategy });
  plan.cwd = resolve(args.cwd || process.cwd());
  if (args.json && command === 'route') console.log(JSON.stringify(plan, null, 2));
  else if (command === 'route') printRoute(plan);
  else {
    if (plan.strategy === 'blocked') {
      if (args.json) console.log(JSON.stringify({ plan, result: { ok: false, error: plan.reason } }, null, 2));
      else printRoute(plan);
      process.exit(3);
    }
    if (!args.json) { printRoute(plan); console.log('\n--- execution ---'); }
    const result = executePlan(plan);
    if (args.json) console.log(JSON.stringify({ plan, result }, null, 2));
    else if (result.ok) console.log(`\n${result.final}`);
    else { console.error(result.error || 'Execution failed.'); console.error(JSON.stringify(result.attempts || [], null, 2)); process.exit(4); }
  }
} else {
  console.error('Usage: llmo status | health [status|reset [provider]] | route --task ... | run --task ... [--cwd path] [--provider codex|claude|grok] [--strategy single|reviewed|ensemble] [--json] | self-test');
  process.exit(2);
}
