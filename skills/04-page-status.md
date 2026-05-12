---
name: lark-wiki-page-status
description: Use when assigning, updating, or auditing the lifecycle status of a Lark Wiki page. Defines 5 statuses (⬜ chưa làm, 🔄 đang làm, 📋 chờ review, ✅ xong, 🗄️ archived) with explicit transition rules and required metadata.
---

# Skill 04 — Trạng thái trang

Mỗi trang Wiki phải gán **1 trong 5 trạng thái** trong **Lark INDEX** (canonical). Trang Lark thật KHÔNG hiển thị status — title chỉ có dotted prefix + tên.

## 5 trạng thái

| Biểu tượng | Tên | Ý nghĩa |
|---|---|---|
| ⬜ | **CHƯA CÓ** | Trang chưa được tạo (chỉ tồn tại trong cấu trúc, chưa có nội dung) |
| 🔄 | **ĐANG VIẾT** | Đang trong quá trình viết, chưa hoàn chỉnh |
| 📋 | **TEMPLATE** | Có khung đầy đủ, chờ người phụ trách điền dữ liệu thực tế |
| ✅ | **HOÀN THÀNH** | Có nội dung đầy đủ, đã review, có thể dùng được |
| ⛔ | **ARCHIVED** | Đã archive, move sang Space ARCHIVE, code gạch ngang trong INDEX |

## Cách gán trạng thái

Status emoji được set ở 2 chỗ (đồng bộ thủ công):

1. **Lark INDEX** (`<WIKI_INDEX_NODE_ID>`) — canonical, cột Status trong table
2. **`docs/status-tracker.md`** trong repo — mirror, cập nhật cùng lúc khi đổi status

**KHÔNG đặt status emoji vào title trang Lark.** Title chỉ có `<dotted-prefix>. <name>` (xem [skill 01](01-page-format.md)).

## Khi nào chuyển trạng thái

```
⬜ CHƯA CÓ      → 🔄 ĐANG VIẾT     khi bắt đầu viết
🔄 ĐANG VIẾT   → 📋 TEMPLATE       khi đã có khung, chờ data
🔄 ĐANG VIẾT   → ✅ HOÀN THÀNH     khi đầy đủ + đã review
📋 TEMPLATE    → ✅ HOÀN THÀNH     khi đã điền data + review
✅ HOÀN THÀNH  → ⛔ ARCHIVED       khi không dùng nữa (move sang Space ARCHIVE)
```

## Quy tắc

1. **Không skip trạng thái.** Mọi trang phải gán 1 trong 5 emoji trong INDEX.
2. **INDEX là canonical.** Khi lệch giữa INDEX và status-tracker.md → INDEX thắng, sửa file mirror.
3. **Trang `📋 TEMPLATE`** phải ghi rõ "chờ ai điền gì" trong cell ghi chú INDEX. Không để TEMPLATE mãi.
4. **Trang `✅ HOÀN THÀNH`** phải có ít nhất 1 lần review (chủ sở hữu Space hoặc trưởng phòng phụ trách).
5. **Đổi status** → update INDEX + status-tracker.md trong cùng commit. Xem [skill 05 Step 5-6](05-publish-workflow.md).

## Hỏi ai khi chưa rõ trạng thái

Maintain bảng owner per Space trong repo của bạn. Ví dụ:

| Space | Người review |
|---|---|
| `I` — CHUNG | Owner Space I (vd CEO) |
| `II` — NỘI BỘ | Trưởng HCNS / KTT |
| `III` — VẬN HÀNH | Trưởng BP phụ trách |
| `IV` — BAN GIÁM ĐỐC | Owner Space IV |

## 🔗 Liên quan

→ ↑ [INDEX — Wiki của bạn](https://<your-lark-tenant>.larksuite.com/wiki/<WIKI_INDEX_NODE_ID>) — canonical
→ [Skill 01 — Page Format](01-page-format.md) — title format `<prefix>. <name>` (không có status emoji)
→ [Skill 05 — Publish Workflow](05-publish-workflow.md) — sync INDEX + status tracker sau publish
→ [Skill 08 — INDEX & Numbering](08-index-and-numbering.md) — quy tắc INDEX

## Cách áp dụng cho team của bạn

- 5 trạng thái (⬜🔄📋✅⛔) là universal — giữ nguyên
- Customize bảng owner per Space + path file mirror status (`docs/status-tracker.md` hoặc tên khác)
- Thay `<WIKI_INDEX_NODE_ID>` bằng node ID INDEX thực tế của bạn
