# Marketing Playbook

Use this for thumbnails, ads, social posts, flyers, banners, listing packets, and brand visuals. Marketing assets need a concrete offer, audience, platform, copy hierarchy, brand constraints, CTA, and delivery format; do not settle for "make it pop" when the asset will be published.

## Routing And Missing Inputs

Ask for missing details only when they change production choices:

- Objective: awareness, lead capture, listing launch, open house, retargeting, newsletter, print handout.
- Platform/placement: YouTube, Instagram feed, story/reel cover, Facebook, LinkedIn, email, print, MLS/listing packet.
- Audience and offer: buyer, seller, renter, investor, luxury, relocation, open-house visitor; avoid protected-class targeting.
- Exact copy: headline, support line, CTA, price, address, date, agent/brokerage details.
- Brand assets: logo file, brand colors, fonts if available, required disclaimers.
- Delivery: draft concept, final raster, editable handoff, paid ad upload, print production.

If exact copy, legal text, logo fidelity, QR codes, maps, or dense layout matters, generate the image/background and finish those elements in Canva, Figma, PowerPoint, HTML/CSS, Photoshop, or another editable/compositing tool.

## YouTube Thumbnails

Goal: clear subject, 2-5 words, emotional contrast, strong readability at small size.

Recommended size: `2048x1152` or `3840x2160`, `quality=high`, `format=png` or `jpeg`.

Real estate thumbnail structures:

- Property reveal: hero exterior + headline.
- Before/after: split screen renovation or staging concept.
- Market update: agent face/reference image + chart-like background.
- Tour hook: best room + short curiosity headline.
- Investor analysis: property image + bold number/ROI text.

Prompt pattern:

```text
Create a 16:9 YouTube thumbnail for a real estate video. Main visual: [property/room/agent/reference]. Large readable headline text exactly: "[2-5 WORD HOOK]". Composition: high contrast, clean safe margins, one dominant focal point, subtle depth, premium real estate color palette, no clutter. Keep the property truthful if using a listing image. Avoid tiny text, fake logos, distorted faces, overdramatic clickbait, and garbled letters.
```

If using an agent photo, keep identity natural and ask for consent if not clear.

Keep critical text, faces, and logos away from edges and platform overlays. For thumbnails, compose with enough empty space that the title does not fight the subject at small sizes.

## Social Ads

Platforms:

- Instagram feed: square `1024x1024` or portrait `1024x1536`.
- Instagram story/reel cover: `2160x3840`.
- Facebook/LinkedIn: square or `1536x1024`.
- Email banner: landscape `1536x1024` or custom crop after generation.

Use conservative safe areas because platform chrome, captions, profile chips, and ad UI can shift. Keep the primary message centered, avoid bottom-heavy CTA placement for vertical video covers, and verify current platform specs before final paid placement.

Prompt pattern:

```text
Design a real estate social ad for [platform]. Audience: [seller/buyer/renter/investor]. Visual: [property/room/community/agent]. Text hierarchy: headline "[headline]", supporting text "[support]", CTA "[CTA]". Use clean modern brokerage styling, readable typography, brand colors [colors], generous margins, and a premium but trustworthy tone. Avoid fair-housing targeting, fake logos, exaggerated claims, and unreadable microtext.
```

## Listing Flyers And Open House Graphics

Use exact text and layout zones. Do not overload with copy.

Prompt pattern:

```text
Create a vertical real estate open-house flyer, 3:4 portrait. Top: large photo/hero visual. Middle: headline "[address or property name]" and key details "[beds] Bed / [baths] Bath / [sq ft] Sq Ft". Bottom: CTA "[open house date/time]" / "[agent name]" / "[phone or website]". Use elegant readable typography, MLS-truthful imagery, restrained color palette, and clean hierarchy. No fake logos or invented brokerage marks.
```

## Print Specs

For print-facing assets, GPT Image should usually create the hero art, background, or concept mockup, not the final production layout.

- Ask for final trim size, bleed, margin, paper/use case, quantity, printer specs, and whether CMYK/PDF export is required.
- Include bleed-safe composition in the prompt, but add final bleed, crop marks, exact text, logos, and QR codes in an editable layout tool.
- Use high quality and the largest practical aspect ratio; upscale or rebuild in layout software if the requested print size exceeds raster quality.
- Do not promise color accuracy from image generation alone; print proofing belongs in the export/layout step.

## Listing Packet And Presentation Visuals

Useful pages:

- cover hero
- neighborhood amenity board
- property features sheet
- renovation potential concept
- pricing strategy chart background
- seller process infographic

Use `quality=high` for text-heavy or print-facing images.

## Brand Consistency

When brand assets are provided:

- Treat image 1 as base/property, image 2 as brand board/logo/style, image 3 as optional agent/headshot.
- Preserve logo proportions; do not invent extra logos.
- Use exact brand colors if supplied.
- Keep typography style compatible, but do not claim font identity unless provided.
- For logo lockups, generate placeholder space or background only, then place the real logo file in a compositing/editable tool.

Prompt pattern:

```text
Use the supplied brand reference for color, tone, and layout inspiration only. Do not distort or invent the logo. Create [asset] with exact text "[copy]". The result should feel like premium real estate marketing: clear hierarchy, tasteful spacing, trustworthy tone, and strong mobile readability.
```

## Before/After And Split-Screen

Use for staging, renovation, curb appeal, cleaning.

Prompt pattern:

```text
Create a clean split-screen real estate marketing graphic. Left panel labeled "Before"; right panel labeled "After". Use the provided image as the before/current state. The after side should show [staged/renovated/cleaned concept]. Keep the structure recognizable and include a clear disclosure note "Concept rendering" if the after is not current property condition. Use balanced lighting, matching perspective, and crisp readable labels.
```

## Text Hierarchy Rules

- Thumbnail: 2-5 words, huge text.
- Social ad: headline + one supporting line + CTA.
- Flyer: address/title + stats + date/CTA.
- Listing packet: title + section labels + small captions.
- Avoid more than 3 text sizes.
- Ask for exact copy when legal/brand text matters.
- For exact, small, legal, multilingual, or dense text, use the image model for composition and an editable tool for final typography.

## Accessibility And Readability

- Maintain strong contrast between text and background.
- Avoid placing text over busy property details unless a solid overlay or quiet negative space is specified.
- Keep headlines short enough to read on mobile without zooming.
- Preserve meaningful visual information for users who may see only a cropped preview.
- Provide suggested alt text or descriptive filename when handing off social or web assets.

## A/B Variants

For campaigns, draft 2-4 variants that each test one meaningful axis:

- Hook: urgency, curiosity, benefit, price/value, social proof.
- Visual: exterior hero, best room, before/after, agent-led, detail/amenity.
- CTA: schedule tour, get valuation, view listing, RSVP, download guide.
- Layout: text-left, text-right, centered title, split-screen, image-first.

Label variants clearly, keep shared facts identical, and regenerate the winning direction at higher quality.

## Asset Handoff

Return handoff metadata for production assets:

- Asset purpose, platform, aspect ratio, size, quality, format.
- Prompt or variant label.
- Source image roles and any masks used.
- Exact copy supplied by the user and any text that must be composited later.
- Brand assets/colors used or missing.
- Disclosure/compliance note.
- QA notes, including mobile readability and property-truth checks.

## Marketing QA

- Can it be understood in one glance?
- Is the text readable on mobile?
- Are critical elements inside platform and print safe areas?
- Is the property still truthful?
- Does the image avoid protected-class targeting?
- Does the asset need a virtual-staging/concept disclosure?
- Are brand claims, prices, dates, and stats provided by the user?
- Should exact logos, QR codes, legal copy, or dense text be finished outside the image model?
