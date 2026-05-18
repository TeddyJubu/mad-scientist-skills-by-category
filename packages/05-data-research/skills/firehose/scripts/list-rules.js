#!/usr/bin/env node
/**
 * List rules for a tap.
 * Usage: node list-rules.js <tap-token>
 */

const tapToken = process.argv[2];

if (!tapToken) {
  console.error('Usage: node list-rules.js <tap-token>');
  process.exit(1);
}

const BASE_URL = 'https://api.firehose.com';

async function listRules() {
  const response = await fetch(`${BASE_URL}/v1/rules`, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${tapToken}`
    }
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Failed to list rules: ${response.status} ${error}`);
  }

  return await response.json();
}

(async () => {
  try {
    const result = await listRules();
    const rules = result.data;

    if (rules.length === 0) {
      console.log('No rules found. Create one with create-rule.js.');
      return;
    }

    console.log(`\n✅ Found ${rules.length} rule(s):\n`);
    rules.forEach((rule, i) => {
      console.log(`${i + 1}. [${rule.id}] ${rule.value}`);
      if (rule.tag) console.log(`   Tag: ${rule.tag}`);
      console.log('');
    });
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
})();
