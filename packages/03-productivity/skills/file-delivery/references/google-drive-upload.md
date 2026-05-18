---
name: google-drive-image-upload
description: Upload generated images to Charles's Google Drive folder for permanent backup
---

⚠️ **Deprecated.** See SKILL.md for the current decision tree — Telegram first, always.



---

## Google Drive Image Upload (variant)

**When the user specifically wants to upload generated images to Google Drive instead of Telegram.**

### Trigger Phrases
- "upload to Google Drive"
- "save to my Drive"
- "put this in Google Drive"

### Google Drive Upload (via Drive API)

```bash
# Install google-drive-upload CLI
curl -fsSL https://github.com/gimite/google-drive-upload/releases/latest/download/google-drive-upload-linux-amd64.sh | bash

# Authenticate (one-time, stores in ~/.gdrive/)
google-drive-upload --path-prefix "/Hermes Generated Images"

# Upload a file
google-drive-upload "/path/to/image.png"
```

### Alternative: rclone

```bash
# Configure rclone with Google Drive
rclone config create gdrive drive

# Upload
rclone copy /path/to/image.png gdrive:/Hermes\ Generated\ Images/
```

### Skill Reference
The full `google-drive-image-upload` skill content is preserved in `references/google-drive-upload.md` for detailed API configuration and troubleshooting.
