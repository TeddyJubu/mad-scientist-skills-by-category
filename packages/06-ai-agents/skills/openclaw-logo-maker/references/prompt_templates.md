# OpenCLAW Logo Maker — Prompt Templates Reference

Full detailed prompt templates used by `generate_logos.py`. Each template is a carefully engineered prompt designed to produce a specific, distinct logo style from the Gemini 3.1 Flash Preview API.

---

## Global Parameters Injected Into Every Prompt

Every prompt automatically receives:
- **Brand Name** — Company/brand name
- **Industry/Niche** — What the brand does
- **Color Palette** — User-provided hex/named colors
- **Brand Personality** — Adjectives describing the feel
- **Optional Tagline** — If provided by user

---

## Style 1: 3D Premium

**Personality:** Sophisticated, dimensional, polished, modern luxury tech

**Core Prompt Elements:**
- Dimensional rendering with depth, soft shadows, polished surfaces
- Rich gradients with gold/platinum highlights
- Modern luxury tech aesthetic
- Photorealistic material rendering

**Ideal For:** Tech companies, AI platforms, premium agencies, SaaS brands

---

## Style 2: Dynamic Gradient

**Personality:** Bold, energetic, forward-motion, sleek modern

**Core Prompt Elements:**
- Bold color transitions from deep to bright tones
- Forward-motion feel, energetic but professional
- Abstract swooshes, motion trails, layered shapes
- Seamless color blends, high-energy visual impact

**Ideal For:** Startups, apps, creative agencies, fitness/performance brands

---

## Style 3: Geometric Abstract

**Personality:** Intelligent, structured, precise, forward-thinking

**Core Prompt Elements:**
- Clean geometric shapes — triangles, hexagons, intersecting lines
- Polygons or tessellated patterns
- Mathematical precision, minimalist execution
- Sharp edges, perfect alignment

**Ideal For:** AI companies, engineering firms, tech consultancies, data companies

---

## Style 4: Luxury Minimal

**Personality:** Understated elegance, refined, premium, timeless

**Core Prompt Elements:**
- Thin clean lines, maximum whitespace
- Muted gold, charcoal, cream, sophisticated dark tones
- High-end fashion house / private bank aesthetic
- Elegant restraint, flawless typography

**Ideal For:** Wealth management, luxury goods, high-end professional services, private equity

---

## Style 5: Modern Flat

**Personality:** Friendly, professional, approachable, credible

**Core Prompt Elements:**
- Clean 2D illustration, solid fills
- No gradients, no shadows
- Works from favicon to billboard
- Two-tone or three-tone palette

**Ideal For:** Any industry — highly versatile, universally scalable

---

## Style 6: Futuristic Tech

**Personality:** Cutting-edge, AI-powered, data-driven, next-gen

**Core Prompt Elements:**
- Sharp angles, circuit-inspired line work
- Circuit board motifs, data stream aesthetics
- Neon accents on dark OR sharp bright tones on white
- Precision line work, technical aesthetic

**Ideal For:** AI companies, cybersecurity, blockchain, deep tech, robotics

---

## Style 7: Iconic Monogram

**Personality:** Sophisticated, distinctive, timeless, memorable

**Core Prompt Elements:**
- Elegant letter-based mark using initials or stylized letterform
- Interlocking letters, negative space, or layered typography
- Luxury fashion house adaptation
- Instantly recognizable as a symbol

**Ideal For:** Brands with multi-word names, luxury brands, professional firms, media companies

---

## Style 8: Nature-Inspired

**Personality:** Organic, growth-oriented, sustainable, professional

**Core Prompt Elements:**
- Organic shapes, leaf motifs, subtle botanical elements
- Flowing curves, growth imagery
- Earth tones, organic greens, warm browns
- Premium sustainable brand aesthetic (not whimsical)

**Ideal For:** Real estate, architecture, sustainability, organic brands, wellness

---

## Style 9: Heritage-Classic

**Personality:** Established, trustworthy, traditional, old-money

**Core Prompt Elements:**
- Traditional palette: navy, burgundy, gold, cream, forest green
- Emblems, crests, or refined traditional wordmark
- Strong typographic hierarchy
- Iconic financial institution or century-old professional firm feel

**Ideal For:** Law firms, accounting, banks, manufacturing, established RE firms

---

## Style 10: Abstract Dynamic

**Personality:** Creative, trend-forward, distinctive, conversation-starting

**Core Prompt Elements:**
- Custom blend of modern trends
- Glitch effects, isometric shapes, liquid gradients, or collage-style
- Vibrant, trend-forward palette
- Most unique and distinctive of all variations

**Ideal For:** Creative agencies, art studios, innovative startups, brands that want to stand out completely

---

## Prompt Engineering Notes

### What Makes These Prompts Effective

1. **Style signals are explicit** — each prompt names the aesthetic and gives concrete visual references
2. **Color context is precise** — hex codes and named palettes guide accurate rendering
3. **Background is always specified** — "fully transparent" is included in every prompt
4. **Negative space is respected** — "centered, clean composition" ensures usable framing
5. **Output format is clear** — "square aspect ratio" keeps all logos consistent
6. **Quality bar is set** — "ultra-high resolution," "pixel-perfect," "photorealistic" sets expectations

### If Results Are Too Similar

If two styles are producing similar outputs, increase the distinctiveness by:
- Adding a specific visual reference (e.g., "inspired by Bauhaus geometry")
- Naming a competitor or iconic brand as a reference point
- Adding more specific negative guidance ("avoid rounded corners entirely")

### If a Style Keeps Failing

Common fixes:
- 3D/Premium fails → simplify to "clean modern logo with subtle depth"
- Geometric fails → reduce shape complexity in the prompt
- Nature-inspired looks cartoony → add "professional, not whimsical"
- Abstract dynamic looks messy → specify fewer trends ("isometric only")

---

*Part of OpenCLAW Logo Maker Skill — James for Charles (The Mad Scientist) • April 2026*
