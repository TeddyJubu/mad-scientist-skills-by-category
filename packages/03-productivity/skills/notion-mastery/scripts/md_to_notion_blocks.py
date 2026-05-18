#!/usr/bin/env python3
"""Convert markdown to a list of Notion block JSON objects.

A small, dependency-free CommonMark-ish converter. Use this when you need client-side
control or your `Notion-Version` predates the native `markdown` field on POST /v1/pages.

Supported:
- Headings (## → heading_2, ### → heading_3, #### → heading_4; # is skipped because
  the page title is implicitly H1)
- Paragraphs
- Bulleted and numbered lists (with simple nesting via indentation)
- Task lists (- [ ] / - [x])
- Blockquotes (with emoji-first-char → callout extension)
- Fenced code blocks (``` with language)
- Horizontal rules (--- or ***)
- Bold (**...**, __...__), italic (*...*, _..._), inline code (`...`), strikethrough (~~...~~), links ([text](url))
- HTML <details><summary>X</summary>...</details> → toggle
- Tables (GFM)

Out of scope: nested lists more than 3 deep, custom container syntax, images as blocks
(use plain HTML or extend yourself).

Usage:
    from md_to_notion_blocks import convert
    blocks = convert(markdown_string)
"""

from __future__ import annotations

import re
import sys
from typing import Iterator

MAX_RICH_TEXT = 2000


# ---------- Public API ----------

def convert(markdown: str) -> list[dict]:
    """Convert ``markdown`` to a list of Notion block JSON objects."""
    return list(_blocks(markdown))


# ---------- Block parsing ----------

def _blocks(markdown: str) -> Iterator[dict]:
    lines = markdown.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]

        if not line.strip():
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^\s*(\*\*\*|---|___)\s*$", line):
            yield {"type": "divider", "divider": {}}
            i += 1
            continue

        # Fenced code
        m = re.match(r"^```(\w*)\s*$", line)
        if m:
            lang = m.group(1) or "plain text"
            i += 1
            buf: list[str] = []
            while i < len(lines) and not re.match(r"^```\s*$", lines[i]):
                buf.append(lines[i])
                i += 1
            i += 1  # consume closing ```
            yield {
                "type": "code",
                "code": {
                    "rich_text": _rich_text("\n".join(buf)),
                    "language": _safe_lang(lang),
                    "caption": [],
                },
            }
            continue

        # HTML details/summary → toggle
        if line.strip().startswith("<details"):
            i, block = _consume_details(lines, i)
            if block:
                yield block
                continue

        # Heading
        m = re.match(r"^(#{1,6})\s+(.+?)\s*$", line)
        if m:
            level = len(m.group(1))
            text = m.group(2)
            if level == 1:
                # Page title is implicit; promote H1 to H2 to keep the content
                level = 2
            level = min(level, 4)
            block_type = f"heading_{level if level <= 3 else 3}"
            # heading_4 only exists on Notion-Version 2026-04-01+ — use heading_3 for safety
            yield {
                block_type: {"rich_text": _rich_text(text), "color": "default"},
                "type": block_type,
            }
            i += 1
            continue

        # Blockquote (callout extension if first non-space char is emoji)
        if line.lstrip().startswith(">"):
            i, block = _consume_blockquote(lines, i)
            yield block
            continue

        # Lists
        m_bullet = re.match(r"^(\s*)([-*+])\s+\[([ xX])\]\s+(.+)$", line)
        if m_bullet:
            i, block = _consume_list_item(lines, i, kind="to_do")
            yield block
            continue

        m_bullet = re.match(r"^(\s*)([-*+])\s+(.+)$", line)
        if m_bullet:
            i, block = _consume_list_item(lines, i, kind="bulleted_list_item")
            yield block
            continue

        m_num = re.match(r"^(\s*)(\d+)\.\s+(.+)$", line)
        if m_num:
            i, block = _consume_list_item(lines, i, kind="numbered_list_item")
            yield block
            continue

        # Table
        if "|" in line and (i + 1 < len(lines) and re.match(r"^\s*\|?[\s|:-]+\|?\s*$", lines[i + 1])):
            i, block = _consume_table(lines, i)
            yield block
            continue

        # Default: paragraph (may span multiple lines until blank)
        para_lines = [line]
        i += 1
        while i < len(lines) and lines[i].strip() and not _is_block_start(lines[i]):
            para_lines.append(lines[i])
            i += 1
        text = " ".join(l.strip() for l in para_lines)
        yield {
            "type": "paragraph",
            "paragraph": {"rich_text": _rich_text(text), "color": "default"},
        }


def _is_block_start(line: str) -> bool:
    return bool(
        re.match(r"^(#{1,6}\s|```|>\s|\s*[-*+]\s|\s*\d+\.\s|---|\*\*\*|___)", line)
        or line.strip().startswith("<details")
    )


def _consume_blockquote(lines: list[str], i: int) -> tuple[int, dict]:
    buf: list[str] = []
    while i < len(lines) and lines[i].lstrip().startswith(">"):
        buf.append(re.sub(r"^\s*>\s?", "", lines[i]))
        i += 1
    text = "\n".join(buf).strip()
    # Callout extension: starts with an emoji
    first = text[:2] if text else ""
    if first and _looks_like_emoji(first[0]):
        emoji = first[0]
        rest = text[1:].lstrip()
        return i, {
            "type": "callout",
            "callout": {
                "rich_text": _rich_text(rest),
                "icon": {"type": "emoji", "emoji": emoji},
                "color": "gray_background",
            },
        }
    return i, {
        "type": "quote",
        "quote": {"rich_text": _rich_text(text), "color": "default"},
    }


def _looks_like_emoji(ch: str) -> bool:
    return ord(ch) > 127 and not ch.isalpha() and not ch.isnumeric()


def _consume_list_item(lines: list[str], i: int, *, kind: str) -> tuple[int, dict]:
    line = lines[i]
    if kind == "to_do":
        m = re.match(r"^(\s*)([-*+])\s+\[([ xX])\]\s+(.+)$", line)
        assert m
        checked = m.group(3).lower() == "x"
        text = m.group(4)
    elif kind == "bulleted_list_item":
        m = re.match(r"^(\s*)([-*+])\s+(.+)$", line)
        assert m
        text = m.group(3)
        checked = False
    else:  # numbered
        m = re.match(r"^(\s*)(\d+)\.\s+(.+)$", line)
        assert m
        text = m.group(3)
        checked = False
    i += 1
    payload: dict = {"rich_text": _rich_text(text), "color": "default"}
    if kind == "to_do":
        payload["checked"] = checked
    block = {"type": kind, kind: payload}
    return i, block


def _consume_table(lines: list[str], i: int) -> tuple[int, dict]:
    header_cells = _table_cells(lines[i])
    i += 2  # skip header + separator
    rows: list[list[list[dict]]] = []
    rows.append([_rich_text(c) for c in header_cells])
    while i < len(lines) and "|" in lines[i] and lines[i].strip():
        cells = _table_cells(lines[i])
        cells = cells[: len(header_cells)] + [""] * max(0, len(header_cells) - len(cells))
        rows.append([_rich_text(c) for c in cells])
        i += 1
    table_rows = [
        {"type": "table_row", "table_row": {"cells": row}} for row in rows
    ]
    return i, {
        "type": "table",
        "table": {
            "table_width": len(header_cells),
            "has_column_header": True,
            "has_row_header": False,
            "children": table_rows,
        },
    }


def _table_cells(line: str) -> list[str]:
    line = line.strip()
    if line.startswith("|"):
        line = line[1:]
    if line.endswith("|"):
        line = line[:-1]
    return [c.strip() for c in line.split("|")]


def _consume_details(lines: list[str], i: int) -> tuple[int, dict | None]:
    summary_match = None
    body: list[str] = []
    j = i
    while j < len(lines):
        if "<summary>" in lines[j]:
            m = re.search(r"<summary>(.*?)</summary>", lines[j])
            if m:
                summary_match = m.group(1)
        elif "</details>" in lines[j]:
            j += 1
            break
        elif "<details" not in lines[j]:
            body.append(lines[j])
        j += 1
    if summary_match is None:
        return i + 1, None
    children = convert("\n".join(body))
    return j, {
        "type": "toggle",
        "toggle": {
            "rich_text": _rich_text(summary_match),
            "color": "default",
            "children": children,
        },
    }


# ---------- Inline parsing ----------

_INLINE_PATTERN = re.compile(
    r"(\*\*([^*]+)\*\*|__([^_]+)__"  # bold
    r"|\*([^*]+)\*|_([^_]+)_"  # italic
    r"|~~([^~]+)~~"  # strikethrough
    r"|`([^`]+)`"  # code
    r"|\[([^\]]+)\]\(([^)]+)\))"  # link
)


def _rich_text(text: str) -> list[dict]:
    """Return a rich_text array, handling inline annotations and 2000-char chunking."""
    elements: list[dict] = []
    pos = 0
    for m in _INLINE_PATTERN.finditer(text):
        if m.start() > pos:
            elements.extend(_plain(text[pos : m.start()]))
        full = m.group(0)
        if full.startswith("**") or full.startswith("__"):
            inner = m.group(2) or m.group(3)
            elements.extend(_annotated(inner, bold=True))
        elif full.startswith("~~"):
            elements.extend(_annotated(m.group(6), strikethrough=True))
        elif full.startswith("`"):
            elements.extend(_annotated(m.group(7), code=True))
        elif full.startswith("["):
            elements.extend(_link(m.group(8), m.group(9)))
        else:
            inner = m.group(4) or m.group(5)
            elements.extend(_annotated(inner, italic=True))
        pos = m.end()
    if pos < len(text):
        elements.extend(_plain(text[pos:]))
    return elements


def _plain(s: str) -> list[dict]:
    return [{"type": "text", "text": {"content": chunk}} for chunk in _chunk(s)]


def _annotated(s: str, **flags: bool) -> list[dict]:
    return [
        {"type": "text", "text": {"content": chunk}, "annotations": {k: True for k in flags}}
        for chunk in _chunk(s)
    ]


def _link(label: str, url: str) -> list[dict]:
    return [
        {"type": "text", "text": {"content": chunk, "link": {"url": url}}}
        for chunk in _chunk(label)
    ]


def _chunk(s: str) -> list[str]:
    if len(s) <= MAX_RICH_TEXT:
        return [s] if s else []
    out: list[str] = []
    while len(s) > MAX_RICH_TEXT:
        cut = s.rfind(" ", 0, MAX_RICH_TEXT) or MAX_RICH_TEXT
        out.append(s[:cut])
        s = s[cut:].lstrip()
    if s:
        out.append(s)
    return out


# ---------- Misc ----------

_VALID_LANGS = {
    "abap", "agda", "arduino", "ascii art", "assembly", "bash", "basic", "bnf", "c",
    "c#", "c++", "clojure", "coffeescript", "coq", "css", "dart", "dhall", "diff",
    "docker", "ebnf", "elixir", "elm", "erlang", "f#", "flow", "fortran", "gherkin",
    "glsl", "go", "graphql", "groovy", "haskell", "hcl", "html", "idris", "java",
    "javascript", "json", "julia", "kotlin", "latex", "less", "lisp", "livescript",
    "llvm ir", "lua", "makefile", "markdown", "markup", "matlab", "mathematica",
    "mermaid", "nix", "notion formula", "objective-c", "ocaml", "pascal", "perl",
    "php", "plain text", "powershell", "prolog", "protobuf", "purescript", "python",
    "r", "racket", "reason", "ruby", "rust", "sass", "scala", "scheme", "scss",
    "shell", "smalltalk", "solidity", "sql", "swift", "toml", "typescript", "vb.net",
    "verilog", "vhdl", "visual basic", "webassembly", "xml", "yaml",
}


def _safe_lang(lang: str) -> str:
    lang = lang.lower()
    alias = {"js": "javascript", "ts": "typescript", "py": "python", "sh": "shell", "yml": "yaml"}
    lang = alias.get(lang, lang)
    return lang if lang in _VALID_LANGS else "plain text"


def main(argv: list[str]) -> int:
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    import json
    text = sys.stdin.read() if argv[0] == "-" else open(argv[0]).read()
    blocks = convert(text)
    json.dump(blocks, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
