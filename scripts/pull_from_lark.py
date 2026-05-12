#!/usr/bin/env python3
"""Pull a snapshot of a Lark Wiki space into a local directory.

Walks the Wiki tree under a given space, downloads each page as XML/raw text,
saves a manifest of all nodes, and supports resume + dry-run.

Usage:
    python pull_from_lark.py --space-id <id>
    python pull_from_lark.py --space-id <id> --output sources/lark-exports/
    python pull_from_lark.py --dry-run
    python pull_from_lark.py --force                  # re-download even if file exists

Reads WIKI_SPACE_ID from environment if --space-id is omitted.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import unicodedata
from pathlib import Path
from typing import Any

from lark_client import LarkClient, LarkClientError

RATE_LIMIT_PER_SEC = 5
_MIN_INTERVAL = 1.0 / RATE_LIMIT_PER_SEC


def slugify(title: str) -> str:
    s = unicodedata.normalize("NFD", title)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    s = s.lower()
    s = re.sub(r"[^a-z0-9]+", "_", s).strip("_")
    return s or "untitled"


class RateLimiter:
    def __init__(self, min_interval: float = _MIN_INTERVAL) -> None:
        self.min_interval = min_interval
        self._last = 0.0

    def wait(self) -> None:
        now = time.monotonic()
        delta = now - self._last
        if delta < self.min_interval:
            time.sleep(self.min_interval - delta)
        self._last = time.monotonic()


def walk_wiki_tree(
    client: LarkClient,
    space_id: str,
    parent_token: str | None,
    path_prefix: str,
    limiter: RateLimiter,
) -> list[dict[str, Any]]:
    """Recursive depth-first walk of a Wiki space; returns a flat list of nodes with paths."""
    out: list[dict[str, Any]] = []
    limiter.wait()
    children = client.list_wiki_children(space_id, parent_token)
    for node in children:
        title = node.get("title") or "(untitled)"
        node_token = node.get("node_token") or node.get("obj_token")
        if not node_token:
            continue
        full_path = f"{path_prefix}/{title}".lstrip("/")
        record = {
            "node_token": node_token,
            "obj_token": node.get("obj_token"),
            "obj_type": node.get("obj_type"),
            "title": title,
            "path": full_path,
            "parent_node_token": parent_token,
            "has_child": bool(node.get("has_child")),
        }
        out.append(record)
        if record["has_child"]:
            out.extend(walk_wiki_tree(client, space_id, node_token, full_path, limiter))
    return out


def dump_node(
    client: LarkClient,
    node: dict[str, Any],
    output_dir: Path,
    force: bool,
    limiter: RateLimiter,
) -> str:
    """Download a node's content. Returns 'skipped', 'wrote', or 'no-content'."""
    obj_token = node.get("obj_token")
    obj_type = node.get("obj_type", "")
    target = output_dir / f"{node['node_token']}.xml"
    if target.exists() and not force:
        return "skipped"
    if not obj_token or obj_type not in ("docx", "doc"):
        return "no-content"
    limiter.wait()
    try:
        content = client.get_docx_content(obj_token)
    except LarkClientError as e:
        print(f"  WARN: failed {node['node_token']}: {e}", file=sys.stderr)
        return "no-content"
    target.write_text(content, encoding="utf-8")
    return "wrote"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--space-id", default=None, help="Wiki space ID (or set WIKI_SPACE_ID env var)")
    parser.add_argument("--output", type=Path, default=Path("sources/lark-exports"),
                        help="Output directory (default: sources/lark-exports/)")
    parser.add_argument("--dry-run", action="store_true",
                        help="List nodes without downloading content")
    parser.add_argument("--force", action="store_true",
                        help="Re-download even if local file exists")
    args = parser.parse_args()

    space_id = args.space_id or os.environ.get("WIKI_SPACE_ID")
    if not space_id:
        print("ERROR: --space-id required (or set WIKI_SPACE_ID in .env)", file=sys.stderr)
        return 1

    try:
        client = LarkClient()
    except LarkClientError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1

    output_dir: Path = args.output
    output_dir.mkdir(parents=True, exist_ok=True)
    limiter = RateLimiter()

    print(f"Walking wiki space: {space_id}")
    nodes = walk_wiki_tree(client, space_id, None, "", limiter)
    print(f"Found {len(nodes)} nodes")

    manifest = {
        "space_id": space_id,
        "node_count": len(nodes),
        "nodes": {n["node_token"]: {
            "title": n["title"],
            "path": n["path"],
            "obj_type": n["obj_type"],
            "parent": n["parent_node_token"],
        } for n in nodes},
    }

    if args.dry_run:
        for n in nodes:
            print(f"  {n['obj_type']:8} {n['node_token']}  {n['path']}")
        print(f"\nDry-run only. Would write {len(nodes)} files to {output_dir}/")
        return 0

    counts = {"wrote": 0, "skipped": 0, "no-content": 0}
    for n in nodes:
        result = dump_node(client, n, output_dir, args.force, limiter)
        counts[result] = counts.get(result, 0) + 1
        if result == "wrote":
            print(f"  wrote   {n['node_token']}  {n['path']}")

    manifest_path = output_dir / "_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nManifest: {manifest_path}")
    print(f"Wrote {counts['wrote']}, skipped {counts['skipped']}, "
          f"no-content {counts['no-content']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
