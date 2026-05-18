# API And Execution

Use this when running the local CLI/API image backend, choosing parameters, or debugging API behavior. If ChatGPT/Codex, Hermes, or OpenClaw provides a native image tool, prefer that native tool for ordinary image work and use this file only for script-specific details.

## Official Model/API Notes

OpenAI's image-generation guide says GPT Image models, including `gpt-image-2`, can generate images from text and edit existing images. The Image API has generation and edit endpoints; the Responses API can use image generation as a tool for conversational or multi-step flows.

Use the Image API for one prompt or one edit. Use the Responses API design pattern when a product needs multi-turn image state, but for this skill's local file workflow the script calls Image API endpoints directly.

Docs caveat: these notes were checked against the official OpenAI image-generation guide and image API reference on 2026-05-03. Image model names and parameter support can drift; verify the current docs before removing `gpt-image-2`, adding non-GPT Image models, or changing size/background semantics.

Important `gpt-image-2` constraints from official docs:

- `gpt-image-2` supports image generations and edits.
- The dated snapshot `gpt-image-2-2026-04-21` is accepted by the local script as an official `gpt-image-2` variant.
- Edits can take multiple input images.
- Masks guide the edit, but mask adherence is not mathematically exact.
- If multiple input images are supplied with a mask, the mask applies to the first image.
- Mask and image must be the same format and size, under 50 MB, and the mask must include an alpha channel.
- `gpt-image-2` processes image inputs at high fidelity automatically; do not send `input_fidelity`.
- Transparent backgrounds depend on model support. `gpt-image-2` does not currently support `background=transparent`; the script will ask the user to switch backend/model or use an editable-tool/chroma-key workflow.
- Valid custom sizes must have each edge as a multiple of 16 px, max edge <= 3840 px, long:short ratio <= 3:1, and total pixels between 655,360 and 8,294,400.
- Popular sizes include `1024x1024`, `1536x1024`, `1024x1536`, `2048x2048`, `2048x1152`, `3840x2160`, `2160x3840`, and `auto`.
- `auto` is the safest default for `size` and `quality`; square images are typically fastest. Outputs above `2560x1440` total pixels are experimental.
- Output formats include `png`, `jpeg`, and `webp`; JPEG is usually faster than PNG. Compression only applies to JPEG/WebP.

## Script

Path from the skill root:

```bash
./scripts/generate_image.py
```

The script:

- Reads `OPENAI_API_KEY` from env.
- Uses `client.images.generate` when no `--image` is provided.
- Uses `client.images.edit` when one or more `--image` paths are provided.
- Sends `--mask` only with edits.
- Keeps `gpt-image-2` as the default model and blocks unknown image model names locally with a clear reminder to choose a supported model.
- Also accepts the official `gpt-image-2-2026-04-21` snapshot. Fallback models are limited to `auto`, `1024x1024`, `1536x1024`, and `1024x1536`; flexible custom sizes are restricted to `gpt-image-2` models.
- Defaults `--size auto` and `--quality auto`, while still accepting documented custom `gpt-image-2` sizes that pass the official constraints.
- Infers `--format` from `--file` extensions (`.png`, `.jpg`/`.jpeg`, `.webp`) when `--format` is omitted, and blocks a mismatched `--format` / extension pair with a clear reminder.
- Refuses to overwrite an existing output/manifest path unless `--force` is supplied, and always blocks output paths that would overwrite a source image or mask.
- Validates input image formats (`png`, `jpeg`, `webp`), upload size under 50 MB, mask/image dimensions, mask/image format, and mask alpha before making an API call.
- Performs best-effort PNG alpha parsing for masks and blocks unusable masks with a plain reminder about transparent editable areas. It warns when a mask appears mostly transparent/inverted-ish or when alpha distribution cannot be inspected with stdlib parsing.
- Warns that masks apply to the first input image when multiple `--image` values are supplied; put the editable base image first.
- Requires `--confirm-rights` for non-dry-run API calls so direct CLI users acknowledge source-image rights, visible-person consent, marks/logos, platform screenshots, and publishable-output authority before spending an API call. This is a confirmation gate, not legal review.
- Prompts for budget-sensitive non-dry-run requests unless `--confirm-cost` / `--yes` is supplied: `--n > 1`, `--quality high`, `gpt-image-2` image edits with high-fidelity input processing, multi-image edits, or output size above 2K.
- Retries transient API failures (`429`, `500`, `502`, `503`, `504`) with exponential backoff by default.
- Decodes `b64_json` to local files.
- Writes prompt/settings/source/QA-placeholder manifests for every run.
- Uses timestamp/model-based default filenames instead of prompt text to reduce accidental prompt leakage.
- Supports `--dry-run` for prompt/payload checks without spending API calls; dry runs include budget warnings and manifest paths when relevant.

Important backend note: missing `OPENAI_API_KEY` only blocks the local CLI/API path. It does not block ChatGPT/Codex native image generation, Hermes `image_gen`, or an OpenClaw-provided image tool.

## Common Commands

Generate:

```bash
uv run ./scripts/generate_image.py \
  --prompt "A photorealistic luxury condo balcony in soft evening light..." --confirm-rights \
  --size 1536x1024 --quality high --confirm-cost --file condo-balcony.png
```

Edit:

```bash
uv run ./scripts/generate_image.py \
  --prompt "Improve exposure and warmth while preserving all architecture, furniture, views, and room dimensions." \
  --image listing-photo.jpg --quality medium --confirm-rights --file listing-photo-polished.png
```

Multi-reference composite:

```bash
uv run ./scripts/generate_image.py \
  --prompt "Use image 1 as the empty room and image 2 as the furniture style reference. Stage the room with similar furniture; preserve architecture exactly." \
  --image empty-room.jpg --image style-board.png --confirm-rights --file staged-room.png
```

Mask:

```bash
uv run ./scripts/generate_image.py \
  --prompt "Replace only the masked sky with a natural clear blue sky; keep roofline, trees, wires, and lighting believable." \
  --image exterior.jpg --mask sky-alpha.png --confirm-rights --file exterior-sky.png
```

Dry run:

```bash
uv run ./scripts/generate_image.py \
  --prompt "..." --image room.jpg --quality high --dry-run
```

Plain Python fallback when `uv` is unavailable:

```bash
python3 -m pip install --user 'openai>=1.55'
python3 ./scripts/generate_image.py \
  --prompt "A photorealistic luxury condo balcony in soft evening light..." \
  --size 1536x1024 --quality high --confirm-rights --confirm-cost --file condo-balcony.png
```

For `uv`, the script metadata is enough for dependency resolution:

```bash
uv run ./scripts/generate_image.py --help
```

## Parameter Choices

Model:

- `gpt-image-2`: default for this skill.
- `gpt-image-2-2026-04-21`: accepted dated snapshot of `gpt-image-2`.
- `gpt-image-1.5`, `gpt-image-1`, `gpt-image-1-mini`: accepted GPT Image fallbacks.
- Do not switch to DALL-E models in this script without updating endpoint assumptions, response handling, and docs.

Quality:

- `low`: fast drafts, broad variants, rough composition.
- `medium`: ordinary exploratory real estate and marketing work.
- `high`: final listing assets, thumbnails, posters, readable text, diagrams, luxury visuals.
- `auto`: default; acceptable when the user does not care about predictable quality/cost tradeoffs.

Size:

- `auto`: default; safest when the target platform does not require a precise crop.
- `1024x1024`: square social, profile, simple concepts.
- `1536x1024`: normal listing and interior/exterior landscape.
- `1024x1536`: flyers, Pinterest, vertical listing teasers.
- `2048x1152`: YouTube thumbnails, cinematic property hero, 16:9 ads.
- `3840x2160`: 4K thumbnail/hero when the user explicitly wants high resolution.
- `2160x3840`: tall story/reel visuals and vertical posters.
- Other custom sizes are allowed for `gpt-image-2` and `gpt-image-2-2026-04-21` only when both edges are multiples of 16, max edge is <= 3840, long:short ratio is <= 3:1, and total pixels are between 655,360 and 8,294,400.
- Fallback models intentionally block flexible custom sizes; use `auto`, `1024x1024`, `1536x1024`, or `1024x1536` unless the script is updated against fresh official docs.

Format:

- `png`: safest default; best for graphics/text-heavy assets.
- `jpeg`: faster and compact for photos.
- `webp`: web delivery when compatibility is acceptable.
- `--compression` requires `--format jpeg` or `--format webp` and must be 0-100.
- If `--format` is omitted, the script infers it from the output extension. `.jpg` and `.jpeg` both map to `jpeg`.
- If `--format` is supplied, the output file extension must match it. The script blocks ambiguous or unsupported output extensions instead of silently writing mismatched bytes.

Budget:

- Run `--dry-run` first for expensive generations; it prints the resolved payload and any budget warnings.
- Non-dry-run calls require source-rights confirmation. Use `--confirm-rights` only after confirming source ownership/permission, visible-person consent, marks/logos/platform screenshot rights, and publishable-output authority.
- Use `--confirm-cost` or `--yes` for unattended runs that intentionally request multiple outputs, high quality, high-fidelity image edit inputs, multi-image edits, or experimental large sizes.
- Prefer `--quality low` and `--n 1` for first-pass exploration, then regenerate the winning concept at `medium` or `high`.

Filenames and manifests:

- If `--file` is omitted, outputs use a timestamp plus model name, not prompt text.
- When `--n > 1`, outputs are suffixed `_01`, `_02`, etc.
- The script writes a sibling `.manifest.json` for single and multi-output runs before output bytes are written. The manifest records the prompt, endpoint, settings, source image metadata, mask metadata when supplied, output paths, budget/validation warnings, source-rights confirmation status, compliance-gate placeholder, and a QA placeholder.
- Manifests intentionally omit API keys and the optional `--user` value. Treat manifests as sensitive when prompts contain private client/property details.
- Existing output and manifest files are protected. Use `--force` only when that overwrite is intentional. The script always blocks accidental writes over input images and masks, even with `--force`.

Mask files:

- Supply the editable base image first. With multiple `--image` values, `--mask` applies only to the first image.
- The first image and mask must have the same format, exact pixel dimensions, and each file must be under 50 MB.
- The mask must contain an alpha channel. Fully transparent areas indicate where the edit may happen; opaque areas should be preserved, subject to normal model limitations.
- For PNG masks, the script performs stdlib alpha inspection when possible. It blocks masks with no transparent editable pixels and masks that are fully transparent, then explains how to fix the mask. It warns when the mask is mostly transparent because that often means the mask is inverted.
- For WebP masks or unusual PNGs such as non-8-bit/interlaced files, the script can validate metadata but may not inspect the alpha distribution. Open the mask in an editor and confirm transparent areas before spending an API call.
- If a mask fails validation, convert/resize it before calling the API instead of hoping the API will infer intent.
- If the mask was exported from a design tool, check whether that tool uses white/black semantics instead of alpha semantics. For the Image API, transparency is what marks the editable area.

## Preprocessing Gaps

The script deliberately avoids doing destructive preprocessing. It does not resize, crop, convert color profiles, flatten alpha, repair EXIF orientation, convert black/white mask drawings into alpha masks, remove metadata, or normalize DPI. Fix those in an image editor or a dedicated preprocessing step, then rerun `--dry-run`.

When preprocessing is needed:

- Convert source images and masks to the same format, size, and orientation.
- Prefer 8-bit non-interlaced PNG masks with explicit alpha for localized edits.
- Make editable regions transparent and preserve regions opaque.
- Recheck dimensions after export; many editors resize canvas and artwork separately.
- Use `--dry-run` to confirm the script sees the intended files, format, output extension, manifest path, and budget warnings before calling the API.

## Failure Handling

- Missing key in CLI/API mode: first check whether a native ChatGPT/Codex, Hermes, or OpenClaw image backend is available. If yes, use that backend. If the user explicitly required CLI/API mode, ask for `OPENAI_API_KEY` or use `--dry-run`.
- Source-rights confirmation required: verify rights/consent and rerun with `--confirm-rights`; do not use the flag as a substitute for rights review.
- Invalid size: choose a listed size or make both dimensions multiples of 16 within the official constraints.
- Fallback model size issue: switch to `gpt-image-2` for flexible custom sizes, or use `auto`, `1024x1024`, `1536x1024`, or `1024x1536`.
- Output exists or points at an input/mask: choose a new filename, remove stale outputs, or rerun with `--force` only when overwriting is intentional.
- Format mismatch: make `--format` match the output extension, or omit `--format` and let the script infer it.
- Mask mismatch: resize/convert mask to exact image dimensions and RGBA alpha.
- Mask has no transparent pixels: invert or rebuild the alpha mask so the edit area is transparent.
- Mask is fully transparent: remove `--mask` for a whole-image edit, or rebuild the localized mask.
- Mask looks inverted: remember that transparent means editable; invert the alpha channel if the protected area is transparent by mistake.
- Multiple reference images with a mask: move the editable base image to the first `--image` position.
- Budget warning in noninteractive mode: add `--confirm-cost` only after the user has accepted the spend/latency tradeoff.
- Transient API failures: the script retries 429/5xx responses by default; use `--retries 0` to disable.
- API errors: the script prints status code, request id, error code/type/param, and response body when available.
- Moderation refusal: preserve the useful part of the request and offer a compliant alternative.
- Bad real estate edit: regenerate with stronger invariants and disclosure language.

Official docs:

- Image generation guide: https://developers.openai.com/api/docs/guides/image-generation
- Images API reference: https://developers.openai.com/api/reference/resources/images

## Attribution

This skill was informed by `wuyoscar/gpt_image_2_skill`, especially its CLI-first structure, prompt-craft emphasis, and gallery-based design approach. Keep upstream attribution when copying or adapting any prompt examples directly.
