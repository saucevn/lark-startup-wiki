#!/usr/bin/env python3
"""Thin wrapper around lark-oapi for the lark-startup-wiki package.

Exposes a `LarkClient` class with the most-used Wiki/Docx/Base operations,
loads credentials from environment (.env or shell), and supports both
international (larksuite.com) and China (feishu.cn) Lark domains via the
LARK_DOMAIN env var.

CLI:
    python lark_client.py --test       # verify auth, print tenant info
    python lark_client.py --whoami     # print app info
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*_args: Any, **_kwargs: Any) -> bool:  # type: ignore[misc]
        return False

try:
    import lark_oapi as lark
    from lark_oapi.api.wiki.v2 import (
        GetSpaceNodeRequest,
        ListSpaceNodeRequest,
    )
    from lark_oapi.api.docx.v1 import GetDocumentRawContentRequest
    from lark_oapi.api.bitable.v1 import (
        ListAppTableRecordRequest,
        UpdateAppTableRecordRequest,
        AppTableRecord,
    )
    _LARK_AVAILABLE = True
except ImportError:
    _LARK_AVAILABLE = False


DOMAIN_INTL = "https://open.larksuite.com"
DOMAIN_CN = "https://open.feishu.cn"


def _find_env_file() -> Path | None:
    """Search current dir and ancestors (up to repo root) for a .env file."""
    here = Path.cwd().resolve()
    for candidate in [here, *here.parents]:
        env = candidate / ".env"
        if env.is_file():
            return env
        if (candidate / ".git").exists():
            break
    script_dir = Path(__file__).resolve().parent
    for candidate in [script_dir, *script_dir.parents]:
        env = candidate / ".env"
        if env.is_file():
            return env
    return None


def _load_env() -> None:
    env_file = _find_env_file()
    if env_file is not None:
        load_dotenv(env_file)


class LarkClientError(RuntimeError):
    """Raised on configuration or API errors."""


class LarkClient:
    """Authenticated Lark API client.

    Reads LARK_APP_ID and LARK_APP_SECRET from environment.
    Optionally reads LARK_DOMAIN ("international" or "china", default "international").
    """

    def __init__(
        self,
        app_id: str | None = None,
        app_secret: str | None = None,
        domain: str | None = None,
    ) -> None:
        _load_env()
        self.app_id = app_id or os.environ.get("LARK_APP_ID")
        self.app_secret = app_secret or os.environ.get("LARK_APP_SECRET")
        self.domain_name = (domain or os.environ.get("LARK_DOMAIN") or "international").lower()

        if not self.app_id:
            raise LarkClientError(
                "Set LARK_APP_ID in .env - see docs/env-vars.md"
            )
        if not self.app_secret:
            raise LarkClientError(
                "Set LARK_APP_SECRET in .env - see docs/env-vars.md"
            )
        if not _LARK_AVAILABLE:
            raise LarkClientError(
                "lark-oapi not installed. Run: pip install -r scripts/requirements.txt"
            )

        self.domain_url = DOMAIN_CN if self.domain_name in ("china", "cn", "feishu") else DOMAIN_INTL
        self._client = (
            lark.Client.builder()
            .app_id(self.app_id)
            .app_secret(self.app_secret)
            .domain(self.domain_url)
            .build()
        )

    @property
    def raw(self) -> Any:
        return self._client

    def get_wiki_node(self, node_id: str) -> dict[str, Any]:
        """Fetch metadata for a single Wiki node by token."""
        req = GetSpaceNodeRequest.builder().token(node_id).build()
        resp = self._client.wiki.v2.space_node.get(req)
        if not resp.success():
            raise LarkClientError(f"get_wiki_node failed: {resp.code} {resp.msg}")
        return json.loads(lark.JSON.marshal(resp.data))

    def list_wiki_children(self, space_id: str, parent_node_token: str | None = None) -> list[dict[str, Any]]:
        """List direct children of a Wiki node (or top-level if parent omitted)."""
        out: list[dict[str, Any]] = []
        page_token: str | None = None
        while True:
            builder = (
                ListSpaceNodeRequest.builder()
                .space_id(space_id)
                .page_size(50)
            )
            if parent_node_token:
                builder = builder.parent_node_token(parent_node_token)
            if page_token:
                builder = builder.page_token(page_token)
            resp = self._client.wiki.v2.space_node.list(builder.build())
            if not resp.success():
                raise LarkClientError(f"list_wiki_children failed: {resp.code} {resp.msg}")
            data = json.loads(lark.JSON.marshal(resp.data))
            out.extend(data.get("items", []))
            if not data.get("has_more"):
                break
            page_token = data.get("page_token")
            if not page_token:
                break
        return out

    def get_docx_content(self, doc_id: str) -> str:
        """Get raw text content of a Docx document."""
        req = GetDocumentRawContentRequest.builder().document_id(doc_id).build()
        resp = self._client.docx.v1.document.raw_content(req)
        if not resp.success():
            raise LarkClientError(f"get_docx_content failed: {resp.code} {resp.msg}")
        data = json.loads(lark.JSON.marshal(resp.data))
        return data.get("content", "")

    def list_base_records(self, app_token: str, table_id: str) -> list[dict[str, Any]]:
        """List all records of a Bitable table (auto-paginates)."""
        out: list[dict[str, Any]] = []
        page_token: str | None = None
        while True:
            builder = (
                ListAppTableRecordRequest.builder()
                .app_token(app_token)
                .table_id(table_id)
                .page_size(100)
            )
            if page_token:
                builder = builder.page_token(page_token)
            resp = self._client.bitable.v1.app_table_record.list(builder.build())
            if not resp.success():
                raise LarkClientError(f"list_base_records failed: {resp.code} {resp.msg}")
            data = json.loads(lark.JSON.marshal(resp.data))
            out.extend(data.get("items", []))
            if not data.get("has_more"):
                break
            page_token = data.get("page_token")
            if not page_token:
                break
        return out

    def update_base_record(
        self,
        app_token: str,
        table_id: str,
        record_id: str,
        fields: dict[str, Any],
    ) -> dict[str, Any]:
        """Update fields of a single Bitable record."""
        record = AppTableRecord.builder().fields(fields).build()
        req = (
            UpdateAppTableRecordRequest.builder()
            .app_token(app_token)
            .table_id(table_id)
            .record_id(record_id)
            .request_body(record)
            .build()
        )
        resp = self._client.bitable.v1.app_table_record.update(req)
        if not resp.success():
            raise LarkClientError(f"update_base_record failed: {resp.code} {resp.msg}")
        return json.loads(lark.JSON.marshal(resp.data))


def _cmd_test() -> int:
    try:
        client = LarkClient()
    except LarkClientError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(f"OK  app_id={client.app_id}  domain={client.domain_url}")
    return 0


def _cmd_whoami() -> int:
    try:
        client = LarkClient()
    except LarkClientError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    print(json.dumps({
        "app_id": client.app_id,
        "domain": client.domain_url,
        "domain_name": client.domain_name,
    }, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--test", action="store_true", help="Verify auth and print tenant info")
    group.add_argument("--whoami", action="store_true", help="Print app info")
    args = parser.parse_args()
    if args.test:
        return _cmd_test()
    if args.whoami:
        return _cmd_whoami()
    return 2


if __name__ == "__main__":
    sys.exit(main())
