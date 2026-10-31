import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { articleLocalTextDocument, prepareArticleResultFromSource, ARTICLE_RENDERER_PROVIDER } from '../runtime/article-renderer.mjs';
import { evaluateLengthRuleSet, LENGTH_RULESET_PROVIDER } from '../runtime/length-ruleset.mjs';

const here = path.dirname(fileURLToPath(import.meta.url));
const engineRoot = process.env.TOPMIND_ENGINE_SRC || path.resolve(here, '..', '..', 'topmind');

test('cross-repo: selected source bytes and local article artifacts match a fresh Kernel snapshot', async t => {
  try { await fs.access(path.join(engineRoot, 'lib', 'kernel-api.mjs')); }
  catch { t.skip('topmind Kernel checkout is not present'); return; }
  const kernel = await import(pathToFileURL(path.join(engineRoot, 'lib', 'kernel-api.mjs')).href);
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'topmind-render-source-test-'));
  try {
    for (const dir of ['00-Inbox', '99-归档', '20-研究/images']) {
      await fs.mkdir(path.join(root, dir), { recursive: true });
    }
    await fs.writeFile(path.join(root, 'topmind.yaml'),
      kernel.stringifyContract(kernel.buildDefaultContract()));
    const targetPath = '20-研究/稿件.md';
    const notePath = path.join(root, targetPath);
    const imagePath = path.join(root, '20-研究/images/a.png');
    const markdown = '# 标题\n\n正文 ![图](images/a.png)\n';
    await fs.writeFile(notePath, markdown);
    await fs.writeFile(imagePath, Buffer.from('image-one'));
    const target = { platform: 'wechat', format: 'article', entrypoint: 'copy-html', account_capability: 'basic' };
    const ruleset = { schemaVersion: 1, id: 'synthetic.rules', version: '1', rules: [{
      id: 'synthetic.local-text', category: 'creator_preference', status: 'proposed_unconfirmed',
      applies_to: target, check: { field: 'body', operation: 'max_characters', counter: 'unicode_code_points', max: 100 },
      outcome: { exceeded: 'warn' }, evidence: { tier: 'user_preference_pending_confirmation' },
    }] };
    const renderInput = { sourcePath: targetPath, sourceBytes: await fs.readFile(notePath),
      platform: 'wechat', theme: 'minimal-ink', title: '标题' };
    const readImage = async relative => 'data:image/png;base64,' +
      (await fs.readFile(path.join(root, relative))).toString('base64');
    const preflight = await prepareArticleResultFromSource(renderInput, readImage);
    const document = articleLocalTextDocument(preflight);
    assert.deepEqual(document, { text_kind: 'platform_text', title: '标题', body: '标题\n\n正文' });
    const selection = { workspaceRoot: root, targetPath, platform: 'wechat', format: 'article',
      entry: 'copy-html', provider: ARTICLE_RENDERER_PROVIDER,
      ruleset,
      accountCapabilities: { account_capability: 'basic' },
      lengthValidation: { document, provider: LENGTH_RULESET_PROVIDER, asOf: '2026-10-29' },
      parameters: { theme: 'minimal-ink', title: '标题' } };
    const snapshot = kernel.buildCreationInputSnapshot(selection);
    assert.equal(snapshot.inputsComplete, true);
    const result = await prepareArticleResultFromSource({ ...renderInput,
      creationSnapshotFingerprint: snapshot.fingerprint,
    }, readImage);
    const matched = kernel.compareCreationArticleResult(snapshot, result);
    assert.equal(matched.matches, true);
    assert.equal(matched.artifactHashesVerified, true);
    assert.equal(matched.renderedImageBytesVerified, true);
    assert.equal(matched.sourceLineageVerified, false);
    assert.equal(matched.publishReady, false);
    const lengthReport = await evaluateLengthRuleSet({ ruleSetJson: JSON.stringify(ruleset),
      target, document, asOf: '2026-10-29', creationSnapshotFingerprint: snapshot.fingerprint });
    assert.equal(lengthReport.verdict, 'review');
    const chain = kernel.compareCreationLocalLengthChain(snapshot, result, lengthReport);
    assert.equal(chain.matches, true);
    assert.equal(chain.localTextChainMatched, true);
    assert.equal(chain.platformEditorVerified, false);
    assert.equal(chain.publishReady, false);
    const changedText = { ...result, artifacts: result.artifacts.map(item => item.role === 'local-clipboard-text'
      ? { ...item, content: '其他正文', sha256: createHash('sha256').update('其他正文').digest('hex') }
      : item) };
    assert.equal(kernel.compareCreationLocalLengthChain(snapshot, changedText, lengthReport).reason,
      'local-text-document-mismatch');
    const otherTheme = await prepareArticleResultFromSource({ ...renderInput,
      theme: 'newsprint', creationSnapshotFingerprint: snapshot.fingerprint }, readImage);
    assert.equal(kernel.compareCreationArticleResult(snapshot, otherTheme).reason,
      'renderer-parameters-mismatch');
    const wrongImage = await prepareArticleResultFromSource({
      sourcePath: targetPath, sourceBytes: await fs.readFile(notePath),
      platform: 'wechat', theme: 'minimal-ink', title: '标题',
      creationSnapshotFingerprint: snapshot.fingerprint,
    }, async () => 'data:image/png;base64,' + Buffer.from('other-image').toString('base64'));
    assert.equal(kernel.compareCreationArticleResult(snapshot, wrongImage).reason, 'rendered-assets-mismatch');
    await fs.writeFile(notePath, '# 标题\n\n<img src="images/a.png">\n');
    const htmlImageSnapshot = kernel.buildCreationInputSnapshot(selection);
    assert.equal(htmlImageSnapshot.inputsComplete, true);
    const htmlImageResult = await prepareArticleResultFromSource({
      sourcePath: targetPath, sourceBytes: await fs.readFile(notePath),
      platform: 'wechat', theme: 'minimal-ink', title: '标题',
      creationSnapshotFingerprint: htmlImageSnapshot.fingerprint,
    }, async () => { throw new Error('HTML image should not be read by the article renderer'); });
    assert.equal(kernel.compareCreationArticleResult(htmlImageSnapshot, htmlImageResult).reason, 'rendered-assets-mismatch');
    await fs.writeFile(notePath, markdown);
    await fs.writeFile(imagePath, Buffer.from('image-two'));
    const refreshed = kernel.buildCreationInputSnapshot(selection);
    assert.equal(kernel.compareCreationArticleResult(refreshed, result).reason, 'snapshot-fingerprint-mismatch');
  } finally {
    await fs.rm(root, { recursive: true, force: true });
  }
});
