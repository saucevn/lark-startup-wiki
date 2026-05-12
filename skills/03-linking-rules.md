---
name: lark-wiki-linking
description: Use when adding internal links between Wiki pages, links to Lark Base records, mention links to people/groups, or external resource links. Defines the 4 required link types (intra-Wiki, Wiki↔Base, mention, external) and when each applies.
---

# Skill 03 — Quy tắc liên kết giữa các trang & Lark Base

## 4 loại link bắt buộc

### Loại 1 — LINK NGANG (giữa các trang Wiki)

- Cuối mỗi trang **bắt buộc** có section `## 🔗 Tài liệu liên quan`
- Tối thiểu **2 link ngang** đến trang liên quan
- Mỗi link phải có lý do: `→ [<dotted-code>. <Tên trang>](url) — [lý do liên quan]`
- Inline link format theo title trang đích (đã có dotted prefix). Vd:
  `[5.7.2. Top 25 lỗi cấm khi livestream — đừng phạm cái nào?](url) — chi tiết 5 nhóm lỗi`

### Loại 2 — LINK XUỐNG (Wiki → Lark Base)

Mọi trang có **dữ liệu tracking** phải link vào Lark Base tương ứng.

Ví dụ:

- Trang `O3K HCNS` → link Lark Base `O3K Tracking`
- Trang `KPI KTT` → link Lark Base `KPI Tháng từng vị trí`
- Trang `Quy trình lương` → link Lark Base `Quy trình lương tháng`

Maintain danh sách mapping Wiki page ↔ Lark Base trong `docs/` repo của bạn.

### Loại 3 — LINK THUẬT NGỮ

Mỗi thuật ngữ chuyên ngành **lần đầu** xuất hiện trong trang:

- Link đến Glossary tương ứng
- HOẶC giải thích trong ngoặc đơn (nếu thuật ngữ chỉ dùng 1 lần)

Xem [skill 02 §3](02-writing-style.md#3-thuật-ngữ-chuyên-ngành--phải-giải-thích-lần-đầu).

### Loại 4 — LINK LÊN (Wiki → INDEX)

Mỗi trang **BẮT BUỘC** có link `↑ INDEX` trong section "🔗 Tài liệu liên quan":

```markdown
→ ↑ [INDEX — Wiki của bạn](https://<your-lark-tenant>.larksuite.com/wiki/<WIKI_INDEX_NODE_ID>) — toàn cảnh các Space
```

Khuyến nghị bổ sung: link `↑ Section cha` (parent folder) để duyệt các trang cùng section.

## Cấu trúc section "🔗 Tài liệu liên quan"

```markdown
## 🔗 Tài liệu liên quan

→ ↑ [INDEX — Wiki của bạn](https://<your-lark-tenant>.larksuite.com/wiki/<WIKI_INDEX_NODE_ID>) — toàn cảnh các Space
→ ↑ [5. Marketing & Content](url) — Section cha, các trang cùng section
→ [5.7.2. Top 25 lỗi cấm khi livestream — đừng phạm cái nào?](url) — chi tiết 5 nhóm lỗi
→ [2.2. Quy trình lương 18 bước](url) — bước 1-3 mô tả cách nhận phiếu BG
→ 📊 [Lark Base — Quy trình lương tháng](url) — track tiến độ real-time
→ 📥 [QuyTrinhLuong_2026.xlsx](sources/excel/...) — file Excel chi tiết
```

## Định dạng link

- **Link nội bộ Wiki:** dùng full title có dotted prefix (vd `[5.7.1. Livestream luật chơi là gì?](url)`)
- **Link Lark Base:** dùng `📊` prefix
- **Link file Excel/PDF:** dùng `📥` prefix
- **Link Section cha:** dùng `↑` prefix

## Khi nào KHÔNG cần link ngang

- Folder pages (Section/Subsection) — đã là TOC liệt kê con
- Trang nhỏ < 200 từ (vẫn cần ≥ 1 link — `↑ INDEX`)

## Kiểm tra trước khi publish

- [ ] Section `🔗 Tài liệu liên quan` có ≥ 2 link?
- [ ] **Có link `↑ INDEX`** trong "🔗 Tài liệu liên quan"?
- [ ] Mỗi link có lý do?
- [ ] Inline link dùng full title có dotted prefix?
- [ ] Mọi thuật ngữ chuyên ngành đã link/giải thích?
- [ ] Nếu trang có dữ liệu tracking → đã link Lark Base?

## Cách áp dụng cho team của bạn

- Thay `<your-lark-tenant>` + `<WIKI_INDEX_NODE_ID>` bằng tenant + INDEX node của bạn
- 4 loại link là universal — nên giữ nguyên cấu trúc
- Có thể customize prefix emoji (📊 cho Lark Base, 📥 cho file đính kèm) theo convention nội bộ
