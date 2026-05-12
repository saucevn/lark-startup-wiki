# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.0] — 2026-05-XX

### Added
- 9 authoring skills (Vietnamese) for Lark Wiki page format, writing style, linking, status, publish workflow, Excel→Wiki conversion, source protection, indexing & numbering, contributor workflow
- Generic scripts: `generate_index.py`, `validate_structure.py`
- Lark API client: `lark_client.py` shared wrapper
- `pull_from_lark.py` — fetch Wiki tree as XML snapshots
- `sync_index_base.py` — config-driven Lark Base sync
- Claude Code plugin manifest + marketplace entry
- npm scaffolder `create-lark-startup-wiki` (interactive prompts → renders templates)
- 9 docs templates with placeholders (company overview, org structure, Wiki architecture, permissions, glossary, Lark Base connections, context notes, status tracker, contributing)
- English README + setup docs (installation, env vars, Lark API setup, customization, migration)
- MIT License
