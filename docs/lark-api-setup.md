# Lark API Setup

> **TL;DR** — Before any script in this package can talk to Lark, you must (1) pick the right Lark domain, (2) create a Custom App in the Lark Open Platform, (3) grant it Wiki + Base + Docx scopes, (4) publish it within your tenant for admin approval, and (5) explicitly add the app to your Wiki space. Allow ~15 minutes end-to-end, plus admin approval lead time. The numbered steps below include "expected outcome" checks at each stage so you can spot mistakes early.

---

## Step 1 — Choose your Lark domain

Lark runs two regional clouds with **non-interchangeable** App IDs and Secrets:

| Domain | Region | Open Platform URL | API base |
|---|---|---|---|
| `larksuite.com` | International (default) | <https://open.larksuite.com> | `open.larksuite.com` |
| `feishu.cn` | China | <https://open.feishu.cn> | `open.feishu.cn` |

Pick the one that matches your Lark tenant (look at the domain in your browser when logged in to Lark). Set `LARK_DOMAIN` accordingly — see [env-vars.md](env-vars.md#lark_domain).

**Expected outcome**: you know which Open Platform URL to use for steps 2–7.

---

## Step 2 — Create a Custom App

1. Open the Open Platform URL from Step 1.
2. Sign in with the Lark account that owns the tenant (usually the admin).
3. Click **Create App** → **Custom App**.
4. Fill in:
   - **App Name**: e.g. `Wiki Manager` (your team will see this)
   - **Description**: e.g. `Manages our company wiki via lark-startup-wiki`
   - **Icon**: any 240×240 PNG
5. Click **Create**.

**Expected outcome**: you land on the app's dashboard at `https://open.larksuite.com/app/<APP_ID>`. The App ID (starts with `cli_`) is shown at the top.

---

## Step 3 — Grant Wiki scopes

Navigate to **Permissions & Scopes** → **Add Scopes**. Search for and add each of:

| Scope | What it enables |
|---|---|
| `wiki:wiki` | Create, update, delete wiki nodes |
| `wiki:wiki:readonly` | List nodes and read metadata (required even if you only write) |
| `wiki:node:read` | Read a single node's contents |
| `wiki:space:read` | Enumerate spaces visible to the app |

Click **Save**.

> **Note:** Adding scopes does not take effect immediately — you must re-publish the app (Step 7) for new scopes to apply.

**Expected outcome**: the four Wiki scopes appear in your "Granted Scopes" list with status "Pending Release".

---

## Step 4 — Grant Base scopes (if syncing INDEX Base)

Skip this step if you don't plan to mirror the INDEX page to a Lark Base.

| Scope | What it enables |
|---|---|
| `bitable:app` | Read and write Base apps (read records, append rows, update fields) |
| `bitable:app:readonly` | Read-only fallback (some endpoints require this even when the write scope is present) |

**Expected outcome**: both scopes appear with status "Pending Release".

---

## Step 5 — Grant Docx scopes (for content read)

Wiki pages are stored as Docx documents. To read or write the actual page body (not just metadata), grant:

| Scope | What it enables |
|---|---|
| `docx:document` | Create, update, delete blocks inside a Docx |
| `docx:document:readonly` | Read blocks and document structure |

**Expected outcome**: both scopes added; "Granted Scopes" panel shows 8 scopes total (4 Wiki + 2 Base + 2 Docx).

---

## Step 6 — Get App ID and Secret

1. Open the **Credentials & Basic Info** tab.
2. Copy the **App ID** (begins with `cli_`) into your `.env` as `LARK_APP_ID`.
3. Click **Show** next to **App Secret**, copy the 32-char string into `LARK_APP_SECRET`.

**Expected outcome**: your `.env` file has both values filled. See [env-vars.md](env-vars.md#required-v1).

> **Warning:** The App Secret is shown in full only once after each rotation. Copy it immediately. If you lose it, click **Reset** to generate a new one (this invalidates the old one).

---

## Step 7 — Publish the app within your tenant

This step trips up most first-time users. Without it, your app's tokens are valid but every API call returns `403`.

1. Open the **Version Management & Release** tab.
2. Click **Create Version**.
3. Fill version notes (e.g. `Initial release for wiki management`).
4. Click **Submit for Release**.
5. A tenant admin (often you, if you own the workspace) receives an approval request in Lark — open it and **Approve**.

**Expected outcome**: the app's status badge changes from `In Development` to `Released`. Without this, no Wiki API calls will succeed.

> **Note:** Every time you change scopes (Steps 3–5), you must re-create a new version and re-approve. Scope changes do not propagate without a fresh release.

---

## Step 8 — Add the app to your Wiki space

Granting scopes lets the app *use* Wiki APIs in general; adding it to a specific space lets it *access that space's contents*.

1. Open your Wiki space in Lark (browser).
2. Click **Settings** (gear icon, top right).
3. Open the **Apps** tab (or **Members** → **Add Bot/App** in some UI variants).
4. Click **Add App** → search by App Name (from Step 2) → select.
5. Grant **Edit** permission (or **View** if read-only).

**Expected outcome**: the app appears in the space's app list with the chosen permission.

> **Note:** Personal Wiki spaces (the ones tied to your individual account) **cannot** be accessed by Custom Apps. Only team Wiki spaces work. If you don't see the option to add an app, check that you opened a team space.

---

## Step 9 — Test the connection

With `.env` populated and the app released + added:

```bash
python scripts/lark_client.py --test
```

### Expected output

```
[OK] Loaded credentials for app cli_a1b2c3d4e5f6g7h8
[OK] Got tenant_access_token (expires in 7200s)
[OK] Wiki space 7234567890123456789 reachable: "My Team Wiki"
[OK] Listed 23 root nodes
[OK] All checks passed.
```

### Common errors

| Error | Cause | Fix |
|---|---|---|
| `invalid app_id or app_secret` | Typo in `.env`, or wrong domain | Re-copy from the console; check `LARK_DOMAIN` |
| `app_not_published` | Skipped Step 7 | Create a release version and approve it |
| `access_denied` on space | Skipped Step 8, or wrong scope | Add app to space; confirm `wiki:wiki` scope is released |
| `forbidden: scope not granted` | Added scope but didn't release a new version | Re-publish (Step 7 again) |
| `space_not_found` | `WIKI_SPACE_ID` is wrong, or it's a personal space | Use a team Wiki space ID |

---

## Common gotchas

### Permission propagation lag

After granting Wiki access in Step 8, expect up to **5 minutes** of propagation delay. If the test in Step 9 fails immediately after adding the app, wait and retry.

### Personal vs team Wiki

A personal Wiki (under "My Library") is private to your account — no app can read it. Move pages to a team space, or create a new team space, then add the app.

### Scope changes need re-publish

This is the #1 source of confusion. The flow is always:

```
Edit scopes  →  Create new version  →  Admin approves  →  Scopes active
```

Without the release step, the scope change is silently inert.

### Token caching

The package caches `tenant_access_token` for the full 2-hour TTL Lark issues. If you reset the App Secret and the cached token is still in memory, calls fail with `invalid_token`. Restart the script.

### Rate limits

- Wiki APIs: ~50 req/sec per app
- Base APIs: ~20 req/sec per app
- Docx APIs: ~10 req/sec per app

The bundled scripts use `lark-oapi`'s built-in retry with exponential backoff. If you write custom scripts, respect these limits or you'll see `429` errors.

### Multiple environments (dev/prod)

Create **two separate Custom Apps** — one for staging, one for production. Don't share `LARK_APP_SECRET` across environments. Use distinct `WIKI_SPACE_ID`s too.

---

## Reference

- Lark Open Platform docs (international): <https://open.larksuite.com/document/home/index>
- Feishu Open Platform docs (China): <https://open.feishu.cn/document/home/index>
- Wiki API reference: <https://open.larksuite.com/document/server-docs/docs/wiki-v2/overview>
- Base API reference: <https://open.larksuite.com/document/server-docs/docs/bitable-v1/app/overview>
- Docx API reference: <https://open.larksuite.com/document/server-docs/docs/docs/docx-v1/document/overview>
- Scope catalog: <https://open.larksuite.com/document/server-docs/api-call-guide/calling-process/scope-list>

---

## Next

- [env-vars.md](env-vars.md) — populate `.env` with the credentials from Step 6
- [installation.md](installation.md) — install the package itself
- [customization.md](customization.md) — adapt scripts and skills to your team
