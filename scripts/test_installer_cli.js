#!/usr/bin/env node
/**
 * topmind-writing-skills 安装器 CLI 负向测试（零依赖：node 直接可跑）。
 *
 * 覆盖 install/uninstall 新行为的负向分支 + 成功路径回归：
 *   1. install 到已存在的技能目录（无 --force）→ 拒绝，报错含已装版本/--force/卸载提示
 *   2. install --force 到已存在目录 → 成功，摘要含 to:/version:/next: 三行
 *   3. uninstall 缺 skill id → 失败并打印用法
 *   4. uninstall 非法 skill id（路径穿越）→ 拒绝
 *   5. uninstall 未安装的技能 → 失败并提示"Nothing to uninstall"，顺带列出该目录已装技能
 *   6. uninstall 目标存在但不是技能目录（无 SKILL.md）→ 拒绝，目录完好
 *   7. uninstall --to 指到包内技能源 → 拒绝，源目录完好
 *   8. uninstall 正常路径：install → uninstall → 目录消失
 *   9. uninstall 未知选项 → 失败
 *  10. install 未知选项 → 失败
 *  11. uninstall --to 经符号链接指向包根 → 拒绝，源目录完好（realpath 守卫）
 *  12. install --force --to 经符号链接指向包根 → 拒绝，源目录完好
 *
 * 隔离设计：把 bin/topmind-writing-skills.js 复制到临时目录，旁边搭假技能树，
 * 最多删 /tmp 下的假目录，绝不碰仓库真技能。
 *
 * 用法：node scripts/test_installer_cli.js
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

function noTraceback(out) {
  return !/Traceback|^\s+at\s/m.test(out);
}

/** 搭隔离环境：<tmp>/bin/topmind-writing-skills.js + <tmp>/testskill/SKILL.md（version: 9.9.9） */
function makeEnv() {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'tms-install-cli-'));
  fs.mkdirSync(path.join(tmp, 'bin'), { recursive: true });
  fs.copyFileSync(REPO_BIN, path.join(tmp, 'bin', 'topmind-writing-skills.js'));
  const skill = path.join(tmp, 'testskill');
  fs.mkdirSync(skill, { recursive: true });
  fs.writeFileSync(
    path.join(skill, 'SKILL.md'),
    '---\nname: testskill\nversion: 9.9.9\ndescription: fake skill for installer cli tests\n---\n# testskill\n'
  );
  return { tmp, skill, bin: path.join(tmp, 'bin', 'topmind-writing-skills.js') };
}

function runCli(env, args, cwd) {
  return spawnSync(process.execPath, [env.bin, ...args], {
    cwd: cwd || env.tmp,
    encoding: 'utf8',
    timeout: 20000,
  });
}

function out(r) {
  return (r.stdout || '') + (r.stderr || '');
}

function destroy(env) {
  fs.rmSync(env.tmp, { recursive: true, force: true });
}

function main() {
  if (!fs.existsSync(REPO_BIN)) {
    console.error('找不到安装器：' + REPO_BIN);
    process.exit(1);
  }

  // 1. install 到已存在目录（无 --force）→ 拒绝：报已装版本，要求 --force
  {
    const env = makeEnv();
    try {
      const destRoot = path.join(env.tmp, 'out');
      const destSkill = path.join(destRoot, 'testskill');
      fs.mkdirSync(destSkill, { recursive: true });
      fs.writeFileSync(
        path.join(destSkill, 'SKILL.md'),
        '---\nname: testskill\nversion: 1.0.0\n---\n# stale copy\n'
      );
      fs.writeFileSync(path.join(destSkill, 'stale.txt'), 'stale');
      const r = runCli(env, ['install', 'testskill', '--to', destRoot]);
      const o = out(r);
      ok(r.status !== 0, 'case1: 已存在目录无 --force 被拒绝（exit 非 0）');
      ok(/installed version:\s*1\.0\.0/.test(o), 'case1: 报错含已装版本号 1.0.0');
      ok(/--force/.test(o), 'case1: 报错提示 --force');
      ok(/uninstall/.test(o), 'case1: 报错提示可先 uninstall');
      ok(noTraceback(o), 'case1: 无 Traceback/堆栈');
      ok(fs.existsSync(path.join(destSkill, 'stale.txt')), 'case1: 旧目录未被改动');
    } finally {
      destroy(env);
    }
  }

  // 2. install --force → 成功，摘要三行齐全
  {
    const env = makeEnv();
    try {
      const destRoot = path.join(env.tmp, 'out');
      const destSkill = path.join(destRoot, 'testskill');
      fs.mkdirSync(destSkill, { recursive: true });
      fs.writeFileSync(path.join(destSkill, 'stale.txt'), 'stale');
      const r = runCli(env, ['install', 'testskill', '--to', destRoot, '--force']);
      const o = out(r);
      ok(r.status === 0, 'case2: --force 安装 exit 0');
      ok(/^\s*to:\s*\S+/m.test(o), 'case2: 摘要有 to: 行（装到哪里）');
      ok(/^\s*version:\s*skill 9\.9\.9/m.test(o), 'case2: 摘要有 version: 行（含技能版本）');
      ok(/^\s*next:\s*\S+/m.test(o), 'case2: 摘要有 next: 行（下一步）');
      ok(!fs.existsSync(path.join(destSkill, 'stale.txt')), 'case2: 旧目标被清空覆盖');
    } finally {
      destroy(env);
    }
  }

  // 3. uninstall 缺 skill id
  {
    const env = makeEnv();
    try {
      const r = runCli(env, ['uninstall']);
      const o = out(r);
      ok(r.status !== 0, 'case3: uninstall 缺 skill id（exit 非 0）');
      ok(/Missing skill id/.test(o) && noTraceback(o), 'case3: 提示缺 id 且无 Traceback');
    } finally {
      destroy(env);
    }
  }

  // 4. uninstall 非法 skill id（路径穿越）
  {
    const env = makeEnv();
    try {
      const r = runCli(env, ['uninstall', '../evil', '--to', path.join(env.tmp, 'out')]);
      const o = out(r);
      ok(r.status !== 0, 'case4: 非法 skill id 被拒绝（exit 非 0）');
      ok(/Invalid skill id/.test(o) && noTraceback(o), 'case4: 报错友好无 Traceback');
    } finally {
      destroy(env);
    }
  }

  // 5. uninstall 未安装的技能 → 干净报错，并列出该目录已装技能
  {
    const env = makeEnv();
    try {
      const destRoot = path.join(env.tmp, 'out');
      const other = path.join(destRoot, 'otherskill');
      fs.mkdirSync(other, { recursive: true });
      fs.writeFileSync(path.join(other, 'SKILL.md'), '---\nname: otherskill\nversion: 2.0.0\n---\n');
      const r = runCli(env, ['uninstall', 'testskill', '--to', destRoot]);
      const o = out(r);
      ok(r.status !== 0, 'case5: 未安装技能 exit 非 0');
      ok(/Nothing to uninstall/.test(o), 'case5: 报错说明未安装');
      ok(/installed here: otherskill/.test(o), 'case5: 列出该目录已装技能');
      ok(noTraceback(o), 'case5: 无 Traceback');
    } finally {
      destroy(env);
    }
  }

  // 6. uninstall 目标存在但不是技能目录 → 拒绝，目录完好
  {
    const env = makeEnv();
    try {
      const destRoot = path.join(env.tmp, 'out');
      const destSkill = path.join(destRoot, 'testskill');
      fs.mkdirSync(destSkill, { recursive: true });
      fs.writeFileSync(path.join(destSkill, 'notes.txt'), 'user data');
      const r = runCli(env, ['uninstall', 'testskill', '--to', destRoot]);
      const o = out(r);
      ok(r.status !== 0, 'case6: 非技能目录被拒绝删除（exit 非 0）');
      ok(/not a skill directory/.test(o), 'case6: 报错说明原因');
      ok(fs.existsSync(path.join(destSkill, 'notes.txt')), 'case6: 用户目录完好');
      ok(noTraceback(o), 'case6: 无 Traceback');
    } finally {
      destroy(env);
    }
  }

  // 7. uninstall --to 指到包内（dest == 技能源目录）→ 拒绝，源完好
  {
    const env = makeEnv();
    try {
      const r = runCli(env, ['uninstall', 'testskill', '--to', env.tmp]); // dest == src
      const o = out(r);
      ok(r.status !== 0, 'case7: --to 指到技能源目录被拒绝（exit 非 0）');
      ok(fs.existsSync(path.join(env.skill, 'SKILL.md')), 'case7: 源目录未被删除');
      ok(/own directory tree|Refusing/i.test(o), 'case7: 报错友好无 Traceback');
    } finally {
      destroy(env);
    }
  }

  // 8. 正常路径：install → uninstall → 目录消失
  {
    const env = makeEnv();
    try {
      const destRoot = path.join(env.tmp, 'out');
      const destSkill = path.join(destRoot, 'testskill');
      let r = runCli(env, ['install', 'testskill', '--to', destRoot]);
      ok(r.status === 0, 'case8: install 成功');
      r = runCli(env, ['uninstall', 'testskill', '--to', destRoot]);
      const o = out(r);
      ok(r.status === 0, 'case8: uninstall exit 0');
      ok(/Uninstalled testskill/.test(o), 'case8: 打印卸载确认');
      ok(!fs.existsSync(destSkill), 'case8: 技能目录已删除');
      ok(fs.existsSync(destRoot), 'case8: 目标根目录保留（只删技能目录）');
    } finally {
      destroy(env);
    }
  }

  // 9. uninstall 未知选项
  {
    const env = makeEnv();
    try {
      const r = runCli(env, ['uninstall', 'testskill', '--bogus']);
      ok(r.status !== 0, 'case9: uninstall 未知选项 exit 非 0');
      ok(noTraceback(out(r)), 'case9: 无 Traceback');
    } finally {
      destroy(env);
    }
  }

  // 10. install 未知选项
  {
    const env = makeEnv();
    try {
      const r = runCli(env, ['install', 'testskill', '--bogus']);
      ok(r.status !== 0, 'case10: install 未知选项 exit 非 0');
      ok(noTraceback(out(r)), 'case10: 无 Traceback');
    } finally {
      destroy(env);
    }
  }

  // 11. uninstall --to 经符号链接指向包根 → 拒绝（词法比对会被绕过），源完好
  {
    const env = makeEnv();
    try {
      const link = path.join(env.tmp, 'linkroot');
      try {
        fs.symlinkSync(env.tmp, link, 'dir');
      } catch (e) {
        ok(false, 'case11: 创建符号链接失败（' + e.message + '），跳过本用例');
      }
      if (fs.existsSync(link)) {
        const r = runCli(env, ['uninstall', 'testskill', '--to', link]);
        const o = out(r);
        ok(r.status !== 0, 'case11: --to 符号链接指向包根被拒绝（exit 非 0）');
        ok(fs.existsSync(path.join(env.skill, 'SKILL.md')), 'case11: 源目录未被删除');
        ok(noTraceback(o), 'case11: 无 Traceback');
      }
    } finally {
      destroy(env);
    }
  }

  // 12. install --force --to 经符号链接指向包根 → 拒绝，源完好（防删源后虚假成功）
  {
    const env = makeEnv();
    try {
      const link = path.join(env.tmp, 'linkroot');
      try {
        fs.symlinkSync(env.tmp, link, 'dir');
      } catch (e) {
        ok(false, 'case12: 创建符号链接失败（' + e.message + '），跳过本用例');
      }
      if (fs.existsSync(link)) {
        const r = runCli(env, ['install', 'testskill', '--to', link, '--force']);
        const o = out(r);
        ok(r.status !== 0, 'case12: install --force 经符号链接指包内被拒绝（exit 非 0）');
        ok(fs.existsSync(path.join(env.skill, 'SKILL.md')), 'case12: 源目录未被删除');
        ok(noTraceback(o), 'case12: 无 Traceback');
      }
    } finally {
      destroy(env);
    }
  }

  // 13. install --to 经 .. 穿越归一化后 == 技能源目录 → 拒绝，源完好
  {
    const env = makeEnv();
    try {
      const r = runCli(env, ['install', 'testskill', '--to', path.join(env.tmp, 'out', '..', 'testskill')]);
      const o = out(r);
      ok(r.status !== 0, 'case13: --to 经 .. 归一化==源目录被拒绝（exit 非 0）');
      ok(fs.existsSync(path.join(env.skill, 'SKILL.md')), 'case13: 源目录未被删除');
      ok(/own directory tree|Refusing/i.test(o) && noTraceback(o), 'case13: 报错友好无 Traceback');
    } finally {
      destroy(env);
    }
  }

  // 14. uninstall --to 经 .. 穿越到包外 → 不误杀（守卫放行，报未安装）
  {
    const env = makeEnv();
    try {
      const r = runCli(env, ['uninstall', 'testskill', '--to', path.join(env.tmp, 'evil', '..', '..', 'tms-outside-' + path.basename(env.tmp))]);
      const o = out(r);
      ok(r.status !== 0, 'case14: --to 经 .. 到包外 exit 非 0');
      ok(/Nothing to uninstall/.test(o), 'case14: 守卫未误杀（报未安装而非拒绝）');
      ok(noTraceback(o), 'case14: 无 Traceback');
    } finally {
      destroy(env);
    }
  }

  // 15. install --to 指向技能目录内部的子目录 → 拒绝（防递归复制），源完好无垃圾
  {
    const env = makeEnv();
    try {
      const sub = path.join(env.skill, 'subdir');
      const r = runCli(env, ['install', 'testskill', '--to', sub]);
      const o = out(r);
      ok(r.status !== 0, 'case15: --to=技能内子目录被拒绝（exit 非 0）');
      ok(fs.existsSync(path.join(env.skill, 'SKILL.md')), 'case15: 源目录未被删除');
      ok(!fs.existsSync(path.join(sub, 'testskill')), 'case15: 未留下递归复制垃圾');
      ok(/own directory tree|Refusing/i.test(o) && noTraceback(o), 'case15: 报错友好无 Traceback');
    } finally {
      destroy(env);
    }
  }

  // 16. install --to 指向包根本身（dest == 技能源目录）→ 拒绝，源完好
  {
    const env = makeEnv();
    try {
      const r = runCli(env, ['install', 'testskill', '--to', env.tmp]); // dest == src
      const o = out(r);
      ok(r.status !== 0, 'case16: --to=包根（dest==源）install 被拒绝（exit 非 0）');
      ok(fs.existsSync(path.join(env.skill, 'SKILL.md')), 'case16: 源目录未被删除');
      ok(/own directory tree|Refusing/i.test(o) && noTraceback(o), 'case16: 报错友好无 Traceback');
    } finally {
      destroy(env);
    }
  }

  // 17. install --to 经符号链接（带不存在的尾巴）指向技能目录内 → 拒绝，源完好
  //     覆盖 realOrResolved() 的"最深存在祖先解析+拼回尾巴"分支
  {
    const env = makeEnv();
    try {
      const link = path.join(env.tmp, 'linkskill');
      try {
        fs.symlinkSync(env.skill, link, 'dir');
      } catch (e) {
        ok(false, 'case17: 创建符号链接失败（' + e.message + '），跳过本用例');
      }
      if (fs.existsSync(link)) {
        const r = runCli(env, ['install', 'testskill', '--to', path.join(link, 'nonexistent-tail')]);
        const o = out(r);
        ok(r.status !== 0, 'case17: 链接+不存在尾巴指技能内被拒绝（exit 非 0）');
        ok(fs.existsSync(path.join(env.skill, 'SKILL.md')), 'case17: 源目录未被删除');
        ok(noTraceback(o), 'case17: 无 Traceback');
      }
    } finally {
      destroy(env);
    }
  }

  // 18. install --to 为包内文件的硬链接 → 干净失败（fail-closed），源完好
  //     硬链接是"另一条路径"，守卫按路径比对放行是正确的；mkdirSync 遇到文件走"无法创建目录"分支
  {
    const env = makeEnv();
    try {
      const hl = path.join(env.tmp, 'hlfile');
      try {
        fs.linkSync(path.join(env.skill, 'SKILL.md'), hl);
      } catch (e) {
        ok(false, 'case18: 创建硬链接失败（' + e.message + '），跳过本用例');
      }
      if (fs.existsSync(hl)) {
        const r = runCli(env, ['install', 'testskill', '--to', hl]);
        const o = out(r);
        ok(r.status !== 0, 'case18: --to=包内文件硬链接 install 被拒绝（exit 非 0）');
        ok(fs.existsSync(path.join(env.skill, 'SKILL.md')), 'case18: 源目录未被删除');
        ok(/Cannot create install directory/.test(o) && noTraceback(o), 'case18: 报错友好无 Traceback');
      }
    } finally {
      destroy(env);
    }
  }

  // 19. uninstall --to 经符号链接直接 == 技能源目录 → 拒绝，源完好
  {
    const env = makeEnv();
    try {
      const link = path.join(env.tmp, 'linkskilldir');
      try {
        fs.symlinkSync(env.skill, link, 'dir');
      } catch (e) {
        ok(false, 'case19: 创建符号链接失败（' + e.message + '），跳过本用例');
      }
      if (fs.existsSync(link)) {
        const r = runCli(env, ['uninstall', 'testskill', '--to', link]); // dest 经链接 == src
        const o = out(r);
        ok(r.status !== 0, 'case19: --to 经链接==源目录 uninstall 被拒绝（exit 非 0）');
        ok(fs.existsSync(path.join(env.skill, 'SKILL.md')), 'case19: 源目录未被删除');
        ok(/own directory tree|Refusing/i.test(o) && noTraceback(o), 'case19: 报错友好无 Traceback');
      }
    } finally {
      destroy(env);
    }
  }

  // 20. install 侧 skill id 路径穿越 → 拒绝
  {
    const env = makeEnv();
    try {
      const r = runCli(env, ['install', '../evil', '--to', path.join(env.tmp, 'out')]);
      const o = out(r);
      ok(r.status !== 0, 'case20: install 非法 skill id 被拒绝（exit 非 0）');
      ok(/Invalid skill id/.test(o) && noTraceback(o), 'case20: 报错友好无 Traceback');
    } finally {
      destroy(env);
    }
  }

  // 21. install --to 相对路径（cwd 在包内）指向技能自身 → 拒绝
  {
    const env = makeEnv();
    try {
      const r = runCli(env, ['install', 'testskill', '--to', 'testskill']); // 相对路径，cwd=env.tmp
      const o = out(r);
      ok(r.status !== 0, 'case21: 相对路径 --to==源目录被拒绝（exit 非 0）');
      ok(fs.existsSync(path.join(env.skill, 'SKILL.md')), 'case21: 源目录未被删除');
      ok(/own directory tree|Refusing/i.test(o) && noTraceback(o), 'case21: 报错友好无 Traceback');
    } finally {
      destroy(env);
    }
  }

  // 22. install --force 时 dest 是指向包外的符号链接 → 只删链接本身，不跟随删目标
  {
    const env = makeEnv();
    try {
      const outside = path.join(env.tmp, 'realdir');
      fs.mkdirSync(outside, { recursive: true });
      fs.writeFileSync(path.join(outside, 'keep.txt'), 'keep');
      const to = path.join(env.tmp, 't');
      fs.mkdirSync(to, { recursive: true });
      let linked = false;
      try {
        fs.symlinkSync(outside, path.join(to, 'testskill'), 'dir');
        linked = true;
      } catch (e) {
        ok(false, 'case22: 创建符号链接失败（' + e.message + '），跳过本用例');
      }
      if (linked) {
        const r = runCli(env, ['install', 'testskill', '--to', to, '--force']);
        const o = out(r);
        const destStat = fs.lstatSync(path.join(to, 'testskill'));
        ok(r.status === 0, 'case22: install --force 成功（exit 0）');
        ok(fs.existsSync(path.join(outside, 'keep.txt')), 'case22: 链接目标目录完好（未被跟随删除）');
        ok(destStat.isDirectory() && !destStat.isSymbolicLink(), 'case22: dest 已是真实目录（链接被替换）');
        ok(noTraceback(o), 'case22: 无 Traceback');
      }
    } finally {
      destroy(env);
    }
  }

  console.log(failures ? `\n[test_installer_cli] ${failures} 项失败` : '\n[test_installer_cli] 全部通过');
  process.exit(failures ? 1 : 0);
}

main();
