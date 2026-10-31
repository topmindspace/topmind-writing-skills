#!/usr/bin/env node
'use strict';
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');
const { createZip } = require('../lib/zip.cjs');
const { createHash } = require('node:crypto');
const { buildHostPack } = require('../lib/host-pack.cjs');
const root = path.resolve(__dirname, '..');
const { manifest, snapshot } = buildHostPack(root);
const output = path.join(root, 'dist');
fs.mkdirSync(output, { recursive: true });
const packageRoot = path.join(output, 'host-pack');
const stage = fs.mkdtempSync(path.join(output, '.host-pack-stage-'));
try {
  for (const [relative, content] of Object.entries(snapshot.resources)) {
    const target = path.join(stage, relative); fs.mkdirSync(path.dirname(target), { recursive: true }); fs.writeFileSync(target, content);
  }
  fs.writeFileSync(path.join(stage, 'topmind-pack.json'), JSON.stringify(manifest, null, 2) + '\n');
  fs.copyFileSync(path.join(root, 'LICENSE'), path.join(stage, 'LICENSE'));
  execFileSync(process.execPath, [path.join(root, 'scripts', 'verify-host-pack-runtime.mjs'), stage],
    { stdio: 'inherit' });
  fs.rmSync(packageRoot, { recursive: true, force: true });
  fs.renameSync(stage, packageRoot);
} finally {
  fs.rmSync(stage, { recursive: true, force: true });
}
const name = `topmind-writing-skills-${manifest.version}.zip`;
const archive = path.join(output, name);
fs.rmSync(archive, { force: true });
fs.writeFileSync(archive, createZip({ ...snapshot.resources, 'topmind-pack.json': JSON.stringify(manifest, null, 2) + '\n', LICENSE: fs.readFileSync(path.join(root, 'LICENSE'), 'utf8') }));
const sum = createHash('sha256').update(fs.readFileSync(archive)).digest('hex');
fs.writeFileSync(path.join(output, `topmind-writing-skills-${manifest.version}.SHA256SUMS`), `${sum}  ${name}\n`);
fs.writeFileSync(path.join(output, 'host-snapshot.json'), JSON.stringify(snapshot) + '\n');
const base = `https://github.com/topmindspace/topmind-writing-skills/releases/download/v${manifest.version}`;
fs.writeFileSync(path.join(output, 'latest.json'), JSON.stringify({ version: manifest.version, writing: manifest.version, assets: [name, `topmind-writing-skills-${manifest.version}.SHA256SUMS`].map(n => ({ name: n, browser_download_url: `${base}/${n}` })) }, null, 2) + '\n');
console.log(`Built ${name}: ${snapshot.skills.length} skills, digest ${manifest.digest}`);
