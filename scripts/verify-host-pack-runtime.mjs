#!/usr/bin/env node
/** Load declared runtime capabilities from an isolated copy of the host pack. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const source = process.argv[2];
if (!source || !path.isAbsolute(source)) {
  console.error('Usage: verify-host-pack-runtime.mjs /absolute/host-pack');
  process.exit(2);
}

const temp = fs.mkdtempSync(path.join(os.tmpdir(), 'topmind-writing-host-'));
const isolated = path.join(temp, 'pack');
try {
  fs.cpSync(source, isolated, { recursive: true });
  const manifest = JSON.parse(fs.readFileSync(path.join(isolated, 'topmind-pack.json'), 'utf8'));
  const capabilities = manifest.runtime?.capabilities;
  if (!Array.isArray(capabilities) || capabilities.length === 0) {
    throw new Error('Host pack has no declared runtime capabilities');
  }
  for (const capability of capabilities) {
    if (typeof capability.id !== 'string' || typeof capability.entry !== 'string' ||
        typeof capability.export !== 'string') throw new Error('Invalid runtime capability declaration');
    const entry = path.resolve(isolated, capability.entry);
    if (!entry.startsWith(`${isolated}${path.sep}`) || !fs.statSync(entry).isFile()) {
      throw new Error(`${capability.id}: runtime entry is outside the pack or missing`);
    }
    try {
      const module = await import(pathToFileURL(entry).href);
      if (typeof module[capability.export] !== 'function') {
        throw new Error(`missing callable export ${capability.export}`);
      }
    } catch (error) {
      throw new Error(`${capability.id}: ${error.message}`, { cause: error });
    }
  }
  console.log(`Host runtime portable: ${capabilities.length} capabilities loaded from isolated pack`);
} catch (error) {
  console.error(`Host runtime portability failed: ${error.message}`);
  process.exitCode = 1;
} finally {
  fs.rmSync(temp, { recursive: true, force: true });
}
