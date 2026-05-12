---
name: lark-wiki-publish-workflow
description: Use BEFORE publishing any draft to Lark Wiki. Manual publish workflow via lark-cli with explicit space_id and node_id. Prevents accidental overwrite of live pages, enforces draft review gate, requires owner approval. Trigger on any task that involves pushing content to Lark.
---

# Skill 05 — Quy trình đẩy nội dung lên Lark Wiki

Repo này KHÔNG phải nơi soạn thảo. Publish thực tế lên **Lark Wiki của bạn** qua `lark-cli`.

Cấu hình env (đặt trong `.env` hoặc shell profile, KHÔNG commit):

```bash
export WIKI_SPACE_ID=<WIKI_SPACE_ID>            # token của wiki space (lấy từ URL)
export WIKI_INDEX_NODE=<WIKI_INDEX_NODE_ID>     # node_token của trang INDEX
export WIKI_INDEX_OBJ=<WIKI_INDEX_OBJ_ID>       # obj_token của INDEX (dùng cho `docs +update`)
```

URL đích: `https://<your-lark-tenant>.larksuite.com/wiki/${WIKI_SPACE_ID}`

## Pre-flight checklist (BẮT BUỘC)

Trước khi publish:

1. [ ] Đã đọc [skill 07 — Source Protection](07-source-protection.md)
2. [ ] Đã xác định đích cụ thể: **Space → Section → Page** trong Wiki architecture của bạn + Lark INDEX
3. [ ] Đã review draft với owner Space (CEO, trưởng phòng…)
4. [ ] Draft đang ở `drafts/` hoặc `/tmp/` — **KHÔNG** ở `skills/`, `docs/`, `sources/`
5. [ ] `git status` working tree sạch
6. [ ] `lark-cli auth status` → user đã login đúng scope (`wiki:node:read wiki:node:write docx:document:readonly docx:document:write_only`)

## Quy trình publish

### Bước 0 — Xác định code + title trên INDEX (BẮT BUỘC)

Mở Lark INDEX (node `${WIKI_INDEX_NODE}`, obj `${WIKI_INDEX_OBJ}`) → xác định:

- Trang mới ở **Space nào** (I/II/III/IV — Roman cố định, xem [skill 08](08-index-and-numbering.md))
- **Section nào** trong Space đó
- **Code X.Y.Z** kế tiếp (vd Section 5 của Space III đang dừng ở `5.6` → trang mới = `5.7`)
- Build **title** với dotted prefix: `<dotted-code>. <name>` (vd `5.7. Livestream luật chơi là gì?`)

```bash
# Fetch current INDEX để xem code đã dùng
lark-cli docs +fetch --api-version v2 --doc ${WIKI_INDEX_OBJ} --format pretty | head -100
```

### Bước 1 — Resolve space_id

```bash
lark-cli wiki spaces get_node --params "{\"token\":\"${WIKI_SPACE_ID}\"}" --format json
```

### Bước 2 — Liệt kê node hiện có (kiểm tra trang đã tồn tại chưa)

```bash
lark-cli wiki nodes list --params '{"space_id":"<id>","parent_node_token":"<parent>"}' --format json --page-all
```

### Bước 3a — Tạo trang MỚI

```bash
lark-cli wiki +node-create \
  --space-id <space_id> \
  --parent-node-token <parent_node_token> \
  --title "5.7. Livestream luật chơi là gì?"
# Output: obj_token + node_token
```

### Bước 3b — Cập nhật trang ĐÃ CÓ (overwrite content)

```bash
# Body markdown — KHÔNG có dòng "📍 Vị trí" callout; title qua --new-title hoặc qua <title> trong XML
cat drafts/livestream-luat-choi.md | lark-cli docs +update \
  --api-version v2 \
  --doc <obj_token> \
  --command overwrite \
  --doc-format markdown \
  --content -
```

### Bước 3c — Rename trang ĐÃ CÓ (đổi title only, GIỮ content)

**⚠️ Gotcha quan trọng:** `--new-title` flag với v2 `overwrite` **bị Lark ignore**. Title chỉ lấy từ tag `<title>...</title>` trong XML body.

Cách rename đúng (preserve content):

```bash
python3 << 'EOF'
import subprocess, json, re
OBJ="<obj_token>"
NEW="5.7. Livestream luật chơi là gì?"
r = subprocess.run(["lark-cli","docs","+fetch","--api-version","v2","--doc",OBJ,"--format","json"], capture_output=True, text=True)
xml = json.loads(r.stdout)["data"]["document"]["content"]
# Replace or prepend <title>
title_esc = NEW.replace("&","&amp;").replace("<","&lt;")
if xml.startswith("<title>"):
    new_xml = re.sub(r'^<title>[^<]*</title>', f'<title>{title_esc}</title>', xml)
else:
    new_xml = f'<title>{title_esc}</title>' + xml
subprocess.run(["lark-cli","docs","+update","--api-version","v2","--doc",OBJ,
                "--command","overwrite","--doc-format","xml","--content","-"],
               input=new_xml, text=True)
EOF
```

(Hoặc dùng v1: `--mode append --markdown " " --new-title "<new>"` — v1 hỗ trợ `--new-title` nhưng phải append content phụ.)

### Bước 4 — Verify

```bash
lark-cli docs +fetch --api-version v2 --doc <obj_token> --format json | python3 -c "import json,sys; print(json.load(sys.stdin)['data']['document']['content'][:500])"
```

Mở URL Lark Wiki trên browser, kiểm tra:

- Title hiển thị đúng (có dotted prefix)?
- Sidebar tree hiển thị `<prefix>. <name>` (vd `5.7. Livestream luật chơi là gì?`)?
- Format markdown đúng?
- Link nội bộ Lark Wiki hoạt động?
- Section "🔗 Tài liệu liên quan" có ↑ INDEX link?

### Bước 5 — Update INDEX manual (BẮT BUỘC)

Thêm row mới vào INDEX:

```bash
# 1. Fetch current INDEX content
lark-cli docs +fetch --api-version v2 --doc ${WIKI_INDEX_OBJ} --format json > /tmp/index.json

# 2. Generate INDEX markdown từ flat tree (có thể viết script sync_index.py),
#    hoặc edit manually bằng cách thêm row vào table Section tương ứng:
#    | **<code>** | [<title-có-prefix>](url) | <status> |

# 3. Push lại
lark-cli docs +update --api-version v2 \
  --doc ${WIKI_INDEX_OBJ} \
  --command overwrite \
  --doc-format markdown \
  --content @/tmp/new_index.md
```

⚠️ KHÔNG bỏ qua bước này. Trang publish mà không có trong INDEX = trang "ma" không tra cứu được.

### Bước 6 — Update status tracker

Nếu repo có code change kèm publish (vd skill update, draft mới):

- Update bảng Space tương ứng trong `docs/status-tracker.md` (hoặc file mirror tương đương)
- Format `<code> — <tên>` (vd `5.7.1 — Livestream luật chơi là gì?`)
- Commit cùng PR với code change

## Quy tắc bắt buộc

1. **Luôn dùng `--api-version v2`** cho mọi lệnh `docs`.
2. **KHÔNG publish file `.py`, `.json`, `.xml`, `.xlsx` source.** Chỉ publish markdown đã review.
3. **KHÔNG dùng workflow CI để auto-publish.** Publish luôn manual.
4. **Bước 5 (update INDEX) không bỏ qua** — đây là điểm dễ quên nhất.
5. **Rename = fetch XML + thay `<title>` tag + push, KHÔNG dùng --new-title flag với v2.** Xem Bước 3c gotcha.
6. **Verify title sau rename:** `lark-cli wiki spaces get_node` → check `title` field. Tin `"ok": true` không đủ.
7. **Log publish** vào commit message nếu có code change kèm.

## Khi gặp lỗi

| Lỗi | Nguyên nhân thường gặp |
|---|---|
| Title thành "Untitled" sau rename | Quên include `<title>...</title>` tag trong XML body. Xem Bước 3c. |
| `Permission denied` | Sai scope. Re-auth với `lark-cli auth login --domain wiki,docs --recommend` |
| `Node not found` | wiki_token sai. Lấy lại từ URL Lark Wiki |
| `Invalid content` | Markdown có syntax sai. Lint local trước bằng `markdownlint-cli2` |
| `partial_success` + timeout warning | Lark có timeout intermittent. Fetch lại verify content có push đủ chưa. Thường OK. |
| `Rate limit` | Đợi 30s rồi thử lại. Lark Wiki có rate limit 100 req/min |

Chi tiết khắc phục: xem skill `lark-shared` (cài qua `~/.agents/skills/lark-shared/`).

## 🔗 Liên quan

→ ↑ [INDEX — Wiki của bạn](https://<your-lark-tenant>.larksuite.com/wiki/${WIKI_INDEX_NODE}) — canonical
→ [Skill 06 — Excel to Wiki](06-excel-to-wiki.md) — chuyển nội dung từ file Excel
→ [Skill 07 — Source Protection](07-source-protection.md) — bảo vệ source khi publish
→ [Skill 08 — INDEX & Numbering](08-index-and-numbering.md) — quy tắc đánh số + sync INDEX

## Cách áp dụng cho team của bạn

- Set 3 env var (`WIKI_SPACE_ID`, `WIKI_INDEX_NODE`, `WIKI_INDEX_OBJ`) trong `.env` hoặc shell profile — KHÔNG commit
- Lấy giá trị từ URL Lark Wiki + `lark-cli wiki spaces get_node`
- Thay `<your-lark-tenant>` bằng subdomain Lark của tenant bạn
- Quy trình 6 bước (Bước 0 → Bước 6) là universal, không nên skip
