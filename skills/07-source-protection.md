---
name: lark-wiki-source-protection
description: Use BEFORE any commit, publish, or destructive file action. Protects sources/, scripts/, .github/workflows/, and other source-of-truth files from accidental modification. Enforces the clean-slate-before-authoring discipline (git status clean, git pull, no draft commits).
---

# Skill 07 — Bảo vệ source code & Clean-slate trước soạn thảo

Đây là **nguyên tắc tối thượng** — mọi AI agent và người dùng phải tuân thủ.

## A. Pre-flight checklist (mỗi phiên soạn thảo)

Trước khi bắt đầu **bất kỳ** phiên soạn thảo Wiki:

```
1. git status              → working tree phải SẠCH
2. git pull                → đồng bộ rules mới nhất
3. Đọc CLAUDE.md           → nắm 2 nguyên tắc + index
4. Đọc skill liên quan     → theo loại task
5. Xác định đích Lark      → Space → Section → Page (theo wiki architecture của bạn)
6. Confirm: draft viết ở   → drafts/ (gitignored) HOẶC /tmp/
                             KHÔNG commit draft vào repo
```

**Nếu working tree không sạch** → `git stash` hoặc commit trước, KHÔNG bắt đầu phiên mới.

## B. Files PROTECTED — không sửa/xóa

| Path | Lý do | Khi nào được sửa |
|---|---|---|
| `sources/lark-exports/*.xml` | Snapshot Lark, sinh từ script | Chạy `scripts/pull_from_lark.py` |
| `sources/excel/*.xlsx` | File nguồn từ owner / trưởng phòng | Khi có version mới, ghi đè rõ ràng |
| `sources/schemas/*.json` | Schema sinh tự động | Pull mới qua script |
| `sources/schemas/*.svg` | Sinh từ schema | Re-generate |
| `.github/workflows/*.yml` | CI rule | Qua PR có review |
| `scripts/*.py` | Tooling | Qua PR có review |
| `CLAUDE.md` | Quy tắc gốc | Qua PR có review (ảnh hưởng mọi agent) |
| `AGENTS.md` | Symlink → CLAUDE.md | Không sửa trực tiếp |

## C. Quy tắc khi gọi `lark-cli`

```
✅ ĐƯỢC:
- Publish file .md đã review từ drafts/
- Publish content trực tiếp qua --content "..."
- Đọc/fetch nội dung từ Lark về local

❌ KHÔNG:
- lark-cli ... publish sources/schemas/lark_wiki_schema.json
- lark-cli ... publish wiki_navigator.py
- lark-cli ... publish *.xml
- Auto-publish trong CI (workflow YAML)
```

## D. Quy tắc khi tổ chức folder

```
Root chỉ chứa:
✅ README.md, CLAUDE.md, AGENTS.md (symlink)
✅ .gitignore, .gitattributes

KHÔNG được ở root:
❌ *.xlsx → phải ở sources/excel/
❌ *_content.xml → phải ở sources/lark-exports/
❌ schema.json → phải ở sources/schemas/
❌ *.py → phải ở scripts/
❌ Draft *.md → phải ở drafts/ (gitignored)
```

CI có thể tự động kiểm tra qua `.github/workflows/structure-validate.yml`.

## E. .gitignore (đã setup)

Xem `.gitignore` ở root. Quan trọng:
- `drafts/` — folder cho draft local, KHÔNG commit
- `.claude/settings.local.json` — có thể chứa token, không commit
- `*.draft.md`, `*.tmp`, `*.bak` — file tạm

## F. Khi nào được tạo file mới ở root

- Khi tạo skill/docs/source/script mới — nhưng phải đặt ĐÚNG folder
- Khi tạo `LICENSE`, `CONTRIBUTING.md`, `CHANGELOG.md` — cần owner repo approve

## G. Khi nào được xóa file

- Xóa nội dung trong `drafts/` — luôn được
- Xóa file `*.tmp`, `*.bak` — luôn được
- Xóa file trong `sources/`, `scripts/`, `skills/`, `docs/` — **CẤM** trừ khi có lệnh rõ ràng từ owner repo
- Xóa file `.github/workflows/*` — **CẤM** trừ qua PR có review

## H. Verify checklist sau mỗi commit

```bash
# 1. Root chỉ có file whitelist
ls /
# Phải thấy: README.md, CLAUDE.md, AGENTS.md, .gitignore, .gitattributes, .git, + folders

# 2. Không có draft trong skills/, docs/, sources/
find skills docs sources -name "*.draft.md" -o -name "*.tmp" -o -name "*.bak"
# Phải rỗng

# 3. Validate cấu trúc
python3 scripts/validate_structure.py
# Exit 0

# 4. Markdown lint
npx markdownlint-cli2 "skills/**/*.md" "docs/**/*.md" "*.md"
# Exit 0
```

## I. Khi cần phá quy tắc

Nếu **buộc phải** vi phạm 1 trong các quy tắc trên (ví dụ: thay file Excel với cùng tên), agent phải:

1. Hỏi owner repo xác nhận
2. Ghi rõ lý do trong commit message với prefix `BREAK-RULE:`
3. Update status tracker ghi nhận sự kiện

---

*Nguyên tắc này quan trọng hơn mọi nguyên tắc khác. Khi conflict, lấy file này làm chuẩn.*

## Cách áp dụng cho team của bạn

- Cấu trúc folder (`sources/`, `scripts/`, `skills/`, `docs/`, `drafts/`) là khung khuyến nghị — có thể giữ nguyên
- Customize danh sách file PROTECTED ở §B theo workflow thực tế của bạn
- Quy tắc clean-slate (git status sạch trước khi soạn) là universal best practice
