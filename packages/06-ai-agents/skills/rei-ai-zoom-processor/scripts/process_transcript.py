#!/usr/bin/env python3.11
"""
REI AI Zoom Processor
Processes a Zoom (or any video) transcript using an LLM to generate:
  1. A concise summary
  2. Timestamped key topic bullet points
  3. A resource/URL extraction list

Outputs:
  - transcript_output.txt  (raw structured text)
  - transcript_summary.md  (formatted Markdown)
  - transcript_summary.pdf (PDF via manus-md-to-pdf)

Optional: Google Doc creation if credentials.json is present.
"""

import argparse
import os
import subprocess
from openai import OpenAI

client = OpenAI()

def llm(prompt, model="gpt-4o-mini"):
    """Call the LLM and return the response text."""
    try:
        completion = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant that processes video transcripts."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Error calling LLM: {e}"


def generate_summary(transcript):
    return llm(f"""Write a single concise paragraph summarizing the key topics and arguments in this transcript.

Transcript:
'''
{transcript}
'''""")


def generate_bullet_points(transcript):
    return llm(f"""Analyze this transcript and identify 8-12 main topics or key points.
For each, write a bullet point starting with its timestamp (e.g. [MM:SS]).
Format: • [MM:SS] – Topic Title: brief description

Transcript:
'''
{transcript}
'''""")


def extract_resources(transcript):
    return llm(f"""From this transcript:
1. Extract all explicit URLs mentioned.
2. Identify companies, products, tools, and services mentioned by name and provide their primary website URL.

Return a clean bullet list in the format:
• Name – https://url.com

Transcript:
'''
{transcript}
'''""")


def infer_title(transcript):
    """Use first non-empty line or ask LLM for a title."""
    for line in transcript.splitlines():
        line = line.strip()
        if line and not line.startswith(('[', '(')):
            if len(line) < 120:
                return line
    return llm(f"Give a short, descriptive title (max 10 words) for this transcript:\n\n{transcript[:1000]}")


def write_markdown(title, source_hint, summary, bullets, resources, output_path):
    source_line = f"\n**Source:** {source_hint}\n" if source_hint else ""
    md = f"""# {title}
{source_line}
---

## Summary

{summary}

---

## Key Topics with Timestamps

{bullets}

---

## Resources

{resources}
"""
    with open(output_path, "w") as f:
        f.write(md)
    print(f"Markdown saved: {output_path}")


def write_text(title, summary, bullets, resources, output_path):
    content = f"""TITLE: {title}

{'='*60}
SUMMARY
{'='*60}
{summary}

{'='*60}
KEY TOPICS WITH TIMESTAMPS
{'='*60}
{bullets}

{'='*60}
RESOURCES
{'='*60}
{resources}
"""
    with open(output_path, "w") as f:
        f.write(content)
    print(f"Text output saved: {output_path}")


def convert_to_pdf(md_path, pdf_path):
    result = subprocess.run(
        ["pandoc", md_path, "-o", pdf_path, "--pdf-engine=weasyprint"],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"PDF saved: {pdf_path}")
    else:
        print(f"PDF conversion failed: {result.stderr}")


def create_google_doc(title, summary, bullets, resources):
    """Optional: create a Google Doc if credentials.json is available."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
        from googleapiclient.errors import HttpError
    except ImportError:
        print("Google API libraries not installed. Skipping Google Doc creation.")
        return

    SCOPES = ["https://www.googleapis.com/auth/documents"]
    skill_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    token_path = os.path.join(skill_dir, "token.json")
    creds_path = os.path.join(skill_dir, "credentials.json")

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                print("credentials.json not found — skipping Google Doc creation.")
                return
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    try:
        service = build("docs", "v1", credentials=creds)
        doc = service.documents().create(body={"title": title}).execute()
        doc_id = doc.get("documentId")

        full_text = f"Summary\n{summary}\n\nKey Topics\n{bullets}\n\nResources\n{resources}"
        requests = [
            {"insertText": {"location": {"index": 1}, "text": full_text}},
            {"updateParagraphStyle": {
                "range": {"startIndex": 1, "endIndex": 8},
                "paragraphStyle": {"namedStyleType": "HEADING_1"},
                "fields": "namedStyleType"
            }},
        ]
        service.documents().batchUpdate(documentId=doc_id, body={"requests": requests}).execute()
        print(f"Google Doc created: https://docs.google.com/document/d/{doc_id}/")
    except Exception as e:
        print(f"Google Doc creation failed: {e}")


def main():
    parser = argparse.ArgumentParser(description="Process a Zoom/video transcript and generate summary documents.")
    parser.add_argument("transcript_file", help="Path to the transcript .txt file.")
    parser.add_argument("--output-dir", default=None, help="Directory for output files (default: same as transcript).")
    parser.add_argument("--google-doc", action="store_true", help="Also attempt to create a Google Doc.")
    args = parser.parse_args()

    if not os.path.exists(args.transcript_file):
        print(f"Error: File not found: {args.transcript_file}")
        return

    with open(args.transcript_file, "r") as f:
        transcript = f.read()

    out_dir = args.output_dir or os.path.dirname(os.path.abspath(args.transcript_file))
    os.makedirs(out_dir, exist_ok=True)

    print("Inferring title...")
    title = infer_title(transcript)

    print("Generating summary...")
    summary = generate_summary(transcript)

    print("Generating timestamped bullet points...")
    bullets = generate_bullet_points(transcript)

    print("Extracting resources...")
    resources = extract_resources(transcript)

    # Detect source URL hint from transcript
    source_hint = ""
    for line in transcript.splitlines()[:10]:
        if "youtube.com" in line or "http" in line:
            source_hint = line.strip()
            break

    # Write outputs
    txt_path = os.path.join(out_dir, "transcript_output.txt")
    md_path = os.path.join(out_dir, "transcript_summary.md")
    pdf_path = os.path.join(out_dir, "transcript_summary.pdf")

    write_text(title, summary, bullets, resources, txt_path)
    write_markdown(title, source_hint, summary, bullets, resources, md_path)
    convert_to_pdf(md_path, pdf_path)

    if args.google_doc:
        print("Attempting Google Doc creation...")
        create_google_doc(title, summary, bullets, resources)

    print("\nDone! Output files:")
    print(f"  Text:     {txt_path}")
    print(f"  Markdown: {md_path}")
    print(f"  PDF:      {pdf_path}")


if __name__ == "__main__":
    main()
