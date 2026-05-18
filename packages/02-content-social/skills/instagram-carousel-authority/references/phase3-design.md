# Phase 3: Carousel Creation

Using carousel_brief.md, create the full carousel with professional design quality.

## Design Tools Available

Choose the best approach based on available tools and design complexity:

### Option 1: AI Image Generation (Gemini Nano Banana Pro)
**Best for:** Complex visual designs, photography-based carousels, illustrative elements

Use the nano-banana-pro skill:
```bash
cd ~/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro
uv run scripts/generate_image.py --prompt "[detailed design prompt]" --filename "slide_01.jpg" --resolution 2K
```

**Prompt engineering for carousels:**
- Specify exact dimensions: "1080x1080 Instagram carousel slide"
- Include typography: "Bold sans-serif headline '[HEADLINE]' in white text, centered"
- Specify colors: "Background: deep blue (#1A237E), accent: bright yellow (#FFC107)"
- Add layout: "Headline at top third, body text centered, logo bottom right"

### Option 2: Programmatic Generation (Python + Pillow)
**Best for:** Text-heavy slides, consistent design systems, precise control

See `scripts/generate_slide.py` for a template using PIL/Pillow.

**When to use:**
- Typography-focused designs
- Need exact control over spacing, alignment, colors
- Batch generation of similar slides
- Custom fonts and pixel-perfect layouts

### Option 3: Hybrid Approach
**Best for:** Mixed carousels with both photography and text-heavy slides

- Use AI generation for Slide 1 (hook) and any photography-based value slides
- Use programmatic generation for text-heavy value slides and CTA slides

## Step 3.1 — Design System Setup

Before creating slides, establish the design system from carousel_brief.md.

### Canvas Specifications
- **Dimensions:** 1080x1080 pixels (Instagram carousel standard)
- **Color mode:** RGB
- **Resolution:** 72 DPI minimum (144 DPI preferred for quality)

### Typography System
- **Headline font:** [From brief] — size, weight, color
- **Body font:** [From brief] — size, weight, color
- **Line height:** 1.2-1.4 for headlines, 1.4-1.6 for body
- **Letter spacing:** 0-2% for headlines, 0% for body

### Color System
Extract hex codes from carousel_brief.md:
- Primary: `#HEXCODE`
- Secondary: `#HEXCODE`
- Accent: `#HEXCODE`
- Background: `#HEXCODE`
- Text: `#HEXCODE`

### Layout Grid
- **Margins:** 60-80px from all edges (safety zone for mobile viewing)
- **Alignment:** [Centered, left-aligned, or custom from brief]
- **Spacing:** Consistent padding between elements

### Brand Assets
- **Logo:** [Source file from intelligence_report.md or business website]
- **Position:** [Bottom right, bottom left, or as specified in brief]
- **Size:** 80-120px width/height
- **Opacity:** [100% or reduced for subtlety]

## Step 3.2 — Slide-by-Slide Production

### Slide 1: Cover/Hook (MOST CRITICAL)

This slide determines whether someone stops scrolling. Prioritize:

**Thumbnail test:**
- View at 200x200px — is the headline instantly readable?
- Does it pass the "1-second scroll test"?

**Visual hierarchy:**
- Headline is the dominant element (largest, highest contrast)
- Supporting text (if any) is clearly secondary
- Minimal visual clutter

**Design execution:**

If using AI generation:
```bash
cd ~/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro
uv run scripts/generate_image.py \
  --prompt "Instagram carousel cover slide, 1080x1080px. Bold sans-serif headline '[HEADLINE FROM BRIEF]' in white text, centered on deep blue background (#1A237E). Minimalist design, high contrast. [Brand name] logo in bottom right corner, 100px width. Professional, modern, scroll-stopping." \
  --filename "slide_01_cover.jpg" \
  --resolution 2K
```

If using programmatic generation:
```python
python3 scripts/generate_slide.py \
  --text "[HEADLINE]" \
  --layout "cover" \
  --bg-color "#1A237E" \
  --text-color "#FFFFFF" \
  --font-size 120 \
  --output "slide_01_cover.png"
```

**Quality check:**
- ✅ Headline readable at thumbnail size
- ✅ High contrast (4.5:1 ratio minimum)
- ✅ Brand logo present but not distracting
- ✅ Visually distinct from competitors' covers

### Slides 2–7: Value Delivery

For each value slide, use the content from carousel_brief.md:

**Slide template:**
- **Headline:** [8 words or fewer, bold, high contrast]
- **Body copy:** [1-2 lines, max 20 words, supporting detail]
- **Authority signal:** [Data point, credential, or proof element]
- **Visual element:** [Icon, graphic, or supporting image if applicable]

**Design execution:**

For text-heavy slides (most common):
```python
python3 scripts/generate_slide.py \
  --headline "[HEADLINE]" \
  --body "[BODY COPY]" \
  --authority "[AUTHORITY SIGNAL]" \
  --layout "value" \
  --bg-color "#FFFFFF" \
  --headline-color "#1A237E" \
  --body-color "#333333" \
  --output "slide_02.png"
```

For image-based slides:
```bash
cd ~/.npm-global/lib/node_modules/openclaw/skills/nano-banana-pro
uv run scripts/generate_image.py \
  --prompt "Instagram carousel slide, 1080x1080px. [Describe visual]. Bold headline '[HEADLINE]' at top. Body text '[BODY]' centered. [Brand] logo bottom right. Clean, professional design." \
  --filename "slide_03.jpg" \
  --resolution 2K
```

**Consistency rules:**
- Same font sizes across all value slides
- Same margin/padding measurements
- Same logo position and size
- Same color palette

**Word count limits:**
- Headline: 8 words maximum
- Body: 20 words maximum
- Authority signal: 10 words maximum
- Total per slide: 40 words absolute maximum

### Slide 8: Key Takeaway (MOST SAVEABLE)

This slide should be **reference-worthy** — something users want to save and return to.

**High-save formats:**

**1. Checklist:**
```
✅ [Action item 1]
✅ [Action item 2]
✅ [Action item 3]
✅ [Action item 4]
✅ [Action item 5]
```

**2. Framework/Matrix:**
```
[Visual representation of a 2x2 matrix, flowchart, or process diagram]
```

**3. Before/After:**
```
❌ Before: [Old way]
✅ After: [New way]
```

**4. Quick Reference:**
```
[Brand Name]'s [Topic] Formula:
1. [Step]
2. [Step]
3. [Step]
```

**Design execution:**

Make this slide visually distinct:
- Use accent color for emphasis
- Clear visual hierarchy
- Scannable format (bullets, numbers, icons)
- High information density but not cramped

### Slide 9: CTA (Call-to-Action)

**Purpose:** Direct next action without hard selling

**Copy formula:**
- **Line 1:** Warm acknowledgment — "You made it to the end 👏"
- **Line 2:** Value reframe — "If this helped, imagine what else you'll learn"
- **Line 3:** Specific CTA — "Follow @[handle] for more [specific benefit]"
- **Line 4 (optional):** Secondary action — "Save this to reference later"

**Design execution:**

Keep it clean and focused:
- CTA text is the primary element
- Minimal visual distraction
- Accent color for the specific action
- Brand logo present but subtle

### Slide 10: Brand/Offer (Optional)

Only include if there's a relevant offer or next step.

**When to include:**
- Lead magnet (free guide, checklist, template)
- Relevant service/product
- Community invitation (Skool, Discord, newsletter)

**When to skip:**
- No offer ready
- Focus is purely on building authority
- CTA is sufficient on Slide 9

**Design execution:**

Soft pitch approach:
- Position as logical next step, not a sales pitch
- Clear value proposition
- Simple call-to-action (DM, link in bio, comment keyword)

## Step 3.3 — Quality Check

Before exporting, verify every slide:

### Readability Tests

**Thumbnail test (200x200px):**
- ✅ Cover slide (Slide 1) headline is instantly readable
- ✅ Other slides have clear visual hierarchy at small size

**Contrast test:**
- ✅ All text passes WCAG AA standard (4.5:1 contrast ratio minimum)
- Use WebAIM Contrast Checker: https://webaim.org/resources/contrastchecker/

**Word count test:**
- ✅ No slide exceeds 40 words of body copy
- ✅ Headlines are 8 words or fewer

### Visual Consistency

**Alignment:**
- ✅ All headlines aligned the same way
- ✅ Body text consistently positioned
- ✅ Logos in exact same position on every slide

**Spacing:**
- ✅ Consistent margins (60-80px from edges)
- ✅ Consistent padding between elements
- ✅ Balanced white space

**Typography:**
- ✅ Same font sizes throughout
- ✅ Same font weights throughout
- ✅ Consistent line heights

**Colors:**
- ✅ Color palette matches carousel_brief.md exactly
- ✅ No random colors introduced
- ✅ Consistent use of primary, secondary, accent colors

### Brand Integrity

**Logo:**
- ✅ Appears on every slide
- ✅ Same size and position throughout
- ✅ High resolution (not pixelated)

**Voice:**
- ✅ Copy matches brand voice from intelligence_report.md
- ✅ Tone is consistent across all slides

## Step 3.4 — Export

Generate three deliverable formats:

### 1. Individual Slide PNGs (numbered in order)

**Naming convention:**
- `slide_01_cover.png`
- `slide_02.png`
- `slide_03.png`
- ...
- `slide_09_cta.png`
- `slide_10_brand.png` (if applicable)

**Specifications:**
- Format: PNG (lossless)
- Dimensions: 1080x1080px
- Color space: sRGB
- Compression: None or minimal

### 2. Combined PDF: carousel_final.pdf

Combine all slides into a single PDF for easy review:

```bash
# Using ImageMagick (if available)
convert slide_*.png carousel_final.pdf

# Or using Python PIL
python3 scripts/combine_slides_to_pdf.py
```

**PDF specifications:**
- Page size: 1080x1080px
- One slide per page
- Maintain exact colors and resolution

### 3. Preview Strip: mockup_preview.png

Create a horizontal preview showing first 3-4 slides side-by-side:

**Purpose:** Quick visual preview of the carousel flow

**Dimensions:** 3240x1080px (3 slides) or 4320x1080px (4 slides)

```bash
# Using ImageMagick
convert slide_01_cover.png slide_02.png slide_03.png +append mockup_preview.png
```

## Output Files

Save all files to workspace:

```
carousel_[business-name]_[date]/
├── slide_01_cover.png
├── slide_02.png
├── slide_03.png
├── slide_04.png
├── slide_05.png
├── slide_06.png
├── slide_07.png
├── slide_08_takeaway.png
├── slide_09_cta.png
├── slide_10_brand.png (optional)
├── carousel_final.pdf
└── mockup_preview.png
```

All files ready for Phase 4 (Instagram Publishing).
