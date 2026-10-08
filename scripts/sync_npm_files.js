#!/usr/bin/env node
/**
 * Sync package.json "files" so every discovered skill directory is listed.
 * Keeps shipping skill dirs on npm without hard-coding a single skill id.
 *
 * Usage: node scripts/sync_npm_files.js [--check]
 *   --check  exit 1 if files is out of sync (CI)
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { discoverSkills, ROOT } = require('./discover_skills');

const PKG_PATH = path.join(ROOT, 'package.json');
const BASE_FILES = ['bin', 'README.md', 'README.en.md', 'LICENSE', 'CHANGELOG.md'];
// 不进 npm 包的大文件（样张与研究图留在 GitHub / Release zip）。npm 的 files 支持 "!" 排除。
// cover 只保留 overview.png 供选风格；单风格样张 52MB、cover-study 研究图 6.6MB 不随包下载。
const EXCLUDE_FILES = [
  '!topmind-cover/assets/examples/*.png',
  'topmind-cover/assets/examples/overview.png',
  '!topmind-cover/references/cover-study/*.png',
];

function desiredFiles(skills) {
  const excludes = EXCLUDE_FILES.filter((e) => skills.some((s) => e.replace(/^!/, '').startsWith(`${s}/`)));
  return [...BASE_FILES, ...skills, ...excludes];
}

function sync({ checkOnly }) {
  const pkg = JSON.parse(fs.readFileSync(PKG_PATH, 'utf8'));
  const skills = discoverSkills();
  const next = desiredFiles(skills);
  const cur = Array.isArray(pkg.files) ? pkg.files : [];
  const same =
    cur.length === next.length && cur.every((v, i) => v === next[i]);

  if (same) {
    console.log(`files already in sync (${skills.length} skill(s)): ${next.join(', ')}`);
    return 0;
  }

  if (checkOnly) {
    console.error('package.json "files" out of sync with discovered skills.');
    console.error(`  current:  ${JSON.stringify(cur)}`);
    console.error(`  expected: ${JSON.stringify(next)}`);
    console.error('Run: npm run sync:files');
    return 1;
  }

  pkg.files = next;
  fs.writeFileSync(PKG_PATH, JSON.stringify(pkg, null, 2) + '\n', 'utf8');
  console.log(`updated files: ${next.join(', ')}`);
  return 0;
}

const checkOnly = process.argv.includes('--check');
process.exit(sync({ checkOnly }));
