# Installation

> **TL;DR** — `lark-startup-wiki` ships in three flavours: a **Claude Code plugin** (one-line install, best if you already use Claude Code), a **standalone clone** (works with Cursor, Codex, Gemini, or any IDE that reads markdown rules), and an **npm scaffolder** (`npx create-lark-startup-wiki`) that generates a fresh, ready-to-edit repo for new teams. Pick the channel that fits your workflow, then jump to [env-vars.md](env-vars.md) and [lark-api-setup.md](lark-api-setup.md) to wire up Lark credentials.

---

## Which install method should I use?

| Method | Best for | Auto-updates? | IDE support |
|---|---|---|---|
| **1. Claude Code plugin** | Solo operators or teams already on Claude Code | Yes (`/plugin update`) | Claude Code only |
| **2. Standalone clone** | Cursor, Codex, Gemini, or hand-rolled setups | Manual `git pull` | Any (markdown rules) |
| **3. npm scaffolder** | New teams starting a fresh wiki repo | One-shot (regenerate) | Any |

> **Note:** Methods 1 and 2 are *consumers* of the package. Method 3 *generates* a new repo that bundles a curated subset of skills + scripts as a starting point — you own the resulting code.

---

## Method 1 — Claude Code plugin

### Prerequisites

- [Claude Code](https://claude.com/claude-code) installed and authenticated
- A workspace folder where you draft Lark Wiki content

### Install

```bash
# 1. Add the marketplace
/plugin marketplace add saucevn/lark-startup-wiki

# 2. Install the plugin
/plugin install lark-startup-wiki@saucevn
```

### Verify

```bash
/plugin list
```

You should see `lark-startup-wiki` in the active plugins list. Inside Claude Code, the skills appear under their namespaced names:

- `lark-startup-wiki:01-page-format`
- `lark-startup-wiki:02-writing-style`
- `lark-startup-wiki:03-linking-rules`
- `lark-startup-wiki:04-page-status`
- `lark-startup-wiki:05-publish-workflow`
- `lark-startup-wiki:06-excel-to-wiki`
- `lark-startup-wiki:07-source-protection`
- `lark-startup-wiki:08-index-and-numbering`
- `lark-startup-wiki:09-contributing-workflow`

### Use it

Open a draft markdown file in Claude Code and ask:

> "Apply skill `lark-startup-wiki:01-page-format` to format this draft as a Wiki page."

Claude will load the skill, follow the format rules, and rewrite your draft. You can chain skills:

> "Use `02-writing-style` then `04-page-status` on this file."

### Update

```bash
/plugin update lark-startup-wiki
```

---

## Method 2 — Standalone clone (Cursor / Codex / Gemini / manual)

### Clone

```bash
git clone https://github.com/saucevn/lark-startup-wiki.git ~/tools/lark-startup-wiki
cd ~/tools/lark-startup-wiki
```

### For Claude Code (without the plugin system)

Symlink or copy the skills into your global Claude skills folder:

```bash
cp -r skills/ ~/.claude/skills/lark-startup-wiki/
```

Restart Claude Code and the skills become available as `lark-startup-wiki/01-page-format` etc.

### For Cursor

Cursor reads project-level rules from `.cursorrules` or `.cursor/rules/*.md`. Copy the skills you want to enforce:

```bash
mkdir -p .cursor/rules
cp ~/tools/lark-startup-wiki/skills/*.md .cursor/rules/
```

Cursor will surface these as project rules in its sidebar.

### For Gemini Code Assist

Gemini supports custom tool definitions. See `references/gemini-tools.md` in the repo for a sample `tools.yaml` that wraps the publish workflow.

### Manual reference (no IDE integration)

Just clone and read. The `skills/` directory is plain markdown; treat it as documentation you consult before editing Wiki content.

---

## Method 3 — npm scaffolder (recommended for new teams)

### Prerequisites

- Node.js 18 or newer (`node --version`)
- Python 3.11 or newer (`python3 --version`)
- `lark-cli` globally installed:

  ```bash
  npm install -g @larksuiteoapi/lark-cli
  ```

### Generate a new repo

```bash
npx create-lark-startup-wiki my-team-wiki
```

### Example interactive session

```
? Project name: my-team-wiki
? Lark domain: (Use arrow keys)
❯ larksuite.com (international)
  feishu.cn (China)
? Default language for skills: (Use arrow keys)
❯ English
  Vietnamese
  Both
? Include example INDEX Base schema? Yes
? Initialize git repo? Yes
? Install Python dependencies now? Yes

Creating my-team-wiki/...
✓ Wrote 47 files
✓ Initialized git
✓ Installed lark-oapi, python-dotenv

Next steps:
  cd my-team-wiki
  cp .env.example .env
  # Fill in LARK_APP_ID, LARK_APP_SECRET, WIKI_SPACE_ID
  python scripts/validate_structure.py
```

### Resulting repo structure

```
my-team-wiki/
├── CLAUDE.md                    # AI agent instructions
├── AGENTS.md                    # mirror of CLAUDE.md
├── README.md
├── .env.example
├── .gitignore
├── pyproject.toml
├── docs/
│   ├── 00-overview.md
│   ├── 01-org-structure.md
│   ├── 02-wiki-architecture.md
│   └── ...
├── skills/                      # editable copies — your team's overrides
│   ├── 01-page-format.md
│   ├── 02-writing-style.md
│   └── ...
├── scripts/
│   ├── lark_client.py
│   ├── pull_from_lark.py
│   ├── sync_index_base.py
│   └── validate_structure.py
├── sources/
│   ├── excel/                   # gitignored except .gitkeep
│   └── lark-exports/
└── drafts/                      # gitignored, your scratch space
```

### Next steps

1. Fill in `.env` — see [env-vars.md](env-vars.md)
2. Create your Lark app — see [lark-api-setup.md](lark-api-setup.md)
3. Run `python scripts/validate_structure.py` to confirm the repo is wired up
4. Customize skills to your team's voice — see [customization.md](customization.md)

---

## Troubleshooting

### Plugin not loading

- Run `/plugin list` — if `lark-startup-wiki` is missing, re-run `/plugin install lark-startup-wiki@saucevn`
- Check Claude Code logs: macOS `~/Library/Logs/Claude/`, Linux `~/.config/Claude/logs/`
- Confirm marketplace is registered: `/plugin marketplace list`

### `npx create-lark-startup-wiki` permission errors

- On macOS/Linux, npm may need `sudo` for global installs. Prefer `npx` (no global install needed) or use a Node version manager (`nvm`, `fnm`, `volta`).
- If you see `EACCES`, fix npm's default folder: <https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally>

### Python virtualenv issues

- The scaffolder creates a `.venv/` — activate it: `source .venv/bin/activate` (macOS/Linux) or `.venv\Scripts\activate` (Windows)
- If `lark-oapi` install fails, upgrade pip: `python3 -m pip install --upgrade pip`
- Apple Silicon: ensure you're using a native arm64 Python build (`python3 -c "import platform; print(platform.machine())"` should print `arm64`)

### Skills not appearing in Cursor

- Cursor only reads `.cursor/rules/*.md` from the **project root**. Symlinks across projects don't always work — copy the files instead.
- Restart Cursor after copying.

---

## Next

- [env-vars.md](env-vars.md) — configure environment variables
- [lark-api-setup.md](lark-api-setup.md) — create a Lark app and grant scopes
- [customization.md](customization.md) — adapt the framework to your team
- [migration-from-private.md](migration-from-private.md) — already have a private wiki repo? Migrate to consume this package as a plugin.
