#!/usr/bin/env node
/**
 * Create a new tap.
 * Usage: node create-tap.js "Tap Name"
 */

const fs = require('fs');
const path = require('path');

const tapName = process.argv[2];

if (!tapName) {
  console.error('Usage: node create-tap.js "Tap Name"');
  process.exit(1);
}

// Load API key
const envPath = path.join(process.env.HOME, '.openclaw', 'workspace', '.secrets', 'firehose.env');
const envContent = fs.readFileSync(envPath, 'utf-8');
const FIREHOSE_MANAGEMENT_KEY = envContent.match(/FIREHOSE_MANAGEMENT_KEY=(.+)/)?.[1]?.trim();

if (!FIREHOSE_MANAGEMENT_KEY) {
  console.error('❌ FIREHOSE_MANAGEMENT_KEY not found in .secrets/firehose.env');
  process.exit(1);
}

const BASE_URL = 'https://api.firehose.com';

async function createTap(name) {
  const response = await fetch(`${BASE_URL}/v1/taps`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${FIREHOSE_MANAGEMENT_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({ name })
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Failed to create tap: ${response.status} ${error}`);
  }

  return await response.json();
}

(async () => {
  try {
    const result = await createTap(tapName);
    console.log(`\n✅ Tap created: ${result.data.name}`);
    console.log(`   ID: ${result.data.id}`);
    console.log(`   Token: ${result.token}`);
    console.log(`\n💾 Store this token securely. Use it to create rules and stream.\n`);
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
})();
