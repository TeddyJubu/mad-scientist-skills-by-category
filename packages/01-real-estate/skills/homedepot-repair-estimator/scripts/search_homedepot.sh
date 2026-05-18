#!/bin/bash
# Search Home Depot via SerpApi and return top products

SEARCH_TERM="$1"
API_KEY="c95610d06d056fec9501ee90ace7f39d256f7323eb359de4113dd3fab0e398b8"

if [ -z "$SEARCH_TERM" ]; then
  echo "Usage: $0 <search_term>"
  exit 1
fi

# URL encode the search term
ENCODED_TERM=$(echo "$SEARCH_TERM" | sed 's/ /%20/g')

# Make API request
curl -s "https://serpapi.com/search.json?engine=home_depot&q=${ENCODED_TERM}&api_key=${API_KEY}&ps=5&country=us" \
  | jq '.products[] | {title, brand, model_number, price, link}'
