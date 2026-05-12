// Main scaffold flow
import fs from 'node:fs';
import path from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import kleur from 'kleur';
import { runPrompts, defaultAnswers } from './prompts.js';
import { renderTemplates } from './render.js';
import { printNextSteps } from './postinstall.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Templates may live either inside the published npm package
// (packages/create-lark-startup-wiki/templates) or, in the monorepo,
// at the repo root (../../../templates). Pick whichever exists.
function resolveTemplatesDir() {
  const candidates = [
    path.resolve(__dirname, '../templates'),
    path.resolve(__dirname, '../../../templates'),
  ];
  for (const c of candidates) {
    if (fs.existsSync(c) && fs.statSync(c).isDirectory()) return c;
  }
  throw new Error(
    `Could not find templates directory. Looked in:\n  ${candidates.join('\n  ')}`
  );
}

export async function run({ targetDir, interactive, dryRun }) {
  if (!targetDir) {
    throw new Error('Missing target directory. Usage: npx create-lark-startup-wiki <dir>');
  }

  const targetPath = path.resolve(process.cwd(), targetDir);

  // Validate target dir
  if (fs.existsSync(targetPath)) {
    const entries = fs.readdirSync(targetPath);
    if (entries.length > 0) {
      throw new Error(`Target directory "${targetDir}" exists and is not empty.`);
    }
  }

  const answers = interactive
    ? await runPrompts({ defaultName: path.basename(targetPath) })
    : defaultAnswers({ defaultName: path.basename(targetPath) });

  const templatesDir = resolveTemplatesDir();

  if (dryRun) {
    console.log(kleur.cyan(`\n[dry-run] Would render templates from: ${templatesDir}`));
    console.log(kleur.cyan(`[dry-run] Would write to: ${targetPath}`));
    const written = renderTemplates({ templatesDir, targetPath, view: answers, dryRun: true });
    console.log(kleur.dim(`[dry-run] ${written.length} files would be created`));
    for (const f of written) console.log(kleur.dim('  ' + f));
    return;
  }

  fs.mkdirSync(targetPath, { recursive: true });
  const written = renderTemplates({ templatesDir, targetPath, view: answers, dryRun: false });

  // Init git
  if (answers.initGit) {
    try {
      execSync('git init', { cwd: targetPath, stdio: 'ignore' });
    } catch (e) {
      console.warn(kleur.yellow('Warning: git init failed (is git installed?). Skipping.'));
    }
  }

  printNextSteps({ targetDir, fileCount: written.length, initGit: answers.initGit });
}
