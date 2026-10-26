import test from 'node:test';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { renderArticle, WRITING_ACTIONS } from '../runtime/article-renderer.mjs';
const { buildHostPack } = createRequire(import.meta.url)('../lib/host-pack.cjs');
test('independent host pack has stable identity, exact skill versions and isolated resources', () => {
  const root = new URL('..', import.meta.url).pathname;
  const a = buildHostPack(root); const b = buildHostPack(root);
  assert.deepEqual(a, b); assert.equal(a.snapshot.skills.length, 8);
  assert.equal(a.manifest.digest.length, 64);
  for (const action of WRITING_ACTIONS) assert.ok(a.snapshot.skills.some(s => s.id === action.id));
  for (const id of a.snapshot.skills.map(s => s.id)) assert.ok(a.snapshot.resources[`${id}/SKILL.md`]);
  assert.ok(a.snapshot.resources['runtime/article-renderer.mjs']);
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
