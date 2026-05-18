#!/usr/bin/env node
// MCP tool discovery via SSE
const http = require('http');
const https = require('https');
const { URL } = require('url');

const MCP_URL = 'https://mcp.zapier.com/api/v1/connect?token=ODAzNmQ3ZWYtMzI1YS00YTNhLTk0OTktMTM1NDUyZGQwM2Q0OktYVzFDV3BoaitFcEhER2gxN3FYSHdLMVIyWHlNM3d2a1J5YlNvRHNId3M9';

// We'll try a simple GET with proper headers first
const parsed = new URL(MCP_URL);
const opts = {
  hostname: parsed.hostname,
  path: parsed.pathname + parsed.search,
  headers: {
    'Accept': 'text/event-stream',
    'Cache-Control': 'no-cache'
  }
};

const req = https.get(opts, (res) => {
  console.log('Status:', res.statusCode);
  console.log('Headers:', JSON.stringify(res.headers, null, 2));
  
  res.setEncoding('utf8');
  res.on('data', (chunk) => {
    console.log('Chunk:', chunk);
  });
  
  req.setTimeout(10000, () => {
    console.log('\nTimeout after 10s - normal for SSE');
    req.destroy();
  });
});

req.on('error', (e) => {
  console.error('Error:', e.message);
});

console.log('Connecting to MCP...\n');