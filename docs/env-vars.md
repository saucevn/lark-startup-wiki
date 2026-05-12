# Environment Variables Reference

> **TL;DR** — `lark-startup-wiki` reads all credentials and runtime config from environment variables (loaded from `.env` via `python-dotenv` or your shell). v1.0 needs three required vars (`LARK_APP_ID`, `LARK_APP_SECRET`, `WIKI_SPACE_ID`) plus a few optional ones for the INDEX Base sync. v2.0 will add three more for the AI reviewer bot. **Never commit `.env` to git.** Prefer `direnv` or `1Password CLI` for per-project loading. See the [security section](#security) below.

---

## Required (v1)

### `LARK_APP_ID`

- **Required**: Yes
- **Used by**: `scripts/lark_client.py`, `scripts/pull_from_lark.py`, `scripts/sync_index_base.py`, (v2: reviewer bot)
- **Example**: `cli_a1b2c3d4e5f6g7h8`
- **How to get**: open.larksuite.com → Apps → Your App → "Credentials & Basic Info" tab → copy "App ID"
- **Notes**: Always starts with `cli_`. Different from your Lark User ID. Do not commit to git.

### `LARK_APP_SECRET`

- **Required**: Yes
- **Used by**: `scripts/lark_client.py`, `scripts/pull_from_lark.py`, `scripts/sync_index_base.py`, (v2: reviewer bot)
- **Example**: `xYz0123456789abcDEFghijKLMnopQRS`
- **How to get**: Same tab as App ID — click "Show" next to App Secret, copy the value
- **Notes**: 32-character alphanumeric. Treat as a password. Rotate every 90 days.

### `WIKI_SPACE_ID`

- **Required**: Yes
- **Used by**: All scripts that touch Wiki nodes
- **Example**: `7234567890123456789`
- **How to get**: Open your Lark Wiki space in a browser. The URL is `https://<tenant>.larksuite.com/wiki/space/<SPACE_ID>` — copy the numeric segment.
- **Notes**: One repo = one Wiki space. If you manage multiple spaces, use one `.env` file per repo or per `direnv` block.

---

## Optional (v1)

### `WIKI_INDEX_NODE`

- **Required**: No (required only for `sync_index_base.py`)
- **Used by**: `scripts/sync_index_base.py`
- **Example**: `UxOkwdRyBi7oBLkFM5WlABIyg8g`
- **How to get**: Open your INDEX page in Lark Wiki. The URL contains `/wiki/<NODE_ID>` — copy that token.
- **Notes**: This is the canonical INDEX page (mục lục) that lists every wiki page with its number, title, and status. The sync script reads this page and mirrors entries to a Lark Base.

### `LARK_BASE_APP_TOKEN`

- **Required**: No (required only for INDEX Base sync)
- **Used by**: `scripts/sync_index_base.py`
- **Example**: `RzABbase123456789xyZ`
- **How to get**: Open the Lark Base in a browser. URL: `https://<tenant>.larksuite.com/base/<APP_TOKEN>` — copy the segment.
- **Notes**: A "Base" is Lark's relational database. The INDEX is mirrored here so non-engineers can filter/sort.

### `LARK_BASE_TABLE_ID`

- **Required**: No (required only for INDEX Base sync)
- **Used by**: `scripts/sync_index_base.py`
- **Example**: `tblABC123XYZ`
- **How to get**: Inside the Base, open the target table → ⋯ menu → "Copy table ID"
- **Notes**: Always starts with `tbl`. One Base can have many tables; this is the specific INDEX table.

### `LARK_DOMAIN`

- **Required**: No
- **Default**: `larksuite.com`
- **Used by**: `scripts/lark_client.py` (constructs API base URL)
- **Allowed values**: `larksuite.com` (international), `feishu.cn` (China)
- **Example**: `LARK_DOMAIN=feishu.cn`
- **Notes**: International tenants use `open.larksuite.com`; China tenants use `open.feishu.cn`. Pick the one that matches your Lark account. Mixing them returns `403 access_denied`.

---

## Future (v2 — preview)

These vars are not used in v1.0 but will be required when the AI reviewer bot ships in v2.0. You can leave them unset for now.

### `ANTHROPIC_API_KEY`

- **Required (v2)**: Yes (reviewer bot only)
- **Used by**: v2 reviewer bot (`scripts/reviewer_bot.py`)
- **Example**: `sk-ant-api03-...`
- **How to get**: <https://console.anthropic.com/> → API Keys → Create Key
- **Notes**: Bot calls Claude to review draft pages against the skills. Budget tip: cache the skills as system prompt to keep cost low.

### `WIKI_REVIEWER_MODEL`

- **Required (v2)**: No
- **Default**: `claude-opus-4` (TBD at v2 release)
- **Used by**: v2 reviewer bot
- **Example**: `claude-opus-4-7`
- **Notes**: Override to use a cheaper model (Haiku/Sonnet) for high-volume teams.

### `REVIEWER_WEBHOOK_SECRET`

- **Required (v2)**: Yes (reviewer bot only)
- **Used by**: v2 reviewer bot HTTP listener
- **Example**: `whsec_a1b2c3...` (any random 32+ char string)
- **How to get**: Generate locally — `python -c "import secrets; print('whsec_' + secrets.token_urlsafe(32))"`
- **Notes**: Verifies that incoming webhooks are from your Lark group, not random callers. Set the same value in your Lark custom bot's webhook config.

---

## Quick reference: `.env.example`

```dotenv
# --- Required (v1) ---
LARK_APP_ID=cli_xxxxxxxxxxxxxxxx
LARK_APP_SECRET=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
WIKI_SPACE_ID=7234567890123456789

# --- Optional (v1) ---
WIKI_INDEX_NODE=UxOkwdRyBi7oBLkFM5WlABIyg8g
LARK_BASE_APP_TOKEN=RzABbase123456789xyZ
LARK_BASE_TABLE_ID=tblABC123XYZ
LARK_DOMAIN=larksuite.com

# --- Future (v2) ---
# ANTHROPIC_API_KEY=sk-ant-api03-...
# WIKI_REVIEWER_MODEL=claude-opus-4-7
# REVIEWER_WEBHOOK_SECRET=whsec_...
```

---

## Security

> **Warning:** `LARK_APP_SECRET` and `ANTHROPIC_API_KEY` are credentials. Never commit them, never paste them into chat, never log them.

### Recommended: `direnv`

[direnv](https://direnv.net) auto-loads `.envrc` when you `cd` into a directory and unloads it when you leave.

```bash
# .envrc (gitignored)
dotenv .env
```

```bash
direnv allow
```

### Recommended: 1Password CLI

[1Password CLI](https://developer.1password.com/docs/cli/) injects secrets at runtime — they never touch disk.

```bash
# .env (committed, references only)
LARK_APP_SECRET=op://Engineering/lark-startup-wiki/app_secret
ANTHROPIC_API_KEY=op://Engineering/lark-startup-wiki/anthropic_key
```

```bash
op run --env-file=.env -- python scripts/pull_from_lark.py
```

### CI / GitHub Actions

Store secrets in **Settings → Secrets and variables → Actions**, then expose them in the workflow:

```yaml
- name: Sync INDEX Base
  env:
    LARK_APP_ID: ${{ secrets.LARK_APP_ID }}
    LARK_APP_SECRET: ${{ secrets.LARK_APP_SECRET }}
    WIKI_SPACE_ID: ${{ secrets.WIKI_SPACE_ID }}
    WIKI_INDEX_NODE: ${{ secrets.WIKI_INDEX_NODE }}
    LARK_BASE_APP_TOKEN: ${{ secrets.LARK_BASE_APP_TOKEN }}
    LARK_BASE_TABLE_ID: ${{ secrets.LARK_BASE_TABLE_ID }}
  run: python scripts/sync_index_base.py
```

### Rotation policy

- **`LARK_APP_SECRET`**: rotate every 90 days, or immediately on suspected leak
- **`ANTHROPIC_API_KEY`**: rotate every 90 days; revoke unused keys monthly
- **`REVIEWER_WEBHOOK_SECRET`**: rotate yearly, or on team membership changes

---

## Troubleshooting

### `lark.exceptions.AppAccessTokenError: invalid app_id or app_secret`

- Check `LARK_APP_ID` starts with `cli_`
- Re-copy `LARK_APP_SECRET` from the Lark console (no trailing whitespace)
- Confirm `LARK_DOMAIN` matches your tenant region — international vs China secrets are not interchangeable

### `WIKI_SPACE_ID not set` or `KeyError: WIKI_SPACE_ID`

- The script needs the env loaded. Either `source .env`, use `direnv`, or run via `python-dotenv`'s auto-load (which requires `from dotenv import load_dotenv; load_dotenv()` at the top of the script — already present in v1 scripts)

### `403 access_denied` on Wiki API calls

- See [lark-api-setup.md](lark-api-setup.md) — your app likely needs Wiki scopes granted and the app added to the Wiki space.

### `LARK_BASE_TABLE_ID` returns `1254030` (table_not_found)

- The Base sync runs against a specific table inside a Base app. `LARK_BASE_APP_TOKEN` identifies the Base; `LARK_BASE_TABLE_ID` identifies the table within it. Confirm both.

---

## See also

- [installation.md](installation.md) — get the package installed
- [lark-api-setup.md](lark-api-setup.md) — create the Lark app these vars point to
- [customization.md](customization.md) — adding your own env vars without clashes
