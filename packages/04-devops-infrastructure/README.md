# DevOps & Infrastructure Skills
**Package:** `@mad-scientist/devops-infrastructure` | **6 Skills** | Version 1.0.0

---

## What This Package Does For You

This package helps you put things on the internet and keep them running safely. If you want to deploy a website, set up a server so it's accessible from anywhere, lock down specific ports so only you can access them, or connect your AI tools to the outside world — this package handles it.

You don't need to remember Linux commands or understand server jargon. Describe what you want in plain English and it gets built.

---

## Skills In This Package

### 1. Vercel Deploy
**What it does:** Takes a web project (a Next.js app, a static HTML site, a React project) and deploys it to Vercel — one of the fastest and most reliable hosting platforms. Your site gets a live URL in under 2 minutes.

**What to say:**  
> "Deploy this Next.js project to Vercel and give me the live URL"

**What you get:** A live website URL (like yourproject.vercel.app) and confirmation that it's live and working.

---

### 2. Vercel Site Deploy
**What it does:** A simplified version for deploying static websites — HTML, CSS, and JavaScript files that don't need a server. Faster setup, instant deployment.

**What to say:**  
> "I have a folder of HTML files I want to put online at a custom domain — deploy it for me"

**What you get:** A live static site at your URL, no server configuration needed.

---

### 3. Vercel Runner
**What it does:** Runs commands on your Vercel deployment — check logs, manage environment variables, trigger rebuilds, and monitor your deployed sites. Everything you used to do through the Vercel dashboard, now through AI.

**What to say:**  
> "Check the logs on my Vercel deployment from the last 24 hours and tell me if there were any errors"

**What you get:** A summary of your deployment logs, any errors highlighted, and recommendations if something is broken.

---

### 4. LB Vercel Skill
**What it does:** Load balancing and traffic routing for your Vercel deployments — makes sure your site stays fast and doesn't crash when you get a traffic spike. Automatically routes visitors to the nearest server.

**What to say:**  
> "Set up load balancing for my landing page so it can handle 10,000 visitors in an hour"

**What you get:** Your site configured with smart traffic routing, CDN acceleration, and DDoS protection.

---

### 5. Traefik Docker Deploy
**What it does:** Sets up Traefik — a reverse proxy and load balancer — in front of your Docker containers so your services are accessible from the internet through your own domain name, with automatic HTTPS.

**What to say:**  
> "I have 3 Docker containers running on my server — set up Traefik so I can access them at app1.mydomain.com, app2.mydomain.com"

**What you get:** All 3 services accessible via subdomains with valid SSL certificates, no manual Nginx config needed.

---

### 6. Systemd Port Reservation
**What it does:** Reserves specific ports on your Linux server so only a specific application can use them. Prevents the "port already in use" errors that happen when two programs fight over the same port.

**What to say:**  
> "Reserve port 3000 for my Node.js app so nothing else can accidentally use it"

**What you get:** Port 3000 permanently locked to your app, with a confirmation and instructions on how to restart the service.

---

## How To Use This Package

### Installation
```bash
npm install @mad-scientist/devops-infrastructure
```

Or symlink into your Hermes skills folder:
```bash
ln -s $(pwd)/skills ~/.hermes/skills/devops-infrastructure
```

### Quick Start
```
skill_view(name="vercel-deploy")
skill_view(name="traefik-docker-deploy")
skill_view(name="systemd-port-reservation")
```

---

## What To Expect

| Skill | Time to Result | Best For |
|-------|---------------|----------|
| Vercel Deploy | 1-2 minutes | Web app deployment |
| Vercel Site Deploy | 30-60 seconds | Static site hosting |
| Vercel Runner | 10-30 seconds | Manage deployed sites |
| LB Vercel Skill | 2-5 minutes | Traffic management |
| Traefik Docker Deploy | 5-10 minutes | Reverse proxy setup |
| Systemd Port Reservation | 1-2 minutes | Port conflict prevention |

---

## License

Proprietary — © 2026 Mad Scientist LLC. All rights reserved. Internal use only.
