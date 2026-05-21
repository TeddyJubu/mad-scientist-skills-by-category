# Image Graphics Skills
**Package:** `@mad-scientist/image-graphics` | **6 Skills** | Version 1.0.0

---

## What This Package Does

Image generation, editing, design, avatars, video, and visual production

## Skills In This Package

### 1. gemini-image-editor
**Folder:** `skills/gemini-image-editor`

Edit, enhance, remove objects, change backgrounds, and transform images using Google AI Studio Gemini Nano Banana Pro (Imagen 3). Use when you need to edit existing images, remove backgrounds, swap objects, change lighting, add/remove elements, or apply artistic transformations.

### 2. Graphic Design
**Folder:** `skills/graphic-design`

Support design understanding from basic visuals to professional production and theory.

### 3. heygen-avatar-video
**Folder:** `skills/heygen-avatar-video`

heygen-avatar-video lets the user generate AI avatar talking-head videos using Charles Blair's custom HeyGen avatar, which is useful when they want to create UGC-style content for TikTok, Reels, or YouTube without filming, produce consistent on-brand video content at scale, or quickly turn a script into a finished talking-head video.

### 4. nano-banana-image-gen
**Folder:** `skills/nano-banana-image-gen`

Generate images using Gemini 3.1 Flash (gemini-3.1-flash-image-preview) — the nano-banana model. Use for thumbnails, infographics, social graphics, and any image generation task. Always use this instead of the image_generate tool (FLUX). Supports reference image input for face/style matching.

### 5. nano-banana-pro
**Folder:** `skills/nano-banana-pro`

Generate/edit images with Nano Banana Pro (Gemini 3 Pro Image). Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 1K/2K/4K; use --input-image.

### 6. remotion
**Folder:** `skills/remotion`

Programmatic video creation using React. Use this skill when you need to create, edit, or render videos using code, leverage Remotion's React-based framework for animations, or manage data-driven video production. Triggers on "Remotion", "programmatic video", "render video with react", or requests to create videos via code.

## Agent Install

```bash
npm install @mad-scientist/image-graphics
```

Or copy the `skills/` directory into your agent skills root.

## License

Proprietary - (c) 2026 Mad Scientist LLC. All rights reserved.
