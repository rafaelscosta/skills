#!/usr/bin/env node
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';

const temp = mkdtempSync(join(tmpdir(), 'llmo-health-test-'));
process.env.LLM_ORCH_HEALTH_FILE = join(temp, 'health.json');
process.env.LLM_ORCH_COOLDOWN_QUOTA_MS = '1000';
process.env.LLM_ORCH_COOLDOWN_RATE_LIMIT_MS = '1000';
process.env.LLM_ORCH_COOLDOWN_AUTH_MS = '1000';
process.env.LLM_ORCH_COOLDOWN_TIMEOUT_MS = '1000';
process.env.LLM_ORCH_PROBE_LEASE_MS = '500';

const health = await import('./health.mjs');
let passed = 0;
const check = (name, fn) => {
  try { fn(); passed++; console.log(`PASS ${name}`); }
  catch (error) { console.error(`FAIL ${name}: ${error.message}`); process.exitCode = 1; }
};

check('fresh cache is closed', () => {
  assert.deepEqual(health.previewCircuit('grok', 1000), { state: 'CLOSED', eligible: true, reason: null, retryAt: null });
});

check('task/model errors do not open circuit', () => {
  assert.equal(health.recordFailure('grok', 'Unknown model fake-model', {}, 1000).opened, false);
  assert.equal(health.previewCircuit('grok', 1000).state, 'CLOSED');
});
check('quota opens circuit', () => {
  const opened = health.recordFailure('grok', 'usage limit reached: quota exhausted', {}, 2000);
  assert.equal(opened.opened, true);
  assert.equal(opened.reason, 'quota');
  const view = health.previewCircuit('grok', 2500);
  assert.equal(view.state, 'OPEN');
  assert.equal(view.eligible, false);
});

check('cooldown expires into half-open', () => {
  const view = health.previewCircuit('grok', 3001);
  assert.equal(view.state, 'HALF_OPEN');
  assert.equal(view.eligible, true);
});

check('half-open allows one probe lease', () => {
  const first = health.beginDispatch('grok', 3001);
  const second = health.beginDispatch('grok', 3002);
  assert.equal(first.allowed, true);
  assert.equal(first.state, 'HALF_OPEN');
  assert.equal(second.allowed, false);
  assert.equal(second.state, 'PROBING');
});

check('successful probe closes circuit', () => {
  health.recordSuccess('grok', 3100);
  assert.equal(health.previewCircuit('grok', 3100).state, 'CLOSED');
});
check('rate limit opens short circuit', () => {
  health.recordFailure('codex', 'HTTP 429 too many requests', {}, 4000);
  assert.equal(health.previewCircuit('codex', 4500).state, 'OPEN');
});

check('auth failure opens circuit', () => {
  health.recordFailure('claude', '401 unauthorized - login required', {}, 5000);
  assert.equal(health.previewCircuit('claude', 5500).state, 'OPEN');
});

check('timeout opens circuit without storing raw error', () => {
  health.recordFailure('grok', 'spawnSync grok ETIMEDOUT secret-value', { signal: 'SIGTERM' }, 6000);
  const raw = readFileSync(process.env.LLM_ORCH_HEALTH_FILE, 'utf8');
  assert.equal(raw.includes('secret-value'), false);
  assert.equal(health.previewCircuit('grok', 6500).state, 'OPEN');
});

check('provider service outage opens short circuit', () => {
  process.env.LLM_ORCH_COOLDOWN_SERVICE_MS = '1000';
  health.recordFailure('codex', '503 service unavailable', {}, 6200);
  assert.equal(health.previewCircuit('codex', 6500).state, 'OPEN');
  health.resetHealth('codex');
});

check('provider reset is surgical', () => {
  health.resetHealth('grok');
  assert.equal(health.previewCircuit('grok', 6500).state, 'CLOSED');
  assert.equal(health.previewCircuit('claude', 5500).state, 'OPEN');
});
check('corrupt cache fails open safely', () => {
  writeFileSync(process.env.LLM_ORCH_HEALTH_FILE, '{not-json');
  assert.equal(health.previewCircuit('codex', 7000).state, 'CLOSED');
});

check('reset all restores clean state', () => {
  health.recordFailure('codex', 'HTTP 429 rate limit', {}, 8000);
  health.recordFailure('grok', 'quota exhausted', {}, 8000);
  health.resetHealth();
  assert.equal(health.previewCircuit('codex', 8000).state, 'CLOSED');
  assert.equal(health.previewCircuit('grok', 8000).state, 'CLOSED');
});

rmSync(temp, { recursive: true, force: true });
console.log(`health ${passed}/13`);
if (process.exitCode) process.exit(process.exitCode);