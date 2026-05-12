#!/usr/bin/env node
// create-lark-startup-wiki — CLI entry point
import { run } from '../src/index.js';

function parseArgs(argv) {
  const args = { targetDir: null, interactive: true, dryRun: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--no-interactive') args.interactive = false;
    else if (a === '--dry-run') args.dryRun = true;
    else if (a === '-h' || a === '--help') args.help = true;
    else if (!a.startsWith('-') && !args.targetDir) args.targetDir = a;
  }
  return args;
}

function printHelp() {
  console.log(`
create-lark-startup-wiki — scaffold a Lark Wiki management repo

Usage:
  npx create-lark-startup-wiki <target-dir> [options]

Options:
  --no-interactive   Skip prompts; use defaults (for testing/CI)
  --dry-run          Render to memory; do not write files
  -h, --help         Show this help

Examples:
  npx create-lark-startup-wiki my-team-wiki
  npx create-lark-startup-wiki acme-wiki --no-interactive --dry-run
`);
}

const args = parseArgs(process.argv.slice(2));

if (args.help) {
  printHelp();
  process.exit(0);
}

run(args).catch((err) => {
  console.error('\nError:', err && err.message ? err.message : err);
  process.exit(1);
});
