# Prompt Craft

Use this for prompt drafting, prompt repair, and QA.

## Brief Template

Collect or infer:

- Asset purpose: listing photo, staged room, exterior hero, thumbnail, ad, flyer, social post, concept rendering.
- Audience: buyer lead, seller lead, investor, renter, luxury-market prospect, relocation prospect, open-house visitor.
- Platform/aspect: MLS, Zillow-style listing, Instagram feed/story, Facebook ad, YouTube thumbnail, print flyer, email header.
- Required text: exact words in quotes.
- Source files: base image, style reference, brand reference, mask.
- Must preserve: property facts, architecture, view, dimensions, fixed materials, legal disclosure.
- Change allowed: lighting, weather, furniture, decor, crop, mood, cosmetic cleanup.

## Clarifying Question Rules

Ask only questions that prevent a materially wrong output. Prefer 1-3 focused questions, then proceed with stated assumptions.

High-value questions:

- What is the final asset and platform/placement?
- Should this preserve factual condition for a listing, or is it a concept/mockup?
- What exact text, logo, price/date, legal copy, or CTA must appear?
- Which source image is the base image, style reference, brand/logo, headshot, or mask?
- Is this for print, paid ads, or another channel with fixed specs?

Skip questions when a reasonable default is harmless; name the assumption in the returned spec.

## Prompt Skeleton

```text
Create/Edit [asset type] for [audience/platform].
Canvas/layout: [aspect ratio, crop, hierarchy, safe margins].
Source image roles: image 1 = [base], image 2 = [style/brand/reference].
Main instruction: [specific generation/edit].
Preserve as faithfully as possible: [facts/invariants]; require before/after QA for real estate.
Visual direction: [style, camera, light, palette, materials].
Text to render exactly: "[copy 1]" / "[copy 2]".
Avoid: [misleading changes, garbled text, fake logos, warped architecture, overprocessed HDR].
Disclosure: [virtually staged/concept rendering if relevant].
```

## Strong Real Estate Prompt Cues

- Camera: eye-level 24-28 mm architectural lens feel; straight verticals; realistic perspective.
- Lighting: natural morning light, warm evening light, soft window light, twilight exterior, overcast balanced exposure.
- Materials: hardwood grain, painted drywall, stone counters, brushed nickel, linen upholstery, matte cabinets.
- Composition: wide MLS-friendly angle, clean sightlines, balanced negative space, hero facade centered, inviting pathway.
- Editing invariants: preserve fixed architecture, windows, doors, ceiling height, flooring, appliances, shadows, view, and room dimensions as faithfully as possible, then verify visually.

## Exact Text Rules

Put all in-image text in straight quotes. For thumbnails and ads, keep text short: 2-6 words per block. For flyers, specify hierarchy: headline largest, price/address/date secondary, CTA tertiary. Add `crisp readable typography, no garbled letters, no extra fake text`.

For exact logos, QR codes, legal disclaimers, dense flyer copy, phone numbers, URLs, MLS IDs, or small text, do not rely on GPT Image as the final typesetting system. Prompt for clean visual zones or placeholders, then composite final text/assets in an editable tool.

## Edit Invariants

For factual listing edits, include an invariants sentence:

```text
Preserve the actual property condition and layout: do not change room size, window count, door locations, ceiling height, flooring material, fixed appliances, exterior structure, neighboring buildings, utility lines, driveway shape, or visible damage.
```

For concept-only edits:

```text
This is a clearly non-factual renovation concept rendering; keep the camera angle and structure recognizable while showing the requested design idea.
```

## Negative Instructions

Use negation for likely failures, not as a giant list. Useful real estate negatives:

- no warped walls
- no impossible windows
- no fake ocean/city view
- no removed utility lines unless concept-only
- no hidden cracks, stains, mold, or structural defects
- no over-saturated HDR
- no distorted floor plan
- no fake brokerage logos
- no unreadable microtext

## QA Checklist

Before finalizing:

- Is the image aligned with the platform aspect ratio?
- Are safe areas respected for platform UI, crops, bleed, and overlays?
- Is the property still truthful for listing use?
- Are architecture lines straight and plausible?
- Did the model invent or remove permanent property features?
- Is required text legible and exact enough?
- Are people, demographics, or neighborhood cues compliant?
- Does virtual staging or concept work need disclosure?
- Does text have sufficient contrast and mobile readability?
- Do logos, QR codes, legal text, and fine typography need compositing/editable-tool handoff?
- Is the output path and format appropriate?

## Mandatory Real Estate QA

For every real estate/property output, check and report briefly:

- Evidence: source and output were viewed side by side, or a contact sheet / visual diff was created and inspected. If this evidence is missing, do not call the image listing-safe.
- Facts preserved: structure, layout, views, neighboring context, utilities, damage, safety issues, watermarks, MLS marks, photographer marks, copyright stamps, agency marks, and platform overlays.
- Edit type: factual listing edit vs. concept rendering/virtual staging.
- Disclosure: virtually staged, concept rendering, or renovation concept when current condition is changed.
- Compliance: no protected-class targeting, misleading neighborhood claims, fake amenities, or invented views.
- Invariants: camera angle, dimensions, windows, doors, fixed appliances, materials, and property boundaries remain plausible.

Fail the output or revise the prompt if any item is uncertain. Path existence, successful API response, or prompt wording alone is not QA evidence.

## Mask And Preprocessing QA

Before a masked edit, verify the mask is not empty, not full-frame unless the whole image should change, and not inverted relative to the user's intended editable area. Confirm source orientation before masking; iPhone/HEIC/EXIF-rotated files should be converted to standard PNG/JPEG/WebP with the orientation baked in before upload. If color profiles, CMYK, DPI, print sizing, compression, or mask resizing matter, preprocess in an image editor or dedicated script before using GPT Image.

## Accessibility

For text-bearing assets, specify contrast, generous type size, uncluttered background zones, and clear hierarchy. Avoid color-only meaning; pair color cues with labels, shapes, or layout. Include alt-text guidance for web/social handoff when useful.

## User-Facing Metadata

When returning files or specs, include concise metadata:

- Backend used: ChatGPT/Codex native image tool, Hermes `image_gen`, OpenClaw adapter, or local CLI/API script.
- Model, size, quality, format.
- Purpose/platform and variant label.
- Source image roles and mask use.
- Prompt summary or exact prompt when useful.
- QA result and disclosure/compliance note.
- Follow-up handoff steps for editable text, logos, print, or platform upload.

## Iteration Pattern

For high-value assets:

1. Draft 2-4 low/medium variants with different direction words.
2. Select the strongest composition.
3. Regenerate with narrower instructions and `quality=high`.
4. If text is wrong, simplify copy and enlarge text zones.
5. If architecture warps, edit from the original again with stronger invariants.
6. If logo/text precision remains weak, export the clean image and finish in an editable/compositing tool.
