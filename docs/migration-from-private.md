# Migrating from a Private Wiki Repo

> **TL;DR** — If you already maintain a private repo with vendored copies of the skills/scripts, this guide walks you through swapping local copies for the public `lark-startup-wiki` plugin so you get free upstream updates while keeping your team's customizations and private content (`docs/`, `sources/`, `.env`) intact. Allow ~1 hour for a typical 50-page wiki repo. Backup first.

---

## Step 1 — Backup first

> **Warning:** This migration deletes files. A backup is non-negotiable.

```bash
# Full repo snapshot
cp -r your-repo your-repo.backup
cd your-repo

# Backup .env separately (it's gitignored, won't be in the snapshot tarball you might make later)
cp .env ~/safe-place/your-repo.env.backup
chmod 600 ~/safe-place/your-repo.env.backup
```

Also push your current `main` to a remote tag in case something goes sideways:

```bash
git tag pre-migration-$(date +%Y%m%d)
git push origin pre-migration-$(date +%Y%m%d)
```

**Expected outcome**: you have a known-good copy you can revert to.

---

## Step 2 — Install the plugin in Claude Code

```bash
/plugin marketplace add saucevn/lark-startup-wiki
/plugin install lark-startup-wiki@saucevn
/plugin list   # confirm it shows up
```

See [installation.md](installation.md#method-1--claude-code-plugin) for details. After this step, the plugin's skills are available alongside your local copies — you'll deduplicate in the next step.

**Expected outcome**: `/plugin list` shows `lark-startup-wiki@saucevn`.

---

## Step 3 — Audit your `skills/` directory

Compare your local skills against the plugin version:

```bash
PLUGIN_SKILLS=~/.claude/plugins/lark-startup-wiki/skills
diff -r skills/ $PLUGIN_SKILLS/
```

For each skill file:

| What `diff` shows | Action |
|---|---|
| Identical (no output) | **Delete** your local copy. Use plugin version. |
| Minor difference (a few examples added) | **Move** to `skills-overrides/<name>.md`. Plugin handles defaults; your version overrides. |
| Major rewrite | **Keep** in `skills-overrides/`. Consider sending the improvement upstream as a PR. |
| You have a skill the plugin doesn't | **Keep** in `skills-overrides/` with a unique name (e.g. `skills-overrides/10-our-tone.md`). |

```bash
mkdir -p skills-overrides
mv skills/03-linking-rules.md skills-overrides/   # example — you customized this one
git rm -r skills/                                  # remove the rest, plugin handles them
```

**Expected outcome**: `skills/` is gone (or only contains overrides). `skills-overrides/` has your team-specific deltas.

---

## Step 4 — Migrate scripts

Same pattern as skills:

```bash
diff -r scripts/ ~/.claude/plugins/lark-startup-wiki/scripts/
```

| Local script | Action |
|---|---|
| `scripts/lark_client.py` (unmodified) | Delete. Use `python -m lark_startup_wiki.lark_client` |
| `scripts/pull_from_lark.py` (unmodified) | Delete. Use `python -m lark_startup_wiki.scripts.pull_from_lark` |
| `scripts/sync_index_base.py` (unmodified) | Delete. Use `python -m lark_startup_wiki.scripts.sync_index_base` |
| `scripts/validate_structure.py` (unmodified) | Delete. Use `python -m lark_startup_wiki.scripts.validate_structure` |
| `scripts/export_to_pdf.py` (your custom script) | **Rename** to `scripts/custom_export_to_pdf.py` (see [customization.md](customization.md#adding-your-own-scripts)) |

Install the package:

```bash
pip install lark-startup-wiki
# or, if you use the scaffolder's pyproject.toml setup:
pip install -e .
```

**Expected outcome**: your `scripts/` folder only contains `custom_*.py` files. Standard scripts run via `python -m lark_startup_wiki.scripts.<name>`.

---

## Step 5 — Update `CLAUDE.md`

Your old `CLAUDE.md` likely references local skills:

**Before:**

```markdown
| Tình huống | File |
|---|---|
| Viết 1 trang Wiki mới | [skills/01-page-format.md](skills/01-page-format.md) |
```

**After:**

```markdown
| Tình huống | Skill |
|---|---|
| Viết 1 trang Wiki mới | `lark-startup-wiki:01-page-format` (override at `skills-overrides/01-page-format.md` if present) |
```

Add a short note at the top:

```markdown
## Skill source
Skills ship via the `lark-startup-wiki` plugin. Local overrides in `skills-overrides/` win.
```

Mirror the same edits to `AGENTS.md` if you keep them in sync.

**Expected outcome**: `CLAUDE.md` no longer hard-codes paths to deleted local skills.

---

## Step 6 — Update `.env`

Old private repos often used inconsistent var names. Migrate to the canonical names from [env-vars.md](env-vars.md):

| Old name (common) | New name |
|---|---|
| `LARK_BOT_APP_ID`, `APP_ID` | `LARK_APP_ID` |
| `LARK_BOT_SECRET`, `APP_SECRET` | `LARK_APP_SECRET` |
| `WIKI_ID`, `SPACE_ID` | `WIKI_SPACE_ID` |
| `INDEX_NODE_ID` | `WIKI_INDEX_NODE` |
| `BASE_TOKEN`, `BITABLE_APP` | `LARK_BASE_APP_TOKEN` |
| `BASE_TABLE`, `TABLE_ID` | `LARK_BASE_TABLE_ID` |
| `LARK_REGION`, `LARK_HOST` | `LARK_DOMAIN` |

Quick rename via `sed` (review the diff before saving!):

```bash
sed -i.bak \
  -e 's/^APP_ID=/LARK_APP_ID=/' \
  -e 's/^APP_SECRET=/LARK_APP_SECRET=/' \
  -e 's/^WIKI_ID=/WIKI_SPACE_ID=/' \
  .env
diff .env.bak .env   # eyeball before discarding the backup
```

**Expected outcome**: `.env` uses the canonical names.

---

## Step 7 — Verify

Run the structure validator:

```bash
python -m lark_startup_wiki.scripts.validate_structure
```

Then sanity-check Lark connectivity:

```bash
python -m lark_startup_wiki.scripts.lark_client --test
```

Open Claude Code in the repo, open a draft wiki page, and ask:

> "Apply skill `lark-startup-wiki:01-page-format` to this draft."

Confirm Claude responds and follows the format.

**Expected outcome**: validator passes, Lark test passes, Claude applies skills.

---

## Step 8 — Commit changes

Suggested commit message format (mirrors your CLAUDE.md commit style):

```
chore(migration): consume lark-startup-wiki as plugin

- Removed local copies of skills 01, 02, 04, 05, 06, 07, 08, 09 (use plugin)
- Kept skill 03 as override (custom linking rules to Acme Base)
- Renamed custom scripts to scripts/custom_*.py prefix
- Migrated .env vars to canonical names (LARK_APP_ID, WIKI_SPACE_ID, ...)
- Updated CLAUDE.md and AGENTS.md to point at plugin skills

Verified: validate_structure passes, lark_client --test passes,
Claude applies plugin skills correctly on draft pages.
```

```bash
git add -A
git commit -m "chore(migration): consume lark-startup-wiki as plugin"
```

---

## What to keep private

These files **stay in your private repo** — the plugin never touches them:

| Path | Why private |
|---|---|
| `docs/` | Company-specific context (org structure, glossary, status tracker) |
| `sources/` | Excel files, Lark XML exports, schemas — proprietary data |
| `.env` | Credentials |
| `skills-overrides/` | Your team's voice and house rules |
| `scripts/custom_*.py` | Your bespoke automation |
| `drafts/` | Scratch space (gitignored anyway) |

The plugin only owns: the default skills, the standard scripts, and the scaffolder templates.

---

## Full example — Acme Wiki migration

Acme has a private repo (`acme-wiki`) with 50 pages, 9 local skills (one customized), and 4 scripts (one custom).

### Before

```
acme-wiki/
├── CLAUDE.md              # references skills/01-page-format.md, etc.
├── .env                   # APP_ID=cli_xxx, APP_SECRET=yyy, WIKI_ID=zzz
├── docs/                  # 8 company docs (private)
├── skills/                # 9 markdown files, copied from upstream
│   ├── 01-page-format.md          # identical to upstream
│   ├── 02-writing-style.md        # identical
│   ├── 03-linking-rules.md        # CUSTOMIZED for Acme's Base IDs
│   ├── 04-page-status.md          # identical
│   └── ... (05-09 identical)
├── scripts/               # 4 .py files
│   ├── lark_client.py             # identical to upstream
│   ├── pull_from_lark.py          # identical
│   ├── sync_index_base.py         # identical
│   └── export_to_confluence.py    # CUSTOM — Acme-specific
└── sources/               # 7 Excel files (private)
```

### Migration walkthrough

```bash
# Step 1
cp -r acme-wiki acme-wiki.backup

# Step 2
/plugin marketplace add saucevn/lark-startup-wiki
/plugin install lark-startup-wiki@saucevn

# Step 3 — only skill 03 is customized
mkdir skills-overrides
mv skills/03-linking-rules.md skills-overrides/
rm -r skills/

# Step 4 — only export_to_confluence.py is custom
mv scripts/export_to_confluence.py scripts/custom_export_to_confluence.py
rm scripts/lark_client.py scripts/pull_from_lark.py scripts/sync_index_base.py
pip install lark-startup-wiki

# Step 5 — edit CLAUDE.md (manual, in editor)

# Step 6 — rename .env vars
sed -i.bak \
  -e 's/^APP_ID=/LARK_APP_ID=/' \
  -e 's/^APP_SECRET=/LARK_APP_SECRET=/' \
  -e 's/^WIKI_ID=/WIKI_SPACE_ID=/' \
  .env
rm .env.bak

# Step 7
python -m lark_startup_wiki.scripts.validate_structure
python -m lark_startup_wiki.scripts.lark_client --test

# Step 8
git add -A
git commit -m "chore(migration): consume lark-startup-wiki as plugin"
git push
```

### After

```
acme-wiki/
├── CLAUDE.md              # references plugin skills + skills-overrides/
├── .env                   # LARK_APP_ID=, LARK_APP_SECRET=, WIKI_SPACE_ID=
├── docs/                  # unchanged (private)
├── skills-overrides/
│   └── 03-linking-rules.md        # only the one Acme-specific skill
├── scripts/
│   └── custom_export_to_confluence.py
└── sources/               # unchanged (private)
```

Lines of code Acme now maintains: ~80 (down from ~2,400). Upstream improvements arrive via `/plugin update lark-startup-wiki`.

---

## Rollback

If something breaks and you need to revert:

```bash
cd ..
rm -rf acme-wiki                # or rename it
mv acme-wiki.backup acme-wiki
cp ~/safe-place/acme-wiki.env.backup acme-wiki/.env
/plugin uninstall lark-startup-wiki
```

You're back exactly where you started.

---

## See also

- [installation.md](installation.md) — fresh install paths
- [customization.md](customization.md) — patterns for keeping team-specific code
- [env-vars.md](env-vars.md) — canonical env var names
- [lark-api-setup.md](lark-api-setup.md) — re-test Lark connectivity after migration
