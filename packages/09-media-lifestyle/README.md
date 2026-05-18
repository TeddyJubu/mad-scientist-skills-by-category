# Media & Lifestyle Skills
**Package:** `@mad-scientist/media-lifestyle` | **10 Skills** | Version 1.0.0

---

## What This Package Does For You

This package connects your AI to the media and lifestyle tools you use every day — YouTube, Spotify, weather services, health tracking, and more. It's the package that turns your AI from a work tool into a helpful daily companion.

Play music, check the weather, track your water and sleep, transcribe videos, and get weather-aware automations — all through conversation.

---

## Skills In This Package

### 1. YouTube Content
**What it does:** Manages your YouTube channel — pulls video data, gets channel statistics, monitors comments, and can help with content research and title optimization.

**What to say:**  
> "What's the view count on my 5 most recent YouTube videos and which one performed best?"

**What you get:** Your video stats broken down, with a ranking of your best-performing recent content.

---

### 2. Video Frames
**What it does:** Extracts individual frames or short clips from any video file. Useful for creating thumbnails, extracting screenshots for social posts, or saving a specific moment.

**What to say:**  
> "Extract 5 dramatic frames from this property walkthrough video for use as social media posts"

**What you get:** 5 image files — one for each extracted frame — ready to post or use in graphics.

---

### 3. YouTube Content (Claude Video)
**What it does:** Uses Claude to watch and analyze YouTube videos — understands the content, answers questions about what's in the video, and can extract specific information.

**What to say:**  
> "Watch this YouTube video and tell me the 3 main points the speaker makes about finding off-market deals"

**What you get:** A plain-English summary of the video's key points, no need to watch it yourself.

---

### 4. Spotify Control
**What it does:** Controls Spotify playback — play specific songs, pause, skip, adjust volume, search for playlists, and get currently playing info. Your AI DJ.

**What to say:**  
> "Play my 'Focus Flow' playlist on Spotify and tell me what's currently playing"
> "Skip to the next song"

**What you get:** Music plays, and you get the track name, artist, album art, and a link to the current song.

---

### 5. Weather
**What it does:** Gets current weather and forecasts for any location — useful for property inspections, outdoor listing photos, or automations that need to know tomorrow's weather.

**What to say:**  
> "What's the weather going to be like in Baltimore this weekend — I have a property inspection scheduled for Saturday"

**What you get:** A forecast with temperature, rain probability, wind, and any weather advisories.

---

### 6. Healthcheck
**What it does:** Tracks your personal health metrics — water intake, sleep hours, and any custom tracking you want to set up. Stores data over time so you can see trends.

**What to say:**  
> "Log that I drank 3 glasses of water and slept 7 hours last night"
> "Give me a summary of my water and sleep for the past week"

**What you get:** Your health log updated, or a weekly summary showing your hydration and sleep trends.

---

### 7. GIF Search
**What it does:** Searches for GIFs on Tenor and returns the direct link — for adding personality to your social posts, texts, or presentations.

**What to say:**  
> "Find a GIF of a celebrate confetti for my 'Deal Closed!' social post"

**What you get:** A GIF file or direct link, ready to paste into your social post or message.

---

### 8. Songsee (Audio Analysis)
**What it does:** Analyzes audio files — extracts musical features like tempo, key, mood, and spectrograms. Useful for understanding the energy profile of music for background use in videos.

**What to say:**  
> "Analyze this royalty-free background track and tell me its tempo and mood for use in a real estate explainer video"

**What you get:** A breakdown of the track's tempo (BPM), musical key, energy level, and recommended use cases.

---

### 9. Heartmula (AI Music Generation)
**What it does:** Generates original music from a text description — describe the mood, genre, instruments, and tempo and it creates a unique audio track. For video soundtracks, hold music, or any project that needs original music.

**What to say:**  
> "Generate a 30-second upbeat instrumental track with acoustic guitar and piano for a real estate promotional video"

**What you get:** An audio file of the generated music, ready to use in your video.

---

### 10. Fish Audio TTS
**What it does:** Text-to-speech — converts any text into a natural-sounding voice audio file. For adding voiceovers to videos, creating podcast intros, or narrated documents.

**What to say:**  
> "Convert this property description to a natural-sounding voiceover: 'Beautiful 3-bedroom ranch in sought-after Glen Burnie...'"

**What you get:** An MP3 audio file of the text read aloud in a clear, natural voice.

---

## How To Use This Package

### Installation
```bash
npm install @mad-scientist/media-lifestyle
```

Or symlink into your Hermes skills folder:
```bash
ln -s $(pwd)/skills ~/.hermes/skills/media-lifestyle
```

### Quick Start
```
skill_view(name="weather")
skill_view(name="spotify")
skill_view(name="youtube-content")
```

---

## What To Expect

| Skill | Time to Result | Best For |
|-------|---------------|----------|
| YouTube Content | 5-15 seconds | Channel stats & research |
| Video Frames | 10-30 seconds | Extract screenshots |
| Claude Video | 15-30 seconds | Understand any YouTube video |
| Spotify Control | 5-10 seconds | Play music, skip songs |
| Weather | 5-10 seconds | Forecasts any location |
| Healthcheck | 5-10 seconds | Water & sleep tracking |
| GIF Search | 5-10 seconds | Find GIFs for posts |
| Songsee | 10-20 seconds | Audio analysis |
| Heartmula | 1-3 minutes | AI music generation |
| Fish Audio TTS | 10-30 seconds | Text to voiceover |

---

## License

Proprietary — © 2026 Mad Scientist LLC. All rights reserved. Internal use only.
