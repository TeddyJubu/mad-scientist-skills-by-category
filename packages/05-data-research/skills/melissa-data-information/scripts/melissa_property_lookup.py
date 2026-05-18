#!/usr/bin/env python3.11
import argparse
import csv
import requests
import sys

# The base URL for the Melissa Property API.
API_BASE_URL = "https://property.melissadata.net/v4/WEB/LookupProperty"

def lookup_property(license_key, address):
    """Looks up a single property by address."""
    params = {
        "id": license_key,
        "ff": address,
        "format": "json",
        "cols": "GrpAll",
    }
    try:
        response = requests.get(API_BASE_URL, params=params)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error calling Melissa API: {e}", file=sys.stderr)
        return None

def process_csv(license_key, input_file, output_file, address_column):
    """Processes a CSV file of addresses and writes the results to a new CSV."""
    try:
        with open(input_file, "r", newline="") as infile, \
             open(output_file, "w", newline="") as outfile:
            reader = csv.DictReader(infile)
            writer = None

            for row in reader:
                address = row.get(address_column)
                if not address:
                    print(f"Skipping row with missing address in column '{address_column}'", file=sys.stderr)
                    continue

                result = lookup_property(license_key, address)
                if result and result.get("Records"):
                    # Get the first record
                    record = result["Records"][0]

                    if writer is None:
                        # Initialize writer with all possible fields from the first record
                        fieldnames = list(record.keys())
                        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                        writer.writeheader()

                    writer.writerow(record)
                else:
                    print(f"No results found for address: {address}", file=sys.stderr)

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_file}'", file=sys.stderr)
    except Exception as e:
        print(f"An error occurred during CSV processing: {e}", file=sys.stderr)

def main():
    parser = argparse.ArgumentParser(description="Melissa Data Property API Lookup")
    parser.add_argument("--license-key", required=True, help="Your Melissa Data license key.")
    parser.add_argument("--address", help="A single address to look up.")
    parser.add_argument("--input-csv", help="Path to the input CSV file.")
    parser.add_argument("--output-csv", default="output.csv", help="Path to the output CSV file.")
    parser.add_argument("--address-column", default="address", help="The name of the column containing addresses in the input CSV.")

    args = parser.parse_args()

    if args.address:
        result = lookup_property(args.license_key, args.address)
        if result:
            print(result)
    elif args.input_csv:
        process_csv(args.license_key, args.input_csv, args.output_csv, args.address_column)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
