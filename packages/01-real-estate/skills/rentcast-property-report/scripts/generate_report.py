#!/usr/bin/env python3.11
import argparse
import requests
import json

API_BASE_URL = "https://api.rentcast.io/v1"

def get_property_details(api_key, address):
    """Fetches detailed property records from Rentcast."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/properties",
            headers={"X-Api-Key": api_key, "accept": "application/json"},
            params={"address": address, "limit": 1}
        )
        response.raise_for_status()
        data = response.json()
        return data[0] if data else None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching property details: {e}")
        return None

def get_value_estimate(api_key, address):
    """Fetches the AVM value estimate and sales comparables."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/avm/value",
            headers={"X-Api-Key": api_key, "accept": "application/json"},
            params={"address": address}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching value estimate: {e}")
        return None

def get_rent_estimate(api_key, address):
    """Fetches the long-term rent estimate and rental comparables."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/avm/rent/long-term",
            headers={"X-Api-Key": api_key, "accept": "application/json"},
            params={"address": address}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching rent estimate: {e}")
        return None

def get_market_stats(api_key, zip_code):
    """Fetches market statistics for a given zip code."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/markets",
            headers={"X-Api-Key": api_key, "accept": "application/json"},
            params={"zipCode": zip_code}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching market stats: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate a comprehensive property report using the Rentcast API.")
    parser.add_argument("--api-key", required=True, help="Your Rentcast API key.")
    parser.add_argument("--address", required=True, help="The full property address.")
    args = parser.parse_args()

    print(f"--- Generating Report for: {args.address} ---")

    # 1. Get Property Details
    property_data = get_property_details(args.api_key, args.address)
    if not property_data:
        print("Could not retrieve property data. Aborting.")
        return
    print("\n--- Property Details ---")
    print(json.dumps(property_data, indent=2))

    # 2. Get Value Estimate
    value_estimate = get_value_estimate(args.api_key, args.address)
    if value_estimate:
        print("\n--- Value Estimate ---")
        print(json.dumps(value_estimate, indent=2))

    # 3. Get Rent Estimate
    rent_estimate = get_rent_estimate(args.api_key, args.address)
    if rent_estimate:
        print("\n--- Rent Estimate ---")
        print(json.dumps(rent_estimate, indent=2))

    # 4. Get Market Stats
    zip_code = property_data.get("zipCode")
    if zip_code:
        market_stats = get_market_stats(args.api_key, zip_code)
        if market_stats:
            print(f"\n--- Market Statistics for {zip_code} ---")
            print(json.dumps(market_stats, indent=2))

if __name__ == "__main__":
    main()
