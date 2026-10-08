#!/usr/bin/env node
/**
 * Run a gate command across all discovered skills.
 *
 * Usage:
 *   node scripts/run_skill_gates.js check
 *   node scripts/run_skill_gates.js audit
 *   node scripts/run_skill_gates.js versions   # 仅 frontmatter version == package.json version
 *   node scripts/run_skill_gates.js package
 *   node scripts/run_skill_gates.js install
 */
'use strict';

const { spawnSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const { discoverSkills, ROOT } = require('./discover_skills');

const PY = process.env.PYTHON || 'python3';

function run(cmd, args, opts = {}) {
  // Windows: `npm` is npm.cmd — spawning it without a shell yields ENOENT.
  const useShell = opts.shell !== undefined ? opts.shell : (process.platform === 'win32' && cmd === 'npm');
  const r = spawnSync(cmd, args, { stdio: 'inherit', cwd: opts.cwd || ROOT, shell: useShell });
  if (r.error) throw r.error;
  if (r.status !== 0) process.exit(r.status || 1);
}

function hasScript(skillDir, name) {
  return fs.existsSync(path.join(skillDir, 'scripts', name));
}

// 审计 严重-1 / 中等-5 的门禁：SKILL.md frontmatter 的 metadata.version（或旧的顶层 version）必须 == package.json version，
// 缺失 version 字段也算失败。只做"一致性"比对，不做版本语义判断
// （版本号取值分歧见审计报告第五节第 1 条，需用户裁决）。
function checkVersionMatch(skillId) {
  const errs = [];
  const dir = path.join(ROOT, skillId);
  let fmVersion = null;
  try {
    const text = fs.readFileSync(path.join(dir, 'SKILL.md'), 'utf8');
    const fm = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (fm) {
      // metadata.version（Agent Skills 规范）优先，兼容旧的顶层 version
      const m = fm[1].match(/^metadata:\s*\n(?:[ \t]+.*\n)*?[ \t]+version:\s*(.+?)\s*$/m) || fm[1].match(/^version:\s*(.+?)\s*$/m);
      if (m) fmVersion = m[1].replace(/^["']|["']$/g, '').trim();
    }
  } catch (e) {
    errs.push(`SKILL.md 不可读：${e.message}`);
  }
  let pkgVersion = null;
  try {
    const pkg = JSON.parse(fs.readFileSync(path.join(dir, 'package.json'), 'utf8'));
    pkgVersion = pkg.version != null ? String(pkg.version).trim() : null;
  } catch (e) {
    errs.push(`package.json 不可读/非法：${e.message}`);
  }
  if (fmVersion == null || fmVersion === '') {
    errs.push('SKILL.md frontmatter 缺 version 字段');
  } else if (pkgVersion == null || pkgVersion === '') {
    errs.push('package.json 缺 version 字段');
  } else if (fmVersion !== pkgVersion) {
    errs.push(`SKILL.md version (${fmVersion}) != package.json version (${pkgVersion})`);
  }
  return errs;
}

function main() {
  const mode = process.argv[2];
  const skills = discoverSkills();
  if (!skills.length) {
    console.error('No skills discovered.');
    process.exit(1);
  }
  console.log(`skills: ${skills.join(', ')}`);

  const versionFailures = [];
  for (const id of skills) {
    const skillDir = path.join(ROOT, id);
    console.log(`\n=== ${mode}: ${id} ===`);

    if (mode === 'check') {
      if (!hasScript(skillDir, 'package_skill.py')) {
        console.log(`skip ${id}: no package_skill.py`);
        continue;
      }
      run(PY, ['scripts/package_skill.py', '--check'], { cwd: skillDir });
    } else if (mode === 'audit') {
      for (const s of ['audit_styles.py', 'audit_docs.py', 'audit_skill.py', 'audit_css.py']) {
        if (!hasScript(skillDir, s)) {
          console.error(`missing ${id}/scripts/${s}`);
          process.exit(1);
        }
      }
      // frontmatter version == package.json version（缺 version 字段也算失败）
      for (const e of checkVersionMatch(id)) {
        console.error(`version gate ✗ ${id}: ${e}`);
        versionFailures.push(`${id}: ${e}`);
      }
      for (const s of ['audit_styles.py', 'audit_docs.py', 'audit_skill.py', 'audit_css.py']) {
        run(PY, [`scripts/${s}`], { cwd: skillDir });
      }
    } else if (mode === 'versions') {
      // 仅做 frontmatter version == package.json version 一致性比对（供 CI 调用）
      for (const e of checkVersionMatch(id)) {
        console.error(`version gate ✗ ${id}: ${e}`);
        versionFailures.push(`${id}: ${e}`);
      }
    } else if (mode === 'package') {
      if (!hasScript(skillDir, 'package_skill.py')) {
        console.log(`skip ${id}: no package_skill.py`);
        continue;
      }
      run(PY, ['scripts/package_skill.py'], { cwd: skillDir });
    } else if (mode === 'install') {
      const lock = path.join(skillDir, 'package-lock.json');
      const pkg = path.join(skillDir, 'package.json');
      if (!fs.existsSync(pkg)) {
        console.log(`skip ${id}: no package.json`);
        continue;
      }
      if (fs.existsSync(lock)) {
        run('npm', ['ci', '--omit=dev'], { cwd: skillDir });
      } else {
        run('npm', ['install', '--omit=dev'], { cwd: skillDir });
      }
    } else {
      console.error(`Unknown mode: ${mode}`);
      process.exit(1);
    }
  }

  if ((mode === 'audit' || mode === 'versions') && versionFailures.length) {
    console.error(`\nversion gate: ${versionFailures.length} 项失败`);
    for (const f of versionFailures) console.error(`  ✗ ${f}`);
    process.exit(1);
  }
}

main();
