---
name: lark-wiki-page-format
description: Use when authoring or editing a Lark Wiki page. Enforces the mandatory 7-section page format (TL;DR → Mục đích → Nội dung → Liên quan → Trạng thái → Lịch sử → Owner). Triggers on any task involving creating, restructuring, or reviewing a Wiki page draft for a Vietnamese-speaking startup using Lark/Feishu Wiki.
---

# Skill 01 — Format chuẩn mỗi trang Wiki

Mọi trang Wiki phải tuân theo format dưới đây. **Không thêm, không bớt mục.**

## Template chuẩn

```markdown
# <dotted-code>. <Tiêu đề theo `kind`>
# Ví dụ:
#   "5.7.1. Livestream — luật chơi là gì?"  (kind: procedure)
#   "4.5. Tên sản phẩm chuẩn (SKU list)"     (kind: reference)
#   "5.1. Template họp nội bộ"               (kind: template)

## 🎯 Dành cho ai
[1 dòng — vị trí hoặc nhóm người cần đọc trang này]

## ⚡ Tóm tắt nhanh
[3 dòng tối đa — đọc 30 giây biết ngay cần làm gì]

## 📋 Chi tiết từng bước

**Bước 1: [Tên bước — động từ hành động]**
- Làm gì cụ thể
- Công cụ / form cần dùng
- Ai phối hợp
- Deadline (nếu có)

**Bước 2: ...**

## ⚠️ Lưu ý quan trọng
[Điểm dễ sai / dễ bỏ qua / rủi ro nếu không làm đúng]

## 🔗 Tài liệu liên quan

→ ↑ [INDEX — Wiki của bạn](https://<your-lark-tenant>.larksuite.com/wiki/<WIKI_INDEX_NODE_ID>) — toàn cảnh các Space
→ ↑ [Section cha — Tên Section](url) — các trang cùng section
→ [<code> — Tên trang](url) — lý do liên quan
→ 📊 [Tên Lark Base](url) — track real-time
→ 📥 [Tên file](sources/excel/...) — đính kèm

## 📅 Lịch sử cập nhật
| Ngày | Người cập nhật | Thay đổi |
|------|----------------|----------|
| ___/____ | ___ | Tạo mới |
```

## Quy tắc bắt buộc

1. **6 section trên là bắt buộc** — không bỏ section nào, không thêm section mới.
2. **Title H1 BẮT BUỘC có dotted prefix** — format `<dotted-code>. <name>`:
   - Page trong Section: `2.1.`, `3.4.5.` v.v. (Roman bỏ vì context implicit từ tree)
   - Subsection (folder): cũng có prefix `1.1.`, `5.7.` v.v.
   - Space root: `<emoji> <Roman>. <NAME>` (vd `🏢 I. CHUNG` — tên space root tuỳ chỉnh theo công ty của bạn)
   - Xem [skill 08](08-index-and-numbering.md) cho quy tắc số.
3. **Title content theo `kind`** ([skill 02](02-writing-style.md)):
   - `procedure` → câu hỏi sau prefix (vd "5.7.1. Livestream luật chơi là gì?")
   - `reference` → noun phrase sau prefix (vd "4.5. Tên sản phẩm chuẩn (SKU list)")
   - `template` → "Template — `<tên>`" sau prefix (vd "5.1. Template họp nội bộ")
4. **Mỗi trang tối đa 2 trang A4** in ra. Dài hơn → tách trang.
5. **Section "🔗 Tài liệu liên quan" phải có ≥ 2 link**, trong đó BẮT BUỘC có `↑ INDEX` ([skill 03](03-linking-rules.md)).
6. **KHÔNG thêm callout breadcrumb** ở đầu trang — title đã có code, INDEX có status. Đơn giản hoá.
7. **Trạng thái trang** chỉ ghi ở INDEX (canonical) + status tracker mirror trong repo.
   Trang Lark không hiển thị status emoji. Xem [skill 04](04-page-status.md).

## Folder pages (Section / Subsection / Space root) — format ngắn

Folder pages chỉ là landing page, không cần 6 section nội dung. Format:

```markdown
# <prefix>. <Tên folder>

## 📚 Mục lục

| Code | Trang | Status |
|---|---|---|
| **<sub-code>** | [Tên trang](url) | ✅ |
| ... |
```

(Folder có thể có thêm intro/overview content nếu cần, sau bảng TOC.)

## Khi nào dùng template này

- Viết trang Wiki mới
- Cập nhật trang cũ không đúng format
- Tạo template tái sử dụng

## Khi nào KHÔNG dùng template này

- Folder pages (Section/Subsection/Space root) — dùng format folder ngắn ở trên
- Trang Thuật ngữ A-Z — dùng table thay vì step
- Trang biên bản họp BGĐ — template riêng theo Space của bạn

## Cách áp dụng cho team của bạn

- Thay `<your-lark-tenant>` + `<WIKI_INDEX_NODE_ID>` bằng tenant + node ID INDEX của bạn (lấy từ URL Lark Wiki)
- Có thể giữ nguyên bộ 6 section bắt buộc — đây là contract của framework
- Có thể customize emoji Space root theo phòng ban thực tế (vd 🏢 I. CHUNG, 💰 II. NỘI BỘ ...)
