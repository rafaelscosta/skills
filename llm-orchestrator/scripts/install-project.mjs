#!/usr/bin/env node
import { chmodSync, cpSync, existsSync, mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { dirname, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const skillRoot = resolve(here, '..');
const target = resolve(process.argv[2] || process.cwd());
const name = 'llm-orchestrator';
const destinations = [
  join(target, '.agents', 'skills', name),
  join(target, '.claude', 'skills', name),
  join(target, '.grok', 'skills', name),
];

for (const dest of destinations) {
  mkdirSync(dirname(dest), { recursive: true });
  cpSync(skillRoot, dest, {
    recursive: true,
    force: true,
    filter: src => !src.includes('/outputs') && !src.endsWith('/.DS_Store') && !src.endsWith('example.mjs') && !src.endsWith('example-reference.md'),
  });
  console.log(`installed: ${dest}`);
}

const launcher = join(target, '.llmo');
const launcherBody = `#!/bin/sh
ROOT="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec node "$ROOT/.agents/skills/llm-orchestrator/scripts/router.mjs" "$@"
`;
if (!existsSync(launcher) || readFileSync(launcher, 'utf8').includes('llm-orchestrator/scripts/router.mjs')) {
  writeFileSync(launcher, launcherBody);
  chmodSync(launcher, 0o755);
  console.log(`installed: ${launcher}`);
} else {
  console.log(`warning: ${launcher} already exists and was left untouched`);
}

console.log(`\nReady in project: ${target}`);
console.log('The three harnesses now share the same project-local skill contract.');
