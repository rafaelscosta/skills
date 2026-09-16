#!/usr/bin/env node
import { spawnSync } from 'node:child_process';
import { chmodSync, mkdtempSync, mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { basename, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const root = resolve(here, '..');
const router = resolve(here, 'router.mjs');
const stub = resolve(root, 'evals', 'stub-provider.mjs');
const temp = mkdtempSync(resolve(tmpdir(), 'llmo-fault-'));
const bin = resolve(temp, 'bin');
const cwd = resolve(temp, 'workspace');
mkdirSync(bin); mkdirSync(cwd);

for (const provider of ['codex','claude','grok']) {
  const path = resolve(bin, provider);
  writeFileSync(path, `#!/bin/sh\nSTUB_PROVIDER=${provider} exec ${JSON.stringify(process.execPath)} ${JSON.stringify(stub)} "$@"\n`);
  chmodSync(path, 0o755);
}

function call(command, task, ready, extraEnv = {}) {
  const r = spawnSync(process.execPath, [router, command, '--task', task, '--cwd', cwd, '--json'], {
    encoding: 'utf8',
    env: { ...process.env, PATH: `${bin}:${process.env.PATH}`, LLM_ORCH_MOCK_READY: ready, ...extraEnv },
    timeout: 15000,
    maxBuffer: 10 * 1024 * 1024,
  });
  const marker = command === 'run' ? r.stdout.indexOf('{\n  "plan"') : r.stdout.indexOf('{');
  const payload = marker >= 0 ? JSON.parse(r.stdout.slice(marker)) : null;
  return { status: r.status, payload, stdout: r.stdout, stderr: r.stderr };
}

const tests = [];
const add = (id, fn) => tests.push({ id, fn });
const ok = (cond, msg) => { if (!cond) throw new Error(msg); };
add('F01 codex-only', () => { const x=call('route','Implement a small fix.','codex'); ok(x.payload.primary==='codex' && x.payload.strategy==='single','codex-only did not degrade to single'); });
add('F02 claude-only', () => { const x=call('route','Review this architecture.','claude'); ok(x.payload.primary==='claude' && x.payload.strategy==='single','claude-only failed'); });
add('F03 grok-only', () => { const x=call('route','Research the latest official docs.','grok'); ok(x.payload.primary==='grok' && x.payload.strategy==='single','grok-only failed'); });
add('F04 none-ready', () => { const x=call('route','Implement a fix.',''); ok(x.payload.strategy==='blocked','none-ready did not block'); });
add('F05 missing-claude reviewed', () => { const x=call('run','Fix the failing test and review the final diff.','codex,grok'); ok(x.payload.result.ok && x.payload.result.primary==='codex' && x.payload.result.reviewer==='grok' && x.payload.result.reviewerIndependent===true,'codex→grok reviewed path failed'); });
add('F06 grok-quota fallback', () => { const x=call('run','Research the latest official docs.','codex,grok',{STUB_BEHAVIOR_GROK:'quota'}); ok(x.payload.result.ok && x.payload.result.primary==='codex','quota did not fall back to codex'); ok(x.payload.result.attempts.some(a=>a.provider==='grok'&&!a.ok),'quota attempt missing'); });
add('F07 codex-runtime fallback', () => { const x=call('run','Rename this variable and run the test.','codex,grok',{STUB_BEHAVIOR_CODEX:'fail'}); ok(x.payload.result.ok && x.payload.result.primary==='grok','codex failure did not fall back to grok'); });
add('F08 codex-invalid-model soft retry', () => { const x=call('run','Rename this variable and run the test.','codex',{LLM_ORCH_CODEX_BALANCED_MODEL:'bad-model',STUB_BEHAVIOR_CODEX:'model-error-on-pin'}); ok(x.payload.result.ok && x.payload.result.primary==='codex','codex model retry failed'); ok(x.payload.result.attempts[0].modelFallbackFrom==='bad-model','codex modelFallbackFrom missing'); });
add('F09 claude-invalid-model soft retry', () => { const x=call('run','Review this implementation independently.','claude',{LLM_ORCH_CLAUDE_BALANCED_MODEL:'bad-model',STUB_BEHAVIOR_CLAUDE:'model-error-on-pin'}); ok(x.payload.result.ok && x.payload.result.primary==='claude','claude model retry failed'); ok(x.payload.result.attempts[0].modelFallbackFrom==='bad-model','claude modelFallbackFrom missing'); });
add('F10 exit-zero incomplete mutation', () => { const x=call('run','Rename this variable and run the test.','codex,grok',{STUB_BEHAVIOR_CODEX:'no-marker'}); ok(x.payload.result.ok && x.payload.result.primary==='grok','missing ORCH_DONE was accepted or fallback failed'); ok(x.payload.result.attempts.some(a=>a.provider==='codex'&&!a.ok),'incomplete codex attempt missing'); });
add('F11 reviewer failure self-review', () => { const x=call('run','Fix the failing test and review the final diff.','codex,grok',{STUB_BEHAVIOR_GROK_REVIEW:'fail'}); ok(x.payload.result.ok && x.payload.result.reviewer==='codex','self-review fallback missing'); ok(x.payload.result.reviewerIndependent===false,'self-review incorrectly marked independent'); });
add('F12 reviewed task with one provider', () => { const x=call('route','Fix the failing test and review the final diff.','codex'); ok(x.payload.strategy==='single','one-provider reviewed task did not degrade to single'); });
add('F13 ensemble degraded to one', () => { const x=call('run','Use every available model independently, compare the results, and return one answer.','codex,claude,grok',{STUB_BEHAVIOR_GROK:'fail',STUB_BEHAVIOR_CLAUDE:'fail'}); ok(x.payload.result.ok && /degraded to one provider/i.test(x.payload.result.warning||''),'ensemble did not report one-provider degradation'); ok(x.payload.result.attempts.length===3,'ensemble attempt ledger incomplete'); });
add('F14 ensemble all fail', () => { const x=call('run','Use every available model independently, compare the results, and return one answer.','codex,claude,grok',{STUB_BEHAVIOR_GROK:'fail',STUB_BEHAVIOR_CLAUDE:'fail',STUB_BEHAVIOR_CODEX:'fail'}); ok(!x.payload.result.ok && /Every ensemble member failed/i.test(x.payload.result.error||''),'all-fail ensemble not surfaced'); });
add('F15 primary timeout fallback', () => { const x=call('run','Rename this variable and run the test.','codex,grok',{STUB_BEHAVIOR_CODEX:'timeout',LLM_ORCH_TIMEOUT_MS:'1000'}); ok(x.payload.result.ok && x.payload.result.primary==='grok','timeout did not fall back to grok'); ok(x.payload.result.attempts.some(a=>a.provider==='codex'&&!a.ok),'timeout attempt missing'); });
const rows=[];
for (const t of tests) {
  try { t.fn(); rows.push({id:t.id,pass:true}); }
  catch (e) { rows.push({id:t.id,pass:false,error:e.message}); }
}
const passed=rows.filter(r=>r.pass).length;
const report=['# LLM Orchestrator Fault Injection','',`Passed: **${passed}/${rows.length}**`,'','| Case | Verdict | Detail |','|---|---|---|'];
for (const r of rows) report.push(`| ${r.id} | ${r.pass?'PASS':'FAIL'} | ${(r.error||'-').replaceAll('|','/')} |`);
const out=resolve(root,'outputs','fault-injection-latest.md');
writeFileSync(out,report.join('\n'));
console.log(`faults ${passed}/${rows.length}`);
for (const r of rows.filter(x=>!x.pass)) console.log(`${r.id} FAIL: ${r.error}`);
console.log(`Report: ${out}`);
rmSync(temp,{recursive:true,force:true});
process.exit(passed===rows.length?0:1);
