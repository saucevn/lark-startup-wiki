---
name: lark-wiki-from-excel
description: Use when converting an Excel source file (HR JD, KPI, payroll, contracts, SOPs) into one or more Wiki pages. Defines the summarize-don't-copy rule, mapping table per Excel category, and verification steps. Trigger when the user has Excel files in sources/excel/ and wants Wiki coverage.
---

# Skill 06 — Chuyển nội dung từ Excel sang Wiki

Nhiều startup có nội dung gốc (JD, KPI, O3K, quy trình lương, hợp đồng…) nằm rải rác trong file Excel. Khi viết trang Wiki tương ứng, **không copy nguyên file** — tóm tắt + link.

Đặt file Excel nguồn ở `sources/excel/` trong repo (hoặc folder khác — quy ước trong [skill 07](07-source-protection.md)).

## Quy tắc

1. **Không copy nguyên bảng Excel vào Wiki.** Wiki tối đa 2 trang A4.
2. **Tóm tắt nội dung quan trọng** thành step-by-step theo [skill 01](01-page-format.md).
3. **Đính kèm link file Excel** trong section `🔗 Tài liệu liên quan`:
   ```
   → 📥 [QuyTrinhLuong_2026.xlsx](sources/excel/QuyTrinhLuong_2026.xlsx) — file chi tiết 18 bước
   ```
4. **Link đến Lark Base** (nếu có tracking dữ liệu real-time).

## Quy trình

### Bước 1 — Đọc file Excel

```bash
python3 -c "
import openpyxl
wb = openpyxl.load_workbook('sources/excel/QuyTrinhLuong_2026.xlsx', data_only=True)
for sheet in wb.sheetnames:
    print(f'=== {sheet} ===')
    ws = wb[sheet]
    for row in ws.iter_rows(max_row=10, values_only=True):
        print(row)
"
```

### Bước 2 — Identify nội dung cần đưa lên Wiki

Phân loại:

- **A. Quy trình step-by-step** → đưa vào "📋 Chi tiết từng bước" của trang Wiki (`kind: procedure`)
- **B. Bảng tham chiếu (mapping, list)** → đưa vào trang Wiki nếu < 20 dòng (`kind: reference`). > 20 dòng → đẩy lên Lark Base + link
- **C. Số liệu mẫu, ví dụ** → đưa vào ⚠️ Lưu ý quan trọng
- **D. Form / Template Excel** → KHÔNG đưa lên Wiki. Để ở `sources/excel/` + link.

### Bước 3 — Xác định code X.Y.Z trên INDEX

Mở Lark INDEX → tra Section đích → lấy code kế tiếp ([skill 05 Step 0](05-publish-workflow.md), [skill 08](08-index-and-numbering.md)).

### Bước 4 — Viết draft theo format chuẩn

Tạo draft tại `drafts/<page-name>.md`. Title H1 có dotted prefix (xem [skill 01](01-page-format.md)):

```markdown
# 6.1.1. Khi xuất hoá đơn — làm thế nào?

## 🎯 Dành cho ai
KT Tổng hợp (KTTH) phụ trách xuất HĐ hàng ngày.

## ⚡ Tóm tắt nhanh
3 cụm việc: (1) nhận file đơn từ sàn, (2) mapping theo file `QuyTrinh_HoaDon.xlsx` cột E, (3) xuất MISA + đối soát cuối ngày.

## 📋 Chi tiết từng bước

**Bước 1: Nhận file đơn từng sàn (08:00-09:00)**
- TikTok Shop, Shopee, Facebook, Website — mỗi sàn 1 file CSV
- Lưu vào folder `MISA/đơn-ngày-DD-MM`
- ...

## 🔗 Tài liệu liên quan

→ ↑ [INDEX — Wiki của bạn](https://<your-lark-tenant>.larksuite.com/wiki/<WIKI_INDEX_NODE_ID>) — canonical
→ 📥 [QuyTrinh_HoaDon_2026.xlsx](sources/excel/QuyTrinh_HoaDon_2026.xlsx) — chi tiết mapping
→ 📊 [Lark Base — Tracking hóa đơn ngày](https://...) — track real-time
```

### Bước 5 — Publish theo [skill 05](05-publish-workflow.md)

## Mapping Excel ↔ trang Wiki (mẫu cho 1 startup HR-heavy)

Đây là **cấu trúc mẫu** — 8 nhóm Excel phổ biến tại startup. Adapt theo phòng ban thực tế của bạn:

| Loại Excel | Đích Wiki (code mẫu) |
|---|---|
| Hệ thống HCNS + O3K (org chart, JD, KPI) | `II> 1.1.2` JD từng vị trí · `II> 3.2.x` O3K HCNS · `II> 1.x` Checklist HCNS |
| Hệ thống Kế toán Trưởng | `II> 2.1` JD KTT · `II> 3.3.x` O3K Kế toán · `II> 3.4.2` KPI KTT |
| File phòng Kế toán (team) | `II> 3.3.x` O3K Team KT · `II> 3.4.3` KPI KTTH · `II> 3.4.4` KPI KT Kho |
| Ma trận phối hợp HCNS ↔ KT | `II> 2.2.3` Ma trận phối hợp |
| Quy trình lương | `II> 2.2` subsection Quy trình lương 18 bước |
| Quy trình hoá đơn | `III> 6.1` subsection xuất HĐ hàng ngày |
| File năm cũ (lưu trữ) | (Chỉ dùng tham chiếu lịch sử, không đẩy lên Wiki) |

## 🔗 Liên quan

→ ↑ [INDEX — Wiki của bạn](https://<your-lark-tenant>.larksuite.com/wiki/<WIKI_INDEX_NODE_ID>) — canonical
→ [Skill 01 — Page Format](01-page-format.md) — format chuẩn 6 section + title `<prefix>. <name>`
→ [Skill 05 — Publish Workflow](05-publish-workflow.md) — đẩy draft lên Lark (có Step 0 resolve code)
→ [Skill 08 — INDEX & Numbering](08-index-and-numbering.md) — quy tắc đánh số

## Cách áp dụng cho team của bạn

- Đổi mapping table ở §"Mapping Excel ↔ trang Wiki" theo phòng ban thực tế (HR/Finance/Ops…)
- 4 phân loại A/B/C/D (procedure / reference / data sample / template form) là universal
- Quy tắc "không copy nguyên bảng Excel vào Wiki, > 20 dòng đẩy lên Lark Base" giữ nguyên
