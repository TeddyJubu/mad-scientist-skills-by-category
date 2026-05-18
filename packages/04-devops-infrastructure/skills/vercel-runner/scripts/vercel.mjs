#!/usr/bin/env node
// Vercel Runner - REST API wrapper
// Commands:
//  projects list
//  projects info --id <projectId>
//  deploy list --project <projectId> [--limit 10]
//  deploy latest --project <projectId>
//  deploy redeploy --deployment <deploymentId>

import fs from 'node:fs';
import path from 'node:path';

const API = 'https://api.vercel.com';

function parseArgs() {
  const a = process.argv.slice(2);
  const out = { _: [] };
  for (let i = 0; i < a.length; i++) {
    const t = a[i];
    if (t.startsWith('--')) {
      const k = t.slice(2);
      const v = (i + 1 < a.length && !a[i + 1].startsWith('--')) ? a[++i] : true;
      out[k] = v;
    } else out._.push(t);
  }
  return out;
}

function loadToken() {
  const candidates = [
    '/data/.openclaw/workspace/.secrets/vercel.env',
    path.join(process.cwd(), '.secrets/vercel.env'),
    path.join(process.cwd(), '..', '.secrets/vercel.env'),
  ];
  for (const p of candidates) {
    try {
      if (fs.existsSync(p)) {
        const txt = fs.readFileSync(p, 'utf8');
        let token = null, team = null;
        for (const line of txt.split(/\r?\n/)) {
          const m1 = line.match(/^\s*VERCEL_TOKEN\s*=\s*(.+)\s*$/);
          const m2 = line.match(/^\s*VERCEL_TEAM_ID\s*=\s*(.+)\s*$/);
          if (m1) token = m1[1].trim();
          if (m2) team = m2[1].trim();
        }
        if (token) return { token, teamId: team || process.env.VERCEL_TEAM_ID || null };
      }
    } catch {}
  }
  return { token: process.env.VERCEL_TOKEN || null, teamId: process.env.VERCEL_TEAM_ID || null };
}

async function http(method, url, { token, teamId, data } = {}) {
  const h = { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' };
  const u = new URL(url);
  if (teamId) u.searchParams.set('teamId', teamId);
  const res = await fetch(u.toString(), { method, headers: h, body: data ? JSON.stringify(data) : undefined });
  const text = await res.text();
  if (!res.ok) throw new Error(`HTTP ${res.status}: ${text}`);
  try { return JSON.parse(text); } catch { return text; }
}

async function cmd_projects(argv, auth) {
  const sub = argv._[1];
  if (sub === 'list') {
    const out = await http('GET', `${API}/v9/projects?limit=100`, auth);
    return console.log(JSON.stringify({ ok: true, projects: out.projects || [] }, null, 2));
  }
  if (sub === 'info') {
    const id = argv.id; if (!id) throw new Error('--id is required');
    const proj = await http('GET', `${API}/v9/projects/${id}`, auth);
    let domains = [];
    try {
      const dom = await http('GET', `${API}/v10/projects/${id}/domains`, auth);
      domains = dom.domains?.map(d => d.name) || [];
    } catch {}
    // latest production deployment
    let latest = null;
    try {
      const deps = await http('GET', `${API}/v13/deployments?projectId=${id}&target=production&state=READY&limit=1`, auth);
      const url = deps.deployments?.[0]?.url ? `https://${deps.deployments[0].url}` : null;
      latest = url;
    } catch {}
    return console.log(JSON.stringify({ ok: true, project: proj, domains, latestProduction: latest }, null, 2));
  }
  throw new Error('projects subcommands: list|info');
}

async function cmd_deploy(argv, auth) {
  const sub = argv._[1];
  if (sub === 'list') {
    const pid = argv.project; if (!pid) throw new Error('--project is required');
    const limit = Number(argv.limit || 10);
    const out = await http('GET', `${API}/v13/deployments?projectId=${pid}&limit=${limit}`, auth);
    return console.log(JSON.stringify({ ok: true, ...out }, null, 2));
  }
  if (sub === 'latest') {
    const pid = argv.project; if (!pid) throw new Error('--project is required');
    const deps = await http('GET', `${API}/v13/deployments?projectId=${pid}&target=production&state=READY&limit=1`, auth);
    const url = deps.deployments?.[0]?.url ? `https://${deps.deployments[0].url}` : null;
    return console.log(JSON.stringify({ ok: true, url, deployment: deps.deployments?.[0] || null }, null, 2));
  }
  if (sub === 'redeploy') {
    const depId = argv.deployment; if (!depId) throw new Error('--deployment is required');
    const out = await http('POST', `${API}/v13/deployments/${depId}/redeploy`, auth);
    return console.log(JSON.stringify({ ok: true, data: out }, null, 2));
  }
  throw new Error('deploy subcommands: list|latest|redeploy');
}

async function main() {
  const argv = parseArgs();
  const cmd = argv._[0];
  const auth = loadToken();
  if (!auth.token) {
    console.error('Missing VERCEL_TOKEN. Put it in .secrets/vercel.env or env.');
    process.exit(2);
  }
  try {
    if (cmd === 'projects') return await cmd_projects(argv, auth);
    if (cmd === 'deploy') return await cmd_deploy(argv, auth);
    console.log(`Usage:
  projects list
  projects info --id <projectId>
  deploy list --project <projectId> [--limit 10]
  deploy latest --project <projectId>
  deploy redeploy --deployment <deploymentId>
`);
    process.exit(1);
  } catch (err) {
    console.error(JSON.stringify({ ok: false, error: String(err.message || err) }));
    process.exit(1);
  }
}

main();
