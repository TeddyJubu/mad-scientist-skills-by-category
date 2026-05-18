# Agent Integrations

Use this when the skill is running inside ChatGPT/Codex, Hermes Agent, OpenClaw, Manus, Genspark, Claude, Gemini, Goose, Cursor, or another agent orchestrator.

## Non-Negotiable Router Rule

Always check for a native image-generation/editing tool before checking for `OPENAI_API_KEY`.

- If a native tool exists, use it for ordinary image work.
- If the user explicitly asked for the local CLI/API path, masks, local file control, or unattended automation, use `scripts/generate_image.py`.
- If neither native image generation nor CLI credentials are available, return a production prompt/spec instead of fabricating placeholder assets.
- Do not say “I cannot generate because there is no API key” until native image tools and orchestrator-provided image tools have been ruled out.

## Non-Technical User Contract

Do not reject incomplete user requests. Return one of these statuses:

- `ready`: enough information to generate.
- `ready_with_notes`: generation can proceed, but the handoff needs a disclosure, QA note, or editable-tool reminder.
- `needs_info`: critical details are missing for the stated purpose; ask plain-language questions or continue only as a clearly labeled draft/concept.
- `prompt_packet_only`: no image backend is available, but the user still receives a usable production prompt.

For missing rights, disclosure, platform, or fair-housing details, say what is needed and why. Example: "To make this safe for a live rental ad, I need confirmation that you own or have permission to edit the photo, and whether the flyer needs a virtual-staging or AI-edited disclosure."

## Shared Image Job Schema

Use this shape when passing work between ChatGPT, Hermes, OpenClaw, MCP tools, HTTP workers, or background agents:

```json
{
  "job_type": "generate | edit | mask_edit | composite | qa_only",
  "asset_type": "listing_photo | virtual_staging | exterior_day_to_dusk | youtube_thumbnail | flyer | social_ad | profile_header | concept_rendering",
  "domain": "real_estate",
  "purpose": "short user-facing purpose",
  "platform": "MLS | Zillow-style listing | YouTube | Instagram | Facebook ad | print flyer | web",
  "prompt": "production image prompt",
  "negative_or_invariants": "facts, geometry, legal, and quality constraints",
  "input_images": [
    {"path_or_id": "image identifier", "role": "base | style_reference | brand_reference | headshot | mask"}
  ],
  "exact_text": ["HOUSE FOR RENT", "$2,400 / month"],
  "size": "auto | 1536x1024 | 2048x1152 | 1024x1536",
  "quality": "auto | low | medium | high",
  "format": "png | jpeg | webp",
  "rights_confirmed": true,
  "real_estate_gate": {
    "use_type": "listing | agent_marketing | concept | internal_test",
    "source_rights_checked": true,
    "disclosure_needed": "virtually staged | concept rendering | none",
    "fair_housing_checked": true
  },
  "outputs": {
    "image_path_or_id": "",
    "manifest_path": "",
    "qa_summary": ""
  }
}
```

When `rights_confirmed` or required real-estate gate fields are missing for publishable listing, brokerage, rental-platform, or agent-marketing work, return `needs_info` with reminders instead of rejecting the job. For synthetic tests or fictional briefs, set `use_type=internal_test` and state that no third-party source image was used.

Validate a job packet before unattended execution:

```bash
python ./scripts/validate_agent_job.py \
  --file image-job.json --json
```

Adapters can use the JSON status instead of failing on exit codes. The validator exits `0` for parseable and incomplete packets; read `status`, `ready_to_execute`, and `reminders`.

## ChatGPT / Codex Native Mode

Use this mode when the model has a built-in image-generation tool.

Workflow:

1. Load this skill and the relevant real-estate/marketing reference.
2. Build the production prompt and QA criteria.
3. Call the native image tool directly. Do not run the CLI script just to see whether `OPENAI_API_KEY` exists.
4. Show the generated image inline when the environment supports it.
5. If the output is project-bound, copy the generated bitmap from the platform's generated-images folder into the workspace; preserve the original.
6. Report the backend as `ChatGPT/Codex native image tool`, plus prompt summary, asset metadata, and QA notes.

Use the CLI script from ChatGPT/Codex only when the user explicitly asks for API/script behavior, needs masks/local file path control, or the native image tool is unavailable.

## Generic Agent Adapter

Use this for Manus, Genspark, Claude, Gemini, Perplexity-style research agents, browser agents, and any platform whose exact tool API may vary.

Agent requirements:

- Accept the shared job schema or a normal user brief.
- Check native image generation first.
- If native image generation is absent, check whether the agent can call ChatGPT/Codex image generation, browser image generation, or the local CLI.
- If critical publishable-use details are missing, return `needs_info` with simple user-facing reminders.
- If exact text/logos/legal copy matter, generate the visual concept and remind the user to finish precise typography in an editable design tool.

Recommended runtime names for `agent_runtime`: `manus`, `genspark`, `claude`, `gemini`, `perplexity`, `goose`, `cursor`, or `generic`.

## Hermes Agent Integration

Hermes supports skills and image-generation toolsets in many deployments. Treat this skill as the image-director layer and Hermes as the execution/orchestration layer.

Recommended setup:

```bash
mkdir -p ~/.hermes/skills
cp -R ./ ~/.hermes/skills/listinglens-studio
hermes -s listinglens-studio
```

Runtime routing:

1. If Hermes has the `image_gen` toolset enabled, call it with the production prompt/job schema.
2. If Hermes lacks `image_gen` but has terminal access and `OPENAI_API_KEY`, call `scripts/generate_image.py` with `--confirm-rights` and, when needed, `--confirm-cost`.
3. If Hermes is operating through Discord/Slack/Telegram, ask for a simple confirmation before publishable listing edits, paid-media work, or anything that changes property condition.
4. Store the manifest/QA summary in the Hermes task result or memory only when it does not leak private client/property data.

Hermes one-shot pattern:

```bash
hermes chat --toolsets "image_gen,vision,file,terminal" -q \
  "Use listinglens-studio for this image job: <paste shared job schema or production brief>"
```

Hermes should never bypass the real-estate compliance reminders just because the request arrived through a gateway or scheduled job. If required details are missing, return `needs_info` with the missing fields and a safe draft/concept option when useful.

## OpenClaw Integration

OpenClaw deployments vary, so use a thin adapter instead of hardcoding assumptions about its internals. First-class integration means OpenClaw can hand this skill a structured image job, receive an output/QA package, and return plain-language reminders for rights/compliance issues.

Adapter contract:

- Input: the shared image job schema above.
- Validation: call `scripts/validate_agent_job.py` before execution when receiving JSON jobs.
- Required tools: either a native image-generation tool, a ChatGPT image-capable session, or terminal access with `OPENAI_API_KEY` for the local CLI script.
- Output: generated image id/path, manifest path if available, prompt summary, backend used, and QA summary.
- Confirmation: ask the operator for the missing rights/disclosure/platform details before publishable real-estate edits, watermark/source-rights ambiguity, people/headshot use, paid ads, or brokerage/MLS/rental-platform output.

OpenClaw routing pseudocode:

```text
if job needs publishable real-estate output and gate incomplete:
  return needs_info(missing_gate_fields, safe_draft_option)
elif native_image_tool_available:
  result = native_image_tool.generate_or_edit(job.prompt, job.input_images)
elif chatgpt_image_session_available:
  result = chatgpt_image_session.generate_or_edit(job.prompt, job.input_images)
elif terminal_available and OPENAI_API_KEY:
  result = run generate_image.py with mapped size/quality/format/input images
else:
  return prompt_packet(job.prompt, missing_backend=true)

qa = run real_estate_or_marketing_qa(result, job)
return {result, qa, backend_used, disclosure_note}
```

Do not let OpenClaw silently downgrade to placeholder SVGs, stock-like mockups, or text-only answers when a native image path exists. If no execution backend exists, return a clean prompt packet and missing-backend reminder.

## Output Package For Orchestrators

Every agent integration should return:

- `backend_used`: native image tool, Hermes image_gen, OpenClaw adapter, or local CLI.
- `image_path_or_id`: absolute path when available, otherwise platform image id.
- `prompt_summary`: concise, not necessarily full private prompt.
- `asset_metadata`: size, quality, format, purpose/platform, source image roles.
- `rights_status`: confirmed, synthetic/internal test, or needs_info.
- `qa_summary`: visual checks performed and remaining risks.
- `disclosure_note`: virtually staged, concept rendering, or none.

For listing-adjacent outputs, never label the result listing-safe unless visual side-by-side QA was actually performed.
