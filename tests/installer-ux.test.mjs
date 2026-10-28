import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';

const sourceCli = new URL('../bin/topmind-writing-skills.js', import.meta.url).pathname;

function setup(t) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'writing-installer-ux-'));
  t.after(() => fs.rmSync(root, { recursive: true, force: true }));
  const pkg = path.join(root, 'package');
  const project = path.join(root, 'project');
  const home = path.join(root, 'home');
  for (const dir of [path.join(pkg, 'bin'), project, home]) fs.mkdirSync(dir, { recursive: true });
  fs.copyFileSync(sourceCli, path.join(pkg, 'bin/topmind-writing-skills.js'));
  fs.writeFileSync(path.join(pkg, 'package.json'), JSON.stringify({ version: '1.0.0' }));
  const writeSkill = (id, version) => {
    const dir = path.join(pkg, id);
    fs.mkdirSync(dir, { recursive: true });
    fs.writeFileSync(path.join(dir, 'SKILL.md'), `---\nname: ${id}\nmetadata:\n  version: "${version}"\n---\n# ${id}\n`);
  };
  const run = (...args) => spawnSync(process.execPath, [path.join(pkg, 'bin/topmind-writing-skills.js'), ...args], {
    cwd: project,
    env: { ...process.env, HOME: home, USERPROFILE: home },
    encoding: 'utf8',
  });
  return { root, pkg, project, home, writeSkill, run };
}

test('default target selects the configured host, and ambiguous hosts require --to', t => {
  const env = setup(t);
  env.writeSkill('topmind-alpha', '1.0.0');
  fs.mkdirSync(path.join(env.project, '.codex'));
  const installed = env.run('install', 'topmind-alpha');
  assert.equal(installed.status, 0, installed.stderr);
  assert.ok(fs.existsSync(path.join(env.project, '.codex/skills/topmind-alpha/SKILL.md')));
  assert.ok(!fs.existsSync(path.join(env.project, '.agents')));
  fs.mkdirSync(path.join(env.project, '.claude/skills/topmind-alpha'), { recursive: true });
  fs.writeFileSync(path.join(env.project, '.claude/skills/topmind-alpha/SKILL.md'), '---\nname: topmind-alpha\n---\n');
  const ambiguous = env.run('status');
  assert.notEqual(ambiguous.status, 0);
  assert.match(ambiguous.stderr, /More than one skill directory|Choose one with --to/);
});

test('install all, status, and update change only already installed skills', t => {
  const env = setup(t);
  env.writeSkill('topmind-alpha', '1.0.0');
  env.writeSkill('topmind-beta', '1.0.0');
  const target = path.join(env.root, 'skills');
  const installed = env.run('install', 'all', '--to', target);
  assert.equal(installed.status, 0, installed.stderr);
  assert.ok(fs.existsSync(path.join(target, 'topmind-alpha/.topmind-install.json')));
  assert.ok(fs.existsSync(path.join(target, 'topmind-beta/.topmind-install.json')));
  assert.match(env.run('status', '--to', target).stdout, /1\.0\.0 \| 1\.0\.0 \| current \| topmind-alpha/);
  fs.mkdirSync(path.join(target, 'topmind-alpha/scripts/__pycache__'), { recursive: true });
  fs.writeFileSync(path.join(target, 'topmind-alpha/scripts/__pycache__/tool.pyc'), 'generated');
  fs.mkdirSync(path.join(target, 'topmind-alpha/dist'));
  fs.writeFileSync(path.join(target, 'topmind-alpha/dist/output.zip'), 'generated');
  assert.match(env.run('status', '--to', target).stdout, /1\.0\.0 \| 1\.0\.0 \| current \| topmind-alpha/);
  env.writeSkill('topmind-alpha', '1.1.0');
  env.writeSkill('topmind-gamma', '1.0.0');
  const updated = env.run('update', '--to', target);
  assert.equal(updated.status, 0, updated.stderr);
  assert.match(fs.readFileSync(path.join(target, 'topmind-alpha/SKILL.md'), 'utf8'), /1\.1\.0/);
  assert.ok(!fs.existsSync(path.join(target, 'topmind-gamma')));
  assert.ok(!fs.readdirSync(target).some(name => name.startsWith('.topmind-alpha-previous-')));
});

test('local edits block automatic updates; force keeps a backup', t => {
  const env = setup(t);
  env.writeSkill('topmind-alpha', '1.0.0');
  const target = path.join(env.root, 'skills');
  assert.equal(env.run('install', 'topmind-alpha', '--to', target).status, 0);
  const dest = path.join(target, 'topmind-alpha');
  fs.writeFileSync(path.join(dest, 'my-notes.txt'), 'local customization');
  env.writeSkill('topmind-alpha', '1.1.0');
  const refused = env.run('update', '--to', target);
  assert.notEqual(refused.status, 0);
  assert.match(refused.stderr, /Local changes/);
  assert.ok(fs.existsSync(path.join(dest, 'my-notes.txt')));
  const forced = env.run('update', '--to', target, '--force');
  assert.equal(forced.status, 0, forced.stderr);
  assert.ok(!fs.existsSync(path.join(dest, 'my-notes.txt')));
  const backup = fs.readdirSync(target).find(name => name.startsWith('.topmind-alpha-previous-'));
  assert.ok(backup);
  assert.equal(fs.readFileSync(path.join(target, backup, 'my-notes.txt'), 'utf8'), 'local customization');
});

test('legacy upgrades keep the prior copy; batch preflight blocks identity conflicts', t => {
  const env = setup(t);
  env.writeSkill('topmind-alpha', '2.0.0');
  env.writeSkill('topmind-beta', '2.0.0');
  const target = path.join(env.root, 'skills');
  fs.mkdirSync(path.join(target, 'topmind-alpha'), { recursive: true });
  fs.writeFileSync(path.join(target, 'topmind-alpha/SKILL.md'), '---\nname: topmind-alpha\nversion: 1.0.0\n---\nold');
  const updated = env.run('update', '--to', target);
  assert.equal(updated.status, 0, updated.stderr);
  assert.match(updated.stdout, /backup:/);
  assert.ok(fs.readdirSync(target).some(name => name.startsWith('.topmind-alpha-previous-')));
  fs.mkdirSync(path.join(target, 'topmind-beta'));
  fs.writeFileSync(path.join(target, 'topmind-beta/keep.txt'), 'user data');
  const blocked = env.run('install', 'all', '--to', target, '--force');
  assert.notEqual(blocked.status, 0);
  assert.match(blocked.stderr, /Refusing to replace/);
  assert.equal(fs.readFileSync(path.join(target, 'topmind-beta/keep.txt'), 'utf8'), 'user data');
});
