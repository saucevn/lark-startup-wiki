# Contributing to lark-startup-wiki

Thanks for your interest. This package is opinionated — the rules in `skills/` are not just style preferences, they're load-bearing for how the whole framework works. Please read the relevant skill before opening a PR that changes it.

## Ways to contribute

- **Bug reports** — open an issue with reproduction steps
- **Skill improvements** — open a discussion first; PRs that change skill rules without prior discussion may be closed
- **New scripts** — must be config-driven (no hardcoded company-specific values)
- **Translations** — EN translations of skills are welcome (file `skills/01-page-format.en.md` alongside the VI version)
- **Templates** — improvements to `templates/docs/*.md.tmpl` placeholders

## Local development

```bash
git clone https://github.com/saucevn/lark-startup-wiki
cd lark-startup-wiki

# For Python scripts
pip install -r scripts/requirements.txt

# For scaffolder
cd packages/create-lark-startup-wiki
npm install
node bin/cli.js test-output  # smoke test
```

## Style

- **Skills**: Vietnamese, imperative voice, concrete examples
- **Docs (this repo)**: English
- **Code**: Python 3.11+, type-hinted, Black-formatted
- **Commit messages**: Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`)

## Before sending a PR

1. Run `python scripts/validate_structure.py` — must pass
2. Run `markdownlint-cli2 "**/*.md"` — must pass
3. If you added a script, add a test in `scripts/tests/`
4. Update `CHANGELOG.md` under `## [Unreleased]`

## Code of Conduct

See [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md). TL;DR: be kind, be specific, no harassment.
