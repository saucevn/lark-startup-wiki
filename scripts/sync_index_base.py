#!/usr/bin/env python3
"""Sync data from a Wiki tree into a Lark Base index table, driven by a YAML config.

The YAML config defines:
  - Which Lark Base (app_token + table_id)
  - Which fields to populate from which sources
  - Which mapping rule to apply

Usage:
    python sync_index_base.py --config lark-sync.yml
    python sync_index_base.py --config lark-sync.yml --dry-run

Example config (also written to lark-sync.yml.example):

    base:
      app_token: "${LARK_BASE_APP_TOKEN}"
      table_id:  "${LARK_INDEX_TABLE_ID}"

    mappings:
      - source: wiki_tree
        target_field: "Page Path"
        rule: "node_path_from_root"
      - source: wiki_status
        target_field: "Status"
        rule: "extract_status_from_page_content"

Mapping rules supported:
  - node_path_from_root          : write the wiki node's path string
  - extract_status_from_page_content : pull a status emoji from page body
  - copy_field:<src>             : copy from another Base field

Exit codes: 0 success, 1 user/config error, 2 system error.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("ERROR: PyYAML not installed. Run: pip install -r scripts/requirements.txt",
          file=sys.stderr)
    sys.exit(2)

from lark_client import LarkClient, LarkClientError

ENV_RE = re.compile(r"\$\{([A-Z_][A-Z0-9_]*)\}")
STATUS_RE = re.compile(r"(✅|🚧|📝|❌|⏸️|🔄)")


def expand_env(value: Any) -> Any:
    if isinstance(value, str):
        def repl(m: re.Match[str]) -> str:
            return os.environ.get(m.group(1), m.group(0))
        return ENV_RE.sub(repl, value)
    if isinstance(value, dict):
        return {k: expand_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [expand_env(v) for v in value]
    return value


def load_config(path: Path) -> dict[str, Any]:
    if not path.is_file():
        print(f"ERROR: config not found: {path}", file=sys.stderr)
        sys.exit(1)
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        print(f"ERROR: config must be a YAML mapping: {path}", file=sys.stderr)
        sys.exit(1)
    return expand_env(raw)


def apply_rule(rule: str, record: dict[str, Any], client: LarkClient) -> Any:
    if rule == "node_path_from_root":
        return record.get("path") or record.get("fields", {}).get("path")
    if rule == "extract_status_from_page_content":
        obj_token = record.get("obj_token") or record.get("fields", {}).get("obj_token")
        if not obj_token:
            return None
        try:
            content = client.get_docx_content(obj_token)
        except LarkClientError:
            return None
        m = STATUS_RE.search(content or "")
        return m.group(1) if m else None
    if rule.startswith("copy_field:"):
        src = rule.split(":", 1)[1]
        return record.get("fields", {}).get(src)
    raise ValueError(f"Unknown rule: {rule}")


def diff_fields(current: dict[str, Any], updates: dict[str, Any]) -> dict[str, Any]:
    return {k: v for k, v in updates.items() if v is not None and current.get(k) != v}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--config", required=True, type=Path, help="YAML config file")
    parser.add_argument("--dry-run", action="store_true",
                        help="Print proposed changes without writing")
    args = parser.parse_args()

    cfg = load_config(args.config)
    base = cfg.get("base") or {}
    app_token = base.get("app_token")
    table_id = base.get("table_id")
    mappings = cfg.get("mappings") or []
    if not app_token or not table_id:
        print("ERROR: config.base.app_token and config.base.table_id are required",
              file=sys.stderr)
        return 1
    if not mappings:
        print("ERROR: config.mappings is empty", file=sys.stderr)
        return 1

    try:
        client = LarkClient()
    except LarkClientError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    print(f"Listing records from base={app_token} table={table_id}...")
    records = client.list_base_records(app_token, table_id)
    print(f"Found {len(records)} records")

    total_changes = 0
    for record in records:
        record_id = record.get("record_id")
        if not record_id:
            continue
        current_fields = record.get("fields", {}) or {}
        proposed: dict[str, Any] = {}
        for m in mappings:
            target = m.get("target_field")
            rule = m.get("rule")
            if not target or not rule:
                continue
            try:
                proposed[target] = apply_rule(rule, record, client)
            except ValueError as e:
                print(f"  WARN: {e}", file=sys.stderr)

        changes = diff_fields(current_fields, proposed)
        if not changes:
            continue
        total_changes += 1
        print(f"  {record_id}: {changes}")
        if not args.dry_run:
            try:
                client.update_base_record(app_token, table_id, record_id, changes)
            except LarkClientError as e:
                print(f"    ERROR updating: {e}", file=sys.stderr)

    print(f"\n{'Would change' if args.dry_run else 'Changed'} {total_changes} records.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
