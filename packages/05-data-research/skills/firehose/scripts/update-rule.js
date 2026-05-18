#!/usr/bin/env node
/**
 * Update a rule.
 * Usage: node update-rule.js <tap-token> <rule-id> ["new query"] ["new tag"] [--nsfw] [--no-quality]
 */

const tapToken = process.argv[2];
const ruleId = process.argv[3];
const newQuery = process.argv[4] && !process.argv[4].startsWith('--') ? process.argv[4] : undefined;
const newTag = process.argv[5] && !process.argv[5].startsWith('--') ? process.argv[5] : undefined;
const nsfw = process.argv.includes('--nsfw') ? true : undefined;
const quality = process.argv.includes('--no-quality') ? false : undefined;

if (!tapToken || !ruleId) {
  console.error('Usage: node update-rule.js <tap-token> <rule-id> ["new query"] ["new tag"] [--nsfw] [--no-quality]');
  process.exit(1);
}

const BASE_URL = 'https://api.firehose.com';

async function updateRule(ruleId, updates) {
  const response = await fetch(`${BASE_URL}/v1/rules/${ruleId}`, {
    method: 'PUT',
    headers: {
      'Authorization': `Bearer ${tapToken}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(updates)
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Failed to update rule: ${response.status} ${error}`);
  }

  return await response.json();
}

(async () => {
  try {
    const updates = {};
    if (newQuery) updates.value = newQuery;
    if (newTag) updates.tag = newTag;
    if (nsfw !== undefined) updates.nsfw = nsfw;
    if (quality !== undefined) updates.quality = quality;

    const result = await updateRule(ruleId, updates);
    console.log(`\n✅ Rule updated:`);
    console.log(`   ID: ${result.data.id}`);
    console.log(`   Query: ${result.data.value}`);
    if (result.data.tag) console.log(`   Tag: ${result.data.tag}`);
    console.log('');
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
})();
