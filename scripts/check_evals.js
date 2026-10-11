#!/usr/bin/env node
/**
 * 评测骨架结构校验（不执行模型，只防止用例集腐烂）：
 *   - 每个已发现技能 ≥3 条用例，其中 ≥1 条负例（expected_skill ≠ target_skill）
 *   - expected_skill 必须是本仓库技能或 external_skills 中声明的外部技能
 *   - id 唯一、prompt / expected_behavior 非空
 *   - description 的 Do NOT 分流只指向存在的技能（本仓库技能或 external_skills）
 *   - 路由词覆盖：expected_skill 为本仓库技能时，prompt 至少命中它的一个触发词
 *     （SKILL.md 的 metadata.triggers + description 里 Use when 到分号前的词），防止新增用例与触发词脱节
 * Usage: node scripts/check_evals.js
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { discoverSkills, ROOT } = require('./discover_skills');

// 读取技能的触发词：metadata.triggers（逗号分隔）+ description 中 "Use when" 到第一个分号之间的词
function loadTriggerTerms(skillId) {
  const text = fs.readFileSync(path.join(ROOT, skillId, 'SKILL.md'), 'utf8');
  const fm = (text.match(/^---\r?\n([\s\S]*?)\r?\n---/) || [])[1] || '';
  const trig = (fm.match(/^[ \t]+triggers:\s*"(.*)"\s*$/m) || [])[1] || '';
  const desc = (fm.match(/^description:\s*"(.*)"\s*$/m) || [])[1] || '';
  let use = desc.includes('Use when') ? desc.split('Use when')[1] : '';
  use = use.split('Do NOT')[0].split(/[；;]/)[0];
  return `${use},${trig}`
    .split(/[、，,]/)
    .map((t) => t.trim().toLowerCase())
    .filter((t) => t.length >= 2);
}

function main() {
  const file = path.join(ROOT, 'evals', 'evals.json');
  const data = JSON.parse(fs.readFileSync(file, 'utf8'));
  const skills = discoverSkills();
  const known = new Set([...skills, ...(data.external_skills || [])]);
  const errs = [];
  for (const sk of skills) {
    const text = fs.readFileSync(path.join(ROOT, sk, 'SKILL.md'), 'utf8');
    const desc = ((text.match(/^description:\s*"(.*)"\s*$/m) || [])[1]) || '';
    for (const ref of new Set(desc.match(/topmind-[a-z][a-z-]*/g) || [])) {
      if (ref !== sk && !known.has(ref)) errs.push(`${sk}: description 指向未知技能 ${ref}（本仓库没有，也不在 external_skills）`);
    }
  }
  const ids = new Set();
  const terms = Object.fromEntries(skills.map((sk) => [sk, loadTriggerTerms(sk)]));
  const per = Object.fromEntries(skills.map((s) => [s, { total: 0, neg: 0 }]));
  for (const e of data.evals || []) {
    if (!e.id || ids.has(e.id)) errs.push(`id 缺失或重复：${e.id}`);
    ids.add(e.id);
    if (!skills.includes(e.target_skill)) errs.push(`${e.id}: target_skill 不是本仓库技能：${e.target_skill}`);
    if (e.expected_skill !== null && !known.has(e.expected_skill)) errs.push(`${e.id}: expected_skill 未知：${e.expected_skill}`);
    if (!String(e.prompt || '').trim()) errs.push(`${e.id}: prompt 为空`);
    if (!String(e.expected_behavior || '').trim()) errs.push(`${e.id}: expected_behavior 为空`);
    if (skills.includes(e.expected_skill)) {
      const prompt = String(e.prompt || '').toLowerCase();
      if (!terms[e.expected_skill].some((t) => prompt.includes(t))) {
        errs.push(`${e.id}: prompt 没有命中 ${e.expected_skill} 的任何触发词，请补触发词或改写用例`);
      }
    }
    if (per[e.target_skill]) {
      per[e.target_skill].total += 1;
      if (e.expected_skill !== e.target_skill) per[e.target_skill].neg += 1;
    }
  }
  for (const [s, c] of Object.entries(per)) {
    if (c.total < 3) errs.push(`${s}: 用例 ${c.total} 条，至少 3 条`);
    if (c.neg < 1) errs.push(`${s}: 缺负例`);
  }
  if (errs.length) {
    console.error(`check_evals: ${errs.length} 项失败`);
    for (const e of errs) console.error(`  ✗ ${e}`);
    return 1;
  }
  console.log(`check_evals: ${ids.size} 条用例，覆盖 ${skills.length} 个技能，每个技能 ≥3 条且含负例，路由词覆盖通过`);
  return 0;
}

process.exit(main());
