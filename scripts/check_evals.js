#!/usr/bin/env node
/**
 * 评测骨架结构校验（不执行模型，只防止用例集腐烂）：
 *   - 每个已发现技能 ≥3 条用例，其中 ≥1 条负例（expected_skill ≠ target_skill）
 *   - expected_skill 必须是本仓库技能或 external_skills 中声明的外部技能
 *   - id 唯一、prompt / expected_behavior 非空
 * Usage: node scripts/check_evals.js
 */
'use strict';

const fs = require('fs');
const path = require('path');
const { discoverSkills, ROOT } = require('./discover_skills');

function main() {
  const file = path.join(ROOT, 'evals', 'evals.json');
  const data = JSON.parse(fs.readFileSync(file, 'utf8'));
  const skills = discoverSkills();
  const known = new Set([...skills, ...(data.external_skills || [])]);
  const errs = [];
  const ids = new Set();
  const per = Object.fromEntries(skills.map((s) => [s, { total: 0, neg: 0 }]));
  for (const e of data.evals || []) {
    if (!e.id || ids.has(e.id)) errs.push(`id 缺失或重复：${e.id}`);
    ids.add(e.id);
    if (!skills.includes(e.target_skill)) errs.push(`${e.id}: target_skill 不是本仓库技能：${e.target_skill}`);
    if (e.expected_skill !== null && !known.has(e.expected_skill)) errs.push(`${e.id}: expected_skill 未知：${e.expected_skill}`);
    if (!String(e.prompt || '').trim()) errs.push(`${e.id}: prompt 为空`);
    if (!String(e.expected_behavior || '').trim()) errs.push(`${e.id}: expected_behavior 为空`);
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
  console.log(`check_evals: ${ids.size} 条用例，覆盖 ${skills.length} 个技能，每个技能 ≥3 条且含负例`);
  return 0;
}

process.exit(main());
