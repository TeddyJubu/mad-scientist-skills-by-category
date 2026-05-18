#!/usr/bin/env python3
"""
search_actors.py - Search the Apify Store for actors matching a query.

Usage:
    python3.11 search_actors.py <api_key> <query> [--sort relevance|popularity] [--limit N]

Output:
    Prints a ranked list of matching actors with title, actor ID, description,
    user count, pricing model, and URL.
"""

import sys
import json
import argparse
import urllib.request
import urllib.parse


def search_actors(api_key: str, query: str, sort_by: str = "relevance", limit: int = 5) -> list:
    params = urllib.parse.urlencode({
        "search": query,
        "sortBy": sort_by,
        "limit": limit,
    })
    url = f"https://api.apify.com/v2/store?{params}"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    })
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read())
    return data.get("data", {}).get("items", [])


def format_actors(actors: list) -> str:
    lines = []
    for i, actor in enumerate(actors, 1):
        title = actor.get("title", "N/A")
        username = actor.get("username", "N/A")
        name = actor.get("name", "N/A")
        description = (actor.get("description") or "")[:200]
        stats = actor.get("stats", {})
        total_users = stats.get("totalUsers", 0)
        rating = actor.get("actorReviewRating")
        review_count = actor.get("actorReviewCount", 0)
        pricing = actor.get("currentPricingInfo", {}).get("pricingModel", "N/A")
        url = actor.get("url", f"https://apify.com/{username}/{name}")
        categories = ", ".join(actor.get("categories") or [])

        lines.append(f"#{i}. {title}")
        lines.append(f"   Actor ID : {username}/{name}")
        if categories:
            lines.append(f"   Category : {categories}")
        lines.append(f"   Users    : {total_users:,}")
        if rating:
            lines.append(f"   Rating   : {rating:.1f}/5 ({review_count} reviews)")
        lines.append(f"   Pricing  : {pricing}")
        lines.append(f"   Desc     : {description}")
        lines.append(f"   URL      : {url}")
        lines.append("")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Search Apify Store for actors.")
    parser.add_argument("api_key", help="Your Apify API key")
    parser.add_argument("query", help="Search query (e.g. 'Google Maps scraper')")
    parser.add_argument("--sort", default="relevance", choices=["relevance", "popularity"],
                        help="Sort results by relevance or popularity (default: relevance)")
    parser.add_argument("--limit", type=int, default=5,
                        help="Number of results to return (default: 5)")
    args = parser.parse_args()

    try:
        actors = search_actors(args.api_key, args.query, sort_by=args.sort, limit=args.limit)
    except Exception as e:
        print(f"Error searching Apify Store: {e}", file=sys.stderr)
        sys.exit(1)

    if not actors:
        print("No actors found for your query. Try different keywords.")
        sys.exit(0)

    print(f"Found {len(actors)} actor(s) for query: '{args.query}'\n")
    print(format_actors(actors))


if __name__ == "__main__":
    main()
