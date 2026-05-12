---
name: lark-wiki-writing-style
description: Use when writing titles, headings, body content, or examples for a Lark Wiki page in Vietnamese. Defines title-by-kind rules, heading hierarchy limits, sentence/paragraph constraints, and approved/banned vocabulary. Apply alongside the page-format skill.
---

# Skill 02 — Quy tắc viết tiêu đề & nội dung

## 1. Tiêu đề — `<prefix>. <name>` theo `kind`

Title H1 luôn có format `<dotted-code>. <name>`. Phần `<name>` phụ thuộc `kind`:

| `kind` | `<name>` rule | Ví dụ full title |
|---|---|---|
| **procedure** | **BẮT BUỘC câu hỏi** | "5.7.1. Livestream luật chơi là gì?" · "2.2. Ngày đầu tiên — làm gì từng giờ?" |
| **reference** | Noun phrase OK | "4.5. Tên sản phẩm chuẩn (SKU list)" · "1.1. Brand Voice của công ty" |
| **template** | `"Template — <tên>"` | "5.1. Template họp nội bộ" · "5.2. Template báo cáo sự cố" |

**Khi nào dùng kind nào:**

- `procedure` — SOP, quy trình, "làm gì", "khi nào", "xử lý thế nào"
- `reference` — danh sách, từ điển, mapping, dashboard, JD, bảng số liệu
- `template` — khung mẫu tái sử dụng (chờ điền data)

**Lý do nới rule:** trang reference (JD, SKU list) là danh sách tra cứu — ép thành câu hỏi gượng.
Trang procedure mới cần câu hỏi vì người đọc đang tìm "phải làm gì".
Phân loại sai (procedure dùng noun phrase) = fix trước khi publish.

❌ SAI cho `kind: procedure`:

- "5.3. Quy trình sản xuất content" → đổi "5.3. Sản xuất content — quy trình thế nào?"
- "4.2. Quy trình xử lý khiếu nại" → đổi "4.2. Khi khách khiếu nại — xử lý thế nào?"

❌ SAI prefix:

- "Công ty là gì?" → thiếu prefix → đổi "1.1. Công ty là gì?"
- "I> 1.1. Công ty là gì?" → thừa Roman → đổi "1.1. Công ty là gì?" (Roman chỉ ở Space root title)

## 2. Nội dung — viết cho người dùng

```
✅ Viết cho người đọc — không phải cho người viết
✅ Mỗi bước = 1 hành động cụ thể — phải có động từ
✅ Có ví dụ thực tế nếu bước phức tạp
✅ Deadline phải có con số cụ thể (24h, 3 ngày, ngày 26 hàng tháng…)
✅ Ai đọc cũng tự làm được — không cần hỏi thêm

❌ Không dùng từ mơ hồ: "nhanh chóng", "kịp thời", "phù hợp"
❌ Không viết quá 2 trang A4
❌ Không gộp nhiều hành động vào 1 bước
❌ Không dùng giọng văn quan liêu, văn bản hành chính
```

## 3. Thuật ngữ chuyên ngành — phải giải thích lần đầu

Khi nhắc đến thuật ngữ chuyên ngành **lần đầu** trong trang:

- **In đậm** từ đó
- *Giải thích ngắn trong ngoặc đơn* HOẶC link đến Glossary của bạn

### Ví dụ

```
Chỉ số **eNPS** *(Employee Net Promoter Score — đo mức độ hài lòng nhân viên)*
cần đạt ≥ 50.
```

```
**Phiếu BG** *(Bảng giao lương — xem Glossary)*
được KTT chuyển cho HCNS trước ngày 03 hàng tháng.
```

## 4. Số liệu — phải cụ thể

```
✅ "Hoàn thành trước 17h ngày 03 hàng tháng"
✅ "Tối đa 30 phút response"
✅ "≥ 50 (theo thang điểm chuẩn eNPS)"

❌ "Hoàn thành sớm"
❌ "Response nhanh"
❌ "Đạt mức tốt"
```

## 5. Định dạng

- **Bold** cho từ khoá, deadline, tên file, tên người
- *Italic* cho thuật ngữ định nghĩa
- `code` cho lệnh, file path, ID
- Block quote (`>`) cho cảnh báo hoặc trích dẫn chính sách

## 6. Tránh

- Emoji ngoài 6 emoji chuẩn của section header (🎯⚡📋⚠️🔗📅) + 4 emoji Space (vd 🏢💰📊🔒 — tuỳ chỉnh theo Space của bạn).
- Viết tắt không có trong Glossary. Lần đầu xuất hiện phải có dạng đầy đủ.
- Câu mở đầu kiểu "Trong bối cảnh…", "Nhằm mục đích…" — vào thẳng vấn đề.
- Callout `📍 Vị trí` ở đầu trang — đã bỏ. Title đã đủ thông tin code/breadcrumb từ tree Lark.

## Cách áp dụng cho team của bạn

- Có thể giữ nguyên 3 `kind` (procedure/reference/template) — đây là phân loại universal
- Customize bộ emoji Space root + glossary path theo cấu trúc thực tế của bạn
- Quy tắc title format `<dotted-code>. <name>` không nên thay đổi — đây là contract của INDEX
