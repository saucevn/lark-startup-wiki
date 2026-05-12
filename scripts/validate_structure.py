#!/usr/bin/env python3
"""Validate folder structure for a lark-startup-wiki repo.

Default: all checks enabled. Use --no-* flags to disable individual checks.

Checks (toggleable):
  --check-sources / --no-check-sources    Excel/XML/Python files live in correct dirs.
  --check-drafts  / --no-check-drafts     drafts/ is gitignored, no draft files committed.
  --check-secrets / --no-check-secrets    No .env or *.key files committed.
  --check-naming  / --no-check-naming     skills/ and docs/ files follow NN-kebab-case.md.
  --check-root    / --no-check-root       Root directory only contains whitelisted entries.

Exit codes: 0 = pass, 1 = violations found, 2 = system error.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT_WHITELIST = {
    "README.md", "CLAUDE.md", "AGENTS.md", "LICENSE",
    "CHANGELOG.md", "CONTRIBUTING.md", "CODE_OF_CONDUCT.md",
    ".gitignore", ".gitattributes", ".markdownlint.json", ".env.example",
    ".git", ".github", ".claude", ".claude-plugin",
    "skills", "docs", "sources", "scripts", "setup", "drafts",
    "templates", "examples", "packages", "tests",
}
ALLOWED_FOLDERS_AT_ROOT = {
    "skills", "docs", "sources", "scripts", "setup", ".github", ".claude",
    ".claude-plugin", ".git", "drafts", "templates", "examples", "packages", "tests",
}

NN_KEBAB_RE = re.compile(r"^\d{2}-[a-z0-9-]+\.md$")
README_RE = re.compile(r"^README\.md$")
SECRET_NAMES = {".env", "credentials.json", "service-account.json"}
SECRET_SUFFIXES = {".key", ".pem"}


def is_git_ignored(repo_root: Path, path: Path) -> bool:
    try:
        subprocess.run(
            ["git", "check-ignore", "-q", "--", str(path)],
            cwd=repo_root, check=True, capture_output=True,
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def check_root(repo_root: Path) -> list[str]:
    violations: list[str] = []
    for entry in repo_root.iterdir():
        name = entry.name
        if name in ROOT_WHITELIST:
            continue
        if entry.is_dir() and name in ALLOWED_FOLDERS_AT_ROOT:
            continue
        if is_git_ignored(repo_root, entry):
            continue
        violations.append(
            f"  Root: '{name}' not whitelisted. Move it under sources/ or scripts/, "
            f"or add to .gitignore."
        )
    return violations


def check_naming(repo_root: Path) -> list[str]:
    violations: list[str] = []
    for folder in ("skills", "docs"):
        folder_path = repo_root / folder
        if not folder_path.is_dir():
            continue
        for f in folder_path.iterdir():
            if f.is_dir() or not f.name.endswith(".md"):
                continue
            if README_RE.match(f.name):
                continue
            if not NN_KEBAB_RE.match(f.name):
                violations.append(
                    f"  {folder}/{f.name}: must follow NN-kebab-case.md "
                    f"(e.g. 01-page-format.md)"
                )
    return violations


def check_sources(repo_root: Path) -> list[str]:
    violations: list[str] = []
    for path in repo_root.rglob("*"):
        if any(p in (".git", "node_modules", ".venv", "venv") for p in path.parts):
            continue
        if not path.is_file():
            continue
        rel = path.relative_to(repo_root)
        parts = rel.parts
        name = rel.name

        if name.endswith(".xlsx"):
            if not (len(parts) >= 2 and parts[0] == "sources" and parts[1] == "excel"):
                violations.append(f"  {rel}: .xlsx must live under sources/excel/")
        elif name.endswith("_content.xml") or name == "templates_index.xml":
            if not (len(parts) >= 2 and parts[0] == "sources" and parts[1] == "lark-exports"):
                violations.append(f"  {rel}: Lark XML must live under sources/lark-exports/")
        elif name.endswith(".py"):
            if not (parts and parts[0] in ("scripts", "tests")):
                violations.append(f"  {rel}: Python files must live under scripts/ or tests/")
    return violations


def check_drafts(repo_root: Path) -> list[str]:
    violations: list[str] = []
    drafts_dir = repo_root / "drafts"
    if not drafts_dir.exists():
        return violations
    if not is_git_ignored(repo_root, drafts_dir):
        violations.append(
            "  drafts/ exists but is NOT gitignored. Add 'drafts/' to .gitignore."
        )
    return violations


def check_secrets(repo_root: Path) -> list[str]:
    violations: list[str] = []
    for path in repo_root.rglob("*"):
        if any(p in (".git", "node_modules", ".venv", "venv") for p in path.parts):
            continue
        if not path.is_file():
            continue
        if is_git_ignored(repo_root, path):
            continue
        rel = path.relative_to(repo_root)
        if rel.name in SECRET_NAMES or path.suffix in SECRET_SUFFIXES:
            violations.append(
                f"  {rel}: looks like a secret. Add to .gitignore and remove from history."
            )
    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--repo-root", type=Path, default=None,
                        help="Repo root (default: parent of this script)")
    for flag in ("root", "naming", "sources", "drafts", "secrets"):
        parser.add_argument(f"--check-{flag}", dest=f"check_{flag}",
                            action="store_true", default=True)
        parser.add_argument(f"--no-check-{flag}", dest=f"check_{flag}",
                            action="store_false")
    args = parser.parse_args()

    repo_root = args.repo_root or Path(__file__).resolve().parent.parent
    if not repo_root.is_dir():
        print(f"ERROR: repo root not found: {repo_root}", file=sys.stderr)
        return 2

    print(f"Validating: {repo_root}")
    print()

    suite: list[tuple[str, list[str]]] = []
    if args.check_root:
        suite.append(("Root whitelist", check_root(repo_root)))
    if args.check_naming:
        suite.append(("skills/docs naming", check_naming(repo_root)))
    if args.check_sources:
        suite.append(("Source file locations", check_sources(repo_root)))
    if args.check_drafts:
        suite.append(("Drafts gitignored", check_drafts(repo_root)))
    if args.check_secrets:
        suite.append(("No committed secrets", check_secrets(repo_root)))

    failed = False
    for label, violations in suite:
        if violations:
            failed = True
            print(f"FAIL {label} - {len(violations)} violation(s):")
            for v in violations:
                print(v)
            print()
        else:
            print(f"PASS {label}")

    print()
    if failed:
        print("FAIL - fix the violations above before committing.")
        return 1
    print("PASS - structure OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
