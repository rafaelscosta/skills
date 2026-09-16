#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { mkdirSync, writeFileSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { routingCases } from '../evals/stress-cases.mjs';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '..');
const router = resolve(here, 'router.mjs');
const outputDir = resolve(root, 'outputs');
mkdirSync(outputDir, { recursive: true });

function route(task, ready = 'codex,claude,grok') {
  const r = spawnSync(process.execPath, [router, 'route', '--task', task, '--json'], {
    encoding: 'utf8',
    env: { ...process.env, LLM_ORCH_MOCK_READY: ready },
    maxBuffer: 10 * 1024 * 1024,
  });
  if (r.status !== 0) throw new Error(r.stderr || `route exited ${r.status}`);
  return JSON.parse(r.stdout);
}

function checkOne(plan, expect) {
  const failures = [];
  for (const flag of expect.flags || []) if (!plan.profile.flags[flag]) failures.push(`missing flag:${flag}`);
  if ('mutation' in expect && plan.profile.mutation !== expect.mutation) failures.push(`mutation=${plan.profile.mutation} expected=${expect.mutation}`);
  if (expect.tier && plan.profile.tier !== expect.tier) failures.push(`tier=${plan.profile.tier} expected=${expect.tier}`);
  if (expect.tierOneOf && !expect.tierOneOf.includes(plan.profile.tier)) failures.push(`tier=${plan.profile.tier} expected one of ${expect.tierOneOf.join(',')}`);
  if (expect.strategy && plan.strategy !== expect.strategy) failures.push(`strategy=${plan.strategy} expected=${expect.strategy}`);
  if (expect.strategyOneOf && !expect.strategyOneOf.includes(plan.strategy)) failures.push(`strategy=${plan.strategy} expected one of ${expect.strategyOneOf.join(',')}`);
  if (expect.primary && plan.primary !== expect.primary) failures.push(`primary=${plan.primary} expected=${expect.primary}`);
  return failures;
}
const results = [];
for (const c of routingCases) {
  const plan = route(c.task);
  const failures = checkOne(plan, c.expect);
  results.push({ id: c.id, task: c.task, pass: failures.length === 0, failures, plan });
}

const invarianceGroups = [
  ['Fix the failing authentication test and verify the fix.', 'The auth test is red. Find out why, correct the actual problem, and prove it works.', 'Investigate and resolve the authentication regression. Keep the patch minimal and validate it.'],
  ['Research the latest official guidance for this dependency.', 'Check current official docs for this package and summarize what changed.', 'Use up-to-date primary sources to inspect this dependency guidance.'],
  ['Review the architecture for migration risks.', 'Audit this system design and identify migration risk.', 'Assess architecture and migration hazards without changing files.'],
];
const invariance = invarianceGroups.map((tasks, i) => {
  const plans = tasks.map(t => route(t));
  const signatures = plans.map(p => `${p.profile.mutation}|${p.profile.tier}|${p.strategy}|${p.primary}`);
  return { id: `I0${i + 1}`, pass: new Set(signatures).size === 1, signatures, tasks };
});

const summary = {
  routing: { total: results.length, passed: results.filter(x => x.pass).length, failed: results.filter(x => !x.pass).length },
  invariance: { total: invariance.length, passed: invariance.filter(x => x.pass).length, failed: invariance.filter(x => !x.pass).length },
};
const stamp = new Date().toISOString().replace(/[:.]/g, '-');
const jsonPath = resolve(outputDir, `stress-routing-${stamp}.json`);
writeFileSync(jsonPath, JSON.stringify({ summary, results, invariance }, null, 2));
const lines = [
  '# LLM Orchestrator Routing Stress Test', '',
  `Routing: **${summary.routing.passed}/${summary.routing.total} passed**`,
  `Paraphrase invariance: **${summary.invariance.passed}/${summary.invariance.total} passed**`, '',
  '## Routing cases', '',
  '| ID | Verdict | Primary | Tier | Strategy | Mutation | Gaps |',
  '|---|---|---|---|---|---|---|',
];
for (const r of results) lines.push(`| ${r.id} | ${r.pass ? 'PASS' : 'FAIL'} | ${r.plan.primary || '-'} | ${r.plan.profile.tier} | ${r.plan.strategy} | ${r.plan.profile.mutation} | ${(r.failures.join('; ') || '-').replaceAll('|','/')} |`);
lines.push('', '## Paraphrase invariance', '', '| ID | Verdict | Signatures |', '|---|---|---|');
for (const x of invariance) lines.push(`| ${x.id} | ${x.pass ? 'PASS' : 'FAIL'} | ${x.signatures.join(' / ')} |`);
lines.push('', '## Failed case details', '');
for (const r of results.filter(x => !x.pass)) {
  lines.push(`### ${r.id}`, '', r.task, '', `- ${r.failures.join('\n- ')}`, '');
}
const mdPath = resolve(outputDir, `stress-routing-${stamp}.md`);
writeFileSync(mdPath, lines.join('\n'));

console.log(`routing ${summary.routing.passed}/${summary.routing.total} | invariance ${summary.invariance.passed}/${summary.invariance.total}`);
for (const r of results.filter(x => !x.pass)) console.log(`${r.id} FAIL: ${r.failures.join('; ')}`);
for (const x of invariance.filter(x => !x.pass)) console.log(`${x.id} FAIL: ${x.signatures.join(' / ')}`);
console.log(`JSON: ${jsonPath}`);
console.log(`Report: ${mdPath}`);
process.exit(summary.routing.failed || summary.invariance.failed ? 1 : 0);
