import test from 'node:test';
import assert from 'node:assert/strict';
import { evaluateLengthRules } from '../runtime/length-rules.mjs';
import { evaluateLengthRuleSet, parseLengthRuleSet } from '../runtime/length-ruleset.mjs';

const target = { platform: 'synthetic', format: 'note', entrypoint: 'web', account_capability: 'basic' };
const document = { text_kind: 'platform_text', body: '123456' };
const rule = {
  id: 'synthetic.body.limit', category: 'platform_limit', status: 'active', applies_to: target,
  check: { field: 'body', operation: 'max_characters', counter: 'unicode_code_points', max: 5 },
  outcome: { exceeded: 'block' },
  evidence: { tier: 'official_primary', url: 'https://example.invalid/synthetic-rule',
    checked_at: '2026-10-01', review_after: '2026-10-29' },
};
const pack = (rules = [rule], version = '1') => ({ schemaVersion: 1, id: 'synthetic.rules', version, rules });
const run = (value, overrides = {}) => evaluateLengthRuleSet({ ruleSetJson: JSON.stringify(value), target,
  document, asOf: '2026-10-29', ...overrides });

test('loads all rules, evaluates one explicit entrypoint and binds the same rule bytes as the low-level evaluator', async () => {
  const loaded = parseLengthRuleSet(JSON.stringify(pack()));
  assert.equal(loaded.rules[0].id, rule.id);
  const report = await run(pack());
  const direct = await evaluateLengthRules({ target, document, rules: loaded.rules, asOf: '2026-10-29' });
  assert.equal(report.capabilityId, 'platform.validate.length-ruleset');
  assert.equal(report.verdict, 'block');
  assert.equal(report.input.rulesDigest, direct.input.rulesDigest);
  assert.equal(report.input.ruleSet.id, 'synthetic.rules');
  assert.match(report.input.fingerprint, /^[a-f0-9]{64}$/u);
  assert.ok(report.diagnostics.some(item => item.code === 'hard-length-exceeded'));
  const otherEntry = await run(pack(), { target: { ...target, entrypoint: 'api' } });
  assert.equal(otherEntry.verdict, 'review');
  assert.deepEqual(otherEntry.checks, []);
});

test('same-version rule edits, version changes and evaluation dates invalidate a report', async () => {
  const before = await run(pack());
  const changedRule = await run(pack([{ ...rule, check: { ...rule.check, max: 6 } }]));
  const changedVersion = await run(pack([rule], '2'));
  const expired = await run(pack(), { asOf: '2026-10-30' });
  const reordered = await run(pack([{ ...rule, evidence: { review_after: rule.evidence.review_after,
    checked_at: rule.evidence.checked_at, url: rule.evidence.url, tier: rule.evidence.tier } }]));
  assert.notEqual(before.input.rulesDigest, changedRule.input.rulesDigest);
  assert.notEqual(before.input.fingerprint, changedRule.input.fingerprint);
  assert.equal(before.input.rulesDigest, changedVersion.input.rulesDigest);
  assert.notEqual(before.input.fingerprint, changedVersion.input.fingerprint);
  assert.notEqual(before.input.fingerprint, expired.input.fingerprint);
  assert.equal(before.input.fingerprint, reordered.input.fingerprint, 'object key order is canonical');
  assert.equal(expired.verdict, 'review');
  assert.ok(expired.diagnostics.some(item => item.code === 'hard-rule-evidence-expired'));
  assert.ok(!expired.diagnostics.some(item => item.code === 'hard-length-exceeded'));
  const tooEarly = await run(pack(), { asOf: '2026-09-30' });
  assert.equal(tooEarly.verdict, 'review');
  assert.ok(tooEarly.diagnostics.some(item => item.code === 'hard-rule-evidence-not-yet-checked'));
});

test('binds a supplied creation snapshot fingerprint and rejects malformed values', async () => {
  const standalone = await run(pack());
  const bound = await run(pack(), { creationSnapshotFingerprint: 'b'.repeat(64) });
  assert.equal(bound.input.creationSnapshotFingerprint, 'b'.repeat(64));
  assert.notEqual(bound.input.fingerprint, standalone.input.fingerprint);
  const otherSnapshot = await run(pack(), { creationSnapshotFingerprint: 'c'.repeat(64) });
  assert.notEqual(bound.input.fingerprint, otherSnapshot.input.fingerprint);
  const malformed = await run(pack(), { creationSnapshotFingerprint: 'bad' });
  assert.equal(malformed.verdict, 'invalid');
  assert.ok(malformed.diagnostics.some(item => item.code === 'invalid-snapshot-fingerprint'));
});

test('rule-array order changes the report fingerprint while preserving the same outcome', async () => {
  const second = { ...rule, id: 'synthetic.title.limit',
    check: { field: 'title', operation: 'max_characters', counter: 'unicode_code_points', max: 10 } };
  const first = await run(pack([rule, second]), { document: { ...document, title: '标题' } });
  const reversed = await run(pack([second, rule]), { document: { ...document, title: '标题' } });
  assert.equal(first.verdict, reversed.verdict);
  assert.notEqual(first.input.rulesDigest, reversed.input.rulesDigest);
  assert.notEqual(first.input.fingerprint, reversed.input.fingerprint);
});

test('a creator preference cannot apply before its confirmation date', async () => {
  const preference = { id: 'synthetic.body.preference', category: 'creator_preference', status: 'active',
    applies_to: target, check: { field: 'body', operation: 'max_characters', counter: 'unicode_code_points', max: 4 },
    outcome: { exceeded: 'warn' }, evidence: { tier: 'user_confirmed', confirmed_at: '2026-10-29' } };
  const before = await run(pack([rule, preference]), { asOf: '2026-10-28' });
  assert.equal(before.verdict, 'block', 'current platform hard limit still applies');
  assert.ok(before.diagnostics.some(item => item.code === 'preference-confirmation-date-unverified'));
  assert.ok(!before.diagnostics.some(item => item.code === 'preference-length-exceeded'));
});

test('validates the whole pack before matching a target', async () => {
  const unrelatedBadRule = { ...rule, id: 'other.bad', applies_to: { ...target, platform: 'other', entrypoint: undefined } };
  const invalid = await run(pack([rule, unrelatedBadRule]));
  assert.equal(invalid.verdict, 'invalid');
  assert.ok(invalid.diagnostics.some(item => item.code === 'invalid-ruleset-rule'));
  assert.deepEqual(invalid.checks, []);
  const duplicate = await run(pack([rule, { ...rule }]));
  assert.ok(duplicate.diagnostics.some(item => item.code === 'duplicate-ruleset-rule'));
});

test('rejects unreviewed dates, hidden fields and malformed input without echoing content', async () => {
  for (const value of [
    pack([{ ...rule, evidence: { ...rule.evidence, review_after: '2026-02-30' } }]),
    pack([{ ...rule, check: { ...rule.check, operation: 'max_weighted_length' } }]),
  ]) {
    const result = await run(value);
    assert.equal(result.verdict, 'invalid');
    assert.equal(result.input.fingerprint, null);
  }
  const secret = await run({ ...pack(), apiKey: 'DO_NOT_ECHO' });
  assert.ok(secret.diagnostics.some(item => item.code === 'forbidden-ruleset-field'));
  assert.equal(JSON.stringify(secret).includes('DO_NOT_ECHO'), false);
  const malformed = await evaluateLengthRuleSet({ ruleSetJson: '{', target, document, asOf: '2026-10-29' });
  assert.ok(malformed.diagnostics.some(item => item.code === 'invalid-ruleset-json'));
  const noDate = await run(pack(), { asOf: undefined });
  assert.ok(noDate.diagnostics.some(item => item.code === 'invalid-evaluation-date'));
});
