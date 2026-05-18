# Real Estate Playbook

Primary use cases: listing-photo edits, virtual staging, exterior cleanup, renovation concepts, community/amenity visuals, YouTube thumbnails for property videos, and agent marketing.

## Scenario Router

- First classify the request as either `current-condition listing/MLS/agent marketing` or `concept/non-listing visualization`.
- If the user wants a listing, MLS, rental-platform, brokerage, or agent-marketing asset, apply the listing compliance gate below before writing a prompt.
- If the user wants a renovation, fantasy, investor, pre-sale, or design concept, label the output as conceptual and do not let it read as a factual current-condition listing image.
- Empty room -> virtual staging.
- Messy occupied room -> declutter/depersonalize, or create a cleaned listing-ready concept.
- Dark photo -> exposure/color correction and window-light balancing.
- Bad weather/exterior -> natural sky/lawn refresh without changing property facts.
- Outdated room -> renovation concept rendering, not factual listing image.
- New construction/pre-sale -> concept render with explicit conceptual status.
- Short-form video/YouTube -> use `marketing-playbook.md`.
- Floor plan/map/diagram -> generate clean informational graphic; verify dimensions externally.

## Listing Compliance Gate

For any listing, MLS, brokerage, rental-platform, or agent-marketing image, ask or confirm before generating:

- Intended use: live listing, sold/portfolio marketing, rental ad, social post, brochure, thumbnail, or private concept.
- Jurisdiction and applicable rules: state/country, local MLS, brokerage policy, rental/sales platform policy, and required disclosures.
- Source rights: the user owns the photo or has written permission from the photographer, broker, seller/landlord, tenant/occupant, and any visible people as needed.
- Disclosure status: whether virtual staging, renovation concepts, day-to-dusk, sky/lawn edits, or compositing must be visibly labeled or accompanied by a caption.

Pause publishable delivery and explain what is needed:

- The source image contains a watermark, MLS mark, photographer logo, copyright stamp, agency mark, or platform overlay that the user wants removed or hidden.
- The requested output would crop out, paint over, blur, conceal, or regenerate around any watermark, MLS mark, photographer logo, copyright stamp, agency mark, or platform overlay without documented authorization and a compliant non-removal workflow.
- The user lacks rights, consent, or authority to edit and publish the source image.
- The requested edit would materially misrepresent current condition, view, location, size, legal boundary, defects, occupancy, fixtures, neighborhood context, or included amenities.
- The user wants the image to evade MLS, brokerage, platform, fair-housing, advertising, copyright, or disclosure rules.

If jurisdiction, MLS, brokerage, or platform policy is unknown, continue only with conservative, clearly disclosed concepts or ask the user to provide the rules. Explain that these details are needed for live listing, rental-platform, brokerage, or paid-ad use.

## Listing Photo Enhancement

Best for: exposure, white balance, lens/perspective correction, gentle cleanup, crop.

Use only for current-condition listing images after the listing compliance gate. Use best-effort preservation language: preserve material property facts and visible condition as faithfully as possible, but still require human before/after review because image generation can unintentionally change details.

Prompt pattern:

```text
Edit this real estate listing photo for a natural MLS-ready finish, assuming the user has rights to the image and the edit complies with applicable jurisdiction, MLS, brokerage, and platform rules. Improve exposure, white balance, contrast, and clarity while keeping the room truthful and realistic. Preserve all architecture, windows, doors, flooring, fixed appliances, visible view, furniture placement, room dimensions, material condition, and any defects or safety issues to the best extent possible. Keep straight vertical lines, natural shadows, realistic window brightness, and no overprocessed HDR. Avoid adding or removing permanent features, hiding defects, changing the property layout, removing marks/watermarks, or making unverifiable claims.
```

Use `quality=medium` for drafts and `high` for final.

Mandatory QA: compare source and output side by side before delivery. Check that room layout, dimensions, fixtures, windows, doors, flooring, visible view, neighboring context, damage/defects, watermarks/marks, and required disclosures were not altered or hidden.

## Virtual Staging

Best for: empty rooms, model homes, rental marketing.

Preserve architecture. Add furniture only. Use a named style that fits the buyer profile:

- Warm modern: broad-market residential listings.
- Japandi/minimal: condos, rentals, calm luxury.
- Transitional luxury: larger suburban homes and move-up listings.
- Mid-century editorial: design-forward listings.
- Coastal light: vacation or waterfront, only if property context supports it.

Prompt pattern:

```text
Virtually stage this empty [room type] for a [buyer/renter profile] listing. Add [style] furniture and decor only: [specific pieces]. Preserve exact room dimensions, windows, doors, ceiling height, flooring, wall color, fixed lighting, camera angle, and view. Keep furniture scale realistic, pathways open, natural window light, and a tasteful uncluttered MLS-ready composition. Do not alter permanent architecture or hide defects. This should be suitable for a clearly disclosed virtually staged listing image.
```

Require before/after QA and a disclosure recommendation. Do not add people, pets, school-age children, religious/cultural cues, accessibility implications, or demographic signals that could imply a preferred or excluded buyer/renter.

## Declutter And Depersonalize

Best for: removing personal items, small mess, visual noise.

Allowed examples: laundry, toys, toiletries, magnets, papers, personal photos, trash bins, loose cords.

Be careful with: stains, damage, cracks, mold, water marks, missing trim, safety hazards. Those are factual condition and should stay for listing use.

Prompt pattern:

```text
Declutter and depersonalize this room for a truthful real estate listing photo. Remove only temporary personal items such as [items]. Keep all furniture, architecture, fixed fixtures, visible damage/condition, room dimensions, wall colors, flooring, windows, doors, appliances, and lighting physically accurate. Make the result clean, natural, and not over-styled.
```

Do not remove evidence of occupancy if doing so would misrepresent lease status, tenant use, safety, or current condition. Keep permanent wear, damage, stains, cracks, mold, water marks, missing trim, or repair needs visible for listing use.

## Exterior Cleanup

Best for: lawn refresh, sky replacement, driveway cleanup, seasonal mood, twilight hero.

Preserve: facade, roofline, neighboring structures, utility lines, trees, driveway, lot boundaries, address numbers, permanent landscaping, visible damage.

Prompt pattern:

```text
Edit this exterior listing photo for a natural professional real estate look. Improve sky, lighting, lawn color, and overall clarity while preserving the actual house facade, roofline, windows, doors, driveway, trees, utility lines, neighboring buildings, lot shape, shadows, and visible property condition. Keep the weather believable and the result MLS-realistic, not fantasy or luxury overprocessing.
```

For day-to-dusk:

```text
Create a realistic twilight version of this exterior photo. Add warm interior window glow and a deep blue evening sky, but preserve the facade, landscaping, driveway, neighboring context, utility lines, roofline, and camera angle. Keep it plausible as a marketing twilight edit and avoid changing permanent property facts.
```

For listing use, pause and ask for source facts if the request would add or exaggerate waterfront, mountain, skyline, golf-course, park, acreage, sunset direction, seasonal condition, privacy, road quietness, or unobstructed views not present in the real property context. Never hide neighboring buildings, power lines, roads, construction, easements, visible hazards, or access limitations.

## Renovation Concepts

Best for: seller consultations, investor decks, design options, "potential" visuals. Do not present as current listing condition.

Prompt pattern:

```text
Create a clearly conceptual renovation rendering from this room photo. Keep the camera angle, structural layout, window/door positions, ceiling height, and room proportions recognizable. Show a [style] renovation concept with [materials/features]. This is a non-factual concept rendering, not a current-condition listing photo. Avoid impossible structural changes unless explicitly requested.
```

Common concepts:

- Kitchen refresh: cabinet color, counters, backsplash, lighting, hardware.
- Bathroom refresh: vanity, mirror, tile, fixtures.
- Curb appeal: paint color, front door, landscaping concept.
- Basement conversion: media room, office, rental suite concept.
- ADU/backyard concept: patio, garden, deck; disclose conceptual.

For luxury, investor, or pre-sale concepts, avoid claims or visuals that imply guaranteed value, guaranteed ROI, permitted expansion, legal rental eligibility, approved ADU status, or included premium features unless the user provides verified source facts and required disclaimers.

## Luxury Listing Editorial

Use for high-end hero images and brochures. Keep tone restrained and believable.

Luxury does not relax compliance. Stop or ask before creating copy or imagery that implies:

- Waterfront, private beach, dock rights, water access, protected views, ski-in/ski-out, golf access, gated security, concierge service, or resort amenities without verified facts.
- School ratings, district desirability, commute times, walkability, safety, crime levels, investment upside, ROI, appreciation, "best neighborhood", "safest area", "guaranteed value", or similar comparative claims without a cited source and platform/broker approval.
- Exclusivity, privacy, celebrity adjacency, or neighborhood status in ways that could create fair-housing or misleading-advertising risk.

Prompt cues:

- editorial architectural photography
- natural light, balanced shadows
- straight verticals, wide lens without distortion
- tactile material detail
- calm premium color palette
- uncluttered sightlines
- magazine-quality but MLS-truthful

## Floor Plans And Maps

GPT Image can create polished diagrams, but dimensions and legal diagrams must be verified outside the model.

Do not use generated floor plans, maps, lot diagrams, school maps, flood-zone graphics, commute maps, or boundary visuals as legal, survey, appraisal, permit, insurance, or MLS-measurement evidence. Ask for source measurements, survey data, parcel maps, or approved brokerage/MLS assets when accuracy matters. Include "approximate" and "not a survey" style language unless verified source data is supplied.

Use for:

- simplified open-house map
- neighborhood amenity map
- conceptual floor-plan graphic
- listing packet diagram

Prompt pattern:

```text
Create a clean real estate information graphic, not a legal survey. Show [zones/rooms/amenities] with clear labels: "[label 1]", "[label 2]". Use a white background, thin lines, readable typography, simple legend, and generous margins. Keep dimensions approximate unless provided; do not invent legal measurements.
```

## Amenities And Neighborhood

Avoid demographic targeting. Focus on physical amenities, commute context, parks, transit, schools only when facts are provided and allowed.

Fair-housing guardrails:

- Do not target, exclude, prefer, or imply suitability for protected classes such as family status, age, disability, race, color, religion, sex, national origin, sexual orientation, gender identity, or other locally protected categories.
- Avoid phrases like "perfect for families", "safe neighborhood", "exclusive community", "walk to top schools", "young professionals", "empty nesters", "near churches", or demographic-coded imagery unless reviewed under applicable rules.
- Use property-centric language: room count, accessibility features if factual, nearby physical amenities, transit routes, parks, and verified services.
- For schools, crime/safety, commute, neighborhood ranking, and investment claims, require user-provided verified data and approval under local advertising, MLS, brokerage, and platform policies.

Prompt pattern:

```text
Create a tasteful listing-packet amenity visual for [property/community]. Show physical amenities: [amenities]. Use neutral inclusive language, no demographic assumptions, no protected-class targeting, and no invented claims. Include exact text: "[headline]" / "[CTA]".
```

## Agent Headshots And Personal Branding

Only edit real-person images with consent and within policy. Favor light retouching, background cleanup, crop, and brand-consistent marketing layouts. Do not materially alter identity, age, body, or create misleading credentials.

Headshots are identity-sensitive. If the user asks to change race, ethnicity, age, disability, body shape, gender presentation, religious markers, facial identity, credentials, awards, licensing status, brokerage affiliation, or other material identity/professional facts, explain that a truthful professional image should preserve identity and credentials, then offer natural retouching, background cleanup, crop, or brand-consistent layout instead. Do not create a realistic headshot of a real agent from scratch without clear consent and source rights. Keep retouching natural and representation truthful.

## Real Estate Red Flags

Pause and ask/remind before:

- Removing damage, mold, cracks, stains, water intrusion, structural issues.
- Changing views, lot boundaries, neighboring buildings, utility lines, street context.
- Adding nonexistent pools, fireplaces, extra windows, skyline/ocean views, or square footage.
- Removing watermarks or MLS/photographer marks.
- Making fair-housing claims or demographic-targeted imagery.
- Presenting renovation concepts as current-condition photos.
- Using a listing image without rights from the photographer, broker, MLS/platform, seller/landlord, tenant/occupant, or visible people as applicable.
- Skipping required virtual-staging, day-to-dusk, renovation-concept, AI-edited, or composite-image disclosures.
- Claiming school quality, commute time, crime/safety, "best neighborhood", ROI, appreciation, rentability, guaranteed value, or legal use without verified source facts and policy approval.
- Treating generated floor plans, maps, lot lines, boundaries, measurements, flood zones, school zones, or commute visuals as legal or verified factual documents.
- Materially altering a real agent/client headshot or creating misleading identity, licensing, awards, or brokerage affiliation.

Before delivering any listing-adjacent output, require a source/output comparison or contact sheet and note unresolved compliance dependencies. If that visual QA was not performed, say the image is not listing-safe yet. If the image is only a concept, say that clearly and keep the visual from being mistaken for current condition. Never treat watermark/MLS/photographer mark removal as allowed merely because the output is conceptual.
