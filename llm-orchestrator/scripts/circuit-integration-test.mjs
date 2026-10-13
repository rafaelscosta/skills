#!/usr/bin/env node
import assert from 'node:assert/strict';
import { mkdtempSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { spawnSync } from 'node:child_process';

const root = resolve(new URL('..', import.meta.url).pathname);
const router = join(root, 'scripts', 'router.mjs');
const temp = mkdtempSync(join(tmpdir(), 'llmo-circuit-integration-'));
const healthFile = join(temp, 'health.json');
process.env.LLM_ORCH_HEALTH_FILE = healthFile;
process.env.LLM_ORCH_TEST_HEALTH = '1';
process.env.LLM_ORCH_MOCK_READY = 'codex,grok';
process.env.LLM_ORCH_COOLDOWN_QUOTA_MS = '1000';

const health = await import('./health.mjs');
health.recordFailure('grok', 'usage limit quota exhausted', {}, 1000);

function runRoute(now, command, extra = []) {
  const env = { ...process.env, LLM_ORCH_NOW_MS: String(now) };
  const r = spawnSync(process.execPath, [router, command, ...extra], { encoding: 'utf8', env });
  assert.equal(r.status, 0, r.stderr || r.stdout);
  return JSON.parse(r.stdout);
}

let passed = 0;
const check = (name, fn) => {
  fn(); passed++; console.log(`PASS ${name}`);
};
check('open circuit removes provider from route', () => {
  const plan = runRoute(1500, 'route', ['--task', 'Research the latest official documentation.', '--json']);
  assert.equal(plan.primary, 'codex');
  assert.equal(plan.circuitBlocked[0].name, 'grok');
  assert.equal(plan.circuitBlocked[0].state, 'OPEN');
});

check('status exposes dispatch readiness', () => {
  const states = runRoute(1500, 'status', ['--json']);
  const grok = states.find(x => x.name === 'grok');
  assert.equal(grok.ready, true);
  assert.equal(grok.dispatchReady, false);
  assert.equal(grok.circuit.state, 'OPEN');
});

check('expired cooldown returns provider half-open', () => {
  const plan = runRoute(2001, 'route', ['--task', 'Research the latest official documentation.', '--json']);
  assert.equal(plan.primary, 'grok');
  assert.equal(plan.ranking[0].circuit, 'HALF_OPEN');
});

check('manual reset restores closed circuit', () => {
  const snapshot = runRoute(2001, 'health', ['reset', 'grok', '--json']);
  assert.equal(snapshot.providers.grok.state, 'CLOSED');
});

rmSync(temp, { recursive: true, force: true });
console.log(`circuit-integration ${passed}/4`);