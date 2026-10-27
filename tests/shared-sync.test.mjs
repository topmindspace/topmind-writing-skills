import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

function fixture(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'writing-shared-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  fs.mkdirSync(path.join(root, 'scripts'));
  for (const name of ['sync_shared.js', 'discover_skills.js']) fs.copyFileSync(new URL(`../scripts/${name}`, import.meta.url), path.join(root, 'scripts', name));
  for (const id of ['alpha', 'beta']) { fs.mkdirSync(path.join(root, id)); fs.writeFileSync(path.join(root, id, 'SKILL.md'), '# fixture'); }
  fs.mkdirSync(path.join(root, 'shared/knowledge/cards'), { recursive: true });
  fs.writeFileSync(path.join(root, 'shared/manifest.json'), JSON.stringify({ files: { 'knowledge/': ['*'] } }));
  fs.writeFileSync(path.join(root, 'shared/knowledge/index.json'), '{}');
  fs.writeFileSync(path.join(root, 'shared/knowledge/cards/card.md'), '正文与例外');
  return { root, run: (...args) => spawnSync(process.execPath, ['scripts/sync_shared.js', ...args], { cwd: root, encoding: 'utf8' }) };
}

test('directory entries distribute new knowledge files to standalone skills and detect drift', t => {
  const { root, run } = fixture(t);
  assert.equal(run().status, 0);
  for (const id of ['alpha', 'beta']) assert.equal(fs.readFileSync(path.join(root, id, 'knowledge/cards/card.md'), 'utf8'), '正文与例外');
  assert.equal(run('--check').status, 0);
  fs.writeFileSync(path.join(root, 'shared/knowledge/cards/new.md'), '新增经验');
  assert.equal(run('--check').status, 1);
  assert.equal(run().status, 0);
  assert.equal(fs.readFileSync(path.join(root, 'beta/knowledge/cards/new.md'), 'utf8'), '新增经验');
  fs.writeFileSync(path.join(root, 'alpha/knowledge/cards/card.md'), 'drift');
  assert.equal(run('--check').status, 1);
});

test('shared directory symlinks are rejected without copying their target', t => {
  const { root, run } = fixture(t);
  fs.writeFileSync(path.join(root, 'outside.md'), 'private fixture');
  fs.symlinkSync(path.join(root, 'outside.md'), path.join(root, 'shared/knowledge/cards/alias.md'));
  const result = run();
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /符号链接/);
  assert.equal(fs.existsSync(path.join(root, 'alpha/knowledge/cards/alias.md')), false);
});
