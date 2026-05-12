"""Unit tests for lark_client that run without real credentials."""
from __future__ import annotations

import os
import sys
import unittest
from pathlib import Path
from unittest import mock

SCRIPTS_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(SCRIPTS_DIR))

import lark_client  # noqa: E402


class TestLarkClientErrors(unittest.TestCase):
    def test_missing_app_id_raises_helpful_error(self) -> None:
        env = {k: v for k, v in os.environ.items()
               if k not in ("LARK_APP_ID", "LARK_APP_SECRET")}
        with mock.patch.dict(os.environ, env, clear=True), \
             mock.patch.object(lark_client, "_load_env", lambda: None):
            with self.assertRaises(lark_client.LarkClientError) as ctx:
                lark_client.LarkClient()
            self.assertIn("LARK_APP_ID", str(ctx.exception))
            self.assertIn(".env", str(ctx.exception))

    def test_missing_app_secret_raises_helpful_error(self) -> None:
        env = {k: v for k, v in os.environ.items() if k != "LARK_APP_SECRET"}
        env["LARK_APP_ID"] = "test_app_id"
        env.pop("LARK_APP_SECRET", None)
        with mock.patch.dict(os.environ, env, clear=True), \
             mock.patch.object(lark_client, "_load_env", lambda: None):
            with self.assertRaises(lark_client.LarkClientError) as ctx:
                lark_client.LarkClient()
            self.assertIn("LARK_APP_SECRET", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
