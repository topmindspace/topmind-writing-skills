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
const { ROOT } = require('./discover_skills');

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
for (const f of info.files) {
  const hit = FORBIDDEN.find((r) => r.re.test(f.path));
  if (hit) bad.push(`${f.path}  ← ${hit.why}`);
}
console.log(`npm pack --dry-run: ${info.entryCount} files, tarball ${info.size} B, unpacked ${info.unpackedSize} B`);
if (bad.length) {
  console.error(`npm 包含有不应发布的文件（${bad.length} 个）：`);
  for (const b of bad) console.error(`  - ${b}`);
  console.error('检查 package.json "files" 的排除项（npm run sync:files）。');
  process.exit(1);
}
console.log('npm 包内容检查通过：不含 dist/、release-assets/、Python 缓存、锁文件与 node_modules/。');
