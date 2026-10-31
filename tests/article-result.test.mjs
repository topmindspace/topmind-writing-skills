import test from 'node:test';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { articleLocalTextDocument, prepareArticleResult, prepareArticleResultFromSource, renderArticle, renderArticleResult } from '../runtime/article-renderer.mjs';

const hash = value => createHash('sha256').update(value).digest('hex');

test('result wraps the existing renderer without changing its delivery', async () => {
  const input = { markdown: '# 标题\n\n我测了 **3 次**。', platform: 'wechat' };
  const legacy = renderArticle(input);
  const result = await renderArticleResult(input);
  assert.equal(result.schemaVersion, 1);
  assert.equal(result.capabilityId, 'article.render');
  assert.equal(result.status, 'ok');
  assert.match(result.input.fingerprint, /^[a-f0-9]{64}$/u);
  assert.deepEqual(result.input.target, { platform: 'wechat', theme: 'minimal-ink' });
  assert.equal(result.diagnostics.length, 0);
  assert.equal(result.artifacts.find(item => item.role === 'preview')?.content, legacy.html);
  assert.equal(result.artifacts.find(item => item.role === 'source-markdown')?.content, legacy.text);
  assert.equal(result.artifacts.find(item => item.role === 'source-markdown')?.format, 'text/markdown');
  for (const artifact of result.artifacts) assert.equal(artifact.sha256, hash(artifact.content));
  assert.deepEqual(result, await renderArticleResult(input));
});

test('source, platform, renderer images and asset bytes contribute to the input fingerprint', async () => {
  const input = { sourcePath: 'posts/article.md', markdown: '![封面](images/cover.png)', platform: 'x' };
  const calls = [];
  const first = await prepareArticleResult(input, async path => { calls.push(path); return 'data:image/png;base64,YQ=='; });
  const second = await prepareArticleResult(input, async path => { calls.push(path); return 'data:image/png;base64,Yg=='; });
  assert.deepEqual(calls, ['posts/images/cover.png', 'posts/images/cover.png']);
  assert.equal(first.status, 'ok');
  assert.equal(first.images[0].status, 'embedded');
  assert.notEqual(first.input.fingerprint, second.input.fingerprint);
  assert.notEqual(first.artifacts[0].sha256, second.artifacts[0].sha256);
  const otherPlatform = await prepareArticleResult({ ...input, platform: 'wechat' }, async () => 'data:image/png;base64,YQ==');
  assert.notEqual(first.input.fingerprint, otherPlatform.input.fingerprint);
});

test('missing images and unsupported constructs yield warnings with source locations', async () => {
  const result = await prepareArticleResult({ sourcePath: 'posts/article.md', markdown: '![图](images/missing.png)\n\n```mermaid\nA-->B\n```' }, async () => { throw new Error('not found'); });
  assert.equal(result.status, 'warning');
  assert.equal(result.images[0].status, 'missing');
  assert.deepEqual(result.diagnostics.find(item => item.code === 'image-unavailable')?.location, { source: 'images/missing.png' });
  assert.ok(result.diagnostics.some(item => item.code === 'diagram-source-only'));
  assert.ok(result.diagnostics.every(item => item.severity === 'warning' && item.message));
  assert.match(result.artifacts.find(item => item.role === 'image-checklist')?.content ?? '', /missing/);
});

test('remote image references remain unverified even when they render in the preview', async () => {
  const result = await renderArticleResult({ markdown: '![远程图](https://example.com/cover.png)' });
  assert.equal(result.images[0].status, 'remote');
  assert.equal(result.status, 'warning');
  assert.deepEqual(result.diagnostics[0].location, { source: 'https://example.com/cover.png' });
  assert.equal(result.diagnostics[0].code, 'remote-image-unverified');
});

test('invalid rendering options return a structured error while the legacy API still throws', async () => {
  assert.throws(() => renderArticle({ platform: 'shell' }));
  const result = await renderArticleResult({ platform: 'shell' });
  assert.equal(result.status, 'error');
  assert.equal(result.input.fingerprint, null);
  assert.deepEqual(result.artifacts, []);
  assert.equal(result.diagnostics[0].code, 'unsupported-platform');
});

test('source Markdown is identified accurately and source path traversal never reaches the host reader', async () => {
  const result = await renderArticleResult({ markdown: '**加粗**\n\n![图](image.png)' });
  const source = result.artifacts.find(item => item.role === 'source-markdown');
  assert.equal(source?.content, '**加粗**\n\n![图](image.png)');
  assert.equal(source?.format, 'text/markdown');
  assert.ok(!result.artifacts.some(item => item.role === 'plain-text'));
  const calls = [];
  const escaped = await prepareArticleResult({ sourcePath: 'posts/../../outside/article.md', markdown: '![图](cover.png)' }, async path => {
    calls.push(path);
    return 'data:image/png;base64,YQ==';
  });
  assert.deepEqual(calls, []);
  assert.equal(escaped.status, 'error');
  assert.equal(escaped.diagnostics[0].code, 'invalid-image-path');
  const ordinary = await prepareArticleResult({ sourcePath: 'posts/../article.md', markdown: '![图](images/cover.png)' }, async path => {
    calls.push(path);
    return 'data:image/png;base64,YQ==';
  });
  assert.deepEqual(calls, ['images/cover.png']);
  assert.equal(ordinary.status, 'ok');
});

test('byte-bound rendering records the exact selected source and keeps local artifacts intact', async () => {
  const sourcePath = '20-研究/文章.md';
  const sourceBytes = Buffer.from('---\ntitle: 测试\n---\n# 标题\n\n正文', 'utf8');
  const input = { sourcePath, sourceBytes, platform: 'wechat', title: '测试',
    creationSnapshotFingerprint: 'a'.repeat(64) };
  const result = await prepareArticleResultFromSource(input, async () => { throw new Error('unexpected image read'); });
  assert.equal(result.status, 'ok');
  assert.deepEqual(result.input.source, { relativePath: sourcePath, sha256: hash(sourceBytes) });
  assert.equal(result.input.creationSnapshotFingerprint, 'a'.repeat(64));
  assert.deepEqual(result.input.renderParameters, { theme: 'minimal-ink', title: '测试' });
  assert.match(result.input.fingerprint, /^[a-f0-9]{64}$/u);
  assert.equal(result.artifacts.find(item => item.role === 'source-markdown')?.content, '# 标题\n\n正文');
  assert.deepEqual(articleLocalTextDocument(result), { text_kind: 'platform_text', title: '测试', body: '标题\n\n正文' });
  for (const artifact of result.artifacts) assert.equal(artifact.sha256, hash(artifact.content));
  const same = await prepareArticleResultFromSource(input, async () => '');
  assert.deepEqual(result, same);
  const longExtension = await prepareArticleResultFromSource({
    ...input, sourcePath: '20-研究/文章.markdown',
  }, async () => '');
  assert.equal(longExtension.status, 'ok');
  const changed = await prepareArticleResultFromSource({ ...input, sourceBytes: Buffer.from('# 标题\n\n改后正文') }, async () => '');
  assert.notEqual(result.input.source.sha256, changed.input.source.sha256);
  assert.notEqual(result.input.fingerprint, changed.input.fingerprint);
  const rebound = await prepareArticleResultFromSource({ ...input,
    creationSnapshotFingerprint: 'b'.repeat(64) }, async () => '');
  assert.notEqual(result.input.fingerprint, rebound.input.fingerprint);
  const mutable = Buffer.from('# 初始稿');
  const pending = prepareArticleResultFromSource({ ...input, sourceBytes: mutable }, async () => '');
  mutable.fill(0x61);
  const copied = await pending;
  assert.equal(copied.input.source.sha256, hash(Buffer.from('# 初始稿')));
  assert.equal(copied.artifacts.find(item => item.role === 'source-markdown')?.content, '# 初始稿');
});

test('local clipboard text is derived from rendered markup and remains distinct from Markdown', async () => {
  const markdown = '# 标题\n\n**加粗** 与 [链接](https://example.com)\n\n- 一\n- 二\n\n`<script>` &lt; 保留';
  const result = await prepareArticleResultFromSource({ sourcePath: 'post.md',
    sourceBytes: Buffer.from(markdown), platform: 'wechat' }, async () => '');
  const document = articleLocalTextDocument(result);
  assert.equal(result.status, 'ok');
  assert.equal(document.text_kind, 'platform_text');
  assert.equal(Object.hasOwn(document, 'title'), false);
  assert.match(document.body, /^标题\n\n加粗 与 链接\[1\]\n\n一\n二\n\n<script> &lt; 保留/u);
  assert.match(document.body, /\[1\] https:\/\/example\.com$/u);
  assert.notEqual(document.body, result.artifacts.find(item => item.role === 'source-markdown').content);
  assert.equal(articleLocalTextDocument(await renderArticleResult({ markdown })), null);
});

test('byte-bound rendering rejects noncanonical paths, invalid bytes and malformed UTF-8 without leaking input', async () => {
  const readCalls = [];
  const readImage = async relative => { readCalls.push(relative); return ''; };
  for (const input of [
    { sourcePath: '../outside.md', sourceBytes: Buffer.from('![图](cover.png)') },
    { sourcePath: '/outside.md', sourceBytes: Buffer.from('![图](cover.png)') },
    { sourcePath: '20-研究/文章.md', sourceBytes: 'DO_NOT_ECHO' },
    { sourcePath: '20-研究/文章.md', sourceBytes: Buffer.from([0xc3, 0x28]) },
    { sourcePath: '20-研究/文章.md', sourceBytes: Buffer.from('正文'),
      creationSnapshotFingerprint: 'bad' },
    { sourcePath: '20-研究/文章.md', sourceBytes: Buffer.from('正文'), images: {} },
  ]) {
    const result = await prepareArticleResultFromSource(input, readImage);
    assert.equal(result.status, 'error');
    assert.equal(result.input.fingerprint, null);
    assert.deepEqual(result.artifacts, []);
    assert.equal(JSON.stringify(result).includes('DO_NOT_ECHO'), false);
  }
  assert.deepEqual(readCalls, []);
  const oversized = await prepareArticleResultFromSource({
    sourcePath: '20-研究/文章.md', sourceBytes: new Uint8Array(16 * 1024 * 1024 + 1),
  }, readImage);
  assert.equal(oversized.diagnostics[0].code, 'source-too-large');
});

test('byte-bound rendering records the bytes supplied for local images', async () => {
  const sourceBytes = Buffer.from('![图](images/a.png)');
  const input = { sourcePath: '20-研究/文章.md', sourceBytes,
    creationSnapshotFingerprint: 'a'.repeat(64) };
  const first = await prepareArticleResultFromSource(input,
    async relative => {
      assert.equal(relative, '20-研究/images/a.png');
      return 'data:image/png;base64,' + Buffer.from('image-one').toString('base64');
    });
  assert.deepEqual(first.input.imageBytes, [{
    relativePath: '20-研究/images/a.png', sha256: hash(Buffer.from('image-one')),
  }]);
  const otherBytes = await prepareArticleResultFromSource(input,
    async () => 'data:image/png;base64,' + Buffer.from('image-two').toString('base64'));
  assert.notEqual(first.input.imageBytes[0].sha256, otherBytes.input.imageBytes[0].sha256);
  assert.notEqual(first.input.fingerprint, otherBytes.input.fingerprint);
  const remote = await prepareArticleResultFromSource(input, async () => 'https://example.invalid/a.png');
  assert.deepEqual(remote.input.imageBytes, []);
});
