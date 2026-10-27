#!/usr/bin/env node
/**
 * 校验 npm 包内容：Release 打包产物（各技能 dist/ 下的 zip 与 manifest）、运行时缓存、
 * npm 锁文件和 node_modules/ 不得进包。
 * 在 CI 与 Release 中，于 package_skill.py 生成 dist/ 之后运行，和 npm publish 看到的文件同口径。
 *
 * Usage: node scripts/check_npm_pack.js
 */
'use strict';

const { execFileSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const { ROOT, discoverSkills } = require('./discover_skills');

const FORBIDDEN = [
  { re: /(^|\/)dist\//, why: 'Release 打包产物（dist/）' },
  { re: /(^|\/)release-assets\//, why: 'Release 附件目录' },
  { re: /(^|\/)__pycache__\//, why: 'Python 字节码缓存' },
  { re: /\.py[co]$/, why: 'Python 字节码文件' },
  { re: /(^|\/)package-lock\.json$/, why: 'npm 锁文件（技能按目录复制安装，用不上）' },
  { re: /(^|\/)npm-shrinkwrap\.json$/, why: 'npm 锁文件' },
  { re: /(^|\/)node_modules\//, why: '本地依赖目录' },
];

const npm = process.platform === 'win32' ? 'npm.cmd' : 'npm';
const out = execFileSync(npm, ['pack', '--dry-run', '--json', '--ignore-scripts'], {
  cwd: ROOT,
  encoding: 'utf8',
  stdio: ['ignore', 'pipe', 'inherit'],
});
const [info] = JSON.parse(out);
const bad = [];
const names = new Set(info.files.map(f => f.path));
for (const id of discoverSkills()) {
  const required = ['SKILL.md', 'README.md', 'README.en.md', 'package.json', 'scripts/knowledge.py', 'knowledge/index.json'];
  const catalog = JSON.parse(fs.readFileSync(path.join(ROOT, id, 'knowledge/index.json'), 'utf8'));
  required.push(...catalog.entries.map(entry => `knowledge/${entry.path}`));
  if (id === 'topmind-cover') {
    required.push('assets/examples/overview.png', 'assets/examples/creative-atlas.html');
    required.push(...fs.readdirSync(path.join(ROOT, id, 'assets/title-specs'))
      .filter(name => name.endsWith('.json')).map(name => `assets/title-specs/${name}`));
  }
  for (const relative of required) if (!names.has(`${id}/${relative}`)) bad.push(`${id}/${relative} ← 缺少必需资源`);
}
for (const f of info.files) {
  const hit = FORBIDDEN.find((r) => r.re.test(f.path));
  if (hit) bad.push(`${f.path}  ← ${hit.why}`);
}
console.log(`npm pack --dry-run: ${info.entryCount} files, tarball ${info.size} B, unpacked ${info.unpackedSize} B`);
if (bad.length) {
  console.error(`npm 包内容不完整或混入不应发布的文件（${bad.length} 项）：`);
  for (const b of bad) console.error(`  - ${b}`);
  console.error('检查 package.json "files" 的排除项（npm run sync:files）。');
  process.exit(1);
}
console.log('npm 包内容检查通过：必需资源完整，无 dist/、release-assets/、Python 缓存、锁文件与 node_modules/。');
