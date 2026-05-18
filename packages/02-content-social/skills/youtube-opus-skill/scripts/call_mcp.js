#!/usr/bin/env node
// Call MCP tools/list
const https = require('https');
const { URL } = require('url');

const TOKEN = 'ODAzNmQ3ZWYtMzI1YS00YTNhLTk0OTktMTM1NDUyZGQwM2Q0OktYVzFDV3BoaitFcEhER2gxN3FYSHdLMVIyWHlNM3d2a1J5YlNvRHNId3M9';
const BASE_URL = 'https://mcp.zapier.com/api/v1';

// First, establish SSE session to get message endpoint
function connectSSE() {
  return new Promise((resolve, reject) => {
    const url = `${BASE_URL}/connect?token=${encodeURIComponent(TOKEN)}`;
    const req = https.get(url, {
      headers: { 'Accept': 'text/event-stream' }
    }, (res) => {
      let body = '';
      res.on('data', (c) => { 
        body += c; 
        // Look for endpoint in first message
        const match = body.match(/data:\s*(.+)/);
        if (match) {
          try {
            const data = JSON.parse(match[1]);
            if (data.id === 1 && data.result?.sseUri) {
              req.destroy();
              resolve(data.result.sseUri);
            }
          } catch (e) {}
        }
      });
      
      setTimeout(() => {
        req.destroy();
        resolve(null);
      }, 5000);
    });
    req.on('error', reject);
  });
}

// Call tools/list via JSON-RPC
async function listTools() {
  try {
    console.log('Connecting to MCP...');
    const endpoint = await connectSSE().catch(() => `${BASE_URL}/rpc`);
    console.log('Endpoint:', endpoint || 'using default');
    
    const payload = JSON.stringify({
      jsonrpc: '2.0',
      method: 'tools/list',
      id: 1
    });
    
    const url = new URL(endpoint || `${BASE_URL}/rpc?token=${TOKEN}`);
    
    const req = https.request({
      hostname: url.hostname,
      path: url.pathname + url.search,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload)
      }
    }, (res) => {
      let data = '';
      res.on('data', c => data += c);
      res.on('end', () => {
        console.log('Response:');
        try {
          const parsed = JSON.parse(data);
          console.log(JSON.stringify(parsed, null, 2));
        } catch (e) {
          console.log(data);
        }
      });
    });
    
    req.on('error', (e) => { console.error('Error:', e.message); });
    req.write(payload);
    req.end();
    
  } catch (e) {
    console.error('Failed:', e.message);
  }
}

listTools();