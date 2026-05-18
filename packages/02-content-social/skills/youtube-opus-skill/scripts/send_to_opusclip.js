#!/usr/bin/env node
/**
 * Send YouTube video to OpusClip via Zapier MCP
 * Returns: {"success": true, "videoUrl": "...", "clipUrl": "..."}
 */

const https = require('https');
const { URL } = require('url');

const TOKEN = 'ODAzNmQ3ZWYtMzI1YS00YTNhLTk0OTktMTM1NDUyZGQwM2Q0OktYVzFDV3BoaitFcEhER2gxN3FYSHdLMVIyWHlNM3d2a1J5YlNvRHNId3M9';
const MCP_RPC_ENDPOINT = 'https://mcp.zapier.com/api/v1/rpc';

const YOUTUBE_URL = process.argv[2];
if (!YOUTUBE_URL) {
  console.error(JSON.stringify({ error: "No YouTube URL provided" }));
  process.exit(1);
}

console.error('Processing:', YOUTUBE_URL);
console.error('Attempting direct RPC call to MCP...');

// Call tools/list via JSON-RPC
function listTools() {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      jsonrpc: '2.0',
      method: 'tools/list',
      id: 2
    });
    
    const url = new URL(`${MCP_RPC_ENDPOINT}?token=${TOKEN}`);
    
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
        try {
          const parsed = JSON.parse(data);
          if (parsed.error) {
            reject(new Error(parsed.error.message));
          } else {
            resolve(parsed.result?.tools || []);
          }
        } catch (e) {
          reject(new Error(`Invalid JSON for tools list: ${data}`));
        }
      });
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

// Call OpusClip tool
function callOpusClip(opusToolName, youtubeUrl) {
  return new Promise((resolve, reject) => {
    const payload = JSON.stringify({
      jsonrpc: '2.0',
      method: 'tools/call',
      params: {
        name: opusToolName,
        arguments: { video_url: youtubeUrl }
      },
      id: 3
    });
    
    const url = new URL(`${MCP_RPC_ENDPOINT}?token=${TOKEN}`);
    
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
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          resolve({ raw: data }); // Return raw if not JSON
        }
      });
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

// Main
async function main() {
  try {
    console.error('Discovering tools...');
    const tools = await listTools();
    
    // Find OpusClip tool (case-insensitive search)
    const opusTool = tools.find(t => 
      t.name?.toLowerCase().includes('opus') ||
      t.name?.toLowerCase().includes('clip')
    );
    
    if (!opusTool) {
      console.error('Available tools:', tools.map(t => t.name).join(', '));
      throw new Error('OpusClip tool not found in MCP tools');
    }
    
    console.error('Found OpusClip tool:', opusTool.name);
    
    // Call the tool
    const result = await callOpusClip(opusTool.name, YOUTUBE_URL);
    console.error('Tool call result:', JSON.stringify(result, null, 2));
    
    // Extract clip URL from result
    const clipUrl = result.result?.clip_url || 
                   result.result?.url || 
                   result.result?.project_url ||
                   result.result?.opus_url ||
                   null;
    
    console.log(JSON.stringify({
      success: true,
      videoUrl: YOUTUBE_URL,
      clipUrl: clipUrl,
      tool: opusTool.name,
      status: result.result?.status || 'processed',
      raw: result.result // Include raw result for debugging
    }));
    
  } catch (e) {
    console.error('Error:', e.message);
    console.log(JSON.stringify({ error: e.message }));
    process.exit(1);
  }
}

main();