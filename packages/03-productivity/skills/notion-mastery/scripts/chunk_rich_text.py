#!/usr/bin/env python3
"""Split a long string into Notion rich_text elements that respect the 2000-char limit.

Notion enforces a maximum of 2000 characters per rich_text element's `content`. Any
single text longer than that has to be split across multiple text elements within the
same rich_text array — they will render as one continuous paragraph.

Usage:
    from chunk_rich_text import chunk

    rich_text = chunk("a very long string ...", annotations={"bold": True})
    block = {
        "type": "paragraph",
        "paragraph": {"rich_text": rich_text, "color": "default"}
    }
"""

from __future__ import annotations

import json
import sys
from typing import Iterable

MAX_CHARS = 2000


def chunk(
    content: str,
    *,
    link: str | None = None,
    annotations: dict | None = None,
    max_chars: int = MAX_CHARS,
) -> list[dict]:
    """Return a rich_text array for ``content``, split as needed at safe boundaries.

    Splits prefer paragraph breaks, then sentence ends, then whitespace. Falls back to
    a hard split at ``max_chars`` for inputs with no natural boundaries.
    """
    if not content:
        return []

    pieces = _split(content, max_chars=max_chars)
    elements: list[dict] = []
    for piece in pieces:
        element: dict = {"type": "text", "text": {"content": piece}}
        if link:
            element["text"]["link"] = {"url": link}
        if annotations:
            element["annotations"] = {**annotations}
        elements.append(element)
    return elements


def _split(s: str, *, max_chars: int) -> list[str]:
    if len(s) <= max_chars:
        return [s]
    out: list[str] = []
    remaining = s
    while len(remaining) > max_chars:
        cut = _find_cut(remaining, max_chars)
        out.append(remaining[:cut])
        remaining = remaining[cut:]
    if remaining:
        out.append(remaining)
    return out


def _find_cut(s: str, max_chars: int) -> int:
    """Return an index to cut ``s`` at. Prefer natural boundaries near ``max_chars``."""
    window = s[:max_chars]
    # Prefer paragraph break
    para = window.rfind("\n\n")
    if para >= max_chars * 0.5:
        return para + 2
    # Then a single newline
    line = window.rfind("\n")
    if line >= max_chars * 0.5:
        return line + 1
    # Then a sentence end
    for sep in (". ", "! ", "? "):
        idx = window.rfind(sep)
        if idx >= max_chars * 0.5:
            return idx + len(sep)
    # Then any whitespace
    ws = window.rfind(" ")
    if ws >= max_chars * 0.5:
        return ws + 1
    # Last resort: hard cut
    return max_chars


def split_paragraph_block(text: str, *, color: str = "default") -> list[dict]:
    """Return one or more ``paragraph`` blocks for ``text``.

    Use this when a single string would exceed the 2000-char rich_text limit AND you
    want it to render as separate paragraphs. (For one continuous paragraph, use
    ``chunk()`` to build a single block with multiple text elements.)
    """
    paragraphs = [p for p in text.split("\n\n") if p.strip()]
    blocks: list[dict] = []
    for p in paragraphs:
        blocks.append({
            "type": "paragraph",
            "paragraph": {"rich_text": chunk(p), "color": color},
        })
    return blocks


def main(argv: Iterable[str]) -> int:
    argv = list(argv)
    if not argv or argv[0] in ("-h", "--help"):
        print(__doc__)
        return 0
    text = sys.stdin.read() if argv[0] == "-" else " ".join(argv)
    rich = chunk(text)
    json.dump(rich, sys.stdout, indent=2, ensure_ascii=False)
    sys.stdout.write("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
