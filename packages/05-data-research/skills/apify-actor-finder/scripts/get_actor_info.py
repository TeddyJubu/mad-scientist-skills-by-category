#!/usr/bin/env python3
"""
get_actor_info.py - Fetch actor details including example input and readme summary.

Used to determine what information is needed from the user before running an actor.

Usage:
    python3.11 get_actor_info.py <api_key> <actor_id>

Output:
    Prints the actor's title, description, readme summary, and example input JSON.
"""

import sys
import json
import urllib.request
import urllib.parse


API_BASE = "https://api.apify.com/v2"


def get_actor_details(api_key: str, actor_id: str) -> dict:
    """Fetch full actor details from the Apify API."""
    url = f"{API_BASE}/acts/{actor_id}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read()).get("data", {})


def get_store_actor(api_key: str, actor_id: str) -> dict:
    """Fetch actor from the store to get readmeSummary."""
    if "~" not in actor_id:
        return {}
    username, name = actor_id.split("~", 1)
    params = urllib.parse.urlencode({"search": name, "limit": 10})
    url = f"{API_BASE}/store?{params}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req) as resp:
        items = json.loads(resp.read()).get("data", {}).get("items", [])
    for item in items:
        if item.get("username") == username and item.get("name") == name:
            return item
    return {}


def main():
    if len(sys.argv) != 3:
        print("Usage: python3.11 get_actor_info.py <api_key> <actor_id>", file=sys.stderr)
        sys.exit(1)

    api_key = sys.argv[1]
    actor_id = sys.argv[2]

    try:
        details = get_actor_details(api_key, actor_id)
        store_info = get_store_actor(api_key, actor_id)
    except Exception as e:
        print(f"Error fetching actor info: {e}", file=sys.stderr)
        sys.exit(1)

    title = details.get("title") or store_info.get("title") or actor_id
    description = details.get("description") or store_info.get("description") or ""
    readme = store_info.get("readmeSummary") or ""

    example_input_raw = details.get("exampleRunInput", {}).get("body", "{}")
    try:
        example_input = json.loads(example_input_raw)
        # Filter out placeholder inputs like {"helloWorld": 123}
        if list(example_input.keys()) == ["helloWorld"]:
            example_input = {}
    except Exception:
        example_input = {}

    print(f"=== {title} ===")
    print(f"Actor ID : {actor_id}")
    print(f"URL      : https://apify.com/{actor_id.replace('~', '/')}")
    print()
    print(f"Description:\n{description}")
    print()
    if readme:
        print(f"README Summary (first 1000 chars):\n{readme[:1000]}")
        print()
    if example_input:
        print(f"Example Input:\n{json.dumps(example_input, indent=2)}")
    else:
        print("Example Input: Not provided — refer to description and README above.")


if __name__ == "__main__":
    main()
