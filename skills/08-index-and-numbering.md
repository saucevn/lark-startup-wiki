---
name: lark-wiki-numbering
description: Use when creating a new page, renaming an existing one, reorganizing the page tree, or onboarding a new contributor to the page-tree convention. Defines the I> 1.2.3 numbering scheme (Roman.Decimal), 4-Space recommended layout, INDEX page as canonical TOC, and rules for re-numbering after a move.
---

# Skill 08 — INDEX & Quy tắc đánh số

INDEX là **nguồn canonical** biết trang nào ở đâu, status gì. Mọi thay đổi cấu trúc Wiki phải sync về INDEX trước khi merge.

## 1. INDEX ở đâu

| Thuộc tính | Giá trị |
|---|---|
| Wiki URL | `https://<your-lark-tenant>.larksuite.com/wiki/<WIKI_INDEX_NODE_ID>` |
| node_token | `<WIKI_INDEX_NODE_ID>` |
| obj_token (dùng cho `docs +update`) | `<WIKI_INDEX_OBJ_ID>` |
| Parent | Wiki space root `<WIKI_SPACE_ID>` |

Thiết lập 3 giá trị này thành env vars (`WIKI_SPACE_ID`, `WIKI_INDEX_NODE`, `WIKI_INDEX_OBJ`) — xem [skill 05](05-publish-workflow.md).

## 2. Quy tắc đánh số

**Code (internal reference):** `<Roman>> <X.Y.Z>` — vd `II> 2.2.1`. Dùng trong skill rules, repo docs, commit messages.

**Title (display trên Lark):** `<dotted-prefix>. <name>` — vd `2.2.1. Lịch lương tháng (ngày 26 → 05)`.

Roman chỉ xuất hiện trong **title của Space root**. Bộ Space khuyến nghị mặc định (4 Space):

| Roman | Space | Title trên Lark | Ví dụ page con |
|---|---|---|---|
| **I** | CHUNG | `🏢 I. CHUNG` | `1.1. Công ty là gì?` |
| **II** | NỘI BỘ (HCNS + Kế toán) | `💰 II. NỘI BỘ` | `2.2.1. Lịch lương tháng (ngày 26 → 05)` |
| **III** | VẬN HÀNH | `📊 III. VẬN HÀNH` | `5.7.1. Livestream luật chơi là gì?` |
| **IV** | BAN GIÁM ĐỐC | `🔒 IV. BAN GIÁM ĐỐC` | `1.1. Chiến lược` |

**Bộ 4 Space này là khuyến nghị mặc định** — phù hợp cho startup 10-50 người. Có thể customize theo phòng ban thực tế (vd `I. SẢN PHẨM / II. KỸ THUẬT / III. KINH DOANH`). **Quy tắc đánh số (`I> 1.2.3`) là phần universal contribution của framework — giữ nguyên.**

**5 quy tắc bắt buộc:**

1. **Tối đa 3 cấp** Arabic — `<Section>.<Page>` HOẶC `<Section>.<Subsection>.<Page>`. KHÔNG có cấp 4.
2. **Subsection optional** — chỉ dùng khi gom nhiều trang cùng chủ đề (vd `5.7. Livestream` gom 5 trang con `5.7.1` → `5.7.5`). Section không có subsection thì page chỉ 2 cấp (`5.6.`).
3. **Append-only** — trang mới luôn cuối section (vd `5.6.` → `5.7.`), KHÔNG chen giữa.
4. **Không tái sử dụng code** — trang xoá → code vẫn reserved, không gán cho trang khác.
5. **Roman cố định** — không thêm Space mới mà không hỏi owner repo / CEO.

## 3. Khi tạo trang mới

Theo [skill 05 Step 0](05-publish-workflow.md):

1. Mở Lark INDEX → xác định Space + Section đích
2. Tìm code cuối trong Section đó (vd Section 5 dừng ở `III> 5.6` → trang mới = `III> 5.7`)
3. Nếu trang mới là phần của nhóm cùng chủ đề → tạo subsection: `5.7.` (folder) + children `5.7.1.`, `5.7.2.`…
4. Build title `<dotted-prefix>. <name>` theo [skill 01](01-page-format.md) + [skill 02 `kind` rule](02-writing-style.md)
5. Tạo node trên Lark với `--title "<full title có prefix>"`
6. Sau khi tạo → update INDEX row mới (skill 05 Step 5)

## 4. Khi đổi status

Sync **2 chỗ** manual:

1. **Lark INDEX** (canonical) → đổi emoji status trong column "Status"
2. **`docs/status-tracker.md`** (mirror) → đổi cùng emoji

**KHÔNG có status emoji trên trang Lark** — title chỉ là `<prefix>. <name>`, status chỉ tra ở INDEX. Xem [skill 04](04-page-status.md).

Nếu lệch giữa 2 nơi → Lark INDEX thắng.

## 5. Khi rename trang

- **GIỮ code cũ** — không đổi số khi rename
- Đổi tên trên 3 nơi: Lark page title (qua `<title>` XML body — KHÔNG dùng `--new-title` flag, xem skill 05 Bước 3c), Lark INDEX row, status tracker
- Update title cũng để trong "🔗 Tài liệu liên quan" của các trang link đến

## 6. Khi xoá trang

1. **KHÔNG delete** — move sang Space "ARCHIVE — Nội dung cũ" (tạo 1 Space riêng cho archive)
2. INDEX: gạch ngang code `~~5.7.1.~~` + chuyển status sang ⛔
3. Trang con của subsection bị xoá → phải xoá hết trang con trước

## 7. Folder pages (Space root / Section / Subsection)

Folder pages là landing page có TOC ([skill 01 — folder format](01-page-format.md)):

```markdown
# <prefix>. <Tên folder>

## 📚 Mục lục

| Code | Trang | Status |
|---|---|---|
| **<sub-code>** | [<sub-title>](url) | ✅ |
| ... |
```

- KHÔNG có callout `📍 Vị trí` ở đầu — title đã đủ thông tin.
- TOC bắt buộc liệt kê đầy đủ các trang con (clickable link).
- Folder pages có thể có thêm content sau TOC (vd Section `1. Về công ty` có timeline whiteboard).

## 8. Bot identity vs User identity

- `lark-cli ... --as user` để edit INDEX (cần scope `wiki:node:read wiki:node:write docx:document:readonly docx:document:write_only`)
- INDEX là document loại `docx`, không phải wiki node thường → dùng `docs +update`, không phải `wiki +node-create`

## 🔗 Tài liệu liên quan

→ ↑ [INDEX — Wiki của bạn](https://<your-lark-tenant>.larksuite.com/wiki/<WIKI_INDEX_NODE_ID>) — canonical
→ [Skill 01 — Page Format](01-page-format.md) — title format `<prefix>. <name>` (no callout 📍)
→ [Skill 02 — Writing Style](02-writing-style.md) — 3 `kind` (procedure/reference/template)
→ [Skill 03 — Linking Rules](03-linking-rules.md) — Loại 4 LINK LÊN INDEX (bắt buộc)
→ [Skill 05 — Publish Workflow](05-publish-workflow.md) — Step 0 + Step 5 sync INDEX + Bước 3c rename gotcha

## Cách áp dụng cho team của bạn

- **Universal (giữ nguyên):** numbering scheme `<Roman>> <X.Y.Z>`, max 3 cấp Arabic, append-only, không tái sử dụng code
- **Customizable:** số lượng Space (4 là khuyến nghị mặc định, có thể 3 hoặc 5), tên Space, emoji Space root
- Thay `<WIKI_SPACE_ID>` / `<WIKI_INDEX_NODE_ID>` / `<WIKI_INDEX_OBJ_ID>` bằng giá trị thực tế của bạn (lấy từ URL Lark Wiki)
- Nếu tổ chức theo phòng ban thay vì 4 Space chuẩn, vẫn giữ pattern `<Roman>> <X.Y.Z>` cho consistency
