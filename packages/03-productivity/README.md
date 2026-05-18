# Productivity Skills
**Package:** `@mad-scientist/productivity` | **9 Skills** | Version 1.0.0

---

## What This Package Does For You

This package connects your AI agent to all the productivity tools you already use — Notion for notes and documents, Gmail for email, Google Drive for file storage, PDF generation, and the ability to send files and reports straight to your phone via Telegram.

Instead of switching between apps, you just tell your AI what you need in plain English. "Save this meeting notes to my Notion project tracker." "Email this report to my contractor." "Generate a PDF of this proposal." It gets done.

---

## Skills In This Package

### 1. Notion Mastery
**What it does:** Your AI agent can read, create, and update pages in Notion — your notes, databases, project trackers, and documents. It can pull information from Notion when you ask, and save new information there automatically.

**What to say:**  
> "Add a new row to my deals pipeline in Notion with the address 123 Main St, offer price $85,000, and status 'Under Review'"
> "What's in my 'Hot Leads' Notion database right now?"

**What you get:** Notion pages updated in real time, or data pulled from your Notion databases and displayed to you.

---

### 2. Notion CLI
**What it does:** A command-line interface for Notion that handles complex operations — bulk imports, database queries, page migrations, and batch updates. For power users who need to move a lot of data in and out of Notion.

**What to say:**  
> "Import this CSV of 50 properties into my Notion deals database"

**What you get:** All 50 rows appear in your Notion database, properly formatted with all columns populated.

---

### 3. Notion Beautiful Systems
**What it does:** Creates beautifully designed Notion pages with proper structure — tables of contents, callout boxes, toggles, embedded images, and clean formatting. Use this when you want a Notion page that looks professional and is easy to navigate.

**What to say:**  
> "Build me a Notion page for my property due diligence process — make it clean with sections for inspection, title, financing, and closing"

**What you get:** A fully formatted Notion page with a table of contents, section dividers, and clean layouts — published and linked.

---

### 4. File Delivery (Telegram + Google Drive)
**What it does:** Takes any file — PDF, image, spreadsheet, document — and sends it directly to your Telegram app or uploads it to your Google Drive. Perfect for reports that need to be in your hands immediately.

**What to say:**  
> "Send the rehab estimate PDF to my Telegram and also upload it to my Google Drive 'Property Reports' folder"

**What you get:** File arrives in your Telegram chat instantly and a Drive link appears in your requested folder.

---

### 5. Agentmail
**What it does:** Gives your AI agent its own email inbox so it can send and receive emails on your behalf. It can read incoming emails, respond to routine inquiries, and send reports or files to anyone you specify.

**What to say:**  
> "Email the monthly deal summary to my accountant at john@accountant.com and CC myself at charles@email.com"

**What you get:** Email sent with the report attached, with a copy saved in your sent folder.

---

### 6. Gmail Unread Auto-Draft
**What it does:** Scans your Gmail unread messages and drafts responses for you to review. Great for staying on top of your inbox when you get too many emails to answer individually.

**What to say:**  
> "Draft replies to all my unread emails from today"

**What you get:** A list of draft replies — one for each unread email — ready for you to review and send with one click.

---

### 7. Google Workspace (Gog)
**What it does:** Connects to your full Google Workspace — Gmail, Google Calendar, Google Drive, and Google Contacts. Your AI can schedule meetings, check your calendar, find files, and manage your Google apps.

**What to say:**  
> "What's on my calendar tomorrow? And find the most recent spreadsheet in my Google Drive called 'Deal Analysis'"

**What you get:** Your calendar for tomorrow listed out, and a direct link to the most recent matching spreadsheet.

---

### 8. PDF Generation
**What it does:** Takes any content — a report, a proposal, a contract summary, a property analysis — and converts it into a professional PDF file. Sends it to Telegram or emails it automatically.

**What to say:**  
> "Generate a PDF of this property analysis and send it to my phone"

**What you get:** A clean, formatted PDF file delivered to your Telegram chat, ready to forward or print.

---

### 9. FileBrowser Deploy
**What it does:** Sets up a web-based file manager (FileBrowser) on your server so you can browse, upload, and download files through a web interface instead of using FTP or command line.

**What to say:**  
> "Set up a file browser at files.mysite.com so I can access my server files from any browser"

**What you get:** A secure, password-protected web interface at your chosen URL for managing server files.

---

## How To Use This Package

### Installation
```bash
npm install @mad-scientist/productivity
```

Or symlink into your Hermes skills folder:
```bash
ln -s $(pwd)/skills ~/.hermes/skills/productivity
```

### Quick Start
```
skill_view(name="notion-mastery")
skill_view(name="file-delivery")
skill_view(name="pdf-generation")
```

---

## What To Expect

| Skill | Time to Result | Best For |
|-------|---------------|----------|
| Notion Mastery | 5-20 seconds | Read/write Notion |
| Notion CLI | 10-60 seconds | Bulk Notion operations |
| Notion Beautiful Systems | 1-2 minutes | Professional Notion pages |
| File Delivery | 5-15 seconds | Send files to Telegram/Drive |
| Agentmail | 10-30 seconds | Send/receive email |
| Gmail Auto-Draft | 15-45 seconds | Batch email responses |
| Google Workspace | 5-15 seconds | Calendar, Drive, Contacts |
| PDF Generation | 10-30 seconds | Create PDF reports |
| FileBrowser Deploy | 2-5 minutes | Web file manager setup |

---

## License

Proprietary — © 2026 Mad Scientist LLC. All rights reserved. Internal use only.
