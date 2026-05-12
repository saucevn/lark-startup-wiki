// Recursively read templates dir, render Mustache, write to target dir.
import fs from 'node:fs';
import path from 'node:path';
import Mustache from 'mustache';

// Disable HTML-escaping — we render markdown/yaml/text, not HTML.
Mustache.escape = (text) => text;

// Walk a dir recursively, returning [{abs, rel}] for every file.
function walk(dir, base = dir, out = []) {
  const entries = fs.readdirSync(dir, { withFileTypes: true });
  for (const entry of entries) {
    if (entry.name.startsWith('_')) continue; // skip _ prefix
    const abs = path.join(dir, entry.name);
    if (entry.isDirectory()) {
      walk(abs, base, out);
    } else if (entry.isFile()) {
      out.push({ abs, rel: path.relative(base, abs) });
    }
  }
  return out;
}

// `.tmpl` → render via Mustache & strip the suffix from the output path.
// Other files → copy bytes as-is.
function shouldRender(rel) {
  return rel.endsWith('.tmpl');
}

function destRel(rel) {
  return rel.endsWith('.tmpl') ? rel.slice(0, -'.tmpl'.length) : rel;
}

export function renderTemplates({ templatesDir, targetPath, view, dryRun = false }) {
  const files = walk(templatesDir);
  const written = [];
  for (const { abs, rel } of files) {
    const outRel = destRel(rel);
    const outAbs = path.join(targetPath, outRel);

    if (!dryRun) {
      fs.mkdirSync(path.dirname(outAbs), { recursive: true });
      if (shouldRender(rel)) {
        const raw = fs.readFileSync(abs, 'utf8');
        const rendered = Mustache.render(raw, view);
        fs.writeFileSync(outAbs, rendered, 'utf8');
      } else {
        fs.copyFileSync(abs, outAbs);
      }
    }
    written.push(outRel);
  }
  return written;
}
