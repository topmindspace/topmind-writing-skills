#!/usr/bin/env node
/**
 * topmind-writing-skills 安装器负向测试（零依赖：node 直接可跑）。
 *
 * 覆盖审计报告 严重-2 的两个实测 case，外加正常 --force 回归。
 * 注意 --to 是目标**根目录**，最终落盘 dest = <to>/<skill-id>，守卫按 dest 比对：
 *   1. dest == 技能源目录（--to 指向源目录的父目录，如 --to .）+ --force
 *      → 必须被拒绝（原 bug：rmSync 先删源目录，再"成功"装空目录——数据丢失 + 虚假成功）
 *   2. dest 落在技能源目录内部（--to 指向源目录自身或其子目录）
 *      → 必须被拒绝（原 bug：copyDir 无限递归复制直至 ENAMETOOLONG，留下垃圾目录树）
 *   3. 正常 --force 安装（目标已存在且在源树之外）仍通过
 *
 * 隔离设计：把 bin/topmind-writing-skills.js 复制到临时目录，旁边搭一个假技能树（ROOT 由 bin 位置推导），
 * 即使守卫回归失效，最多删掉 /tmp 下的假目录，绝不碰仓库真技能。
 *
 * 用法：node scripts/test_install_guards.js
 * 任一失败 → 打印 ✗ 并 exit 1。
 */
'use strict';

const { spawnSync } = require('child_process');
const fs = require('fs');
const os = require('os');
const path = require('path');

const REPO_BIN = path.resolve(__dirname, '..', 'bin', 'topmind-writing-skills.js');
let failures = 0;

function ok(cond, msg) {
  console.log((cond ? '  ✓ ' : '  ✗ ') + msg);
  if (!cond) failures++;
}

/** 搭隔离环境：<tmp>/bin/topmind-writing-skills.js + <tmp>/testskill/SKILL.md */
function makeEnv() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tms-install-guard-'));
  fs.mkdirSync(path.join(tmp, 'bin'), { recursive: true });
  fs.copyFileSync(REPO_BIN, path.join(tmp, 'bin', 'topmind-writing-skills.js'));
  const skill = path.join(tmp, 'testskill');
  fs.mkdirSync(skill, { recursive: true });
  fs.writeFileSync(
    path.join(skill, 'SKILL.md'),
    '---\nname: testskill\ndescription: fake skill for installer guard tests\n---\n# testskill\n'
  );
  return { tmp, skill, bin: path.join(tmp, 'bin', 'topmind-writing-skills.js') };
}

function runInstall(env, args, cwd) {
  return spawnSync(process.execPath, [env.bin, 'install', 'testskill', ...args], {
    cwd: cwd || env.tmp,
    encoding: 'utf8',
    timeout: 20000, // 守卫失效导致递归复制时兜底杀掉，避免无限跑
  });
}

function destroy(env) {
  fs.rmSync(env.tmp, { recursive: true, force: true });
}

function main() {
  if (!fs.existsSync(REPO_BIN)) {
    console.error('找不到安装器：' + REPO_BIN);
    process.exit(1);
  }

  // 1. dest == 技能源目录（--to 指向源目录的父目录）→ 必须拒绝，源目录完好
  {
    const env = makeEnv();
    try {
      const r = runInstall(env, ['--to', env.tmp, '--force']); // dest = tmp/testskill == src
      const out = (r.stdout || '') + (r.stderr || '');
      ok(r.status !== 0, 'case1: dest 落在源目录上被拒绝（exit 非 0）');
      ok(fs.existsSync(path.join(env.skill, 'SKILL.md')), 'case1: 源目录未被 rmSync 删除');
      ok(/own directory tree|拒绝|Refusing/i.test(out), 'case1: 报错信息友好（说明原因）');
    } finally {
      destroy(env);
    }
  }

  // 2. dest 落在技能源目录内部（--to 指向源目录自身）→ 必须拒绝，不产生递归垃圾
  {
    const env = makeEnv();
    try {
      const r = runInstall(env, ['--to', env.skill, '--force']); // dest = src/testskill
      ok(r.status !== 0, 'case2: dest 在源目录内部被拒绝（exit 非 0）');
      ok(!fs.existsSync(path.join(env.skill, 'testskill')), 'case2: 未创建递归垃圾目录树');
      ok(fs.existsSync(path.join(env.skill, 'SKILL.md')), 'case2: 源目录完好');
    } finally {
      destroy(env);
    }
  }

  // 2b. 相对路径写法同样被拦截（path.resolve 归一化后比对）
  {
    const env = makeEnv();
    try {
      const r = runInstall(env, ['--to', './testskill', '--force'], env.tmp); // dest = src/testskill
      ok(r.status !== 0, 'case2b: 相对路径 --to ./testskill 被拒绝');
      ok(!fs.existsSync(path.join(env.skill, 'testskill')), 'case2b: 未创建递归垃圾目录树');
    } finally {
      destroy(env);
    }
  }

  // 3. 正常 --force 安装（目标已存在且在源树之外）→ 通过并覆盖
  {
    const env = makeEnv();
    try {
      const destRoot = path.join(env.tmp, 'out');
      const destSkill = path.join(destRoot, 'testskill');
      fs.mkdirSync(destSkill, { recursive: true });
      fs.writeFileSync(path.join(destSkill, 'stale.txt'), 'stale');
      const r = runInstall(env, ['--to', destRoot, '--force']);
      ok(r.status === 0, 'case3: 正常 --force 安装 exit 0');
      ok(!fs.existsSync(path.join(destSkill, 'stale.txt')), 'case3: 旧目标被清空覆盖');
      ok(fs.existsSync(path.join(destSkill, 'SKILL.md')), 'case3: 技能文件已安装');
    } finally {
      destroy(env);
    }
  }

  console.log(failures ? `\n[test_install_guards] ${failures} 项失败` : '\n[test_install_guards] 全部通过');
  process.exit(failures ? 1 : 0);
}

main();
