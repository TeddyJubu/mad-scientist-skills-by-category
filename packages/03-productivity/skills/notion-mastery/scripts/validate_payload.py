#!/usr/bin/env python3
"""Pre-flight validation for Notion API payloads.

Run this on a payload before you POST it. It checks the most common mistakes —
missing parent, missing type discriminators, oversized rich_text, too many
children — and returns a list of human-readable issues. Catches ~90% of the
errors that come back as `validation_error` from the Notion API.

Usage:
    from validate_payload import validate_page_create, validate_blocks_append

    issues = validate_page_create(payload)
    if issues:
        for i in issues: print("-", i)
        raise SystemExit("Fix issues before calling Notion")

The validator is conservative — it complains when it's pretty sure something
is wrong, but doesn't catch every possible mistake. Use it as a first pass.
"""

from __future__ import annotations

import json
import sys
from typing import Any

MAX_CHILDREN = 100
MAX_NESTING = 2
MAX_RICH_TEXT_CHARS = 2000
MAX_TITLE_CHARS = 200
MAX_URL_CHARS = 2000

KNOWN_BLOCK_TYPES = {
    "paragraph", "heading_1", "heading_2", "heading_3", "heading_4",
    "bulleted_list_item", "numbered_list_item", "to_do", "toggle",
    "quote", "callout", "divider", "code",
    "image", "video", "audio", "file", "pdf", "bookmark", "embed", "link_preview",
    "table", "table_row", "column_list", "column",
    "synced_block", "template", "breadcrumb", "table_of_contents",
    "equation", "child_page", "child_database", "link_to_page",
}


def validate_page_create(payload: dict) -> list[str]:
    """Validate a `POST /v1/pages` body. Returns a list of issue strings."""
    issues: list[str] = []
    parent = payload.get("parent")
    if not parent:
        issues.append("Missing top-level `parent`.")
    elif "page_id" not in parent and "database_id" not in parent and "workspace" not in parent:
        issues.append("`parent` must have one of `page_id`, `database_id`, or `workspace: true`.")

    properties = payload.get("properties")
    if properties is None:
        issues.append("Missing `properties` (at minimum, a title for the page).")

    if "icon" in payload:
        issues.extend(_validate_icon_or_cover(payload["icon"], "icon"))
    if "cover" in payload:
        issues.extend(_validate_icon_or_cover(payload["cover"], "cover"))

    children = payload.get("children", [])
    if len(children) > MAX_CHILDREN:
        issues.append(
            f"`children` has {len(children)} blocks but max is {MAX_CHILDREN}. "
            "Split into multiple calls."
        )
    for i, block in enumerate(children):
        issues.extend(_validate_block(block, path=f"children[{i}]", depth=1))

    return issues


def validate_blocks_append(payload: dict) -> list[str]:
    """Validate a `PATCH /v1/blocks/{id}/children` body."""
    issues: list[str] = []
    children = payload.get("children")
    if not isinstance(children, list):
        issues.append("Missing or non-list `children`.")
        return issues
    if len(children) > MAX_CHILDREN:
        issues.append(
            f"`children` has {len(children)} blocks but max is {MAX_CHILDREN}. "
            "Split into multiple calls."
        )
    for i, block in enumerate(children):
        issues.extend(_validate_block(block, path=f"children[{i}]", depth=1))
    return issues


def _validate_block(block: Any, *, path: str, depth: int) -> list[str]:
    issues: list[str] = []
    if not isinstance(block, dict):
        issues.append(f"{path}: not an object.")
        return issues
    t = block.get("type")
    if not t:
        issues.append(f"{path}: missing `type`.")
        return issues
    if t not in KNOWN_BLOCK_TYPES:
        issues.append(f"{path}: unknown block type `{t}`. Check api-reference.md §1.")
    sub = block.get(t)
    if sub is None:
        issues.append(f"{path}: missing `{t}` payload object (sibling of `type`).")
        return issues

    rich = sub.get("rich_text") if isinstance(sub, dict) else None
    if isinstance(rich, list):
        for j, el in enumerate(rich):
            issues.extend(_validate_rich_text_element(el, path=f"{path}.{t}.rich_text[{j}]"))

    children = sub.get("children") if isinstance(sub, dict) else None
    if isinstance(children, list):
        if depth >= MAX_NESTING:
            issues.append(
                f"{path}: nested children at depth {depth + 1}; max is "
                f"{MAX_NESTING} per call. Append children in a follow-up call instead."
            )
        for j, child in enumerate(children):
            issues.extend(
                _validate_block(child, path=f"{path}.{t}.children[{j}]", depth=depth + 1)
            )

    # column and column_list have shape constraints
    if t == "column_list":
        cols = (sub or {}).get("children", [])
        non_col = [i for i, c in enumerate(cols) if isinstance(c, dict) and c.get("type") != "column"]
        if non_col:
            issues.append(f"{path}: column_list children must all be `column` blocks (offending: {non_col}).")
        if len(cols) < 2:
            issues.append(f"{path}: column_list needs at least 2 columns (has {len(cols)}).")

    return issues


def _validate_rich_text_element(el: Any, *, path: str) -> list[str]:
    issues: list[str] = []
    if not isinstance(el, dict):
        issues.append(f"{path}: not an object.")
        return issues
    t = el.get("type", "text")
    if t == "text":
        text = (el.get("text") or {}).get("content", "")
        if len(text) > MAX_RICH_TEXT_CHARS:
            issues.append(
                f"{path}: text content is {len(text)} chars; max {MAX_RICH_TEXT_CHARS}. "
                "Use chunk_rich_text.py to split."
            )
    elif t == "mention":
        if not el.get("mention"):
            issues.append(f"{path}: mention element missing `mention` payload.")
    elif t == "equation":
        if not (el.get("equation") or {}).get("expression"):
            issues.append(f"{path}: equation element missing `equation.expression`.")
    return issues


def _validate_icon_or_cover(obj: Any, label: str) -> list[str]:
    issues: list[str] = []
    if not isinstance(obj, dict):
        issues.append(f"{label}: not an object.")
        return issues
    t = obj.get("type")
    if t not in ("emoji", "external", "file"):
        issues.append(f"{label}: type must be one of `emoji`, `external`, `file`; got {t!r}.")
        return issues
    if t == "emoji" and not obj.get("emoji"):
        issues.append(f"{label}: emoji type missing `emoji` value.")
    if t == "external":
        url = (obj.get("external") or {}).get("url", "")
        if not url:
            issues.append(f"{label}: external type missing `external.url`.")
        elif len(url) > MAX_URL_CHARS:
            issues.append(f"{label}: external url length {len(url)} > {MAX_URL_CHARS}.")
    return issues


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print("Usage: validate_payload.py [page|append] <payload.json>")
        return 0
    mode = argv[0]
    path = argv[1]
    with open(path) as f:
        payload = json.load(f)
    if mode == "page":
        issues = validate_page_create(payload)
    elif mode == "append":
        issues = validate_blocks_append(payload)
    else:
        print(f"unknown mode {mode!r}", file=sys.stderr)
        return 2
    if not issues:
        print("OK")
        return 0
    for i in issues:
        print(f"- {i}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
