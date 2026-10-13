#!/usr/bin/env node
import { basename } from 'node:path';
import { readFileSync, writeFileSync } from 'node:fs';

const provider = process.env.STUB_PROVIDER || basename(process.argv[1]);
const args = process.argv.slice(2);
let prompt = '';
const pf = args.indexOf('--prompt-file');
if (pf >= 0 && args[pf + 1]) prompt = readFileSync(args[pf + 1], 'utf8');
if (!prompt) {
  try { prompt = readFileSync(0, 'utf8'); } catch {}
}
const role = /Review the current workspace/i.test(prompt) ? 'review'
  : /Synthesize the independent analyses/i.test(prompt) ? 'synthesize'
  : /Execute the task in the current workspace/i.test(prompt) ? 'execute'
  : 'analyze';
const key = `STUB_BEHAVIOR_${provider.toUpperCase()}_${role.toUpperCase()}`;
const behavior = process.env[key] || process.env[`STUB_BEHAVIOR_${provider.toUpperCase()}`] || 'ok';

if (behavior === 'timeout') await new Promise(r => setTimeout(r, 3000));
if (behavior === 'fail') { console.error(`${provider} forced failure`); process.exit(9); }
if (behavior === 'quota') { console.error('usage limit quota exhausted'); process.exit(10); }
if (behavior === 'model-error-on-pin' && args.includes('bad-model')) { console.error('unknown model bad-model'); process.exit(11); }
let text = role === 'review' ? 'VERDICT: PASS'
  : role === 'synthesize' ? `SYNTHESIS_OK ${provider}`
  : role === 'execute' ? `EXECUTION_OK ${provider}\nORCH_DONE: stub execution passed`
  : `ANALYSIS_OK ${provider}`;
if (behavior === 'no-marker' && role === 'execute') text = `EXECUTION_INCOMPLETE ${provider}`;

if (provider === 'codex') {
  const oi = args.indexOf('--output-last-message');
  if (oi >= 0 && args[oi + 1]) writeFileSync(args[oi + 1], text);
  else process.stdout.write(text);
} else {
  process.stdout.write(text);
}
