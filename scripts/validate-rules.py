#!/usr/bin/env python3
"""Validate CursorRules .mdc files and cross-references."""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
RULES_DIR = REPO_ROOT / ".cursor" / "rules"
LARGE_FILE_LINES = 250

# Example/placeholder rule names that may be cited but need not exist.
MDC_PLACEHOLDERS = frozenset(
    {
        "project-specific-standards.mdc",
        "myproject-conventions.mdc",
        "code-complexity-quality-metrics.mdc",
    }
)

# Foreign project path fragments that must not appear in shared rules.
FOREIGN_PATH_DENYLIST = ("searchaton/",)

# Version-pair groups: both families should not ship together without pruning.
VERSION_PAIR_GROUPS = (
    ("swift-5-9-", "swift-6-"),
    ("java-17-", "java-21-"),
)

MDC_REF_RE = re.compile(r"`([a-z0-9_*-]+\.mdc)`", re.IGNORECASE)
DOCS_REF_RE = re.compile(r"`(docs/[a-zA-Z0-9_./-]+\.md)`")
GLOB_STRING_RE = re.compile(r"^globs:\s*[\"'][^\"']+[\"']\s*$", re.MULTILINE)


class Reporter:
    def __init__(self) -> None:
        self.errors: list[str] = []
        self.warnings: list[str] = []

    def error(self, message: str) -> None:
        self.errors.append(message)

    def warn(self, message: str) -> None:
        self.warnings.append(message)

    def ok(self) -> bool:
        return not self.errors


def parse_frontmatter(text: str) -> dict[str, str] | None:
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    block = text[3:end].strip()
    fields: dict[str, str] = {}
    for line in block.splitlines():
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        fields[key.strip()] = value.strip()
    return fields


def parse_globs(raw: str) -> list[str]:
    raw = raw.strip()
    if not raw:
        return []
    if raw.startswith("["):
        return re.findall(r'"([^"]+)"', raw) or re.findall(r"'([^']+)'", raw)
    if raw.startswith('"') or raw.startswith("'"):
        inner = raw.strip("\"'")
        return [part.strip() for part in inner.split(",") if part.strip()]
    return [raw]


def check_frontmatter(path: Path, text: str, reporter: Reporter) -> dict[str, str] | None:
    rel = path.relative_to(REPO_ROOT)
    fm = parse_frontmatter(text)
    if fm is None:
        reporter.error(f"{rel}: missing frontmatter block")
        return None
    if "description" not in fm:
        reporter.error(f"{rel}: frontmatter missing description")
    if "alwaysApply" not in fm:
        reporter.error(f"{rel}: frontmatter missing alwaysApply")
    elif fm["alwaysApply"] not in {"true", "false"}:
        reporter.error(f"{rel}: alwaysApply must be true or false, got {fm['alwaysApply']!r}")
    if GLOB_STRING_RE.search(text[:500]):
        reporter.warn(f"{rel}: globs uses comma-separated string; prefer YAML array")
    return fm


def check_cross_refs(path: Path, text: str, reporter: Reporter) -> None:
    rel = path.relative_to(REPO_ROOT)
    for match in MDC_REF_RE.finditer(text):
        name = match.group(1)
        if "*" in name:
            continue
        if name in MDC_PLACEHOLDERS:
            continue
        target = RULES_DIR / name
        if not target.is_file():
            reporter.error(f"{rel}: unresolved .mdc reference `{name}`")

    for match in DOCS_REF_RE.finditer(text):
        doc_path = REPO_ROOT / match.group(1)
        if not doc_path.is_file():
            reporter.error(f"{rel}: unresolved docs reference `{match.group(1)}`")


def check_foreign_paths(path: Path, text: str, reporter: Reporter) -> None:
    rel = path.relative_to(REPO_ROOT)
    for fragment in FOREIGN_PATH_DENYLIST:
        if fragment in text:
            reporter.error(f"{rel}: contains foreign project path {fragment!r}")


def check_large_files(path: Path, text: str, reporter: Reporter) -> None:
    rel = path.relative_to(REPO_ROOT)
    line_count = text.count("\n") + (1 if text and not text.endswith("\n") else 0)
    if line_count > LARGE_FILE_LINES:
        reporter.warn(f"{rel}: {line_count} lines exceeds {LARGE_FILE_LINES}-line review threshold")


def check_version_pair_collisions(rule_files: list[Path], reporter: Reporter) -> None:
    glob_to_files: dict[str, list[str]] = {}
    for path in rule_files:
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if not fm or "globs" not in fm:
            continue
        for glob_pattern in parse_globs(fm["globs"]):
            glob_to_files.setdefault(glob_pattern, []).append(path.name)

    for prefix_a, prefix_b in VERSION_PAIR_GROUPS:
        family_a = [name for names in glob_to_files.values() for name in names if name.startswith(prefix_a)]
        family_b = [name for names in glob_to_files.values() for name in names if name.startswith(prefix_b)]
        if not family_a or not family_b:
            continue
        shared_globs = [
            glob_pattern
            for glob_pattern, names in glob_to_files.items()
            if any(n.startswith(prefix_a) for n in names)
            and any(n.startswith(prefix_b) for n in names)
        ]
        if shared_globs:
            reporter.warn(
                "version-pair collision: "
                f"{prefix_a}* and {prefix_b}* share globs {shared_globs}; "
                "projects should prune one family at install time"
            )


def check_always_on_budget(rule_files: list[Path], reporter: Reporter) -> None:
    total_lines = 0
    files: list[str] = []
    for path in rule_files:
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if fm and fm.get("alwaysApply") == "true":
            line_count = text.count("\n") + 1
            total_lines += line_count
            files.append(f"{path.name} ({line_count})")
    if files:
        reporter.warn(
            f"always-on budget: {total_lines} lines across {len(files)} files: {', '.join(files)}"
        )


def main() -> int:
    reporter = Reporter()
    rule_files = sorted(RULES_DIR.glob("*.mdc"))
    if not rule_files:
        reporter.error("no .mdc files found in .cursor/rules/")
        return 1

    for path in rule_files:
        text = path.read_text(encoding="utf-8")
        check_frontmatter(path, text, reporter)
        check_cross_refs(path, text, reporter)
        check_foreign_paths(path, text, reporter)
        check_large_files(path, text, reporter)

    check_version_pair_collisions(rule_files, reporter)
    check_always_on_budget(rule_files, reporter)

    for warning in reporter.warnings:
        print(f"WARNING: {warning}", file=sys.stderr)
    for error in reporter.errors:
        print(f"ERROR: {error}", file=sys.stderr)

    if reporter.errors:
        print(f"\nValidation failed: {len(reporter.errors)} error(s), {len(reporter.warnings)} warning(s).")
        return 1

    print(f"Validation passed: 0 errors, {len(reporter.warnings)} warning(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
