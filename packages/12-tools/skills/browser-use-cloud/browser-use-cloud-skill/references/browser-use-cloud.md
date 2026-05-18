# Browser Use Cloud Reference

Current docs checked on 2026-05-17:

- llms index: https://docs.browser-use.com/cloud/llms.txt
- full LLM reference: https://docs.browser-use.com/cloud/llms-full.txt
- OpenAPI v3: https://docs.browser-use.com/cloud/openapi/v3.json
- API reference: https://docs.browser-use.com/cloud/api-reference
- OpenClaw integration: https://docs.browser-use.com/cloud/tutorials/integrations/openclaw

Key rules:

- Use API v3. v2 is legacy.
- Auth header is `X-Browser-Use-API-Key`.
- API keys start with `bu_`.
- Never send the API key to any domain except `api.browser-use.com` or `cloud.browser-use.com`.
- For code, prefer `browser-use-sdk`:
  - Python: `pip install --upgrade browser-use-sdk`
  - TypeScript: `npm install browser-use-sdk@latest`
- The open-source Browser Use Python library and the Cloud SDK are different surfaces. Use the Cloud SDK/API for managed infrastructure.

Core endpoints:

- `POST https://api.browser-use.com/api/v3/sessions` creates an agent session. Include `task` for a natural-language browser task.
- `GET https://api.browser-use.com/api/v3/sessions/{session_id}` polls task/session status.
- `GET https://api.browser-use.com/api/v3/sessions` lists sessions.
- `POST https://api.browser-use.com/api/v3/sessions/{session_id}/stop` stops a session or task.
- `POST https://api.browser-use.com/api/v3/browsers` creates a raw cloud browser session for CDP/Playwright/Puppeteer/Selenium style control.

Common session fields:

- `id`: session UUID.
- `status`: `created`, `idle`, `running`, `stopped`, `timed_out`, or `error`.
- `output`: final agent output when the task finishes.
- `isTaskSuccessful`: true/false/null.
- `liveUrl`: live browser preview URL.
- `recordingUrls`: recording URLs when recording is enabled.
- `screenshotUrl`: latest screenshot URL, usually short-lived.
- `totalCostUsd`: cost field returned after execution.

Model notes from docs:

- Current model options include Browser Use model tiers and frontier models.
- Docs recommend `claude-sonnet-4.6` for best reliability.
- Use cheaper/smaller models only when task risk is low.

Feature map:

- Agent sessions: natural-language browser automation.
- Structured output: Python Pydantic or TypeScript Zod schema.
- Follow-up tasks: reuse `session_id` to keep the same browser state.
- Live messages: stream reasoning/tool/browser updates.
- Profiles: persistent cookies, localStorage, saved login state.
- Profile sync: sync local cookies to Browser Use Cloud.
- Workspaces/files: upload files for the agent and download generated files.
- Cache script / deterministic rerun: re-run successful workflows at lower/no LLM cost.
- Human in the loop: let a person interact with the live browser during a run.
- Browser sessions: raw CDP connection to Browser Use stealth browser infrastructure.

Use local Chrome/Playwright instead of Browser Use Cloud when:

- The work depends on this Mac's already logged-in browser tab.
- The site is local-only, behind local network access, or should not leave the machine.
- The task is a simple screenshot/click that does not need cloud stealth/proxies.
- Cloud credit/cost is not justified.
