#!/usr/bin/env node
/**
 * Print skill ids (one per line): root directories that contain SKILL.md,
 * skipping known infra dirs. Shared by npm scripts, CI, and sync:files.
 */
'use strict';

const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
const INFRA_DIRS = new Set([
  'bin', 'docs', 'scripts', 'shared', 'evals', 'node_modules', 'dist', 'release-assets',
]);

function discoverSkills() {
  return fs
    .readdirSync(ROOT, { withFileTypes: true })
    .filter((d) => d.isDirectory() && !INFRA_DIRS.has(d.name) && !d.name.startsWith('.'))
    .filter((d) => fs.existsSync(path.join(ROOT, d.name, 'SKILL.md')))
    .map((d) => d.name)
    .sort();
}

if (require.main === module) {
  for (const id of discoverSkills()) {
    console.log(id);
  }
}

module.exports = { discoverSkills, ROOT };
