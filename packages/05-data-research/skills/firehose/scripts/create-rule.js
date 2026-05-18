#!/usr/bin/env node
/**
 * Create a rule for a tap.
 * Usage: node create-rule.js <tap-token> "lucene query" ["tag"] [--nsfw] [--no-quality]
 */

const tapToken = process.argv[2];
const query = process.argv[3];
const tag = process.argv[4] && !process.argv[4].startsWith('--') ? process.argv[4] : undefined;
const nsfw = process.argv.includes('--nsfw');
const quality = !process.argv.includes('--no-quality');

if (!tapToken || !query) {
  console.error('Usage: node create-rule.js <tap-token> "lucene query" ["tag"] [--nsfw] [--no-quality]');
  process.exit(1);
}

const BASE_URL = 'https://api.firehose.com';

async function createRule(value, tag, nsfw, quality) {
  const body = { value };
  if (tag) body.tag = tag;
  body.nsfw = nsfw;
  body.quality = quality;

  const response = await fetch(`${BASE_URL}/v1/rules`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${tapToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Failed to create rule: ${response.status} ${error}`);
  }

  return await response.json();
}

(async () => {
  try {
    const result = await createRule(query, tag, nsfw, quality);
    console.log(`\n✅ Rule created:`);
    console.log(`   ID: ${result.data.id}`);
    console.log(`   Query: ${result.data.value}`);
    if (result.data.tag) console.log(`   Tag: ${result.data.tag}`);
    console.log('');
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
})();
