#!/usr/bin/env node
/**
 * List all taps for the authenticated organization.
 * Returns tap IDs, names, tokens, and metadata.
 */

const fs = require('fs');
const path = require('path');

// Load API key from .secrets/firehose.env
const envPath = path.join(process.env.HOME, '.openclaw', 'workspace', '.secrets', 'firehose.env');
const envContent = fs.readFileSync(envPath, 'utf-8');
const FIREHOSE_MANAGEMENT_KEY = envContent.match(/FIREHOSE_MANAGEMENT_KEY=(.+)/)?.[1]?.trim();

if (!FIREHOSE_MANAGEMENT_KEY) {
  console.error('❌ FIREHOSE_MANAGEMENT_KEY not found in .secrets/firehose.env');
  process.exit(1);
}

const BASE_URL = 'https://api.firehose.com';

async function listTaps() {
  const response = await fetch(`${BASE_URL}/v1/taps`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${FIREHOSE_MANAGEMENT_KEY}`
    }
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Failed to list taps: ${response.status} ${error}`);
  }

  const result = await response.json();
  return result.data;
}

(async () => {
  try {
    const taps = await listTaps();

    if (taps.length === 0) {
      console.log('No taps found. Create one with create-tap.js.');
      return;
    }

    console.log(`\n✅ Found ${taps.length} tap(s):\n`);
    taps.forEach((tap, i) => {
      console.log(`${i + 1}. ${tap.name}`);
      console.log(`   ID: ${tap.id}`);
      console.log(`   Token: ${tap.token}`);
      console.log(`   Rules: ${tap.rules_count}`);
      console.log(`   Last Used: ${tap.last_used_at || 'Never'}`);
      console.log(`   Created: ${tap.created_at}`);
      console.log('');
    });
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
})();
