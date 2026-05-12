# Customization

> **TL;DR** — You can adapt `lark-startup-wiki` to your team's voice, structure, and workflow **without forking** the package. Override individual skills locally, edit scaffolder templates for new repos, namespace your custom scripts and env vars to avoid clashes with package updates, and (in v2) plug in a custom AI reviewer prompt. Translations back to English are welcome via PR.

---

## Customizing skills

Skills are plain markdown files. Claude Code prefers a **local override** at the project level over the plugin version.

### Workflow

1. Find the skill you want to tweak in the plugin folder (Method 1: `~/.claude/plugins/lark-startup-wiki/skills/01-page-format.md`; Method 2/3: `skills/01-page-format.md` in your repo).
2. Copy it to a `skills-overrides/` folder in your project root:

   ```bash
   mkdir -p skills-overrides
   cp ~/.claude/plugins/lark-startup-wiki/skills/01-page-format.md skills-overrides/
   ```

3. Edit the local copy — change examples to match your domain, tighten or relax rules.
4. Tell Claude in `CLAUDE.md` that local overrides win:

   ```markdown
   ## Skill resolution order
   1. `./skills-overrides/<name>.md` (project-local)
   2. `lark-startup-wiki:<name>` (plugin)
   ```

> **Note:** If you change a skill in a way you think the whole community would benefit from, send a PR back to `saucevn/lark-startup-wiki`.

---

## Customizing the 4-Space structure

The default architecture (4 Spaces × 4 tiers) lives in `templates/docs/02-wiki-architecture.md.tmpl`. This template is **only consumed by the npm scaffolder** (Method 3) — editing it does **not** retroactively change existing repos.

To use a different structure (e.g. 3 Spaces, or department-based instead of function-based):

1. Fork the template to your own internal scaffolder, OR
2. After running `npx create-lark-startup-wiki`, edit the generated `docs/02-wiki-architecture.md` directly. The scaffolder is a one-shot generator; you own the output.

> **Warning:** Other docs in the package reference the 4-Space structure (e.g. skill 02 talks about cross-space linking). If you deviate, audit those references too.

---

## Adding your own scripts

The package follows a naming convention to keep upgrades safe:

| Prefix | Owned by | Will be overwritten on update? |
|---|---|---|
| `scripts/lark_*.py` | Package | Yes — do not edit |
| `scripts/sync_*.py` | Package | Yes |
| `scripts/validate_*.py` | Package | Yes |
| `scripts/custom_*.py` | **You** | No — safe |

So if you need a script that, say, exports the Wiki to PDF, name it `scripts/custom_export_pdf.py`. Future package updates won't touch it.

You can import package internals freely:

```python
# scripts/custom_export_pdf.py
from lark_startup_wiki.lark_client import get_client
from lark_startup_wiki.wiki import iter_nodes

client = get_client()
for node in iter_nodes(space_id="..."):
    ...  # your logic
```

---

## Custom env vars

To avoid clashing with package vars (which are listed in [env-vars.md](env-vars.md)), prefix yours with `MY_*` or your team initials:

```dotenv
# Yours — package will never read these
MY_S3_BUCKET=my-team-wiki-backups
MY_SLACK_WEBHOOK=https://hooks.slack.com/services/...
ACME_INTERNAL_API_TOKEN=...
```

Package-reserved prefixes (don't use these for your own vars):

- `LARK_*`
- `WIKI_*`
- `ANTHROPIC_*`
- `REVIEWER_*`

---

## Custom numbering scheme

Skill `08-index-and-numbering.md` documents the default `<Roman>> <X.Y.Z>` system (e.g. `III> 5.7.1`). It works well for function-organized wikis with up to ~10 top-level sections.

### Alternatives

| Scheme | When to use | Example |
|---|---|---|
| `<Roman>> <X.Y.Z>` (default) | Function-organized, ≤10 top-level sections | `III> 5.7.1` |
| `<Dept>> <X.Y.Z>` | Department-organized, dynamic top-level | `ENG> 2.1.4`, `OPS> 3.1.1` |
| `<YYYY-MM>-<NNN>` | Time-keyed (changelog-like wikis) | `2026-05-014` |
| Flat slug | Tiny wikis (<50 pages) | `livestream-rules` |

To switch: copy `skills/08-index-and-numbering.md` into `skills-overrides/`, edit the rules, and update your INDEX page on Lark accordingly.

---

## Custom AI reviewer prompt (v2 preview)

In v2, the reviewer bot reads a config file `reviewer-prompt.yml` from your repo root:

```yaml
# reviewer-prompt.yml (v2 — preview, subject to change)
model: claude-opus-4-7
system: |
  You are the wiki reviewer for the Acme team. Apply skills 01–04 strictly.
  Reject pages that lack a "Tài liệu liên quan" section.
skills_to_apply:
  - 01-page-format
  - 02-writing-style
  - 04-page-status
tone: friendly  # friendly | strict | terse
language: vi    # vi | en | bilingual
```

If the file is absent, the bot uses package defaults. We'll lock the schema before v2.0 ships — track [the v2 milestone](https://github.com/saucevn/lark-startup-wiki/milestones) for updates.

---

## Translating skills to English

Skills ship in Vietnamese by default (the original Thích Cay use case). To contribute English versions:

1. Copy `skills/01-page-format.md` to `skills/01-page-format.en.md`.
2. Translate, keeping section structure intact.
3. Open a PR — the package picks the right language based on the user's `LANG` or an explicit `WIKI_SKILL_LANG=en` env var.

Existing English-translated skills:

- (none yet — be the first!)

---

## See also

- [installation.md](installation.md) — base install
- [env-vars.md](env-vars.md) — full env var reference
- [migration-from-private.md](migration-from-private.md) — moving from a private repo to consume the package
