#!/usr/bin/env node
/**
 * Full MCP client for Zapier OpusClip integration
 * Handles SSE initialization and JSON-RPC calls
 */

const https = require('https');
const { URL } = require('url');

const TOKEN = 'ODAzNmQ3ZWYtMzI1YS00YTNhLTk0OTktMTM1NDUyZGQwM2Q0OktYVzFDV3BoaitFcEhER2gxN3FYSHdLMVIyWHlNM3d2a1J5YlNvRHNId3M9';
const YOUTUBE_URL = process.argv[2];

if (!YOUTUBE_URL) {
  console.error('{"error":"No YouTube URL provided"}');
  process.exit(1);
}

let messageEndpoint = null;
let sessionId = null;
let receivedInit = false;

// Connect to MCP SSE
const connectUrl = new URL(`https://mcp.zapier.com/api/v1/connect?token=${TOKEN}`);

const sseReq = https.get({
  hostname: connectUrl.hostname,
  path: connectUrl.pathname + connectUrl.search,
  headers: {
    'Accept': 'text/event-stream',
    'Cache-Control': 'no-cache'
  }
}, (res) => {
  if (res.statusCode !== 200) {
    console.error(`{"error":"SSE connection failed: ${res.statusCode}"}`);
    process.exit(1);
  }

  let eventBuffer = '';
  
  res.on('data', (chunk) => {
    eventBuffer += chunk.toString();
    const lines = eventBuffer.split('\r\n');
    eventBuffer = lines.pop();
    
    const events = [];
    let currentEvent = {};
    
    for (const line of lines) {
      if (line.startsWith('event:')) {
        currentEvent.event = line.slice(6).trim();
      } else if (line.startsWith('id:')) {
        currentEvent.id = line.slice(3).trim();
      } else if (line.startsWith('data:')) {
        if (!currentEvent.data) currentEvent.data = '';
        currentEvent.data += line.slice(5).trim();
      } else if (line === '' && currentEvent.data) {
        events.push(currentEvent);
        currentEvent = {};
      }
    }
    
    for (const event of events) {
      try {
        const data = JSON.parse(event.data);
        
        if (data.id === 1 && data.result) {
          messageEndpoint = data.result.http || data.result.sseUri;
          sessionId = data.result.sessionId;
          receivedInit = true;
          
          // Now call tools/list
          callJsonRpc('tools/list', {}, 2, (toolsResult) => {
            const tools = toolsResult?.tools || [];
            if (tools.length === 0) {
              console.error('{"error":"No tools available in MCP connection"}');
              process.exit(1);
            }
            
            const opusTool = tools.find(t => 
              t.name?.toLowerCase().includes('opus') ||
              t.name?.toLowerCase().includes('clip')
            ) || tools[0];
            
            // Call the tool
            callJsonRpc('tools/call', {
              name: opusTool.name,
              arguments: { video_url: YOUTUBE_URL }
            }, 3, (toolResult) => {
              const clipUrl = toolResult?.clip_url || 
                             toolResult?.url || 
                             toolResult?.project_url ||
                             toolResult?.data?.clip_url ||
                             null;
              
              console.log(JSON.stringify({
                success: true,
                videoUrl: YOUTUBE_URL,
                tool: opusTool.name,
                clipUrl: clipUrl,
                status: toolResult?.status || 'submitted',
                raw: toolResult
              }));
              
              sseReq.destroy();
              process.exit(0);
            });
          });
        }
        
        if (data.error) {
          console.error(JSON.stringify({ error: data.error.message }));
          sseReq.destroy();
          process.exit(1);
        }
      } catch (e) {
        console.error('Parse error:', e.message);
      }
    }
  });
});

function callJsonRpc(method, params, id, callback) {
  if (!messageEndpoint) {
    console.error('{"error":"No message endpoint available"}');
    process.exit(1);
  }
  
  const payload = JSON.stringify({
    jsonrpc: '2.0',
    method: method,
    params: params,
    id: id
  });
  
  const url = new URL(messageEndpoint);
  
  const req = https.request({
    hostname: url.hostname,
    port: url.port || 443,
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
          console.error(JSON.stringify({ error: parsed.error.message }));
          process.exit(1);
        }
        callback(parsed.result);
      } catch (e) {
        console.error(JSON.stringify({ error: 'Invalid JSON response', details: data }));
        process.exit(1);
      }
    });
  });
  
  req.on('error', (e) => {
    console.error(JSON.stringify({ error: e.message }));
    process.exit(1);
  });
  
  req.write(payload);
  req.end();
}

sseReq.on('error', (e) => {
  console.error(JSON.stringify({ error: e.message }));
  process.exit(1);
});

// Timeout after 15 seconds
setTimeout(() => {
  if (!receivedInit) {
    console.error('{"error":"Timeout waiting for MCP initialization"}');
    sseReq.destroy();
    process.exit(1);
  }
}, 15000);