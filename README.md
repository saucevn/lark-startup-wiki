# lark-startup-wiki

> 🇻🇳 **Skills + công cụ** giúp startup Việt biến **Lark Wiki** thành "Operating System" của công ty — có quy tắc, có index, có review, không thành mớ hỗn độn sau 3 tháng.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-9-blue)](./skills)
[![Plugin](https://img.shields.io/badge/Claude%20Code-Plugin-purple)](.claude-plugin/plugin.json)
[![Made for Lark](https://img.shields.io/badge/made%20for-Lark%2FFeishu-00B96B)](https://www.larksuite.com)

---

## 🎯 Cho ai

Bạn là **founder / COO / HR Lead / Trợ lý CEO** của một startup Việt **đang dùng Lark** (hoặc đang tính dùng), và bạn nhận ra:

- ❌ Wiki Lark sau 3-6 tháng trở thành **đầm lầy** — trang nằm khắp nơi, không ai biết trang nào mới nhất
- ❌ Người mới vào không biết **đọc trang nào trước**, đọc xong cũng không biết tin được không
- ❌ Mỗi người viết một kiểu — **không có quy tắc** về tiêu đề, status, link
- ❌ Muốn dùng AI (Claude, Cursor, Gemini) để soạn Wiki nhưng **không biết "huấn luyện" nó như thế nào**
- ❌ Đã tốn tiền thuê HR/COO viết SOP nhưng **3 tháng sau không ai mở lại**

`lark-startup-wiki` cho bạn **9 quy tắc soạn thảo + công cụ + template** để giải quyết tận gốc.

---

## ⚡ Dùng thử trong 30 giây

```bash
npx create-lark-startup-wiki wiki-cua-team
cd wiki-cua-team
cat CLAUDE.md     # Xem ruleset cho AI agent (Claude/Cursor/Gemini đều đọc được)
ls docs/          # 9 file template đã điền sẵn, bạn chỉ cần customize
```

> ⚠️ **Hiện tại:** `npx create-lark-startup-wiki` **đang chờ publish lên npm** (cần chủ tài khoản nhập 2FA). Trong lúc chờ, dùng cách 2 hoặc 3 dưới đây.

---

## 📦 Có gì trong package

### 1. **9 Skills (quy tắc soạn thảo, viết bằng tiếng Việt)**

Đây là phần "linh hồn" — quy tắc opinionated cho **mọi trang Wiki** của bạn:

| # | Skill | Để làm gì |
|---|---|---|
| 01 | Page format | Format chuẩn 7 mục (TL;DR → Mục đích → Nội dung → Liên quan → Trạng thái → Lịch sử → Owner) cho mỗi trang |
| 02 | Writing style | Quy tắc tiêu đề theo `kind`, dùng từ ngữ, độ dài câu/đoạn |
| 03 | Linking rules | 4 loại link bắt buộc: trang ↔ trang, Wiki ↔ Base, mention người, link ngoài |
| 04 | Page status | 5 trạng thái với emoji (⬜ 🔄 📋 ✅ 🗄️) + rule chuyển đổi |
| 05 | Publish workflow | Workflow publish manual qua `lark-cli` — chống publish nhầm trang live |
| 06 | Excel → Wiki | Chuyển file Excel HR/Lương/JD/SOP thành trang Wiki — tóm tắt, không copy nguyên |
| 07 | Source protection | Bảo vệ source code, enforce clean-slate trước mỗi phiên soạn thảo |
| 08 | Index & numbering | Hệ đánh số `I> 1.2.3` (Roman.thập phân) + INDEX page là canonical TOC |
| 09 | Contributing flow | Workflow 3 bước cho người không biết Git đóng góp Wiki qua group Lark + bot review |

### 2. **Templates** (scaffolder render ra repo cho bạn)

- `CLAUDE.md` — ruleset cho AI agent đọc trước khi làm việc
- 9 file docs (`docs/00-09`) — context công ty bạn (org chart, glossary, permissions, ...) đã điền sẵn placeholder
- `.env.example` — schema env var cho Lark App
- `.gitignore`, `.markdownlint.json`, GitHub Actions validate

### 3. **5 Python scripts**

- `lark_client.py` — wrapper quanh `lark-oapi`, đọc env vars
- `pull_from_lark.py` — pull toàn bộ Wiki tree về máy dạng XML (backup/diff)
- `sync_index_base.py` — sync trạng thái trang giữa Wiki ↔ Lark Base INDEX
- `validate_structure.py` — lint cấu trúc folder, chạy trong CI
- `generate_index.py` — auto-generate `README.md` từ H1 các file

### 4. **npm Scaffolder**

`npx create-lark-startup-wiki <tên-team>` — hỏi bạn 5-7 câu (tên công ty, URL Wiki, ...) rồi render ra repo hoàn chỉnh.

---

## 🚀 3 cách cài (chọn 1)

| Cách | Phù hợp với | Lệnh |
|---|---|---|
| **1. Plugin Claude Code** | Bạn đang dùng [Claude Code](https://claude.com/claude-code) để làm việc | `/plugin marketplace add saucevn/lark-startup-wiki` |
| **2. Scaffolder npm** ⏳ | Team mới setup từ zero, muốn 1 lệnh xong | `npx create-lark-startup-wiki ten-team` *(đang chờ publish)* |
| **3. Git clone** | Dùng Cursor/Codex/Gemini hoặc xem trước rồi quyết | `git clone https://github.com/saucevn/lark-startup-wiki` |

### Chi tiết cách 1 — Claude Code Plugin

```
/plugin marketplace add saucevn/lark-startup-wiki
/plugin install lark-startup-wiki@saucevn
```

Khởi động lại Claude Code. Skills sẽ tự xuất hiện. Lúc soạn Wiki, Claude sẽ tự gợi ý áp dụng skill phù hợp — ví dụ bạn nói *"viết trang onboarding cho nhân viên mới"*, Claude sẽ tự gọi skill `lark-wiki-page-format` + `lark-wiki-writing-style` + `lark-wiki-numbering`.

### Chi tiết cách 2 — npm Scaffolder

```bash
npx create-lark-startup-wiki wiki-cua-team
```

Sẽ hỏi bạn:
- Tên công ty?
- Tagline (1 câu)?
- Tên CEO/Founder?
- URL Lark Wiki Space?
- Có Lark Base làm INDEX không?
- Có nhiều brand không?
- Init git?

Sau đó render ra repo có sẵn `CLAUDE.md`, `docs/`, `.env.example`, GitHub Actions.

### Chi tiết cách 3 — Git clone

```bash
git clone https://github.com/saucevn/lark-startup-wiki
cd lark-startup-wiki

# Copy skills cho Claude Code
cp -r skills/ ~/.claude/skills/lark-startup-wiki/

# Hoặc copy vào dự án Cursor
cp -r skills/ /path/to/your/project/.cursor/rules/
```

---

## 📚 Sau khi cài, đọc gì tiếp

1. **[`docs/lark-api-setup.md`](docs/lark-api-setup.md)** — tạo Lark App, lấy App ID + Secret (9 bước có hình)
2. **[`docs/env-vars.md`](docs/env-vars.md)** — điền `.env` với credential và Wiki space ID
3. **[`skills/05-publish-workflow.md`](skills/05-publish-workflow.md)** — hiểu quy tắc publish manual (đừng publish nhầm!)
4. Test auth: `python scripts/lark_client.py --test`

---

## 💡 Tại sao package này tồn tại

Hầu hết startup Việt chọn Lark vì free + all-in-one (Wiki + Base + IM + Calendar + Doc). Nhưng **Lark Wiki tự nó không có ý kiến** — bạn được tự do viết kiểu gì cũng được. Sau 3-6 tháng, kết quả thường là:

```
Wiki Space (sau 6 tháng)
├── Quy trình tuyển dụng (cập nhật 3 tháng trước)
├── QUY TRÌNH TUYỂN DỤNG MỚI (cập nhật 1 tháng trước)
├── [V2] Tuyển dụng - Bảo viết
├── tuyen-dung-final-final.md (đã xóa nhưng vẫn có người gửi link)
├── ... (thêm 47 trang khác, không ai biết trang nào active)
```

Package này **áp đặt 5 quy tắc** giải quyết:

1. ✅ **INDEX page là canonical** — 1 trang Lark Base liệt kê mọi trang, status, owner. Trang nào không có trong INDEX = không tồn tại.
2. ✅ **7 mục bắt buộc/trang** — TL;DR, mục đích, nội dung, liên quan, trạng thái, lịch sử, owner. Reader biết đọc gì trước, AI biết viết gì ở đâu.
3. ✅ **Hệ đánh số `I> 1.2.3`** — La Mã cho Space (I=Chung, II=Nhân sự, III=Vận hành, IV=Sản phẩm), thập phân cho cấp con. Renumbering đơn giản khi reorganize.
4. ✅ **Publish workflow tách bạch draft/live** — soạn ngoài repo, review, mới publish qua `lark-cli`. Drafts không bao giờ leak vào tree live.
5. ✅ **AI agent đọc rules trước khi viết** — file `CLAUDE.md` (cũng làm work cho Cursor/Gemini/Codex) gắn sẵn rules vào mọi session AI.

---

## ❓ Câu hỏi thường gặp

<details>
<summary><b>Tôi chưa dùng Claude Code, có cài được không?</b></summary>

Có. Cách 2 (npm scaffolder) và cách 3 (git clone) không cần Claude Code. Skills là file markdown — Cursor, Gemini CLI, Codex, hoặc thậm chí ChatGPT cũng đọc được.
</details>

<details>
<summary><b>Có cần biết Git không?</b></summary>

Cho contributor nội bộ (HR, vận hành) — **không cần**. Workflow contributing có quy trình 3 bước qua group Lark + bot review (xem skill 09).

Cho người setup ban đầu — biết Git cơ bản (clone, commit, push) là đủ.
</details>

<details>
<summary><b>Skills này áp dụng được cho công ty không-startup không?</b></summary>

Được. Mọi tổ chức dùng Lark Wiki để document quy trình đều dùng được. Nhưng package này được tune cho:
- Team 5-50 người (size startup giai đoạn seed → series A)
- Có 4 mảng chính (Chung / Nhân sự / Vận hành / Sản phẩm)
- Dùng tiếng Việt là ngôn ngữ chính

Team lớn hơn (>200 người) hoặc đa quốc gia có thể cần customize sâu hơn.
</details>

<details>
<summary><b>Có cần trả phí Lark gì không?</b></summary>

Không. Toàn bộ tính năng dùng Lark **gói Free** đều hoạt động. Bạn chỉ cần tạo 1 Lark App custom (free, không cần plan trả phí).
</details>

<details>
<summary><b>Bot AI Reviewer (v2.0) tốn tiền không?</b></summary>

Bot v2.0 dùng API Claude — bạn tự pay cho Anthropic API key của bạn. Estimate: ~$5-15/tháng cho team 10 người, tuỳ tần suất sửa Wiki.

v1.0 (hiện tại) **không cần API key**, không tốn gì.
</details>

<details>
<summary><b>Tôi đã có repo private quản lý Wiki, migrate được không?</b></summary>

Được. Xem **[`docs/migration-from-private.md`](docs/migration-from-private.md)** — hướng dẫn từng bước backup, cài plugin, xóa skills cũ, update CLAUDE.md.
</details>

<details>
<summary><b>Lark vs Feishu — package này dùng được cả 2 không?</b></summary>

Có. Set env var `LARK_DOMAIN=larksuite.com` (mặc định, quốc tế) hoặc `LARK_DOMAIN=feishu.cn` (Trung Quốc). Tất cả script tự switch endpoint.
</details>

<details>
<summary><b>Tôi muốn customize skill, có được không?</b></summary>

Được. Xem **[`docs/customization.md`](docs/customization.md)** — copy skill về `skills-overrides/` của bạn, Claude Code ưu tiên local override hơn plugin version.
</details>

---

## 🗺️ Roadmap

- ✅ **v1.0** (đã release) — Skills + scaffolder + sync scripts
- 🚧 **v2.0** (3-6 tháng tới) — **AI Wiki Reviewer Bot**: webhook khi có ai sửa Wiki → Claude review tự động → comment ngược lại trên trang Lark
- 🔮 **v3.0** — Skills tiếng Anh, hosted SaaS reviewer (không cần self-host), VS Code extension

---

## 🤝 Đóng góp

PR welcome. Đọc [`CONTRIBUTING.md`](CONTRIBUTING.md) trước.

Nếu bạn có **case study** dùng package này thực tế cho team Việt — mở PR vào `examples/` hoặc reach out để mình feature.

---

## 🇬🇧 English summary

`lark-startup-wiki` is an opinionated framework that turns a Lark/Feishu Wiki into a versionable, AI-assisted source of truth for Vietnamese-speaking startups. Ships as: (a) Claude Code plugin, (b) npm scaffolder `create-lark-startup-wiki`, (c) standalone clone. Skills are written in Vietnamese; package documentation is bilingual (this README) and English (`docs/`).

**Quick start (English speakers):** [`docs/installation.md`](docs/installation.md)

---

## 📄 License

[MIT](LICENSE) © 2026 [saucevn](https://github.com/saucevn) · Built for Lark / Feishu Wiki · Optimized for Vietnamese startups
