---
name: lark-wiki-contributor-flow
description: Use when reviewing a contributor draft as the @wiki-reviewer bot persona, when onboarding a non-Git contributor through the 3-step Lark-group flow, or when explaining the publish-after-approval gate. Trigger on any task that involves the human-facing contribution loop (vs. direct AI authoring).
---

# Skill 09 — Workflow Contributing + Bot Review

Cách AI agent (Claude/Codex/người trực) đảm nhận role **`@wiki-reviewer`** — đọc trang Lark do nhân viên gửi, check format theo skills/01-08, comment kết quả trên trang + cập nhật INDEX.

Phía nhân viên đọc `docs/contributing.md` (quy trình 3 bước qua group chat). File này dành cho **AI agent / dev trực**.

---

## 1. Hai phase

| Phase | Trạng thái | Cách bot nhận trigger |
|---|---|---|
| **Phase 1 — Manual** | 🟡 Backup | Agent on-duty đọc message trong group chat (hoặc inbox group email), chạy `lark-cli` thủ công, post result qua **incoming webhook**. Dùng khi Phase 2 down. |
| **Phase 2 — Event-driven** | ✅ Running | Claude MCP bot subscribe `im.message.receive_v1` → `scripts/wiki_reviewer_bot.py` chạy 5-dim qualitative review (skill 09 §3) → comment + webhook notification. |

⚠️ **Đừng nhầm 2 thực thể trong group:**

| Thực thể | Vai trò | Direction |
|---|---|---|
| **`@wiki-reviewer`** (incoming webhook) | **Notification channel** — chỉ POST status text vào group | 1 chiều OUT |
| **Claude MCP bot** (custom app `cli_…` — credentials managed externally, không commit) | **Brain** — nhận event, chạy review, gọi Lark API | 2 chiều IN+OUT |

Workflow Phase 2 đầy đủ:

```
Nhân viên paste URL + @mention Claude MCP bot
  ↓ im.message.receive_v1
Claude MCP bot endpoint → Claude agent chạy skill 09 §3
  ↓
Comment trên trang Lark (drive comment API)
  ↓
POST notification về group qua @wiki-reviewer webhook
  ↓
Owner repo reply "approved" trong group → Claude MCP bot update INDEX
```

**Hạ tầng cần có:**

| Item | Value |
|---|---|
| Group chat | Group contributor của bạn (vd `WikiContributor`) |
| Notification webhook (`@wiki-reviewer`, 1-way OUT) | URL incoming webhook từ Lark, lưu trong env `LARK_WEBHOOK_URL` |
| Brain bot | Claude MCP custom app, `app_id` + `app_secret` lưu trong env (KHÔNG commit) |
| Group email (fallback input) | Email group của bạn (Lark group có sẵn email) |
| INDEX node | `<WIKI_INDEX_NODE_ID>` · obj `<WIKI_INDEX_OBJ_ID>` |

---

## 2. Trigger & extract obj_token

URL nhân viên paste có 2 dạng:

```
https://<your-lark-tenant>.larksuite.com/wiki/<wiki_node_token>
https://<your-lark-tenant>.larksuite.com/docx/<obj_token>          # ít gặp
```

Bot extract token từ URL:

```python
import re
m = re.search(r"/wiki/([A-Za-z0-9]+)", url)
wiki_node_token = m.group(1) if m else None
```

Sau đó resolve sang `obj_token` (để fetch content) qua:

```bash
lark-cli wiki spaces get_node --params '{"token":"<wiki_node_token>"}' --format json
# Lấy field obj_token + space_id + title hiện tại
```

---

## 3. Bot review — 5 chiều đánh giá định tính

Bot **KHÔNG chấm pass/fail**. Bot chấm **điểm 0-10 cho 5 chiều**, ra điểm tổng `x.x/10` có trọng số, KÈM ≥ 1 điểm mạnh + 0-4 gợi ý cải thiện.

Triết lý: giúp người viết hoàn thiện, KHÔNG bới lỗi.

| # | Chiều | Trọng số | Câu hỏi đánh giá |
|---|---|---|---|
| 1 | **Detail (độ chi tiết)** | 3 | Đọc xong có làm được việc thật? Có thiếu bước, deadline, người phối hợp, ví dụ cụ thể? |
| 2 | **Linking (tính liên kết)** | 2 | Có link tới INDEX, Section cha, trang liên quan, Lark Base? Section "🔗 Tài liệu liên quan" đầy đủ? |
| 3 | **Feasibility (đối chiếu nguồn)** | 3 | Claims có xác thực được với Excel / Lark Base / SOP gốc? Có mâu thuẫn? |
| 4 | **Structure (cấu trúc)** | 1 | Đủ section bắt buộc 🎯/⚡/📋/⚠️/🔗? Title format `X.Y.Z. <name>`? KHÔNG có callout 📍? |
| 5 | **Writing (văn phong)** | 1 | Tiếng Việt tự nhiên, không lặp ý, đúng kind (procedure/reference/template)? |

**Overall** = `Σ (score_i × weight_i) / Σ weights` → `x.x / 10` (1 chữ số thập phân).

**Thresholds:**

| Score | Emoji | Tier | Action |
|---|---|---|---|
| **≥ 8.0** | ✨ | **Excellent** | Có thể tag owner duyệt |
| **6.5 – 7.9** | 👍 | **Good** | Có thể tag owner duyệt, kèm gợi ý nhỏ |
| **5.0 – 6.4** | 🔄 | **Khá** | Người viết xem comment + revise 1-2 điểm |
| **< 5.0** | 🌱 | **Cần đầu tư thêm** | Người viết xem comment + viết lại section |

Chấm thoáng — trang OK xứng 7+, trang tốt 8+, xuất sắc 9+.

---

## 4. Bot output format

**Quy tắc tone bắt buộc:**
- KHÔNG dùng "FAIL", "PASS", "TEST", "vi phạm".
- LUÔN ít nhất 1 điểm mạnh (`strengths`) trước gợi ý — kể cả trang sơ sài.
- `suggestions` dùng dạng "có thể bổ sung…" / "gợi ý thêm…" — KHÔNG mệnh lệnh.

### Comment trên trang Lark (Markdown, ≤ 1000 chars)

```text
## ✨ Wiki Review — 2.2. Ngày đầu tiên · 8.2/10 (Excellent)

**Điểm mạnh:**
- ✅ Cấu trúc bước rõ ràng theo giờ (sáng / trưa / chiều)
- ✅ Có ví dụ cụ thể về biểu mẫu HCNS cần ký

**Có thể cải thiện thêm:**
- 💡 Bước "Gặp mặt team trưa" — thêm thời lượng dự kiến để người mới chuẩn bị
- 💡 Phần "cài đặt công cụ" — có thể link sang trang 3.1 "Danh sách công cụ"

**Chi tiết điểm số:** Độ chi tiết 8/10 · Liên kết 6/10 · Khả thi 9/10 · Cấu trúc 9/10 · Văn phong 8/10

— @wiki-reviewer (skill 09 v2)
```

### Webhook notification (1 dòng, group chat)

```text
✨ 2.2. Ngày đầu tiên — 8.2/10. Có thể tag owner duyệt: <url>
👍 3.1. Danh sách công cụ — 7.0/10. Có thể tag owner duyệt: <url>
🔄 4.3. Chính sách đổi trả — 5.8/10. Người viết xem comment + revise 1-2 điểm: <url>
🌱 1.4. Ai là ai? — 3.5/10. Người viết xem comment + viết lại section: <url>
```

---

## 5. Sau khi pass — update INDEX

Bot thực hiện **2 update** trên INDEX (obj `<WIKI_INDEX_OBJ_ID>`):

### 5a. Status cell

- Trang mới → `📋` (chờ owner duyệt) HOẶC giữ nguyên `🔄` nếu trang đang viết.
- Owner duyệt → đổi sang `✅`.

### 5b. Contributed cell

Append `<cite type="user" user-id="<ou_xxx>"></cite>` vào cell `Contributed` của row tương ứng. **Dedupe** (1 user chỉ xuất hiện 1 lần).

Logic dedupe:

```python
import re
def add_contributor(cell_xml: str, user_id: str) -> str:
    if f'user-id="{user_id}"' in cell_xml:
        return cell_xml  # đã có
    new_cite = f'<cite type="user" user-id="{user_id}"></cite>'
    # Append vào cell (giữ các cite cũ)
    return cell_xml.rstrip('</p></td>') + new_cite + '</p></td>'
```

**Khi nào append:**
- User edit > 5 blocks → contributor đáng kể, append.
- User chỉ fix typo → không append (không spam cell).

Bot dùng `lark-cli docs +update --api-version v2 --command str_replace --doc <WIKI_INDEX_OBJ_ID>` với:
- `--old`: cell hiện tại
- `--new`: cell + cite mới

---

## 6. Owner duyệt cuối (Approval flow)

**Cơ chế detect:** Bot listen mọi message trong group contributor. Nếu
1 message thoả **cả 2 điều kiện**:

1. **Là reply trong thread** (event có `parent_id` ≠ null)
2. **Nội dung khớp keyword approval**: `approved` / `approve` / `duyệt` /
   `ok` / `✅` / `👍` (regex case-insensitive, optional prefix `@wiki-reviewer`)

→ bot trigger approval flow.

**Approval flow:**

1. Bot kiểm tra `sender_open_id` có trong whitelist `LARK_APPROVER_OPEN_IDS`
   (env var). Nếu whitelist rỗng = mọi user approve được (TEST only).
2. Bot fetch parent message qua `im.v1.message.get` API → extract wiki URL.
3. Bot fetch INDEX XML (qua `lark-cli docs +fetch`, dùng user auth của owner
   trên máy chạy bot).
4. Mutate row matching `href="<url>"`:
   - Status cell (cột 3) → `<p>✅</p>` (replace nội dung cũ)
   - Contributed cell (cột 4) → append `<cite type="user" user-id="<open_id>"></cite>`
     (dedupe — nếu open_id đã có thì skip)
5. Push INDEX qua `lark-cli docs +update --command overwrite`.
6. POST webhook notification: `✅ Đã duyệt. INDEX cập nhật...: <url>`.

| User reply trong thread | Bot action |
|---|---|
| `approved` / `approve` / `duyệt` / `ok` / `✅` / `👍` | Update status → `✅` + append Contributed |
| Khác (không match keyword) | Bot bỏ qua |

**Quy tắc:**

- Bot KHÔNG tự đổi `✅` khi không có user trong whitelist approve.
- Whitelist `LARK_APPROVER_OPEN_IDS` rỗng → TEST mode (anyone), không dùng prod.
- Khi parent message không có wiki URL hoặc fetch fail → bot bỏ qua silently
  (log INFO).
- `back` / `archive` actions chưa implement — fallback manual qua
  `scripts/sync_index_contributed_column.py`.

---

## 7. Identity & scopes cần có

### Phase 2 — Claude MCP bot (chính)

Claude MCP custom app trong group contributor cần các scope sau (cấp trong Lark Developer Console):

```text
wiki:node:read wiki:node:write
docx:document:readonly docx:document:write_only
drive:comment
im:message im:message.group_at_msg im:message.group_at_msg:readonly
```

Credentials (`app_id`, `app_secret`) **KHÔNG hardcode** trong repo. Lưu qua env:

```bash
export LARK_APP_ID=cli_xxx               # không commit
export LARK_APP_SECRET=xxx               # không commit, rotate khi nghi leak
export LARK_WEBHOOK_URL=https://...      # @wiki-reviewer webhook (có thể commit nếu webhook private)
```

### Phase 1 — Manual fallback

```bash
# Agent on-duty dùng user identity (owner repo hoặc admin)
lark-cli auth login --as user --recommend
```

Không cần custom app — chỉ cần user scope đủ để fetch + update doc + comment.

---

## 8. Phase 2 — setup checklist

Status: 🟢 Running — `scripts/wiki_reviewer_bot.py` đang chạy persistent WS.

- [x] Claude MCP custom app trên Lark Developer Console
- [x] App add vào group contributor
- [x] Persistent connection mode (Official SDK, không cần endpoint URL)
- [x] Scopes: `wiki:node:read docx:document:readonly drive:comment im:message`
- [x] Runner: `scripts/wiki_reviewer_bot.py` (lark-oapi + Anthropic SDK)
- [x] E2E test với trang thật
- [ ] Secret rotation policy: rotate mỗi 90 ngày HOẶC khi nghi leak

**Migration từ Phase 1 → Phase 2:** Mọi rule trong skill này (§2-§6, §9) **GIỮ NGUYÊN**. Chỉ thay tầng trigger (manual đọc message → event webhook).

**Khi Phase 2 down:** rollback về Phase 1 manual workflow (chỉ cần `lark-cli auth login --as user`).

---

## 8.5. System prompt cho Claude MCP bot

Triển khai thực tế: dùng `scripts/wiki_reviewer_bot.py`. Prompt + tool schema
hard-coded trong script (`SYSTEM_PROMPT` + `REVIEW_TOOL`) — sửa rules thì
sửa script, KHÔNG paste prompt vào Lark Developer Console nữa.

Outline rules (rút gọn để tham khảo nhanh):

```text
Bạn là @wiki-reviewer — agent đánh giá CHẤT LƯỢNG NỘI DUNG trang Wiki
của công ty. Mục tiêu: GIÚP người viết hoàn thiện, KHÔNG phải tìm lỗi.

Bắt buộc trả qua tool `submit_review` với:
- scores: 5 chiều, mỗi 0-10 (detail, linking, feasibility, structure, writing)
- strengths: 1-3 điểm mạnh CỤ THỂ (luôn có ít nhất 1, kể cả trang sơ sài)
- suggestions: 0-4 gợi ý "có thể bổ sung..." (không mệnh lệnh)
- title, code

Chấm thoáng: OK = 7+, tốt = 8+, xuất sắc = 9+.

Quy tắc tone:
- KHÔNG dùng "FAIL", "PASS", "TEST", "vi phạm"
- LUÔN khen trước, gợi ý sau
- Gợi ý dạng "có thể bổ sung..." / "tham khảo trang X..." — không mệnh lệnh
```

Chi tiết đầy đủ + tool schema xem trực tiếp trong
[`scripts/wiki_reviewer_bot.py`](../scripts/wiki_reviewer_bot.py) (constants
`SYSTEM_PROMPT` + `REVIEW_TOOL`).

---

## 9. Multi-contributor scenario

Khi 1 trang được nhiều người sửa qua nhiều phiên:

- Mỗi phiên review pass → bot append user vào cell Contributed (dedupe).
- Cell có thể list 3-5 user mention — OK.
- Nếu cell quá nhiều (> 5) → bot warn owner repo, suggest tách trang.

---

## 🔗 Tài liệu liên quan

→ ↑ [INDEX — Wiki của bạn](https://<your-lark-tenant>.larksuite.com/wiki/<WIKI_INDEX_NODE_ID>) — canonical
→ `docs/contributing.md` — phía nhân viên (3 bước đóng góp)
→ [Skill 01 — Page Format](01-page-format.md) — check title + section bắt buộc
→ [Skill 03 — Linking Rules](03-linking-rules.md) — check `↑ INDEX` link
→ [Skill 05 — Publish Workflow](05-publish-workflow.md) — Step 5 sync INDEX
→ [Skill 08 — INDEX & Numbering](08-index-and-numbering.md) — quy tắc đánh số

## Cách áp dụng cho team của bạn

- **Bot framework:** giữ nguyên `@wiki-reviewer` (notification webhook) + Claude MCP bot (brain) — đây là kiến trúc của framework v2.0
- **Customize:** tên group chat (vd `WikiContributor`), email group, danh sách approver (`LARK_APPROVER_OPEN_IDS`)
- **Env vars cần set:** `LARK_APP_ID`, `LARK_APP_SECRET`, `LARK_WEBHOOK_URL`, `WIKI_INDEX_NODE`, `WIKI_INDEX_OBJ`, `LARK_APPROVER_OPEN_IDS`
- 5-dim scoring rubric + thresholds (8.0/6.5/5.0) là universal — có thể giữ nguyên hoặc tinh chỉnh trọng số theo ưu tiên team
