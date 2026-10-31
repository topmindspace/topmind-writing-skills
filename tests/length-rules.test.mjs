import test from 'node:test';
import assert from 'node:assert/strict';
import { evaluateLengthRules as evaluateRawLengthRules } from '../runtime/length-rules.mjs';

const evaluateLengthRules = input => evaluateRawLengthRules({ asOf: '2026-10-29', ...input });

const target = { platform: 'studio', format: 'short_post', entrypoint: 'composer', account_capability: 'basic' };
const document = body => ({ text_kind: 'platform_text', body });
const hard = (max, overrides = {}) => ({
  id: 'synthetic.hard.body',
  category: 'platform_limit',
  status: 'active',
  applies_to: { ...target },
  check: { field: 'body', operation: 'max_characters', counter: 'unicode_code_points', max },
  outcome: { exceeded: 'block' },
  evidence: { tier: 'official_primary', url: 'https://example.invalid/synthetic-rule', checked_at: '2026-01-01', review_after: '2026-10-29' },
  ...overrides,
});
const preference = (max, overrides = {}) => ({
  id: 'synthetic.preference.body',
  category: 'creator_preference',
  status: 'active',
  applies_to: { ...target },
  check: { field: 'body', operation: 'max_characters', counter: 'unicode_code_points', max },
  outcome: { exceeded: 'warn' },
  evidence: { tier: 'user_confirmed', confirmed_at: '2026-10-29' },
  ...overrides,
});

test('hard upper bound blocks even when creator preference is wider, independent of rule order', async () => {
  const input = { target, document: document('123456'), rules: [hard(5), preference(10)] };
  const first = await evaluateLengthRules(input);
  const second = await evaluateLengthRules({ ...input, rules: [...input.rules].reverse() });
  assert.equal(first.input.fingerprint, second.input.fingerprint);
  assert.deepEqual(first.checks, second.checks);
  assert.deepEqual(first.diagnostics, second.diagnostics);
  assert.equal(first.verdict, 'block');
  assert.equal(first.status, 'error');
  assert.deepEqual(first.effectiveLimits, [{ field: 'body', unit: 'unicode_code_points', hardMax: 5, preferenceMax: 10, effectiveMax: 5 }]);
  assert.ok(first.diagnostics.some(item => item.code === 'hard-length-exceeded'));
  assert.ok(first.diagnostics.some(item => item.code === 'preference-widens-hard-limit'));
  assert.match(first.input.fingerprint, /^[a-f0-9]{64}$/u);
  assert.match(first.input.rulesDigest, /^[a-f0-9]{64}$/u);
  assert.notEqual(first.input.rulesDigest, second.input.rulesDigest, 'rule array order is part of the bound content');
});

test('rule content digest is stable across object key order and changes with same-version rule edits', async () => {
  const one = hard(5);
  const reordered = { evidence: { review_after: one.evidence.review_after, checked_at: one.evidence.checked_at,
    url: one.evidence.url, tier: one.evidence.tier },
    outcome: one.outcome, check: one.check, applies_to: one.applies_to, status: one.status,
    category: one.category, id: one.id };
  const first = await evaluateLengthRules({ target, document: document('123'), rules: [one] });
  const same = await evaluateLengthRules({ target, document: document('123'), rules: [reordered] });
  const changed = await evaluateLengthRules({ target, document: document('123'), rules: [hard(6)] });
  assert.equal(first.input.rulesDigest, same.input.rulesDigest);
  assert.notEqual(first.input.rulesDigest, changed.input.rulesDigest);
  assert.equal(first.input.fingerprint, same.input.fingerprint);
});

test('matches the shared rules content digest test vector', async () => {
  const rules = [{ id: 'a', check: { max: 5, field: 'body' } }];
  const result = await evaluateLengthRules({ target, document: document('123'), rules });
  assert.equal(result.input.rulesDigest,
    '83e4ff278a5b6eb76112c55654c54865b3a8a03dcef6bbebbb6c98ed88e29a49');
});

test('binds the exact prepared platform text independently from rule and target data', async () => {
  const first = await evaluateLengthRules({ target, document: { text_kind: 'platform_text', body: '123' }, rules: [hard(5)] });
  const same = await evaluateLengthRules({ target, document: { body: '123', text_kind: 'platform_text' }, rules: [hard(5)] });
  const changed = await evaluateLengthRules({ target, document: { text_kind: 'platform_text', body: '124' }, rules: [hard(5)] });
  assert.match(first.input.documentDigest, /^[a-f0-9]{64}$/u);
  assert.equal(first.input.documentDigest, '9877f12d041804ff4ea36f1f71639614aae6c38bcd84f8024ff02f0dbab25407');
  assert.equal(first.input.documentDigest, same.input.documentDigest);
  assert.notEqual(first.input.documentDigest, changed.input.documentDigest);
  assert.notEqual(first.input.fingerprint, changed.input.fingerprint);
});

test('rejects sensitive and non-JSON rule content before producing a bound report', async () => {
  for (const rules of [[{ ...hard(5), apiKey: 'DO_NOT_ECHO' }], [{ ...hard(5), max: Infinity }]]) {
    const result = await evaluateLengthRules({ target, document: document('123'), rules });
    assert.equal(result.verdict, 'invalid');
    assert.deepEqual(result.input, { fingerprint: null });
    assert.ok(result.diagnostics.some(item => item.code === 'input-fingerprint-failed'));
    assert.equal(JSON.stringify(result).includes('DO_NOT_ECHO'), false);
  }
});

test('confirmed tighter preference warns but does not masquerade as a platform block', async () => {
  const result = await evaluateLengthRules({ target, document: document('123456'), rules: [hard(8), preference(5)] });
  assert.equal(result.verdict, 'review');
  assert.equal(result.status, 'warning');
  assert.equal(result.effectiveLimits[0].effectiveMax, 5);
  assert.ok(result.diagnostics.some(item => item.code === 'preference-length-exceeded' && item.severity === 'warning'));
  assert.ok(!result.diagnostics.some(item => item.code === 'hard-length-exceeded'));
});

test('creator preference alone cannot certify a platform length check', async () => {
  const result = await evaluateLengthRules({ target, document: document('123'), rules: [preference(5)] });
  assert.equal(result.verdict, 'review');
  assert.equal(result.status, 'warning');
  assert.equal(result.effectiveLimits[0].hardMax, null);
  assert.ok(result.diagnostics.some(item => item.code === 'no-applicable-platform-limit'));
});

test('a hard title limit does not certify a body preference without a body platform limit', async () => {
  const titleRule = hard(10, { id: 'synthetic.hard.title', check: { field: 'title', operation: 'max_characters', counter: 'unicode_code_points', max: 10 } });
  const result = await evaluateLengthRules({ target,
    document: { text_kind: 'platform_text', title: '标题', body: '正文' }, rules: [titleRule, preference(10)] });
  assert.equal(result.verdict, 'review');
  assert.ok(result.diagnostics.some(item => item.code === 'no-applicable-platform-limit' && item.location?.field === 'body'));
});

test('dated hard evidence requires a reproducible date and expires without blocking', async () => {
  const rule = hard(5, { evidence: { ...hard(5).evidence, review_after: '2026-10-29' } });
  const valid = await evaluateLengthRules({ target, document: document('123456'), rules: [rule], asOf: '2026-10-29' });
  assert.equal(valid.verdict, 'block');
  const expired = await evaluateLengthRules({ target, document: document('123456'), rules: [rule], asOf: '2026-10-30' });
  assert.equal(expired.verdict, 'review');
  assert.ok(expired.diagnostics.some(item => item.code === 'hard-rule-evidence-expired'));
  assert.ok(!expired.diagnostics.some(item => item.code === 'hard-length-exceeded'));
  const undated = await evaluateRawLengthRules({ target, document: document('123'), rules: [rule] });
  assert.equal(undated.verdict, 'review');
  assert.ok(undated.diagnostics.some(item => item.code === 'hard-rule-evaluation-date-required'));
  const badDate = await evaluateLengthRules({ target, document: document('123'), rules: [rule], asOf: '2026-02-30' });
  assert.equal(badDate.verdict, 'invalid');
  assert.deepEqual(badDate.input, { fingerprint: null });
});

test('direct low-level calls cannot activate hard or personal rules without their review dates', async () => {
  const hardWithoutReview = hard(5, { evidence: { tier: 'official_primary',
    url: 'https://example.invalid/synthetic-rule', checked_at: '2026-01-01' } });
  const missingHardDate = await evaluateLengthRules({ target, document: document('123456'), rules: [hardWithoutReview] });
  assert.equal(missingHardDate.verdict, 'review');
  assert.ok(missingHardDate.diagnostics.some(item => item.code === 'hard-rule-review-date-invalid'));
  assert.ok(!missingHardDate.diagnostics.some(item => item.code === 'hard-length-exceeded'));
  const preferenceWithoutConfirmation = preference(5, { evidence: { tier: 'user_confirmed' } });
  const missingPreferenceDate = await evaluateLengthRules({ target, document: document('123456'), rules: [preferenceWithoutConfirmation] });
  assert.equal(missingPreferenceDate.verdict, 'review');
  assert.ok(missingPreferenceDate.diagnostics.some(item => item.code === 'preference-confirmation-date-unverified'));
  assert.deepEqual(missingPreferenceDate.checks, []);
});

test('inactive rule for a different target does not contaminate a valid applicable check', async () => {
  const result = await evaluateLengthRules({ target, document: document('123'), rules: [
    hard(5),
    hard(2, { id: 'other.platform', status: 'proposed_unconfirmed', applies_to: { ...target, platform: 'other' } }),
  ] });
  assert.equal(result.verdict, 'pass');
  assert.equal(result.status, 'ok');
  assert.deepEqual(result.checks.map(check => check.ruleId), ['synthetic.hard.body']);
  assert.deepEqual(result.diagnostics, []);
});

test('entrypoint mismatch does not apply the hard rule or return an unjustified pass', async () => {
  const result = await evaluateLengthRules({ target: { ...target, entrypoint: 'web' }, document: document('123456789'), rules: [hard(5)] });
  assert.equal(result.verdict, 'review');
  assert.deepEqual(result.checks, []);
  assert.ok(result.diagnostics.some(item => item.code === 'no-applicable-length-rule'));
  assert.ok(!result.diagnostics.some(item => item.code === 'hard-length-exceeded'));
});

test('missing rule scope is invalid and unknown account capability requires review', async () => {
  const missing = await evaluateLengthRules({ target, document: document('123456'), rules: [hard(5, { applies_to: { platform: 'studio', format: 'short_post', entrypoint: 'composer' } })] });
  assert.equal(missing.verdict, 'invalid');
  assert.ok(missing.diagnostics.some(item => item.code === 'invalid-rule-scope'));
  const unknown = await evaluateLengthRules({ target: { ...target, account_capability: 'unknown' }, document: document('123456'), rules: [hard(5)] });
  assert.equal(unknown.verdict, 'review');
  assert.ok(unknown.diagnostics.some(item => item.code === 'target-scope-unknown' && item.dimension === 'account_capability'));
  assert.ok(!unknown.diagnostics.some(item => item.code === 'hard-length-exceeded'));
  const broad = hard(10, { applies_to: { ...target, account_capability: 'any' } });
  const unknownButBroad = await evaluateLengthRules({ target: { ...target, account_capability: 'unknown' }, document: document('123'), rules: [broad] });
  assert.equal(unknownButBroad.checks.length, 1);
  assert.equal(unknownButBroad.verdict, 'review');
  assert.ok(unknownButBroad.diagnostics.some(item => item.code === 'target-dimension-unknown'));
  const unknownRule = await evaluateLengthRules({ target, document: document('123'), rules: [hard(10, { applies_to: { ...target, account_capability: 'unknown' } })] });
  assert.equal(unknownRule.verdict, 'invalid');
  assert.ok(unknownRule.diagnostics.some(item => item.code === 'invalid-rule-scope'));
});

test('unverified hard rule and unconfirmed preference cannot be activated implicitly', async () => {
  const result = await evaluateLengthRules({ target, document: document('123456789'), rules: [
    hard(5, { evidence: { tier: 'third_party' } }),
    preference(3, { status: 'proposed_unconfirmed', evidence: { tier: 'user_preference_pending_confirmation' } }),
  ] });
  assert.equal(result.verdict, 'review');
  assert.deepEqual(result.checks, []);
  assert.ok(result.diagnostics.some(item => item.code === 'hard-rule-evidence-unverified'));
  assert.ok(result.diagnostics.some(item => item.code === 'rule-inactive'));
});

test('unsupported weighted counting cannot silently pass as Unicode character counting', async () => {
  const rule = hard(5, { check: { field: 'body', operation: 'max_weighted_length', counter: 'twitter_text_v3', max: 5 } });
  const result = await evaluateLengthRules({ target, document: document('123456'), rules: [rule] });
  assert.equal(result.verdict, 'review');
  assert.ok(result.diagnostics.some(item => item.code === 'unsupported-length-operation'));
});

test('the supported counter counts Unicode code points and requires a complete target', async () => {
  const good = await evaluateLengthRules({ target, document: document('甲😊乙'), rules: [hard(3)] });
  assert.equal(good.verdict, 'pass');
  assert.equal(good.checks[0].observed, 3);
  const missingTarget = await evaluateLengthRules({ target: { platform: 'studio' }, document: document('123'), rules: [hard(2)] });
  assert.equal(missingTarget.verdict, 'invalid');
  assert.ok(missingTarget.diagnostics.some(item => item.code === 'invalid-target-scope'));
  const rawMarkdown = await evaluateLengthRules({ target, document: { body: '**123**' }, rules: [hard(2)] });
  assert.equal(rawMarkdown.verdict, 'invalid');
  assert.ok(rawMarkdown.diagnostics.some(item => item.code === 'invalid-content-kind'));
});
