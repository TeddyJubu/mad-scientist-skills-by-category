#!/usr/bin/env python3
"""
GoHighLevel API Executor
Usage: python ghl_api.py <method> <endpoint> [--body '{"key":"value"}'] [--params '{"key":"value"}']

Examples:
  python ghl_api.py GET /contacts/ --params '{"locationId":"abc123","limit":20}'
  python ghl_api.py POST /contacts/ --body '{"locationId":"abc123","firstName":"John","email":"j@x.com"}'
  python ghl_api.py PUT /contacts/CONTACT_ID --body '{"firstName":"Jane"}'
  python ghl_api.py DELETE /contacts/CONTACT_ID
"""

import sys
import os
import json
import argparse
import requests

API_KEY  = os.environ.get("GHL_API_KEY", "pit-105d0b1f-3e18-41f1-95ad-00aca3775ddf")
BASE_URL = "https://services.leadconnectorhq.com"
HEADERS  = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type":  "application/json",
    "Version":       "2021-07-28",
}

def call(method: str, endpoint: str, params: dict = None, body: dict = None) -> dict:
    url  = BASE_URL.rstrip("/") + "/" + endpoint.lstrip("/")
    resp = requests.request(
        method.upper(),
        url,
        headers=HEADERS,
        params=params or {},
        json=body or None,
        timeout=30,
    )
    try:
        data = resp.json()
    except Exception:
        data = {"raw": resp.text}
    return {"status_code": resp.status_code, "response": data}

def main():
    parser = argparse.ArgumentParser(description="GoHighLevel API Executor")
    parser.add_argument("method",   help="HTTP method: GET, POST, PUT, PATCH, DELETE")
    parser.add_argument("endpoint", help="API endpoint path, e.g. /contacts/")
    parser.add_argument("--body",   default=None, help="JSON string for request body")
    parser.add_argument("--params", default=None, help="JSON string for query parameters")
    args = parser.parse_args()

    body   = json.loads(args.body)   if args.body   else None
    params = json.loads(args.params) if args.params else None

    result = call(args.method, args.endpoint, params=params, body=body)
    print(json.dumps(result, indent=2))
    return 0 if result["status_code"] < 400 else 1

if __name__ == "__main__":
    sys.exit(main())
