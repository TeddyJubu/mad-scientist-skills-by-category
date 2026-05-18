#!/usr/bin/env python3
"""Append a long list of Notion blocks to a parent in 100-block batches.

Notion's PATCH /v1/blocks/{id}/children endpoint accepts at most 100 children per
call. This helper splits a larger list into batches, calls the endpoint sequentially,
and handles 429 rate limits and transient 5xx with exponential backoff.

It accepts either a raw HTTP client (requests/httpx) or an SDK-style client with
``client.blocks.children.append(block_id, children)`` — see ``append_blocks_http`` and
``append_blocks_sdk`` below.

Usage with notion-sdk-py:
    from notion_client import Client
    from batch_append import append_blocks_sdk

    notion = Client(auth=os.environ["NOTION_TOKEN"])
    append_blocks_sdk(notion, parent_id="...", children=big_block_list)

Usage with raw requests:
    import requests
    from batch_append import append_blocks_http

    session = requests.Session()
    session.headers["Authorization"] = f"Bearer {token}"
    session.headers["Notion-Version"] = "2025-09-03"
    session.headers["Content-Type"] = "application/json"

    append_blocks_http(session, parent_id="...", children=big_block_list)
"""

from __future__ import annotations

import time
from typing import Any, Callable, Iterable, Iterator

MAX_CHILDREN_PER_CALL = 100
MAX_RETRIES = 5


def _batches(children: Iterable[dict], size: int = MAX_CHILDREN_PER_CALL) -> Iterator[list[dict]]:
    batch: list[dict] = []
    for item in children:
        batch.append(item)
        if len(batch) == size:
            yield batch
            batch = []
    if batch:
        yield batch


def append_blocks_sdk(
    client: Any,
    *,
    parent_id: str,
    children: Iterable[dict],
    on_batch: Callable[[int, list[dict]], None] | None = None,
) -> list[dict]:
    """Append ``children`` to ``parent_id`` using a notion-sdk-py-style client.

    ``client.blocks.children.append(block_id, children)`` must exist. Returns the
    aggregated list of created block objects.
    """
    created: list[dict] = []
    for i, batch in enumerate(_batches(children)):
        if on_batch:
            on_batch(i, batch)
        result = _with_retry(
            lambda: client.blocks.children.append(block_id=parent_id, children=batch)
        )
        created.extend(result.get("results", []))
    return created


def append_blocks_http(
    session: Any,
    *,
    parent_id: str,
    children: Iterable[dict],
    base_url: str = "https://api.notion.com/v1",
    on_batch: Callable[[int, list[dict]], None] | None = None,
) -> list[dict]:
    """Append ``children`` to ``parent_id`` using a requests-style session.

    The session must already have ``Authorization``, ``Notion-Version``, and
    ``Content-Type: application/json`` headers set.
    """
    created: list[dict] = []
    url = f"{base_url}/blocks/{parent_id}/children"
    for i, batch in enumerate(_batches(children)):
        if on_batch:
            on_batch(i, batch)
        result = _with_retry(lambda: _do_patch(session, url, {"children": batch}))
        created.extend(result.get("results", []))
    return created


def _do_patch(session: Any, url: str, body: dict) -> dict:
    resp = session.patch(url, json=body)
    if resp.status_code == 429:
        retry_after = int(resp.headers.get("Retry-After", "1"))
        raise _RateLimited(retry_after)
    if 500 <= resp.status_code < 600:
        raise _Transient(resp.status_code, resp.text)
    if not resp.ok:
        raise RuntimeError(f"Notion {resp.status_code}: {resp.text}")
    return resp.json()


class _RateLimited(Exception):
    def __init__(self, retry_after: int) -> None:
        self.retry_after = retry_after


class _Transient(Exception):
    def __init__(self, status: int, body: str) -> None:
        self.status = status
        self.body = body


def _with_retry(fn: Callable[[], dict], max_retries: int = MAX_RETRIES) -> dict:
    for attempt in range(max_retries):
        try:
            return fn()
        except _RateLimited as e:
            time.sleep(max(1, e.retry_after))
        except _Transient:
            time.sleep(2 ** attempt)
        # SDK clients can raise typed errors; if you want to retry those, catch them here.
    raise RuntimeError("Notion API: exceeded retry budget")
