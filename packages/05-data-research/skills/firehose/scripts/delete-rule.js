#!/usr/bin/env node
/**
 * Delete a rule.
 * Usage: node delete-rule.js <tap-token> <rule-id>
 */

const tapToken = process.argv[2];
const ruleId = process.argv[3];

if (!tapToken || !ruleId) {
  console.error('Usage: node delete-rule.js <tap-token> <rule-id>');
  process.exit(1);
}

const BASE_URL = 'https://api.firehose.com';

async function deleteRule(ruleId) {
  const response = await fetch(`${BASE_URL}/v1/rules/${ruleId}`, {
    method: 'DELETE',
    headers: {
      'Authorization': `Bearer ${tapToken}`
    }
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Failed to delete rule: ${response.status} ${error}`);
  }
}

(async () => {
  try {
    await deleteRule(ruleId);
    console.log(`\n✅ Rule ${ruleId} deleted.\n`);
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
})();
