import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import { renderArticle, WRITING_ACTIONS } from '../runtime/article-renderer.mjs';
const { buildHostPack } = createRequire(import.meta.url)('../lib/host-pack.cjs');
test('independent host pack has stable identity, exact skill versions and isolated resources', () => {
  const root = new URL('..', import.meta.url).pathname;
  const a = buildHostPack(root); const b = buildHostPack(root);
  assert.deepEqual(a, b); assert.equal(a.snapshot.skills.length, 8);
  assert.equal(a.manifest.digest.length, 64);
  for (const action of WRITING_ACTIONS) assert.ok(a.snapshot.skills.some(s => s.id === action.id));
  for (const id of a.snapshot.skills.map(s => s.id)) {
    assert.ok(a.snapshot.resources[`${id}/SKILL.md`]);
    assert.ok(a.snapshot.resources[`${id}/scripts/knowledge.py`]);
    const catalog = JSON.parse(a.snapshot.resources[`${id}/knowledge/index.json`]);
    for (const entry of catalog.entries) assert.ok(a.snapshot.resources[`${id}/knowledge/${entry.path}`]);
  }
  assert.ok(a.snapshot.resources['topmind-cover/assets/examples/creative-atlas.html']);
  assert.ok(a.snapshot.resources['runtime/article-renderer.mjs']);
  assert.ok(a.snapshot.resources['runtime/content-sha256.mjs']);
  assert.ok(a.snapshot.resources['runtime/length-rules.mjs']);
  assert.ok(a.snapshot.resources['runtime/length-rules.d.mts']);
  assert.ok(a.snapshot.resources['runtime/length-ruleset.mjs']);
  assert.ok(a.snapshot.resources['runtime/length-ruleset.d.mts']);
  assert.equal(a.manifest.runtime.entry, 'runtime/article-renderer.mjs');
  assert.deepEqual(a.manifest.runtime.capabilities.map(item => item.id),
    ['article.render', 'article.renderFromSource', 'article.localTextDocument', 'length.evaluate', 'length.ruleset.evaluate']);
  for (const capability of a.manifest.runtime.capabilities) {
    assert.ok(a.snapshot.resources[capability.entry]);
  }
});
test('host runtime imports in isolation and rejects an unbundled package or missing export', () => {
  const root = fileURLToPath(new URL('..', import.meta.url));
  const { manifest, snapshot } = buildHostPack(root);
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'topmind-host-test-'));
  const pack = path.join(temp, 'host-pack');
  const verify = () => spawnSync(process.execPath,
    [path.join(root, 'scripts', 'verify-host-pack-runtime.mjs'), pack], { encoding: 'utf8' });
  try {
    for (const [relative, content] of Object.entries(snapshot.resources)) {
      const target = path.join(pack, relative);
      fs.mkdirSync(path.dirname(target), { recursive: true });
      fs.writeFileSync(target, content);
    }
    fs.writeFileSync(path.join(pack, 'topmind-pack.json'), JSON.stringify(manifest));
    const portable = verify();
    assert.equal(portable.status, 0, portable.stderr);
    const entry = path.join(pack, 'runtime', 'length-rules.mjs');
    fs.appendFileSync(entry, "\nimport 'topmind-unbundled-test-dependency';\n");
    const missingDependency = verify();
    assert.equal(missingDependency.status, 1);
    assert.match(missingDependency.stderr, /length\.evaluate.*topmind-unbundled-test-dependency/u);
    fs.writeFileSync(entry, snapshot.resources['runtime/length-rules.mjs']);
    fs.writeFileSync(path.join(pack, 'topmind-pack.json'), JSON.stringify({ ...manifest,
      runtime: { ...manifest.runtime, capabilities: [{ ...manifest.runtime.capabilities[0], export: 'missingExport' }] } }));
    const missingExport = verify();
    assert.equal(missingExport.status, 1);
    assert.match(missingExport.stderr, /article\.render.*missing callable export/u);
  } finally {
    fs.rmSync(temp, { recursive: true, force: true });
  }
});
test('a failed isolated runtime check preserves the last built host pack', () => {
  const sourceRoot = fileURLToPath(new URL('..', import.meta.url));
  const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'topmind-host-build-test-'));
  const root = path.join(temp, 'source');
  try {
    for (const dir of ['lib', 'scripts', 'runtime', 'demo-skill']) fs.mkdirSync(path.join(root, dir), { recursive: true });
    for (const file of ['lib/host-pack.cjs', 'lib/zip.cjs', 'scripts/build-host-pack.cjs',
      'scripts/verify-host-pack-runtime.mjs']) {
      fs.copyFileSync(path.join(sourceRoot, file), path.join(root, file));
    }
    fs.cpSync(path.join(sourceRoot, 'runtime'), path.join(root, 'runtime'), { recursive: true });
    fs.writeFileSync(path.join(root, 'package.json'), JSON.stringify({ version: '0.0.0', license: 'MIT', repository: {} }));
    fs.writeFileSync(path.join(root, 'LICENSE'), 'Synthetic test license\n');
    fs.writeFileSync(path.join(root, 'demo-skill', 'SKILL.md'), '---\nname: demo-skill\n---\n');
    fs.writeFileSync(path.join(root, 'demo-skill', 'package.json'), JSON.stringify({ version: '1.0.0' }));
    const build = () => spawnSync(process.execPath, [path.join(root, 'scripts', 'build-host-pack.cjs')],
      { cwd: root, encoding: 'utf8' });
    const first = build();
    assert.equal(first.status, 0, first.stderr);
    const pack = path.join(root, 'dist', 'host-pack');
    const archive = path.join(root, 'dist', 'topmind-writing-skills-0.0.0.zip');
    const previousManifest = fs.readFileSync(path.join(pack, 'topmind-pack.json'));
    const previousArchive = fs.readFileSync(archive);
    fs.appendFileSync(path.join(root, 'runtime', 'length-rules.mjs'),
      "\nimport 'topmind-unbundled-test-dependency';\n");
    const failed = build();
    assert.notEqual(failed.status, 0);
    assert.match(failed.stderr, /topmind-unbundled-test-dependency/u);
    assert.deepEqual(fs.readFileSync(path.join(pack, 'topmind-pack.json')), previousManifest);
    assert.deepEqual(fs.readFileSync(archive), previousArchive);
    assert.equal(fs.readdirSync(path.join(root, 'dist')).some((name) => name.startsWith('.host-pack-stage-')), false);
  } finally {
    fs.rmSync(temp, { recursive: true, force: true });
  }
});
test('deliveries share source, keep facts, and apply platform links and tables', () => {
  const markdown = '---\ntitle: 示例\n---\n# 标题\n\n我测了 **3 次**，通过 2 次。\n\n[来源](https://example.com/report)\n\n| 指标 | 数字 |\n| --- | --- |\n| 用时 | 12ms |';
  const w = renderArticle({ markdown }); const x = renderArticle({ markdown, platform: 'x' });
  assert.equal(w.text, x.text); assert.match(w.body, /3 次/); assert.match(w.body, /12ms/);
  assert.match(w.body, /<sup>\[1\]/); assert.match(x.body, /<a href=/); assert.match(x.body, /<table/);
  assert.ok(x.diagnostics.some(d => d.code === 'table-paste-check'));
});
test('raw HTML, hostile links, image protocols and token injection never execute', () => {
  const r = renderArticle({ markdown: '<script>alert(1)</script>\n\n[x](javascript:alert)\n\n![x](file:///etc/passwd)\n\n\u00010\u0002' });
  assert.doesNotMatch(r.body, /<script|javascript:|file:\/\//); assert.match(r.body, /&lt;script&gt;/);
  assert.equal(r.images[0].status, 'missing');
  assert.throws(() => renderArticle({ platform: 'shell' }));
  assert.throws(() => renderArticle({ theme: '__proto__' }));
});
test('local images require explicit host bytes, code is escaped, unsupported features are reported', () => {
  const r = renderArticle({ markdown: '![图](images/a.png)\n\n```mermaid\nA-->B\n```\n\n::: tip', images: { 'images/a.png': 'data:image/png;base64,YQ==' } });
  assert.equal(r.images[0].status, 'embedded'); assert.ok(r.diagnostics.some(d => d.code === 'diagram-source-only'));
  assert.ok(r.diagnostics.some(d => d.code === 'container-as-text'));
});
test('installer version, skill metadata and changelog name the shipped release', () => {
  const root = fileURLToPath(new URL('..', import.meta.url));
  const version = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8')).version;
  assert.match(version, /^\d+\.\d+\.\d+$/u);
  const changelog = fs.readFileSync(path.join(root, 'CHANGELOG.md'), 'utf8');
  assert.match(changelog, new RegExp(`^## \\[${version}\\] - `, 'mu'));
  const built = buildHostPack(root);
  assert.equal(built.manifest.version, version);
  assert.equal(built.snapshot.version, version);
  const skills = fs.readdirSync(root).filter((id) => fs.existsSync(path.join(root, id, 'SKILL.md')));
  assert.ok(skills.length >= 8);
  for (const id of skills) {
    const pkg = JSON.parse(fs.readFileSync(path.join(root, id, 'package.json'), 'utf8')).version;
    const frontmatter = fs.readFileSync(path.join(root, id, 'SKILL.md'), 'utf8').match(/^---\r?\n([\s\S]*?)\r?\n---/u)[1];
    const metadata = frontmatter.match(/^\s*version:\s*["']?([^"'\n]+)/mu);
    assert.ok(metadata, id);
    assert.equal(metadata[1].trim(), pkg, id);
    assert.equal(built.snapshot.skills.find((skill) => skill.id === id).version, pkg);
  }
});
