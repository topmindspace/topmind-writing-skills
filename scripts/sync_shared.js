#!/usr/bin/env node
/**
 * 共享文件：shared/ 是唯一真源，各技能目录里保留逐字节相同的副本（自包含安装仍可用）。
 *
 * Usage:
 *   node scripts/sync_shared.js           # 把 shared/ 真源写进各技能副本
 *   node scripts/sync_shared.js --check   # 只校验，任一副本缺失或不一致 → exit 1（CI / prepack）
 *
 * 清单：shared/manifest.json（"*" = 全部已发现技能）。
 * 规则：只改 shared/ 下的真源，再运行本脚本；不要直接改技能目录里的副本。
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { discoverSkills, ROOT } = require('./discover_skills');

const SHARED = path.join(ROOT, 'shared');
const MANIFEST = path.join(SHARED, 'manifest.json');

function loadManifest() {
  const raw = JSON.parse(fs.readFileSync(MANIFEST, 'utf8'));
  if (!raw || typeof raw.files !== 'object') {
    throw new Error('shared/manifest.json 缺 files 字段');
  }
  return raw.files;
}

function plan() {
  const skills = discoverSkills();
  const files = loadManifest();
  const pairs = [];
  for (const [rel, targets] of Object.entries(files)) {
    if (rel.includes('..') || path.isAbsolute(rel)) {
      throw new Error(`非法共享路径：${rel}`);
    }
    const src = path.join(SHARED, rel);
    if (!fs.existsSync(src)) throw new Error(`真源缺失：shared/${rel}`);
    const list = targets.includes('*') ? skills : targets;
    for (const skill of list) {
      if (!skills.includes(skill)) throw new Error(`manifest 引用了不存在的技能：${skill}（${rel}）`);
      pairs.push({ rel, skill, src, dest: path.join(ROOT, skill, rel) });
    }
  }
  return pairs;
}

function main() {
  const checkOnly = process.argv.includes('--check');
  let pairs;
  try {
    pairs = plan();
  } catch (e) {
    console.error(`sync_shared: ${e.message}`);
    return 1;
  }
  const drift = [];
  let written = 0;
  for (const p of pairs) {
    const want = fs.readFileSync(p.src);
    const have = fs.existsSync(p.dest) ? fs.readFileSync(p.dest) : null;
    if (have && Buffer.compare(want, have) === 0) continue;
    if (checkOnly) {
      drift.push(`${p.skill}/${p.rel}${have ? ' 与真源不一致' : ' 缺失'}`);
      continue;
    }
    fs.mkdirSync(path.dirname(p.dest), { recursive: true });
    fs.writeFileSync(p.dest, want);
    // 保留可执行位与真源一致
    fs.chmodSync(p.dest, fs.statSync(p.src).mode & 0o777);
    written += 1;
    console.log(`synced ${p.skill}/${p.rel}`);
  }
  if (checkOnly) {
    if (drift.length) {
      console.error(`sync_shared --check: ${drift.length} 份副本与 shared/ 真源不一致`);
      for (const d of drift) console.error(`  ✗ ${d}`);
      console.error('只改 shared/ 下的真源，再运行：npm run sync:shared');
      return 1;
    }
    console.log(`sync_shared --check: ${pairs.length} 份副本与真源逐字节一致`);
    return 0;
  }
  console.log(`sync_shared: ${written} 份副本已更新，共 ${pairs.length} 份`);
  return 0;
}

process.exit(main());
