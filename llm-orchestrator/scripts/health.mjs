#!/usr/bin/env node
import { existsSync, mkdirSync, readFileSync, renameSync, writeFileSync } from 'node:fs';
import { homedir } from 'node:os';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

export const HEALTH_SCHEMA = 1;
const PROVIDERS = ['codex', 'claude', 'grok'];

const nowMs = () => Number(process.env.LLM_ORCH_NOW_MS || Date.now());
const disabled = () => process.env.LLM_ORCH_DISABLE_HEALTH === '1' ||
  (process.env.LLM_ORCH_MOCK_READY !== undefined && process.env.LLM_ORCH_TEST_HEALTH !== '1');

export function healthFilePath() {
  if (process.env.LLM_ORCH_HEALTH_FILE) return resolve(process.env.LLM_ORCH_HEALTH_FILE);
  const cacheRoot = process.env.XDG_CACHE_HOME || join(homedir(), '.cache');
  return join(cacheRoot, 'llm-orchestrator', 'health.json');
}

const blankState = () => ({ schema: HEALTH_SCHEMA, providers: {} });

export function readHealth() {
  if (disabled()) return blankState();
  const file = healthFilePath();
  try {
    if (!existsSync(file)) return blankState();
    const parsed = JSON.parse(readFileSync(file, 'utf8'));
    return parsed?.schema === HEALTH_SCHEMA && parsed?.providers ? parsed : blankState();
  } catch { return blankState(); }
}function writeHealth(state) {
  if (disabled()) return;
  const file = healthFilePath();
  mkdirSync(dirname(file), { recursive: true });
  const temp = `${file}.${process.pid}.tmp`;
  writeFileSync(temp, `${JSON.stringify(state, null, 2)}\n`);
  renameSync(temp, file);
}

function cooldownMs(reason) {
  const defaults = {
    quota: 60 * 60 * 1000,
    rate_limit: 5 * 60 * 1000,
    auth: 15 * 60 * 1000,
    timeout: 2 * 60 * 1000,
    service: 60 * 1000,
  };
  const key = `LLM_ORCH_COOLDOWN_${reason.toUpperCase()}_MS`;
  return Number(process.env[key] || defaults[reason] || 0);
}

export function classifyDispatchFailure(error = '', meta = {}) {
  const text = `${error || ''} ${meta.signal || ''}`.toLowerCase();
  if (/quota|usage limit|insufficient[_ -]?quota|credits? exhausted|billing limit/.test(text)) return 'quota';
  if (/rate.?limit|too many requests|\b429\b/.test(text)) return 'rate_limit';
  if (/not authenticated|authentication required|unauthorized|login required|\b401\b/.test(text)) return 'auth';
  if (/timed? ?out|timeout|etimedout|sigterm/.test(text)) return 'timeout';
  if (/service unavailable|temporarily unavailable|econnreset|econnrefused|\b50[0234]\b/.test(text)) return 'service';
  return null;
}

export function previewCircuit(provider, at = nowMs()) {
  if (disabled()) return { state: 'CLOSED', eligible: true, reason: null, retryAt: null };
  const entry = readHealth().providers[provider];
  if (!entry) return { state: 'CLOSED', eligible: true, reason: null, retryAt: null };
  if (entry.state === 'OPEN' && Number(entry.retryAt || 0) > at) {
    return { state: 'OPEN', eligible: false, reason: entry.reason, retryAt: entry.retryAt };
  }
  if (entry.state === 'HALF_OPEN' && Number(entry.probeUntil || 0) > at) {
    return { state: 'PROBING', eligible: false, reason: entry.reason, retryAt: entry.probeUntil };
  }
  if (entry.state === 'OPEN' || entry.state === 'HALF_OPEN') {
    return { state: 'HALF_OPEN', eligible: true, reason: entry.reason, retryAt: entry.retryAt || null };
  }
  return { state: 'CLOSED', eligible: true, reason: null, retryAt: null };
}export function beginDispatch(provider, at = nowMs()) {
  const view = previewCircuit(provider, at);
  if (!view.eligible) return { allowed: false, ...view };
  if (view.state !== 'HALF_OPEN' || disabled()) return { allowed: true, ...view };

  const state = readHealth();
  state.providers[provider] = {
    ...(state.providers[provider] || {}),
    state: 'HALF_OPEN',
    probeStartedAt: at,
    probeUntil: at + Number(process.env.LLM_ORCH_PROBE_LEASE_MS || 60_000),
  };
  writeHealth(state);
  return { allowed: true, state: 'HALF_OPEN', eligible: true, reason: view.reason, retryAt: view.retryAt };
}

export function recordSuccess(provider, at = nowMs()) {
  if (disabled()) return;
  const state = readHealth();
  if (!state.providers[provider]) return;
  delete state.providers[provider];
  writeHealth(state);
}

export function recordFailure(provider, error = '', meta = {}, at = nowMs()) {
  if (disabled()) return { opened: false, reason: null };
  const reason = classifyDispatchFailure(error, meta);
  if (!reason) return { opened: false, reason: null };
  const state = readHealth();
  const previous = state.providers[provider] || {};
  const failures = Number(previous.failures || 0) + 1;
  const base = cooldownMs(reason);
  const multiplier = reason === 'timeout' || reason === 'rate_limit' ? Math.min(4, 2 ** Math.max(0, failures - 1)) : 1;
  state.providers[provider] = {
    state: 'OPEN', reason, failures,
    openedAt: at,
    retryAt: at + (base * multiplier),
    lastStatus: meta.status ?? null,
    lastSignal: meta.signal ?? null,
  };
  writeHealth(state);
  return { opened: true, reason, retryAt: state.providers[provider].retryAt };
}export function resetHealth(provider = null) {
  if (disabled()) return;
  const state = readHealth();
  if (provider) delete state.providers[provider];
  else state.providers = {};
  writeHealth(state);
}

export function healthSnapshot(providers = PROVIDERS, at = nowMs()) {
  return {
    file: healthFilePath(),
    providers: Object.fromEntries(providers.map(provider => [provider, previewCircuit(provider, at)])),
  };
}

function cli() {
  const [command = 'status', provider] = process.argv.slice(2);
  if (command === 'reset') {
    if (provider && !PROVIDERS.includes(provider)) {
      console.error(`Unknown provider: ${provider}`);
      process.exit(2);
    }
    resetHealth(provider || null);
    console.log(provider ? `reset: ${provider}` : 'reset: all');
    return;
  }
  if (command !== 'status') {
    console.error('Usage: health.mjs status | reset [codex|claude|grok]');
    process.exit(2);
  }
  console.log(JSON.stringify(healthSnapshot(), null, 2));
}

if (process.argv[1] && resolve(process.argv[1]) === resolve(fileURLToPath(import.meta.url))) cli();