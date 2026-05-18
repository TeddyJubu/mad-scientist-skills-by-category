#!/usr/bin/env node

/**
 * Census Data API Query Runner
 * Fetch demographic, economic, and population data from the U.S. Census Bureau API.
 * 
 * Usage:
 *   ./run-census-query.js --dataset acs/acs5 --year 2021 --variables NAME,B01003_001E --for "state:*"
 *   ./run-census-query.js --url "https://api.census.gov/data/2021/acs/acs5?get=NAME,B01003_001E&for=state:*"
 *   ./run-census-query.js --query "population by state 2021"
 */

import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Load API key from .secrets/census.env
function loadApiKey() {
  const envPath = path.join(__dirname, '.secrets', 'census.env');
  if (!fs.existsSync(envPath)) {
    console.error('❌ API key not found. Expected at:', envPath);
    process.exit(1);
  }
  const envContent = fs.readFileSync(envPath, 'utf-8');
  const match = envContent.match(/CENSUS_API_KEY=(.+)/);
  if (!match) {
    console.error('❌ CENSUS_API_KEY not found in .secrets/census.env');
    process.exit(1);
  }
  return match[1].trim();
}

// Parse command-line arguments
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    dataset: null,
    year: null,
    variables: null,
    for: null,
    in: null,
    predicates: {},
    url: null,
    query: null,
    output: null,
    format: 'json',
    descriptive: false,
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const next = args[i + 1];

    if (arg === '--dataset' && next) {
      options.dataset = next;
      i++;
    } else if (arg === '--year' && next) {
      options.year = next;
      i++;
    } else if (arg === '--variables' && next) {
      options.variables = next;
      i++;
    } else if (arg === '--for' && next) {
      options.for = next;
      i++;
    } else if (arg === '--in' && next) {
      options.in = next;
      i++;
    } else if (arg === '--url' && next) {
      options.url = next;
      i++;
    } else if (arg === '--query' && next) {
      options.query = next;
      i++;
    } else if (arg === '--output' && next) {
      options.output = next;
      i++;
    } else if (arg === '--format' && next) {
      options.format = next;
      i++;
    } else if (arg === '--descriptive') {
      options.descriptive = true;
    } else if (arg.startsWith('--') && next) {
      // Additional predicates (e.g., --AGEGROUP 0)
      const predicate = arg.replace('--', '');
      options.predicates[predicate] = next;
      i++;
    }
  }

  return options;
}

// Build Census API URL from structured options
function buildUrl(options, apiKey) {
  if (options.url) {
    // Direct URL provided
    const separator = options.url.includes('?') ? '&' : '?';
    return `${options.url}${separator}key=${apiKey}`;
  }

  if (!options.dataset || !options.year || !options.variables) {
    console.error('❌ Missing required parameters: --dataset, --year, --variables (or use --url or --query)');
    process.exit(1);
  }

  let url = `https://api.census.gov/data/${options.year}/${options.dataset}?get=${options.variables}`;

  // Add geography predicates
  if (options.for) {
    url += `&for=${encodeURIComponent(options.for)}`;
  }
  if (options.in) {
    url += `&in=${encodeURIComponent(options.in)}`;
  }

  // Add custom predicates
  for (const [key, value] of Object.entries(options.predicates)) {
    url += `&${key}=${encodeURIComponent(value)}`;
  }

  // Add output format
  if (options.format === 'csv') {
    url += '&outputFormat=csv';
  }

  // Add descriptive labels
  if (options.descriptive) {
    url += '&descriptive=true';
  }

  // Add API key
  url += `&key=${apiKey}`;

  return url;
}

// Execute Census API request
async function executeQuery(url) {
  console.log('\n🔍 Querying Census API...');
  console.log(`📍 URL: ${url.replace(/key=[^&]+/, 'key=***')}\n`);

  try {
    const response = await fetch(url);

    if (!response.ok) {
      const errorText = await response.text();
      console.error(`❌ API Error (${response.status}):`, errorText);
      process.exit(1);
    }

    const contentType = response.headers.get('content-type');

    if (contentType.includes('application/json')) {
      return await response.json();
    } else if (contentType.includes('text/csv')) {
      return await response.text();
    } else {
      return await response.text();
    }
  } catch (error) {
    console.error('❌ Network error:', error.message);
    process.exit(1);
  }
}

// Format JSON response as markdown table
function formatJsonResponse(data) {
  if (!Array.isArray(data) || data.length === 0) {
    return '❌ No data returned.';
  }

  const headers = data[0];
  const rows = data.slice(1);

  let markdown = '\n## Results\n\n';
  markdown += `| ${headers.join(' | ')} |\n`;
  markdown += `| ${headers.map(() => '---').join(' | ')} |\n`;

  for (const row of rows) {
    markdown += `| ${row.join(' | ')} |\n`;
  }

  markdown += `\n**Total rows**: ${rows.length}\n`;

  return markdown;
}

// Save output to file
function saveOutput(data, filename, format) {
  let content;

  if (format === 'json') {
    content = JSON.stringify(data, null, 2);
  } else if (format === 'csv') {
    content = data;
  } else {
    content = data;
  }

  fs.writeFileSync(filename, content, 'utf-8');
  console.log(`\n✅ Saved to: ${filename}`);
}

// Main execution
async function main() {
  const options = parseArgs();
  const apiKey = loadApiKey();

  if (options.query) {
    console.log('🤖 Natural language query interpretation not yet implemented.');
    console.log('💡 Use structured flags (--dataset, --year, --variables, --for) or --url for now.');
    process.exit(0);
  }

  const url = buildUrl(options, apiKey);
  const data = await executeQuery(url);

  // Display results
  if (typeof data === 'string') {
    // CSV or plain text
    console.log('\n' + data);
  } else if (Array.isArray(data)) {
    // JSON array (standard Census format)
    console.log(formatJsonResponse(data));
  } else {
    // Other JSON
    console.log('\n' + JSON.stringify(data, null, 2));
  }

  // Save to file if requested
  if (options.output) {
    const outputFormat = options.format === 'csv' || typeof data === 'string' ? 'csv' : 'json';
    saveOutput(data, options.output, outputFormat);
  }

  console.log('\n✅ Query complete.\n');
}

main();
