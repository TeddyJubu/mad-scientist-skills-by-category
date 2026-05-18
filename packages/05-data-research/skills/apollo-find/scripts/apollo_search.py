#!/usr/bin/env python3
"""
Apollo.io People Search — CSV export utility
Usage: python3 apollo_search.py --titles "CTO" --locations "maryland" --pages 2 --output out.csv
"""

import argparse
import csv
import json
import os
import sys
import time
from pathlib import Path

try:
    import requests
except ImportError:
    print("Installing requests...", file=sys.stderr)
    os.system("pip install requests -q")
    import requests

# ── Auth ─────────────────────────────────────────────────────────────────────
SECRETS_PATH = Path(__file__).parent.parent.parent.parent / ".secrets/apollo.env"
API_KEY = None

if SECRETS_PATH.exists():
    for line in SECRETS_PATH.read_text().splitlines():
        if line.startswith("APOLLO_API_KEY="):
            API_KEY = line.split("=", 1)[1].strip()

if not API_KEY:
    API_KEY = os.environ.get("APOLLO_API_KEY")

if not API_KEY:
    print("ERROR: APOLLO_API_KEY not found. Set it in .secrets/apollo.env", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://api.apollo.io/api/v1/mixed_people/api_search"
HEADERS = {"x-api-key": API_KEY, "Content-Type": "application/json"}


def build_payload(args, page: int) -> dict:
    payload: dict = {"page": page, "per_page": min(args.per_page, 100)}

    if args.titles:
        payload["person_titles"] = args.titles
    if args.locations:
        payload["person_locations"] = args.locations
    if args.org_locations:
        payload["organization_locations"] = args.org_locations
    if args.seniority:
        payload["person_seniorities"] = args.seniority
    if args.domains:
        payload["organization_domains"] = args.domains
    if args.employees:
        payload["organization_num_employees_ranges"] = args.employees
    if args.keywords:
        payload["q_keywords"] = args.keywords
    if args.technologies:
        payload["currently_using_any_of_technology_uids"] = args.technologies
    if args.email_status:
        payload["email_status"] = args.email_status

    return payload


def flatten_person(p: dict) -> dict:
    org = p.get("organization") or {}
    return {
        "id": p.get("id", ""),
        "first_name": p.get("first_name", ""),
        "last_name": p.get("last_name", ""),
        "title": p.get("title", ""),
        "company": org.get("name", p.get("organization_name", "")),
        "domain": org.get("primary_domain", ""),
        "city": p.get("city", ""),
        "state": p.get("state", ""),
        "country": p.get("country", ""),
        "linkedin_url": p.get("linkedin_url", ""),
        "email": p.get("email", ""),
        "phone": p.get("sanitized_phone", ""),
        "employees": org.get("num_employees", ""),
        "industry": org.get("industry", ""),
        "keywords": ", ".join(org.get("keywords", []) or []),
    }


def search(args):
    all_people = []
    total_pages = args.pages

    for page in range(1, total_pages + 1):
        payload = build_payload(args, page)
        print(f"  Fetching page {page}/{total_pages}...", file=sys.stderr)

        try:
            resp = requests.post(BASE_URL, headers=HEADERS, json=payload, timeout=30)
            resp.raise_for_status()
        except requests.HTTPError as e:
            print(f"  HTTP error on page {page}: {e}", file=sys.stderr)
            break

        data = resp.json()
        people = data.get("people", [])
        pagination = data.get("pagination", {})

        if not people:
            print(f"  No more results at page {page}.", file=sys.stderr)
            break

        all_people.extend(people)
        total_entries = pagination.get("total_entries", "?")
        print(f"  Got {len(people)} results (total in DB: {total_entries})", file=sys.stderr)

        if page < total_pages:
            time.sleep(0.5)  # rate limit courtesy

    return all_people


def write_csv(people: list, output_path: str):
    if not people:
        print("No results to write.", file=sys.stderr)
        return

    rows = [flatten_person(p) for p in people]
    fields = list(rows[0].keys())

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"\n✅ Exported {len(rows)} contacts → {output_path}", file=sys.stderr)


def main():
    parser = argparse.ArgumentParser(description="Apollo.io People Search")
    parser.add_argument("--titles", nargs="+", help="Job titles to search")
    parser.add_argument("--locations", nargs="+", help="Person locations (city/state/country)")
    parser.add_argument("--org-locations", nargs="+", dest="org_locations", help="HQ locations")
    parser.add_argument("--seniority", nargs="+", help="Seniority levels")
    parser.add_argument("--domains", nargs="+", help="Company domains")
    parser.add_argument("--employees", nargs="+", help="Employee ranges e.g. '1,200'")
    parser.add_argument("--keywords", help="Free-text keyword filter")
    parser.add_argument("--technologies", nargs="+", help="Tech stack filters")
    parser.add_argument("--email-status", nargs="+", dest="email_status",
                        choices=["verified", "unverified", "likely to engage", "unavailable"])
    parser.add_argument("--pages", type=int, default=1, help="Number of pages to fetch (default: 1)")
    parser.add_argument("--per-page", type=int, default=25, dest="per_page",
                        help="Results per page (max 100, default: 25)")
    parser.add_argument("--output", default="apollo_results.csv", help="Output CSV filename")
    parser.add_argument("--json", action="store_true", help="Print raw JSON instead of CSV")

    args = parser.parse_args()

    if not any([args.titles, args.locations, args.org_locations, args.domains, args.keywords]):
        print("ERROR: Provide at least one filter (--titles, --locations, --domains, --keywords)",
              file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    print(f"\n🔍 Apollo Search starting...", file=sys.stderr)
    people = search(args)
    print(f"\n📊 Total fetched: {len(people)}", file=sys.stderr)

    if args.json:
        print(json.dumps(people, indent=2))
    else:
        write_csv(people, args.output)
        # Also print summary to stdout
        print(f"\n--- TOP RESULTS ---")
        for p in people[:10]:
            r = flatten_person(p)
            print(f"• {r['first_name']} {r['last_name']} | {r['title']} | {r['company']} | {r['city']}, {r['state']}")
        if len(people) > 10:
            print(f"  ... and {len(people) - 10} more in {args.output}")


if __name__ == "__main__":
    main()
