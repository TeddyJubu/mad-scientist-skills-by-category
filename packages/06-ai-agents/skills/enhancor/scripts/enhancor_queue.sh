#!/usr/bin/env bash
# enhancor_queue.sh — Submit a video generation job to Seedance/Enhancor API
# Usage: ./enhancor_queue.sh [options]
#
# Required:
#   --type image-to-video|text-to-video
#   --webhook-url URL
#   --prompt "scene description" (required unless --mode multi_frame)
#
# For image-to-video also:
#   --mode ugc|multi_reference|extend|multi_frame|lipsyncing|voice_clone|first_n_last_frames
#
# Media (mode-dependent):
#   --product-url URL          (ugc mode, repeatable, max 9 total with influencers+images)
#   --influencer-url URL       (ugc mode, repeatable, max 9 total)
#   --image-url URL            (non-ugc modes, repeatable, max 9)
#   --video-url URL            (non-ugc modes, repeatable, max 3, combined <15s)
#   --audio-url URL            (non-ugc modes, repeatable, max 3, combined <15s)
#   --first-frame-url URL      (first_n_last_frames mode)
#   --last-frame-url URL       (first_n_last_frames mode)
#   --lipsync-audio-url URL    (lipsyncing / voice_clone mode)
#
# Multi-frame scenes:
#   --scene "prompt" --scene-duration N  (multi_frame mode, repeatable)
#
# Settings:
#   --duration 4-15
#   --resolution 480p|720p|1080p
#   --aspect-ratio 16:9|9:16|4:3|3:4|1:1|21:9
#   --fast-mode true|false
#   --full-access true|false

set -e

API_KEY="${ENHANCOR_API_KEY:-3778dcad6b8406f39e1ed08bdbab27930a5bdaace4e555b02617ff57224072c7}"
BASE_URL="https://apireq.enhancor.ai/api/enhancor-ugc-full-access/v1"

# Defaults
TYPE="image-to-video"
MODE="ugc"
DURATION="5"
RESOLUTION="480p"
ASPECT_RATIO="16:9"
FAST_MODE="false"
FULL_ACCESS="false"
WEBHOOK_URL=""

# Arrays for repeatable params
PRODUCT_URLS=()
INFLUENCER_URLS=()
IMAGE_URLS=()
VIDEO_URLS=()
AUDIO_URLS=()
SCENE_PROMPTS=()
SCENE_DURATIONS=()

usage() {
  echo "Usage: $0 \\"
  echo "  --type image-to-video|text-to-video \\"
  echo "  --mode ugc|multi_reference|extend|multi_frame|lipsyncing|voice_clone|first_n_last_frames \\"
  echo "  --prompt 'Scene description' \\"
  echo "  --webhook-url 'https://your-server.com/webhook' \\"
  echo "  [--duration 4-15] \\"
  echo "  [--resolution 480p|720p|1080p] \\"
  echo "  [--aspect-ratio 16:9|9:16|4:3|3:4|1:1|21:9] \\"
  echo "  [--fast-mode true|false] \\"
  echo "  [--full-access true|false] \\"
  echo "  [--product-url URL] (ugc, repeatable) \\"
  echo "  [--influencer-url URL] (ugc, repeatable) \\"
  echo "  [--image-url URL] (non-ugc, repeatable) \\"
  echo "  [--video-url URL] (non-ugc, repeatable) \\"
  echo "  [--audio-url URL] (non-ugc, repeatable) \\"
  echo "  [--first-frame-url URL] (first_n_last_frames) \\"
  echo "  [--last-frame-url URL] (first_n_last_frames) \\"
  echo "  [--lipsync-audio-url URL] (lipsyncing/voice_clone) \\"
  echo "  [--scene 'prompt' --scene-duration N] (multi_frame, repeatable)"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case $1 in
    --type) TYPE="$2"; shift 2 ;;
    --mode) MODE="$2"; shift 2 ;;
    --prompt) PROMPT="$2"; shift 2 ;;
    --webhook-url) WEBHOOK_URL="$2"; shift 2 ;;
    --duration) DURATION="$2"; shift 2 ;;
    --resolution) RESOLUTION="$2"; shift 2 ;;
    --aspect-ratio) ASPECT_RATIO="$2"; shift 2 ;;
    --fast-mode) FAST_MODE="$2"; shift 2 ;;
    --full-access) FULL_ACCESS="$2"; shift 2 ;;
    --product-url) PRODUCT_URLS+=("$2"); shift 2 ;;
    --influencer-url) INFLUENCER_URLS+=("$2"); shift 2 ;;
    --image-url) IMAGE_URLS+=("$2"); shift 2 ;;
    --video-url) VIDEO_URLS+=("$2"); shift 2 ;;
    --audio-url) AUDIO_URLS+=("$2"); shift 2 ;;
    --first-frame-url) FIRST_FRAME_URL="$2"; shift 2 ;;
    --last-frame-url) LAST_FRAME_URL="$2"; shift 2 ;;
    --lipsync-audio-url) LIPSYNC_AUDIO_URL="$2"; shift 2 ;;
    --scene)
      SCENE_PROMPTS+=("$2")
      # Look ahead for --scene-duration
      if [[ $# -ge 2 && "${2:-}" != --* && "${3:-}" == "--scene-duration" ]]; then
        SCENE_DURATIONS+=("$4")
        shift 3
      else
        echo "Error: --scene requires --scene-duration after it"
        usage
      fi
      ;;
    *) echo "Unknown option: $1"; usage ;;
  esac
done

if [[ -z "$WEBHOOK_URL" ]]; then
  echo "Error: --webhook-url is required"
  usage
fi

if [[ -z "$PROMPT" && "$MODE" != "multi_frame" ]]; then
  echo "Error: --prompt is required (unless mode is multi_frame)"
  usage
fi

# ─── Build base JSON ────────────────────────────────────────────────────────
BODY=$(jq -n \
  --arg type "$TYPE" \
  --arg mode "$MODE" \
  --arg duration "$DURATION" \
  --arg resolution "$RESOLUTION" \
  --arg aspect_ratio "$ASPECT_RATIO" \
  --arg fast_mode "$FAST_MODE" \
  --arg full_access "$FULL_ACCESS" \
  --arg webhook_url "$WEBHOOK_URL" \
  '{
    type: $type,
    mode: $mode,
    duration: $duration | tonumber,
    resolution: $resolution,
    aspect_ratio: $aspect_ratio,
    fast_mode: ($fast_mode == "true"),
    full_access: ($full_access == "true"),
    webhook_url: $webhook_url
  }')

# Add prompt if provided
[[ -n "$PROMPT" ]] && BODY=$(echo "$BODY" | jq --arg prompt "$PROMPT" '. + {prompt: $prompt}')

# ─── UGC mode: products + influencers ────────────────────────────────────
if [[ "$MODE" == "ugc" ]]; then
  [[ ${#PRODUCT_URLS[@]} -gt 0 ]] && {
    JSON=$(printf '%s\n' "${PRODUCT_URLS[@]}" | jq -R . | jq -s .)
    BODY=$(echo "$BODY" | jq --argjson products "$JSON" '. + {products: $products}')
  }
  [[ ${#INFLUENCER_URLS[@]} -gt 0 ]] && {
    JSON=$(printf '%s\n' "${INFLUENCER_URLS[@]}" | jq -R . | jq -s .)
    BODY=$(echo "$BODY" | jq --argjson influencers "$JSON" '. + {influencers: $influencers}')
  }
fi

# ─── Non-ugc mode: images, videos, audios ─────────────────────────────────
if [[ "$MODE" != "ugc" ]]; then
  [[ ${#IMAGE_URLS[@]} -gt 0 ]] && {
    JSON=$(printf '%s\n' "${IMAGE_URLS[@]}" | jq -R . | jq -s .)
    BODY=$(echo "$BODY" | jq --argjson images "$JSON" '. + {images: $images}')
  }
  [[ ${#VIDEO_URLS[@]} -gt 0 ]] && {
    JSON=$(printf '%s\n' "${VIDEO_URLS[@]}" | jq -R . | jq -s .)
    BODY=$(echo "$BODY" | jq --argjson videos "$JSON" '. + {videos: $videos}')
  }
  [[ ${#AUDIO_URLS[@]} -gt 0 ]] && {
    JSON=$(printf '%s\n' "${AUDIO_URLS[@]}" | jq -R . | jq -s .)
    BODY=$(echo "$BODY" | jq --argjson audios "$JSON" '. + {audios: $audios}')
  }
fi

# ─── Mode-specific fields ───────────────────────────────────────────────────
[[ -n "$FIRST_FRAME_URL" ]] && BODY=$(echo "$BODY" | jq --arg first_frame_image "$FIRST_FRAME_URL" '. + {first_frame_image: $first_frame_image}')
[[ -n "$LAST_FRAME_URL" ]]  && BODY=$(echo "$BODY" | jq --arg last_frame_image "$LAST_FRAME_URL" '. + {last_frame_image: $last_frame_image}')
[[ -n "$LIPSYNC_AUDIO_URL" ]] && BODY=$(echo "$BODY" | jq --arg lipsyncing_audio "$LIPSYNC_AUDIO_URL" '. + {lipsyncing_audio: $lipsyncing_audio}')

# ─── Multi-frame scenes ─────────────────────────────────────────────────────
if [[ "$MODE" == "multi_frame" && ${#SCENE_PROMPTS[@]} -gt 0 ]]; then
  FRAMES_JSON="["
  for i in $(seq 0 $((${#SCENE_PROMPTS[@]} - 1))); do
    DUR="${SCENE_DURATIONS[$i]:-5}"
    PROMPT_ESC="${SCENE_PROMPTS[$i]}"
    FRAMES_JSON+=$(jq -n --arg prompt "$PROMPT_ESC" --arg duration "$DUR" \
      '{prompt: $prompt, duration: ($duration | tonumber)}')
    [[ $i -lt $((${#SCENE_PROMPTS[@]} - 1)) ]] && FRAMES_JSON+=","
  done
  FRAMES_JSON+="]"
  BODY=$(echo "$BODY" | jq --argjson multi_frame_prompts "$FRAMES_JSON" '. + {multi_frame_prompts: $multi_frame_prompts}')
fi

# ─── Submit ─────────────────────────────────────────────────────────────────
echo "Submitting to Seedance/Enhancor..."
echo "Type: $TYPE | Mode: $MODE | Duration: ${DURATION}s | Resolution: $RESOLUTION | Aspect: $ASPECT_RATIO"
[[ -n "$PROMPT" ]] && echo "Prompt: $PROMPT"

RESPONSE=$(curl -s -X POST "${BASE_URL}/queue" \
  -H "x-api-key: ${API_KEY}" \
  -H "Content-Type: application/json" \
  -d "$BODY")

SUCCESS=$(echo "$RESPONSE" | jq -r '.success // empty')
REQUEST_ID=$(echo "$RESPONSE" | jq -r '.requestId // empty')

if [[ "$SUCCESS" == "true" && -n "$REQUEST_ID" ]]; then
  echo "✅ Job queued!"
  echo "Request ID: $REQUEST_ID"
  echo ""
  echo "Poll status with:"
  echo "  ./enhancor_status.sh --request-id $REQUEST_ID"
else
  echo "❌ Submission failed:"
  echo "$RESPONSE" | jq .
  exit 1
fi
