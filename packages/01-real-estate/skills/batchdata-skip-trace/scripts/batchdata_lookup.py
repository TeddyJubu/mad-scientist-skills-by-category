#!/usr/bin/env python3
"""
BatchData Skip Trace Lookup
Single address or CSV batch property owner lookup via BatchData API.
Uses POST /api/v1/property/skip-trace (not /property/search).
"""

import json
import os
import sys
import csv
import time
import re
from datetime import datetime
from pathlib import Path

API_URL = "https://api.batchdata.com/api/v1/property/skip-trace"
SECRETS_FILE = Path.home() / ".secrets" / "batchdata.env"


def load_api_key():
    """Load BatchData API key from secrets file."""
    if SECRETS_FILE.exists():
        for line in SECRETS_FILE.read_text().splitlines():
            if line.startswith("BATCHDATA_API_KEY="):
                return line.split("=", 1)[1].strip()
    return os.environ.get("BATCHDATA_API_KEY", "")


def parse_address(address: str) -> dict:
    """
    Parse a freeform address string into components.
    Handles formats like:
      '109 S Gilmor St, Baltimore, MD 21223'
      '109 S Gilmor St Baltimore MD 21223'
    Returns dict with street, city, state, zip keys.
    """
    # US state abbreviations + full names
    states = {
        "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID",
        "IL","IN","IA","KS","KY","LA","ME","MD","MA","MI","MN","MS",
        "MO","MT","NE","NV","NH","NJ","NM","NY","NC","ND","OH","OK",
        "OR","PA","RI","SC","SD","TN","TX","UT","VT","VA","WA","WV",
        "WI","WY","DC"
    }

    address = address.strip()
    # Split on commas first
    parts = [p.strip() for p in address.split(",")]
    result = {"street": "", "city": "", "state": "", "zip": ""}

    if len(parts) >= 3:
        # Format: "street, city, state zip"
        result["street"] = parts[0]
        result["city"] = parts[1]
        # Last part contains state + zip
        last = parts[-1]
        state_zip_match = re.match(r'^([A-Za-z]{2})\s+(.{3,10})$', last)
        if state_zip_match:
            result["state"] = state_zip_match.group(1).upper()
            result["zip"] = state_zip_match.group(2).strip()
        else:
            # Try to extract state from the last part by finding a state abbrev
            for s in states:
                idx = last.upper().find(s)
                if idx != -1:
                    result["state"] = s
                    result["zip"] = last[idx + 2:].strip()
                    if result["city"] == "":
                        result["city"] = last[:idx].strip()
                    break
    elif len(parts) == 2:
        result["street"] = parts[0]
        result["city"] = parts[1]
    elif len(parts) == 1:
        # Try space-based parsing: street city state zip
        tokens = address.split()
        for i, tok in enumerate(tokens):
            if tok.upper() in states and i + 1 < len(tokens):
                result["state"] = tok.upper()
                # zip is the last token
                result["zip"] = tokens[-1] if len(tokens[-1]) >= 5 else ""
                # city is the token before state
                if i > 0:
                    result["city"] = tokens[i - 1]
                # street is everything before city
                result["street"] = " ".join(tokens[:i - 1]) if i > 1 else tokens[0]
                break
        if not result["state"]:
            result["street"] = address

    return result


def lookup_address(api_key: str, address: str) -> dict:
    """
    Call BatchData skip-trace API for a single address.
    Returns dict from the first matched person, or {} if no match.
    """
    if not api_key:
        return {}

    parsed = parse_address(address)
    if not parsed.get("street"):
        print(f"  [WARN] Could not parse address: {address}", file=sys.stderr)
        return {}

    import urllib.request
    payload = json.dumps({
        "requests": [
            {
                "propertyAddress": {
                    "street": parsed["street"],
                    "city": parsed["city"],
                    "state": parsed["state"],
                    "zip": parsed["zip"]
                }
            }
        ]
    }).encode()

    req = urllib.request.Request(
        API_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read())
            persons = data.get("results", {}).get("persons", [])
            for person in persons:
                meta = person.get("meta", {})
                if meta.get("matched") and not meta.get("error"):
                    return person
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        if e.code == 403 and "Insufficient balance" in body:
            print(f"  [ERROR] BatchData insufficient balance — skip-trace credits needed", file=sys.stderr)
        else:
            print(f"  [WARN] HTTP {e.code} for '{address}': {body[:200]}", file=sys.stderr)
    except Exception as e:
        print(f"  [WARN] Error looking up '{address}': {e}", file=sys.stderr)
    return {}


def extract_result(person: dict, source_address: str) -> dict:
    """Extract key fields from a BatchData skip-trace person record."""

    # Core person fields
    name_full = person.get("name", {}).get("full", "")
    phones = person.get("phoneNumbers", [])
    emails = person.get("emails", [])
    mailing = person.get("mailingAddress", {})
    prop_addr = person.get("propertyAddress", {})
    meta = person.get("meta", {})

    # Nested property record (owner on deed)
    prop = person.get("property", {})
    owner = prop.get("owner", {})
    owner_name = owner.get("name", {}).get("full", "")
    owner_mailing = owner.get("mailingAddress", {})

    # Build phone string
    phone_strs = []
    for p in phones:
        num = p.get("number", "")
        ptype = p.get("type", "")
        reachable = p.get("reachable", "")
        phone_strs.append(f"{num} ({ptype})" if ptype else num)

    # Build email string
    email_str = ", ".join(emails) if emails else ""

    # Owner name priority: skip-trace name > property deed name
    final_owner = name_full or owner_name or ""

    return {
        "source_address": source_address,
        "owner_name": final_owner,
        "owner_street": mailing.get("street", "") or owner_mailing.get("street", ""),
        "owner_city": mailing.get("city", "") or owner_mailing.get("city", ""),
        "owner_state": mailing.get("state", "") or owner_mailing.get("state", ""),
        "owner_zip": mailing.get("zip", "") or owner_mailing.get("zip", ""),
        "owner_full_mailing": (
            f"{mailing.get('street','')} {mailing.get('city','')} "
            f"{mailing.get('state','')} {mailing.get('zip','')}".strip()
        ) or (
            f"{owner_mailing.get('street','')} {owner_mailing.get('city','')} "
            f"{owner_mailing.get('state','')} {owner_mailing.get('zip','')}".strip()
        ),
        "phones": "; ".join(phone_strs),
        "emails": email_str,
        "property_street": prop_addr.get("street", ""),
        "property_city": prop_addr.get("city", ""),
        "property_state": prop_addr.get("state", ""),
        "property_zip": prop_addr.get("zip", ""),
        "match_error": meta.get("errorMessage", ""),
        # These fields only available via /property/search, not skip-trace
        "estimated_value": "",
        "equity": "",
        "ltv_pct": "",
        "open_liens": "",
        "lien_balance": "",
        "owner_occupied": "",
        "absentee_owner": "",
        "free_and_clear": "",
        "bedrooms": "",
        "bathrooms": "",
        "year_built": "",
        "property_type": "",
        "last_sale_price": "",
        "last_sale_date": "",
    }


def is_csv_file(path_or_address: str) -> bool:
    """Return True if input looks like a CSV file path."""
    p = Path(path_or_address)
    return p.exists() and p.suffix.lower() in (".csv", ".txt")


def read_addresses_from_csv(csv_path: str) -> list:
    """Read addresses from CSV. Supports 'address' column or street,city,state,zip columns."""
    addresses = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if "address" in row and row["address"].strip():
                addresses.append(row["address"].strip())
            else:
                street = row.get("street", "").strip()
                city = row.get("city", "").strip()
                state = row.get("state", "").strip()
                zipcode = row.get("zip", row.get("zipcode", "")).strip()
                if street:
                    addr = f"{street}, {city}, {state} {zipcode}".strip(", ")
                    addresses.append(addr)
    return addresses


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 batchdata_lookup.py <address_or_csv_path>")
        sys.exit(1)

    api_key = load_api_key()
    if not api_key:
        print("ERROR: No BatchData API key found. Set BATCHDATA_API_KEY env var or add to ~/.secrets/batchdata.env", file=sys.stderr)
        sys.exit(1)

    arg = sys.argv[1]

    if is_csv_file(arg):
        addresses = read_addresses_from_csv(arg)
        print(f"Loaded {len(addresses)} addresses from CSV")
    else:
        addresses = [arg]

    results = []
    total = len(addresses)
    matched = 0

    for i, addr in enumerate(addresses, 1):
        print(f"[{i}/{total}] Looking up: {addr}")
        person = lookup_address(api_key, addr)
        if person:
            matched += 1
            row = extract_result(person, addr)
            row["match_status"] = "MATCH"
        else:
            row = {"source_address": addr, "match_status": "NO_MATCH"}
            for key in [
                "owner_name","owner_street","owner_city","owner_state","owner_zip",
                "owner_full_mailing","phones","emails",
                "property_street","property_city","property_state","property_zip",
                "match_error","estimated_value","equity","ltv_pct","open_liens",
                "lien_balance","owner_occupied","absentee_owner","free_and_clear",
                "bedrooms","bathrooms","year_built","property_type",
                "last_sale_price","last_sale_date"
            ]:
                row.setdefault(key, "")
        results.append(row)
        time.sleep(0.25)  # rate limit guard

    # Write results CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_path = Path(__file__).parent / f"skip_trace_results_{timestamp}.csv"
    fieldnames = [
        "source_address","match_status","owner_name",
        "owner_street","owner_city","owner_state","owner_zip","owner_full_mailing",
        "phones","emails",
        "property_street","property_city","property_state","property_zip",
        "match_error",
        "estimated_value","equity","ltv_pct","open_liens","lien_balance",
        "owner_occupied","absentee_owner","free_and_clear",
        "bedrooms","bathrooms","year_built","property_type",
        "last_sale_price","last_sale_date",
    ]

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n=== Done ===")
    print(f"Total: {total} | Matched: {matched} | No Match: {total - matched}")
    print(f"Results saved to: {output_path}")


if __name__ == "__main__":
    main()
