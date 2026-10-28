#!/usr/bin/env node
/**
 * topmind-writing-skills — TopMindspace agent skills installer
 *
 * Recommended channel (when published): npm @topmindspace/topmind-writing-skills
 * GitHub npx remains available for HEAD / offline clone.
 *
 * Usage:
 *   npx @topmindspace/topmind-writing-skills list
 *   npx @topmindspace/topmind-writing-skills install topmind-briefs
 *   npx @topmindspace/topmind-writing-skills install topmind-briefs --to ./skills-out
 *   npx @topmindspace/topmind-writing-skills install topmind-briefs --force
 *   npx @topmindspace/topmind-writing-skills uninstall topmind-briefs --to ./skills-out
 *   npx github:topmindspace/topmind-writing-skills install topmind-briefs   # follow repo HEAD
 */
'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const ROOT = path.resolve(__dirname, '..');
// Skills live at repo root (one directory per skill with SKILL.md).
const INFRA_DIRS = new Set(['bin', 'docs', 'scripts', 'shared', 'evals', 'node_modules', 'dist', 'release-assets']);
const SKILL_ID_RE = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const INSTALL_RECORD = '.topmind-install.json';

function die(msg, code = 1) {
  console.error(msg);
  process.exit(code);
}

function skillDir(skillId) {
  return path.join(ROOT, skillId);
}

function assertSkillId(skillId) {
  if (!skillId || typeof skillId !== 'string') {
    die('Missing skill id.\n\n' + usageText());
  }
  if (
    skillId.includes('..') ||
    skillId.includes('/') ||
    skillId.includes('\\') ||
    path.isAbsolute(skillId) ||
    !SKILL_ID_RE.test(skillId)
  ) {
    die(
      `Invalid skill id: ${JSON.stringify(skillId)}\n` +
        'Skill ids must match ^[a-z0-9]+(?:-[a-z0-9]+)*$ (no paths, dots, or slashes).'
    );
  }
}

function listSkillIds() {
  return fs
    .readdirSync(ROOT, { withFileTypes: true })
    .filter((d) => d.isDirectory() && !INFRA_DIRS.has(d.name) && !d.name.startsWith('.'))
    .filter((d) => fs.existsSync(path.join(ROOT, d.name, 'SKILL.md')))
    .map((d) => d.name)
    .sort();
}

function readSkillMeta(skillId) {
  const skillPath = skillDir(skillId);
  const skillMd = path.join(skillPath, 'SKILL.md');
  if (!fs.existsSync(skillMd)) return { id: skillId, description: '' };
  const text = fs.readFileSync(skillMd, 'utf8');
  const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
  if (!m) return { id: skillId, description: '' };
  const fm = m[1];
  let desc = '';
  // 块标量：description: >- / > / | / |- 后跟缩进行
  const block = fm.match(/^description:\s*[>|][-+]?\s*$/m);
  if (block) {
    const lines = [];
    // slice 起点是 description 行尾，split 后首元素恒为空，直接丢掉
    const rest = fm.slice(block.index + block[0].length).split(/\r?\n/).slice(1);
    for (const ln of rest) {
      if (/^[ \t]+\S/.test(ln)) lines.push(ln.trim()); // 缩进的内容行
      else break; // 空行或顶格行 → 块结束
    }
    const folded = /^description:\s*>/.test(block[0]);
    desc = folded ? lines.join(' ') : lines.join('\n');
  } else {
    desc = ((fm.match(/^description:\s*"(.*)"\s*$/m) || fm.match(/^description:\s*(.+)\s*$/m) || [])[1] || '');
  }
  return { id: skillId, description: String(desc).slice(0, 120) };
}

/** 读技能目录下 SKILL.md frontmatter 的 version 字段（读不到返回 ''，调用方兜底）。 */
function readSkillVersion(skillPath) {
  try {
    const p = path.join(skillPath, 'SKILL.md');
    if (!fs.existsSync(p)) return '';
    const text = fs.readFileSync(p, 'utf8');
    const m = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    if (!m) return '';
    // 新格式在 metadata.version（Agent Skills 规范），旧格式在顶层 version，两种都认
    const v = m[1].match(/^metadata:\s*\n(?:[ \t]+.*\n)*?[ \t]+version:\s*(.+?)\s*$/m) || m[1].match(/^version:\s*(.+?)\s*$/m);
    return v ? v[1].replace(/^["']|["']$/g, '') : '';
  } catch {
    return '';
  }
}

function installerVersion() {
  try {
    const pkg = JSON.parse(fs.readFileSync(path.join(ROOT, 'package.json'), 'utf8'));
    return pkg.version || 'unknown';
  } catch {
    return 'unknown';
  }
}

function resolveDefaultTarget() {
  const home = process.env.HOME || process.env.USERPROFILE || '';
  const candidates = [...new Set([
    path.join(process.cwd(), '.agents', 'skills'),
    path.join(process.cwd(), '.claude', 'skills'),
    path.join(process.cwd(), '.cursor', 'skills'),
    path.join(process.cwd(), '.codex', 'skills'),
    path.join(process.cwd(), '.mimocode', 'skills'),
    path.join(home, '.claude', 'skills'),
    path.join(home, '.agents', 'skills'),
    path.join(home, '.cursor', 'skills'),
    path.join(home, '.codex', 'skills'),
  ])];
  const choose = (paths) => {
    if (paths.length === 1) return paths[0];
    if (paths.length > 1) die(`More than one skill directory matches:\n  ${paths.join('\n  ')}\nChoose one with --to <dir>.`);
    return null;
  };
  // Prefer the user's existing TopMind installation, then an existing skills
  // directory, then a single host configuration. A mere cwd is not a signal.
  const ids = listSkillIds();
  const withTopmind = candidates.filter((dir) => ids.some((id) => fs.existsSync(path.join(dir, id, 'SKILL.md'))));
  const withSkills = candidates.filter((dir) => fs.existsSync(dir));
  const withHost = candidates.filter((dir) => fs.existsSync(path.dirname(dir)) && path.dirname(dir) !== process.cwd() && path.dirname(dir) !== home);
  for (const group of [withTopmind, withSkills, withHost]) {
    const selected = choose(group);
    if (selected) return selected;
  }
  // No host exists yet: use the cross-agent project convention explicitly.
  return path.join(process.cwd(), '.agents', 'skills');
}

function readSkillName(skillPath) {
  try {
    const text = fs.readFileSync(path.join(skillPath, 'SKILL.md'), 'utf8');
    const fm = text.match(/^---\r?\n([\s\S]*?)\r?\n---/);
    return (fm && fm[1].match(/^name:\s*([a-z0-9-]+)\s*$/m) || [])[1] || '';
  } catch { return ''; }
}

function skipGeneratedEntry(entry) {
  return (entry.isDirectory() && ['node_modules', 'dist', '__pycache__'].includes(entry.name)) ||
    (entry.isFile() && entry.name.endsWith('.pyc'));
}

function skillDigest(skillPath) {
  const hash = crypto.createHash('sha256');
  const walk = (dir, relative = '') => {
    for (const entry of fs.readdirSync(dir, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      if (!relative && entry.name === INSTALL_RECORD) continue;
      if (skipGeneratedEntry(entry)) continue;
      const rel = path.join(relative, entry.name);
      const absolute = path.join(dir, entry.name);
      if (entry.isDirectory()) {
        walk(absolute, rel);
      } else {
        hash.update(rel.replace(/\\/g, '/') + '\0');
        if (entry.isFile()) hash.update(fs.readFileSync(absolute));
        else hash.update(`non-regular:${entry.name}`);
        hash.update('\0');
      }
    }
  };
  walk(skillPath);
  return hash.digest('hex');
}

function installedState(skillId, targetRoot) {
  const dest = path.join(targetRoot, skillId);
  let stat;
  try { stat = fs.lstatSync(dest); } catch (error) {
    if (error.code === 'ENOENT' || error.code === 'ENOTDIR') return { kind: 'missing', version: '' };
    throw error;
  }
  if (!stat.isDirectory() || readSkillName(dest) !== skillId) return { kind: 'conflict', version: '' };
  const version = readSkillVersion(dest);
  const recordPath = path.join(dest, INSTALL_RECORD);
  if (!fs.existsSync(recordPath)) return { kind: 'legacy', version };
  try {
    const record = JSON.parse(fs.readFileSync(recordPath, 'utf8'));
    if (record.id === skillId && record.digest === skillDigest(dest)) return { kind: 'managed', version };
  } catch { /* Treat unreadable records as local changes. */ }
  return { kind: 'modified', version };
}

function copyDir(src, dest) {
  fs.mkdirSync(dest, { recursive: true });
  for (const entry of fs.readdirSync(src, { withFileTypes: true })) {
    const s = path.join(src, entry.name);
    const d = path.join(dest, entry.name);
    if (entry.isDirectory()) {
      if (skipGeneratedEntry(entry)) continue;
      copyDir(s, d);
    } else if (entry.isFile()) {
      if (skipGeneratedEntry(entry)) continue;
      fs.copyFileSync(s, d);
    } else {
      console.warn(`warning: skipping non-regular file: ${s}`);
    }
  }
}

function normPath(p) {
  const s = path.resolve(p);
  return process.platform === 'win32' ? s.toLowerCase() : s;
}

/** realpath 能解析就解析（跟符号链接），失败回退 path.resolve。
 *  dest 可能还不存在（install 流程）：往上找最深存在的祖先解析后再拼回。
 *  否则 --to 经符号链接指向包内时，词法比对会被绕过（rmSync 会跟链接删掉源）。 */
function realOrResolved(p) {
  let cur = path.resolve(p);
  const tail = [];
  for (;;) {
    try {
      return path.join(fs.realpathSync(cur), ...tail);
    } catch {
      const parent = path.dirname(cur);
      if (parent === cur) return path.join(cur, ...tail);
      tail.unshift(path.basename(cur));
      cur = parent;
    }
  }
}

/** 安装目标守卫（审计 严重-2）：
 *  dest == 技能源目录  → --force 会先 rmSync 删掉源目录，再"成功"装出空目录（数据丢失 + 虚假成功）；
 *  dest 在源目录内部  → copyDir 无限递归复制直至 ENAMETOOLONG，并留下垃圾目录树。
 *  realpath 归一化后比对（dest === src，或 dest 以 src + 路径分隔符开头），
 *  防止 --to 经符号链接指向包内绕过词法比对；
 *  Windows 下额外做大小写归一。无论是否 --force，一律拒绝。
 */
function assertDestOutsideSource(src, dest) {
  const absSrc = normPath(realOrResolved(src));
  const absDest = normPath(realOrResolved(dest));
  if (absDest === absSrc || absDest.startsWith(absSrc + path.sep)) {
    die(
      `Refusing to install into the skill's own directory tree.\n` +
        `  skill source: ${absSrc}\n` +
        `  destination:  ${absDest}\n` +
        `Choose a --to directory outside the skill source ` +
        `(installing into it would delete or recurse into the source).`
    );
  }
}

/** 比较版本 a 与 b：a>b 返回 1，相等 0，a<b -1。b 缺失或解析不了视为最旧（返回 1）。 */
function parseVer(v) {
  const m = String(v || '').trim().replace(/^["']|["']$/g, '').replace(/^v/, '').match(/^(\d+)\.(\d+)\.(\d+)/);
  return m ? m.slice(1, 4).map(Number) : null;
}
function compareVersions(a, b) {
  const pa = parseVer(a);
  const pb = parseVer(b);
  if (!pb) return 1;
  if (!pa) return -1;
  for (let i = 0; i < 3; i++) if (pa[i] !== pb[i]) return pa[i] > pb[i] ? 1 : -1;
  return 0;
}

function planInstall(skillId, targetRoot, force) {
  assertSkillId(skillId);
  const src = skillDir(skillId);
  if (!fs.existsSync(path.join(src, 'SKILL.md'))) {
    die(`Skill not found: ${skillId}\nAvailable: ${listSkillIds().join(', ') || '(none)'}`);
  }
  const dest = path.join(targetRoot, skillId);
  assertDestOutsideSource(src, dest);
  const state = installedState(skillId, targetRoot);
  if (state.kind === 'conflict') die(`Refusing to replace ${dest}: it is not a ${skillId} skill directory.`);
  if (state.kind === 'modified' && !force) {
    die(`Local changes found in ${dest}. Keep them or pass --force to replace; the previous copy will be retained.`);
  }
  const packageVer = readSkillVersion(src) || 'unknown';
  const cmp = compareVersions(packageVer, state.version);
  if (state.kind !== 'missing' && !force && cmp < 0) {
    die(`Installed ${skillId} ${state.version} is newer than packaged ${packageVer}; not downgrading. Pass --force (or -f) to downgrade.`);
  }
  return { src, dest, state, packageVer, cmp };
}

function install(skillId, targetRoot, { force = false, defaultTarget = false } = {}) {
  const { src, dest, state, cmp } = planInstall(skillId, targetRoot, force);
  if (state.kind !== 'missing' && !force && cmp === 0) {
    console.log(`Already up to date: ${skillId} ${state.version} (use --force to reinstall)`);
    console.log(`  at:      ${dest}`);
    return;
  }
  try {
    fs.mkdirSync(targetRoot, { recursive: true });
  } catch (e) {
    die(
      `Cannot create install directory: ${targetRoot}\n` +
        `  reason: ${e.message}\n` +
        'Choose a --to directory that can be created (not a file, not unwritable).'
    );
  }
  const upgradedFrom = state.kind !== 'missing' && cmp > 0 ? state.version || 'unknown' : null;
  const retainPrevious = state.kind === 'legacy' || state.kind === 'modified';
  const stage = fs.mkdtempSync(path.join(targetRoot, `.${skillId}-stage-`));
  let previous = null;
  try {
    copyDir(src, stage);
    fs.writeFileSync(path.join(stage, INSTALL_RECORD), JSON.stringify({
      id: skillId,
      version: readSkillVersion(src),
      digest: skillDigest(stage),
    }, null, 2) + '\n');
    if (state.kind !== 'missing') {
      previous = fs.mkdtempSync(path.join(targetRoot, `.${skillId}-previous-`));
      fs.rmdirSync(previous);
      fs.renameSync(dest, previous);
    }
    try { fs.renameSync(stage, dest); }
    catch (error) { if (previous) { fs.renameSync(previous, dest); previous = null; } throw error; }
    if (previous && !retainPrevious) {
      try { fs.rmSync(previous, { recursive: true, force: true }); }
      catch { console.warn(`Previous copy retained at: ${previous}`); }
    }
  } catch (error) {
    fs.rmSync(stage, { recursive: true, force: true });
    die(`Install failed; the previous installed skill was retained. ${error.message}`);
  } finally { fs.rmSync(stage, { recursive: true, force: true }); }
  // 安装摘要三行：装到哪里 / 装了什么版本 / 下一步。
  const toNote = defaultTarget ? '  (default, auto-detected — no --to given)' : '';
  const skillVer = readSkillVersion(dest) || 'unknown';
  if (upgradedFrom) console.log(`Upgraded ${skillId} ${upgradedFrom} -> ${skillVer}`);
  else console.log(`Installed ${skillId}`);
  console.log(`  to:      ${dest}${toNote}`);
  console.log(`  version: skill ${skillVer} (installer ${installerVersion()})`);
  if (previous && retainPrevious) console.log(`  backup:  ${previous} (previous untracked or locally changed copy)`);
  console.log(`  next:    ${nextStep(skillId, dest)}`);
}

function status(targetRoot) {
  console.log(`Skill directory: ${targetRoot}`);
  console.log('Packaged version | Installed version | State | Skill');
  for (const id of listSkillIds()) {
    const packaged = readSkillVersion(skillDir(id)) || 'unknown';
    const state = installedState(id, targetRoot);
    let label = state.kind;
    if (state.kind === 'managed' || state.kind === 'legacy') {
      const cmp = compareVersions(packaged, state.version);
      label = cmp > 0 ? 'update available' : cmp < 0 ? 'installed newer' : state.kind === 'legacy' ? 'untracked' : 'current';
    }
    console.log(`${packaged} | ${state.version || '—'} | ${label} | ${id}`);
  }
}

function nextStep(skillId, dest) {
  return 'restart your agent so it picks up the skill';
}

/** 列出目标根目录下已安装的技能（有 SKILL.md 的子目录）。 */
function listInstalledIds(targetRoot) {
  try {
    return fs
      .readdirSync(targetRoot, { withFileTypes: true })
      .filter((d) => d.isDirectory() && fs.existsSync(path.join(targetRoot, d.name, 'SKILL.md')))
      .map((d) => d.name)
      .sort();
  } catch {
    return [];
  }
}

function uninstall(skillId, targetRoot) {
  assertSkillId(skillId);
  const src = skillDir(skillId);
  const dest = path.join(targetRoot, skillId);
  // 守卫：--to 指到包内时，dest 会命中安装器自带的技能源目录 → 一律拒绝，
  // 防止把仓库自身的技能目录删掉（同 install 的 assertDestOutsideSource）。
  if (fs.existsSync(path.join(src, 'SKILL.md'))) {
    assertDestOutsideSource(src, dest);
  }
  if (!fs.existsSync(dest)) {
    const installed = listInstalledIds(targetRoot);
    die(
      `Nothing to uninstall: ${dest}\n` +
        `  skill '${skillId}' is not installed under ${targetRoot}.` +
        (installed.length ? `\n  installed here: ${installed.join(', ')}` : '')
    );
  }
  if (!fs.existsSync(path.join(dest, 'SKILL.md'))) {
    die(
      `Refusing to uninstall: ${dest}\n` +
        `  not a skill directory (missing SKILL.md) — will not delete arbitrary folders.`
    );
  }
  fs.rmSync(dest, { recursive: true, force: true });
  console.log(`Uninstalled ${skillId}`);
  console.log(`  from ${dest}`);
}

function usageText() {
  return `topmind-writing-skills — install TopMindspace agent skills

Usage:
  topmind-writing-skills list|ls
  topmind-writing-skills status [--to|-t <dir>]
  topmind-writing-skills install <skill-id|all> [--to|-t <dir>] [--force|-f]
  topmind-writing-skills update [skill-id|all] [--to|-t <dir>] [--force|-f]
  topmind-writing-skills uninstall <skill-id> [--to|-t <dir>]
  topmind-writing-skills help

Behavior:
  status     compares the local package with skills installed in <dir>.
  install    installs one skill or all eight; newer packaged versions upgrade
             existing copies. Equal versions are left alone. A newer installed
             version requires --force. Locally changed managed copies are kept
             unless --force is explicit. Untracked older copies are backed up
             during upgrade. The replacement is staged before switching.
  update     upgrades only installed skills (all by default); does not add new ones.
  uninstall  removes <dir>/<skill-id>/ (refuses: not installed, not a skill
             directory, or the package's own skill source).
  No --to: choose a single existing TopMind installation, skills directory or
  host configuration. Ambiguous matches require --to. With no host configured,
  use ./.agents/skills and print the chosen location.

Target probe order (no --to): ./.agents/skills, ./.claude/skills,
  ./.cursor/skills, ./.codex/skills, ./.mimocode/skills, then
  ~/.claude/skills, ~/.agents/skills, ~/.cursor/skills, ~/.codex/skills.

Examples (npm recommended when published):
  npx @topmindspace/topmind-writing-skills list
  npx @topmindspace/topmind-writing-skills status
  npx @topmindspace/topmind-writing-skills install all
  npx @topmindspace/topmind-writing-skills@latest update
  npx @topmindspace/topmind-writing-skills install topmind-briefs
  npx @topmindspace/topmind-writing-skills install topmind-briefs --to ./.agents/skills
  npx @topmindspace/topmind-writing-skills install topmind-briefs --force
  npx @topmindspace/topmind-writing-skills uninstall topmind-briefs --to ./.agents/skills

  # Follow repo HEAD:
  npx github:topmindspace/topmind-writing-skills install topmind-briefs

Privacy: the installer is fully local — it never collects or uploads anything.
`;
}

function usage() {
  console.log(usageText());
}

function parseOptions(args, start, { allowForce = false } = {}) {
  let to = null;
  let force = false;
  for (let i = start; i < args.length; i++) {
    if (args[i] === '--to' || args[i] === '-t') {
      to = args[++i];
      if (!to || to.startsWith('-')) die('Option --to requires a directory path.');
    } else if (allowForce && (args[i] === '--force' || args[i] === '-f')) {
      force = true;
    } else {
      die(`Unknown option: ${args[i]}\n\n` + usageText());
    }
  }
  return { targetRoot: to ? path.resolve(to) : resolveDefaultTarget(), force, defaultTarget: !to };
}

function main(argv) {
  const args = argv.slice(2);
  const cmd = args[0];

  if (!cmd || cmd === 'help' || cmd === '--help' || cmd === '-h') {
    usage();
    return;
  }

  if (cmd === 'list' || cmd === 'ls') {
    const ids = listSkillIds();
    if (!ids.length) {
      console.log('No skills found in package.');
      return;
    }
    for (const id of ids) {
      const meta = readSkillMeta(id);
      console.log(`${id}`);
      if (meta.description) console.log(`  ${meta.description}…`);
    }
    return;
  }

  if (cmd === 'status') {
    const { targetRoot } = parseOptions(args, 1);
    status(targetRoot);
    return;
  }

  if (cmd === 'install' || cmd === 'update') {
    const requested = cmd === 'update' && (!args[1] || args[1].startsWith('-')) ? 'all' : args[1];
    if (!requested || requested.startsWith('-')) {
      die('Missing skill id.\n\n' + usageText());
    }
    const optionStart = cmd === 'update' && requested === 'all' && args[1] !== 'all' ? 1 : 2;
    const options = parseOptions(args, optionStart, { allowForce: true });
    const ids = requested === 'all' ? listSkillIds() : [requested];
    const selected = cmd === 'update'
      ? ids.filter(id => installedState(id, options.targetRoot).kind !== 'missing')
      : ids;
    if (!selected.length) {
      console.log(`No TopMind writing skills installed in ${options.targetRoot}. Run install all to get started.`);
      return;
    }
    // Check every target before the first write; a conflict should not leave
    // an avoidably half-updated set.
    for (const id of selected) planInstall(id, options.targetRoot, options.force);
    for (const id of selected) install(id, options.targetRoot, options);
    if (selected.length > 1) console.log(`${cmd === 'install' ? 'Installed' : 'Updated'} ${selected.length} writing skills in ${options.targetRoot}.`);
    return;
  }

  if (cmd === 'uninstall') {
    const skillId = args[1];
    if (!skillId || skillId.startsWith('-')) {
      die('Missing skill id.\n\n' + usageText());
    }
    let to = null;
    for (let i = 2; i < args.length; i++) {
      if (args[i] === '--to' || args[i] === '-t') {
        to = args[++i];
        if (!to) die('Option --to requires a directory path.');
      } else {
        die(`Unknown option: ${args[i]}\n\n` + usageText());
      }
    }
    const targetRoot = to ? path.resolve(to) : resolveDefaultTarget();
    uninstall(skillId, targetRoot);
    return;
  }

  die(`Unknown command: ${cmd}\n\n` + usageText());
}

main(process.argv);
