/** Official portable host distribution. Independent from any host checkout. */
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { createHash } = require('node:crypto');
const hash = value => createHash('sha256').update(value).digest('hex');
function buildHostPack(root) {
  const pkg = JSON.parse(fs.readFileSync(path.join(root, 'package.json'), 'utf8'));
  const ids = fs.readdirSync(root).filter(id => /^[a-z0-9-]+$/.test(id) && fs.existsSync(path.join(root, id, 'SKILL.md'))).sort();
  const resources = {};
  const files = {};
  function walk(dir, relative) {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name < b.name ? -1 : a.name > b.name ? 1 : 0)) {
      if (entry.name.startsWith('.') || ['node_modules', 'dist', '__pycache__'].includes(entry.name)) continue;
      const rel = `${relative}/${entry.name}`;
      if (entry.isSymbolicLink()) throw new Error(`Symlink in host pack: ${rel}`);
      if (entry.isDirectory()) walk(path.join(dir, entry.name), rel);
      else if (entry.isFile() && /\.(md|py|json|yaml|yml|css|html|txt|js|mjs|mts)$/i.test(entry.name)) {
        const content = fs.readFileSync(path.join(dir, entry.name), 'utf8');
        resources[rel] = content; files[rel] = hash(content);
      }
    }
  }
  for (const id of [...ids, 'runtime']) walk(path.join(root, id), id);
  const skills = ids.map(id => {
    const raw = resources[`${id}/SKILL.md`];
    const meta = JSON.parse(fs.readFileSync(path.join(root, id, 'package.json'), 'utf8'));
    if (!/^---\r?\n/u.test(raw) || !/^name:\s*/mu.test(raw)) throw new Error(`Invalid skill: ${id}`);
    return { id, name: id, description: meta.description || id, version: meta.version, packId: 'topmind-writing-skills' };
  });
  const manifest = { schema_version: 1, name: 'topmind-writing-skills', version: pkg.version, license: pkg.license, repository: pkg.repository, entry_files: ids.map(id => `${id}/SKILL.md`), files, runtime: { api: 1, entry: 'runtime/article-renderer.mjs', update: 'host-release' } };
  const digest = hash(JSON.stringify(manifest));
  return { manifest: { ...manifest, digest }, snapshot: { id: manifest.name, version: pkg.version, source: 'https://github.com/topmindspace/topmind-writing-skills', license: pkg.license, digest, skills, resources } };
}
module.exports = { buildHostPack };
