#!/usr/bin/env node
/**
 * Stream matching pages from Firehose (Server-Sent Events).
 * Usage: node stream.js <tap-token> [--since 1h] [--limit 10] [--timeout 60]
 */

const tapToken = process.argv[2];

if (!tapToken) {
  console.error('Usage: node stream.js <tap-token> [--since 1h] [--limit 10] [--timeout 60]');
  process.exit(1);
}

const sinceIndex = process.argv.indexOf('--since');
const limitIndex = process.argv.indexOf('--limit');
const timeoutIndex = process.argv.indexOf('--timeout');

const since = sinceIndex !== -1 ? process.argv[sinceIndex + 1] : undefined;
const limit = limitIndex !== -1 ? parseInt(process.argv[limitIndex + 1], 10) : undefined;
const timeout = timeoutIndex !== -1 ? parseInt(process.argv[timeoutIndex + 1], 10) : 300;

const BASE_URL = 'https://api.firehose.com';

async function stream() {
  const params = new URLSearchParams();
  if (since) params.append('since', since);
  if (limit) params.append('limit', limit);
  params.append('timeout', timeout);

  const url = `${BASE_URL}/v1/stream?${params.toString()}`;

  console.log(`\n🔥 Streaming from Firehose... (timeout: ${timeout}s)\n`);

  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${tapToken}`,
      'Accept': 'text/event-stream'
    }
  });

  if (!response.ok) {
    const error = await response.text();
    throw new Error(`Failed to stream: ${response.status} ${error}`);
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });
    const lines = buffer.split('\n');
    buffer = lines.pop(); // keep incomplete line in buffer

    for (const line of lines) {
      if (line.startsWith('event:')) {
        const eventType = line.substring(6).trim();
        console.log(`\n📡 Event: ${eventType}`);
      } else if (line.startsWith('data:')) {
        const data = line.substring(5).trim();
        if (data && data !== '[]') {
          try {
            const json = JSON.parse(data);
            if (json.document) {
              console.log(`\n✅ Match:`);
              console.log(`   URL: ${json.document.url}`);
              console.log(`   Title: ${json.document.title || 'N/A'}`);
              console.log(`   Language: ${json.document.language || 'N/A'}`);
              console.log(`   Categories: ${json.document.page_category?.join(', ') || 'N/A'}`);
              console.log(`   Types: ${json.document.page_types?.join(', ') || 'N/A'}`);
              console.log(`   Query ID: ${json.query_id}`);
              console.log(`   Matched At: ${json.matched_at}`);
              if (json.document.diff) {
                console.log(`   Diff Chunks: ${json.document.diff.chunks.length}`);
              }
              console.log('');
            } else if (json.message) {
              console.log(`   Message: ${json.message}`);
            }
          } catch (e) {
            // not JSON, skip
          }
        }
      }
    }
  }

  console.log('\n🔥 Stream closed.\n');
}

(async () => {
  try {
    await stream();
  } catch (error) {
    console.error('❌ Error:', error.message);
    process.exit(1);
  }
})();
