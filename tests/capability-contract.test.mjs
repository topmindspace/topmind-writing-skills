import test from 'node:test';
import assert from 'node:assert/strict';
import { renderArticleResult } from '../runtime/article-renderer.mjs';
import { evaluateLengthRules } from '../runtime/length-rules.mjs';

const target = { platform: 'synthetic', format: 'short_post', entrypoint: 'editor', account_capability: 'basic' };
const rule = {
  id: 'synthetic.length',
  category: 'platform_limit',
  status: 'active',
  applies_to: target,
  check: { field: 'body', operation: 'max_characters', counter: 'unicode_code_points', max: 12 },
  outcome: { exceeded: 'block' },
  evidence: { tier: 'official_primary', url: 'https://example.invalid/synthetic-rule', checked_at: '2026-01-01', review_after: '2026-10-29' },
};
const commonFields = ['schemaVersion', 'capabilityId', 'provider', 'status', 'input', 'artifacts', 'diagnostics'];

test('render and length validation share a stable result envelope for real calls', async () => {
  const articleInput = { markdown: '# 标题\n\n正文', platform: 'wechat' };
  const lengthInput = { target, document: { text_kind: 'platform_text', body: '正文' }, rules: [rule], asOf: '2026-10-29' };
  const article = await renderArticleResult(articleInput);
  const length = await evaluateLengthRules(lengthInput);
  for (const result of [article, length]) {
    for (const field of commonFields) assert.ok(Object.hasOwn(result, field), `${result.capabilityId}: ${field}`);
    assert.equal(result.schemaVersion, 1);
    assert.match(result.input.fingerprint, /^[a-f0-9]{64}$/u);
    assert.ok(Array.isArray(result.artifacts));
    assert.ok(Array.isArray(result.diagnostics));
    assert.equal(typeof result.provider.id, 'string');
    assert.equal(typeof result.provider.version, 'string');
  }
  assert.deepEqual(length.input.target, target);
  assert.deepEqual(length.artifacts, []);
  assert.deepEqual(article, await renderArticleResult(articleInput));
  assert.deepEqual(length, await evaluateLengthRules(lengthInput));
});

test('invalid inputs do not manufacture a target or input fingerprint', async () => {
  const article = await renderArticleResult({ markdown: '正文', platform: 'unsupported' });
  const length = await evaluateLengthRules({ target: { platform: 'synthetic' }, document: { text_kind: 'platform_text', body: '正文' }, rules: [rule] });
  for (const result of [article, length]) {
    assert.equal(result.status, 'error');
    assert.deepEqual(result.input, { fingerprint: null });
    assert.deepEqual(result.artifacts, []);
  }
});
