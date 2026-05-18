#!/usr/bin/env python3
"""Coach-check a ListingLens Studio agent image job.

Reads JSON from --file or stdin and returns plain-language reminders instead
of rejecting non-technical users for incomplete packets.
"""

from __future__ import annotations

import argparse
import json
import sys
from typing import Any


PUBLISHABLE_USE_TYPES = {
    "listing",
    "agent_marketing",
    "brokerage",
    "mls",
    "rental_platform",
    "paid_ad",
}

VALID_JOB_TYPES = {"generate", "edit", "mask_edit", "composite", "qa_only"}

POPULAR_AGENT_RUNTIMES = {
    "chatgpt",
    "codex",
    "hermes",
    "openclaw",
    "manus",
    "genspark",
    "claude",
    "gemini",
    "perplexity",
    "goose",
    "cursor",
    "generic",
}


def load_job(path: str | None) -> tuple[dict[str, Any], list[str]]:
    raw = sys.stdin.read() if path in (None, "-") else open(path, "r", encoding="utf-8").read()
    try:
        value = json.loads(raw)
    except json.JSONDecodeError as exc:
        return {}, [f"The job packet is not valid JSON yet: {exc}. Ask the user or caller to send a JSON object, or continue by creating a normal prompt brief."]
    if not isinstance(value, dict):
        return {}, ["The job packet should be a JSON object. Ask for a normal object with job_type, asset_type, and prompt, or continue by creating a prompt brief."]
    return value, []


def require_string(job: dict[str, Any], key: str, reminders: list[str]) -> None:
    if not isinstance(job.get(key), str) or not job[key].strip():
        reminders.append(f"Please provide {key}; it helps the agent create the right image.")


def validate(job: dict[str, Any]) -> tuple[str, list[str], list[str]]:
    reminders: list[str] = []
    warnings: list[str] = []

    job_type = job.get("job_type")
    if job_type not in VALID_JOB_TYPES:
        reminders.append(f"Please choose job_type as one of: {', '.join(sorted(VALID_JOB_TYPES))}. If unsure, use generate.")

    for key in ("asset_type", "prompt"):
        require_string(job, key, reminders)

    if job_type in {"edit", "mask_edit", "composite"} and not job.get("input_images"):
        reminders.append(f"For {job_type}, attach or identify the image to work on. Without it, continue as a prompt/spec draft only.")

    gate = job.get("real_estate_gate")
    if gate is not None and not isinstance(gate, dict):
        reminders.append("real_estate_gate should be an object. If this is real-estate marketing, ask simple questions about use, rights, disclosure, and fair-housing review.")
        gate = {}

    use_type = ""
    if isinstance(gate, dict):
        use_type = str(gate.get("use_type", "")).strip()

    domain = str(job.get("domain", "")).lower()
    publishable = use_type in PUBLISHABLE_USE_TYPES
    real_estate = domain == "real_estate" or bool(gate)

    if real_estate and not gate:
        reminders.append("For real-estate work, ask whether this is a live listing, rental ad, agent marketing, concept, or internal test.")

    if publishable:
        if job.get("rights_confirmed") is not True:
            reminders.append("Before making a publishable asset, confirm the user has rights/permission for the source photo, visible people, logos, and final use.")
        if gate.get("source_rights_checked") is not True:
            reminders.append("Ask the user to confirm source photo rights and any photographer/MLS/brokerage/platform permissions.")
        if gate.get("fair_housing_checked") is not True:
            reminders.append("Remind the user to avoid fair-housing risks: no protected-class targeting, demographic cues, or unverifiable neighborhood claims.")
        disclosure = str(gate.get("disclosure_needed", "")).strip()
        if not disclosure:
            reminders.append("Ask whether a disclosure is needed, such as virtually staged, concept rendering, AI-edited, or none.")
    elif real_estate and use_type == "internal_test":
        warnings.append("Internal test real-estate job: okay to continue, but do not label output listing-safe.")
    elif real_estate:
        warnings.append("Real-estate job is not marked publishable. Continue as a draft, concept, or prompt/spec until the user supplies publishable-use details.")

    exact_text = job.get("exact_text")
    if exact_text is not None and not isinstance(exact_text, list):
        reminders.append("If exact flyer/ad text matters, provide exact_text as a list of short text strings.")

    runtime = str(job.get("agent_runtime", job.get("agent", "generic"))).lower().strip()
    if runtime and runtime not in POPULAR_AGENT_RUNTIMES:
        warnings.append(f"Unknown agent runtime {runtime!r}; use the generic native-image-tool routing contract.")

    if reminders:
        status = "needs_info"
    elif warnings:
        status = "ready_with_notes"
    else:
        status = "ready"

    return status, reminders, warnings


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a ListingLens Studio agent job JSON.")
    parser.add_argument("--file", "-f", help="Job JSON file. Defaults to stdin; '-' also means stdin.")
    parser.add_argument("--json", action="store_true", help="Emit machine-readable validation result.")
    args = parser.parse_args()

    job, parse_reminders = load_job(args.file)
    if parse_reminders:
        status = "needs_info"
        reminders = parse_reminders
        warnings: list[str] = []
    else:
        status, reminders, warnings = validate(job)

    ready_to_execute = status in {"ready", "ready_with_notes"}
    result = {
        "valid": True,
        "status": status,
        "ready_to_execute": ready_to_execute,
        "reminders": reminders,
        "warnings": warnings,
        "supported_agent_runtimes": sorted(POPULAR_AGENT_RUNTIMES),
        "recommended_backend_order": [
            "native_image_tool",
            "chatgpt_codex_native_image_tool",
            "hermes_image_gen",
            "openclaw_adapter",
            "manus_native_image_tool_or_browser_adapter",
            "genspark_native_image_tool_or_browser_adapter",
            "local_cli_with_OPENAI_API_KEY",
            "prompt_packet_only",
        ],
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"agent job: {status}")
        for reminder in reminders:
            print(f"reminder: {reminder}")
        for warning in warnings:
            print(f"warning: {warning}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
