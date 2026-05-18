#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = ["openai>=1.55"]
# ///
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import struct
import sys
import time
import zlib
from datetime import datetime
from pathlib import Path
from typing import Any


SIZE_SHORTCUTS = {
    "auto": "auto",
    "square": "1024x1024",
    "1k": "1024x1024",
    "landscape": "1536x1024",
    "portrait": "1024x1536",
    "2k": "2048x2048",
    "wide": "2048x1152",
    "4k": "3840x2160",
    "tall": "2160x3840",
}

GPT_IMAGE_2_MODELS = {
    "gpt-image-2",
    "gpt-image-2-2026-04-21",
}
SUPPORTED_MODELS = {
    *GPT_IMAGE_2_MODELS,
    "gpt-image-1.5",
    "gpt-image-1",
    "gpt-image-1-mini",
}
SUPPORTED_INPUT_FORMATS = {"png", "jpeg", "webp"}
OUTPUT_FORMAT_BY_SUFFIX = {"png": "png", "jpg": "jpeg", "jpeg": "jpeg", "webp": "webp"}
FALLBACK_ALLOWED_SIZES = {"auto", "1024x1024", "1536x1024", "1024x1536"}
MAX_INPUT_BYTES = 50 * 1024 * 1024
EXPERIMENTAL_PIXEL_COUNT = 2560 * 1440
TRANSIENT_STATUS_CODES = {429, 500, 502, 503, 504}


def slugify(text: str, max_len: int = 36) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    slug = re.sub(r"[\s-]+", "-", slug)
    return (slug[:max_len].strip("-") or "gpt-image-2")


def resolve_size(value: str) -> str:
    return SIZE_SHORTCUTS.get(value.lower(), value)


def is_gpt_image_2_model(model: str) -> bool:
    return model in GPT_IMAGE_2_MODELS


def validate_size(size: str, model: str) -> None:
    if size == "auto":
        return
    match = re.fullmatch(r"(\d+)x(\d+)", size)
    if not match:
        raise SystemExit(f"error: invalid --size {size!r}; use a shortcut or WIDTHxHEIGHT")
    if not is_gpt_image_2_model(model) and size not in FALLBACK_ALLOWED_SIZES:
        allowed = ", ".join(sorted(FALLBACK_ALLOWED_SIZES))
        raise SystemExit(
            f"error: flexible custom --size values are only supported for gpt-image-2; "
            f"{model} accepts: {allowed}"
        )
    width, height = int(match.group(1)), int(match.group(2))
    pixels = width * height
    if width % 16 or height % 16:
        raise SystemExit("error: --size dimensions must be multiples of 16")
    if max(width, height) > 3840:
        raise SystemExit("error: --size max edge must be <= 3840")
    if max(width, height) / min(width, height) > 3:
        raise SystemExit("error: --size long:short ratio must be <= 3:1")
    if pixels < 655_360 or pixels > 8_294_400:
        raise SystemExit("error: --size total pixels must be between 655,360 and 8,294,400")


def size_pixels(size: str) -> int | None:
    if size == "auto":
        return None
    width, height = (int(part) for part in size.split("x", maxsplit=1))
    return width * height


def validate_model(model: str) -> None:
    if model in SUPPORTED_MODELS:
        return
    models = ", ".join(sorted(SUPPORTED_MODELS))
    raise SystemExit(f"error: unsupported --model {model!r}; supported GPT Image models: {models}")


def default_file(model: str, fmt: str | None) -> Path:
    ext = fmt or "png"
    stamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    return Path.cwd() / f"{stamp}-{slugify(model)}.{ext}"


def output_format_from_suffix(path: Path) -> str | None:
    suffix = path.suffix.lower().lstrip(".")
    return OUTPUT_FORMAT_BY_SUFFIX.get(suffix)


def resolve_output_file_and_format(args: argparse.Namespace) -> Path:
    inferred_format = output_format_from_suffix(args.file) if args.file else None
    if args.output_format and inferred_format and args.output_format != inferred_format:
        raise SystemExit(
            f"error: --format {args.output_format} does not match output extension "
            f"{args.file.suffix!r}; use a matching .png, .jpg/.jpeg, or .webp path"
        )
    if args.file and args.file.suffix and inferred_format is None:
        raise SystemExit(
            f"error: unsupported output extension {args.file.suffix!r}; "
            "use .png, .jpg/.jpeg, or .webp"
        )
    args.output_format = args.output_format or inferred_format or "png"
    if args.file:
        if args.file.suffix:
            return args.file
        ext = "jpg" if args.output_format == "jpeg" else args.output_format
        return args.file.with_suffix(f".{ext}")
    return default_file(args.model, args.output_format)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate or edit images with OpenAI gpt-image-2.")
    parser.add_argument("--prompt", "-p", required=True, help="Image prompt or edit instruction.")
    parser.add_argument("--file", "-f", type=Path, help="Output file path.")
    parser.add_argument("--image", "-i", action="append", type=Path, help="Reference/base image. Repeat for multi-reference edits.")
    parser.add_argument("--mask", "-m", type=Path, help="Alpha mask for localized edits. Requires --image.")
    parser.add_argument("--model", default="gpt-image-2", help="Image model. Default: gpt-image-2.")
    parser.add_argument("--size", default="auto", help="Shortcut, WIDTHxHEIGHT, or auto. Default: auto.")
    parser.add_argument("--quality", default="auto", choices=["auto", "low", "medium", "high"], help="Default: auto.")
    parser.add_argument("--n", type=int, default=1, help="Number of outputs. Default: 1.")
    parser.add_argument("--format", dest="output_format", choices=["png", "jpeg", "webp"], help="Output format.")
    parser.add_argument("--compression", dest="output_compression", type=int, help="JPEG/WebP compression 0-100.")
    parser.add_argument("--background", choices=["auto", "opaque", "transparent"], help="Background handling when supported by the selected model.")
    parser.add_argument("--moderation", choices=["auto", "low"], help="Generation moderation setting.")
    parser.add_argument("--user", help="Optional end-user identifier.")
    parser.add_argument(
        "--confirm-rights",
        action="store_true",
        help="Confirm you have rights/consent for source images, marks, logos, and publishable output.",
    )
    parser.add_argument("--confirm-cost", "--yes", action="store_true", help="Acknowledge budget-sensitive settings without an interactive prompt.")
    parser.add_argument("--force", action="store_true", help="Allow overwriting existing output/manifest files. Never allows overwriting input or mask paths.")
    parser.add_argument("--retries", type=int, default=2, help="Retries for transient 429/5xx API errors. Default: 2.")
    parser.add_argument("--dry-run", action="store_true", help="Print resolved endpoint and payload without calling the API.")
    return parser.parse_args()


def clean_payload(payload: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in payload.items() if value is not None}


def validate_options(args: argparse.Namespace) -> None:
    validate_model(args.model)
    if args.n < 1:
        raise SystemExit("error: --n must be at least 1")
    if is_gpt_image_2_model(args.model) and args.background == "transparent":
        raise SystemExit("error: gpt-image-2 does not currently support --background transparent")
    if args.output_compression is not None:
        if not 0 <= args.output_compression <= 100:
            raise SystemExit("error: --compression must be between 0 and 100")
        if args.output_format not in {"jpeg", "webp"}:
            raise SystemExit("error: --compression requires --format jpeg or --format webp")


def png_info(data: bytes) -> dict[str, Any] | None:
    if not data.startswith(b"\x89PNG\r\n\x1a\n") or len(data) < 33:
        return None
    if data[12:16] != b"IHDR":
        return None
    width, height = struct.unpack(">II", data[16:24])
    bit_depth = data[24]
    color_type = data[25]
    compression = data[26]
    filter_method = data[27]
    interlace = data[28]
    return {
        "width": width,
        "height": height,
        "alpha": color_type in {4, 6},
        "bit_depth": bit_depth,
        "color_type": color_type,
        "compression": compression,
        "filter_method": filter_method,
        "interlace": interlace,
    }


def png_chunks(data: bytes) -> list[tuple[bytes, bytes]]:
    chunks: list[tuple[bytes, bytes]] = []
    index = 8
    while index + 8 <= len(data):
        length = struct.unpack(">I", data[index:index + 4])[0]
        chunk_type = data[index + 4:index + 8]
        chunk_data = data[index + 8:index + 8 + length]
        if index + 12 + length > len(data):
            break
        chunks.append((chunk_type, chunk_data))
        index += 12 + length
        if chunk_type == b"IEND":
            break
    return chunks


def unfilter_png_scanline(filter_type: int, raw: bytes, previous: bytes, bpp: int) -> bytes:
    row = bytearray(raw)
    for index, value in enumerate(row):
        left = row[index - bpp] if index >= bpp else 0
        up = previous[index] if previous else 0
        up_left = previous[index - bpp] if previous and index >= bpp else 0
        if filter_type == 1:
            row[index] = (value + left) & 0xFF
        elif filter_type == 2:
            row[index] = (value + up) & 0xFF
        elif filter_type == 3:
            row[index] = (value + ((left + up) // 2)) & 0xFF
        elif filter_type == 4:
            predictor = left + up - up_left
            pa = abs(predictor - left)
            pb = abs(predictor - up)
            pc = abs(predictor - up_left)
            nearest = left if pa <= pb and pa <= pc else up if pb <= pc else up_left
            row[index] = (value + nearest) & 0xFF
        elif filter_type != 0:
            raise ValueError(f"unsupported PNG filter type {filter_type}")
    return bytes(row)


def png_alpha_stats(data: bytes) -> dict[str, Any]:
    info = png_info(data)
    if not info or not info["alpha"]:
        return {"inspectable": False, "reason": "PNG has no alpha channel"}
    if info["bit_depth"] != 8:
        return {"inspectable": False, "reason": f"PNG bit depth {info['bit_depth']} is not supported by stdlib alpha inspection"}
    if info["compression"] != 0 or info["filter_method"] != 0 or info["interlace"] != 0:
        return {"inspectable": False, "reason": "PNG uses unsupported compression/filter/interlace settings"}
    channels = 4 if info["color_type"] == 6 else 2
    alpha_offset = 3 if info["color_type"] == 6 else 1
    idat = b"".join(chunk for chunk_type, chunk in png_chunks(data) if chunk_type == b"IDAT")
    if not idat:
        return {"inspectable": False, "reason": "PNG has no IDAT chunks"}
    try:
        decompressed = zlib.decompress(idat)
    except zlib.error as exc:
        return {"inspectable": False, "reason": f"PNG IDAT decompression failed: {exc}"}
    width = int(info["width"])
    height = int(info["height"])
    row_len = width * channels
    expected = height * (row_len + 1)
    if len(decompressed) < expected:
        return {"inspectable": False, "reason": "PNG pixel data is shorter than expected"}
    previous = b"\x00" * row_len
    total = transparent = opaque = partial = 0
    min_alpha = 255
    max_alpha = 0
    offset = 0
    try:
        for _row_index in range(height):
            filter_type = decompressed[offset]
            offset += 1
            row = unfilter_png_scanline(filter_type, decompressed[offset:offset + row_len], previous, channels)
            offset += row_len
            previous = row
            for alpha_index in range(alpha_offset, row_len, channels):
                alpha = row[alpha_index]
                total += 1
                transparent += int(alpha == 0)
                opaque += int(alpha == 255)
                partial += int(0 < alpha < 255)
                min_alpha = min(min_alpha, alpha)
                max_alpha = max(max_alpha, alpha)
    except (IndexError, ValueError) as exc:
        return {"inspectable": False, "reason": f"PNG alpha inspection failed: {exc}"}
    return {
        "inspectable": True,
        "total_pixels": total,
        "transparent_pixels": transparent,
        "opaque_pixels": opaque,
        "partial_alpha_pixels": partial,
        "transparent_ratio": round(transparent / total, 6) if total else 0,
        "opaque_ratio": round(opaque / total, 6) if total else 0,
        "min_alpha": min_alpha,
        "max_alpha": max_alpha,
    }


def jpeg_info(data: bytes) -> tuple[int, int] | None:
    if not data.startswith(b"\xff\xd8"):
        return None
    index = 2
    while index + 9 < len(data):
        if data[index] != 0xFF:
            index += 1
            continue
        marker = data[index + 1]
        index += 2
        while marker == 0xFF and index < len(data):
            marker = data[index]
            index += 1
        if marker in {0xD8, 0xD9}:
            continue
        if index + 2 > len(data):
            return None
        length = struct.unpack(">H", data[index:index + 2])[0]
        if length < 2 or index + length > len(data):
            return None
        if marker in {
            0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
            0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF,
        }:
            height, width = struct.unpack(">HH", data[index + 3:index + 7])
            return width, height
        index += length
    return None


def webp_info(data: bytes) -> tuple[int, int, bool] | None:
    if len(data) < 30 or data[:4] != b"RIFF" or data[8:12] != b"WEBP":
        return None
    chunk = data[12:16]
    if chunk == b"VP8X" and len(data) >= 30:
        flags = data[20]
        width = 1 + int.from_bytes(data[24:27], "little")
        height = 1 + int.from_bytes(data[27:30], "little")
        return width, height, bool(flags & 0x10)
    if chunk == b"VP8 " and len(data) >= 30:
        width = struct.unpack("<H", data[26:28])[0] & 0x3FFF
        height = struct.unpack("<H", data[28:30])[0] & 0x3FFF
        return width, height, False
    if chunk == b"VP8L" and len(data) >= 25:
        b0, b1, b2, b3 = data[21], data[22], data[23], data[24]
        width = 1 + (((b1 & 0x3F) << 8) | b0)
        height = 1 + (((b3 & 0x0F) << 10) | (b2 << 2) | ((b1 & 0xC0) >> 6))
        return width, height, False
    return None


def image_info(path: Path) -> dict[str, Any]:
    size = path.stat().st_size
    if size >= MAX_INPUT_BYTES:
        raise SystemExit(f"error: image input must be under 50 MB: {path}")
    data = path.read_bytes()
    png = png_info(data)
    if png:
        return {"path": path, "format": "png", **png, "bytes": size}
    jpeg = jpeg_info(data)
    if jpeg:
        width, height = jpeg
        return {"path": path, "format": "jpeg", "width": width, "height": height, "alpha": False, "bytes": size}
    webp = webp_info(data)
    if webp:
        width, height, alpha = webp
        return {"path": path, "format": "webp", "width": width, "height": height, "alpha": alpha, "bytes": size}
    allowed = ", ".join(sorted(SUPPORTED_INPUT_FORMATS))
    raise SystemExit(f"error: unsupported image format for {path}; expected one of: {allowed}")


def inspect_mask_alpha(path: Path, mask_info: dict[str, Any]) -> tuple[dict[str, Any] | None, list[str]]:
    if mask_info["format"] != "png":
        return None, [
            "mask alpha distribution could not be inspected with the stdlib for non-PNG masks; "
            "verified format, dimensions, size, and alpha-channel presence only"
        ]
    stats = png_alpha_stats(path.read_bytes())
    if not stats.get("inspectable"):
        return stats, [
            f"mask alpha distribution could not be inspected: {stats.get('reason', 'unknown reason')}; "
            "verify transparent edit regions manually"
        ]
    total = stats["total_pixels"]
    transparent = stats["transparent_pixels"]
    opaque = stats["opaque_pixels"]
    partial = stats["partial_alpha_pixels"]
    if transparent == 0:
        raise SystemExit("error: --mask has no fully transparent editable pixels; transparent pixels indicate the edit area")
    if opaque == 0 and partial == 0:
        raise SystemExit("error: --mask is fully transparent, so the whole image would be editable; remove --mask for full-image edits")
    warnings: list[str] = []
    transparent_ratio = transparent / total if total else 0
    if transparent_ratio > 0.80:
        warnings.append(
            f"mask is {transparent_ratio:.1%} transparent; transparent pixels are edited, "
            "so this may be inverted if you intended a small localized edit"
        )
    if transparent_ratio < 0.001 and partial == 0:
        warnings.append(
            f"mask has only {transparent} fully transparent pixels; confirm the editable region is intentional"
        )
    return stats, warnings


def check_files(args: argparse.Namespace) -> tuple[list[dict[str, Any]], dict[str, Any] | None, list[str]]:
    if args.mask and not args.image:
        raise SystemExit("error: --mask requires at least one --image")
    for image in args.image or []:
        if not image.is_file():
            raise SystemExit(f"error: --image not found: {image}")
    if args.mask and not args.mask.is_file():
        raise SystemExit(f"error: --mask not found: {args.mask}")
    image_infos = [image_info(path) for path in args.image or []]
    mask_info = None
    validation_warnings: list[str] = []
    if args.mask:
        mask_info = image_info(args.mask)
        base_info = image_infos[0]
        if len(image_infos) > 1:
            print(
                "warning: with multiple --image values, --mask applies to the first image only; "
                "put the editable base image first.",
                file=sys.stderr,
            )
        if mask_info["format"] != base_info["format"]:
            raise SystemExit("error: --mask and the first --image must have the same format")
        if (mask_info["width"], mask_info["height"]) != (base_info["width"], base_info["height"]):
            raise SystemExit("error: --mask and the first --image must have the same pixel dimensions")
        if not mask_info["alpha"]:
            raise SystemExit("error: --mask must include an alpha channel")
        alpha_stats, mask_warnings = inspect_mask_alpha(args.mask, mask_info)
        if alpha_stats:
            mask_info["alpha_stats"] = alpha_stats
        validation_warnings.extend(mask_warnings)
    for warning in validation_warnings:
        print(f"warning: {warning}", file=sys.stderr)
    return image_infos, mask_info, validation_warnings


def output_paths(out_file: Path, count: int) -> list[Path]:
    if count <= 1:
        return [out_file]
    return [out_file.with_name(f"{out_file.stem}_{index + 1:02d}{out_file.suffix}") for index in range(count)]


def manifest_path(out_file: Path) -> Path:
    return out_file.with_suffix(".manifest.json")


def comparable_path(path: Path) -> Path:
    return path.expanduser().resolve(strict=False)


def validate_output_targets(args: argparse.Namespace, out_file: Path) -> None:
    targets = output_paths(out_file, args.n)
    targets.append(manifest_path(out_file))
    source_paths = {comparable_path(path) for path in (args.image or [])}
    if args.mask:
        source_paths.add(comparable_path(args.mask))
    seen: set[Path] = set()
    for target in targets:
        normalized = comparable_path(target)
        if normalized in seen:
            raise SystemExit(f"error: output path would be written more than once: {target}")
        seen.add(normalized)
        if normalized in source_paths:
            raise SystemExit(f"error: output path would overwrite an input or mask file: {target}; choose a different --file")
        if target.exists() and not args.force:
            raise SystemExit(f"error: output path already exists: {target}; rerun with --force to overwrite")


def budget_warnings(args: argparse.Namespace) -> list[str]:
    warnings: list[str] = []
    if args.n > 1:
        warnings.append(f"--n {args.n} requests multiple paid outputs")
    if args.quality == "high":
        warnings.append("--quality high can cost more and take longer")
    if args.image and is_gpt_image_2_model(args.model):
        input_count = len(args.image)
        if input_count > 1:
            warnings.append(
                f"multi-image edit uploads {input_count} high-fidelity inputs; input processing can materially increase cost"
            )
        else:
            warnings.append("gpt-image-2 edit inputs are processed at high fidelity and can add input cost")
    pixels = size_pixels(args.size)
    if is_gpt_image_2_model(args.model) and args.size not in FALLBACK_ALLOWED_SIZES:
        warnings.append(
            f"--size {args.size} uses gpt-image-2 flexible/custom sizing; run a live smoke test before production if API docs or account support are uncertain"
        )
    if pixels and pixels > EXPERIMENTAL_PIXEL_COUNT:
        warnings.append(f"--size {args.size} is above 2K output and is experimental")
    return warnings


def confirm_budget(args: argparse.Namespace, warnings: list[str]) -> None:
    if not warnings or args.confirm_cost:
        return
    message = "Budget-sensitive image request:\n- " + "\n- ".join(warnings)
    if not sys.stdin.isatty():
        raise SystemExit(f"error: {message}\nRerun with --confirm-cost to acknowledge.")
    reply = input(f"{message}\nContinue? [y/N] ").strip().lower()
    if reply not in {"y", "yes"}:
        raise SystemExit("cancelled: cost confirmation was not accepted")


def extract_output_bytes(items: list[Any]) -> list[bytes]:
    output_bytes: list[bytes] = []
    for index, item in enumerate(items):
        b64_json = getattr(item, "b64_json", None)
        if not b64_json and isinstance(item, dict):
            b64_json = item.get("b64_json")
        if not b64_json:
            raise SystemExit(f"error: output item {index} has no b64_json")
        output_bytes.append(base64.b64decode(b64_json))
    return output_bytes


def write_outputs(output_bytes: list[bytes], out_file: Path, force: bool) -> list[Path]:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    total = len(output_bytes)
    for index, raw in enumerate(output_bytes):
        target = out_file
        if total > 1:
            target = out_file.with_name(f"{out_file.stem}_{index + 1:02d}{out_file.suffix}")
        if target.exists() and not force:
            raise SystemExit(f"error: output path already exists: {target}; rerun with --force to overwrite")
        target.write_bytes(raw)
        written.append(target)
    return written


def json_safe_image_info(info: dict[str, Any]) -> dict[str, Any]:
    return {key: (str(value) if isinstance(value, Path) else value) for key, value in info.items()}


def write_manifest(
    out_file: Path,
    written: list[Path],
    endpoint: str,
    payload: dict[str, Any],
    image_infos: list[dict[str, Any]],
    mask_info: dict[str, Any] | None,
    budget: list[str],
    validation_warnings: list[str],
    rights_confirmed: bool,
    force: bool,
) -> Path:
    manifest = out_file.with_suffix(".manifest.json")
    if manifest.exists() and not force:
        raise SystemExit(f"error: manifest path already exists: {manifest}; rerun with --force to overwrite")
    manifest_payload = {
        "created_at": datetime.now().isoformat(timespec="seconds"),
        "endpoint": endpoint,
        "prompt": payload.get("prompt"),
        "settings": {
            key: value
            for key, value in payload.items()
            if key not in {"prompt", "image", "mask", "user"}
        },
        "source_images": [json_safe_image_info(info) for info in image_infos],
        "mask": json_safe_image_info(mask_info) if mask_info else None,
        "outputs": [str(path) for path in written],
        "budget_warnings": budget,
        "validation_warnings": validation_warnings,
        "qa": {
            "status": "not_reviewed",
            "source_rights_status": "confirmed_by_cli_flag" if rights_confirmed else "not_confirmed_by_script",
            "compliance_gate_status": "not_reviewed_by_script",
            "checks": [
                "open each output at full size",
                "confirm prompt intent and source-image invariants",
                "confirm mask region behavior when a mask was used",
                "record acceptance notes before delivery",
            ],
            "notes": [],
        },
    }
    manifest.write_text(json.dumps(manifest_payload, indent=2) + "\n")
    return manifest


def confirm_source_rights(args: argparse.Namespace) -> None:
    if args.confirm_rights:
        return
    message = (
        "Source-rights confirmation required: confirm you have rights/consent for any source images, "
        "visible people, marks/logos, platform screenshots, and publishable output. The script cannot "
        "detect or approve watermark/copyright removal."
    )
    raise SystemExit(f"error: {message}\nRerun with --confirm-rights after confirming rights.")


def status_code_for(exc: Exception) -> int | None:
    status_code = getattr(exc, "status_code", None)
    if isinstance(status_code, int):
        return status_code
    response = getattr(exc, "response", None)
    response_status = getattr(response, "status_code", None)
    return response_status if isinstance(response_status, int) else None


def is_transient(exc: Exception) -> bool:
    status_code = status_code_for(exc)
    return status_code in TRANSIENT_STATUS_CODES


def request_with_retries(operation: Any, retries: int) -> Any:
    attempts = max(0, retries) + 1
    for attempt in range(1, attempts + 1):
        try:
            return operation()
        except Exception as exc:
            if attempt >= attempts or not is_transient(exc):
                raise
            delay = min(2 ** (attempt - 1), 8)
            print(
                f"warning: transient OpenAI error ({status_code_for(exc)}); "
                f"retrying in {delay}s ({attempt}/{attempts - 1})",
                file=sys.stderr,
            )
            time.sleep(delay)
    raise RuntimeError("unreachable retry state")


def error_details(exc: Exception) -> str:
    parts = [f"{exc.__class__.__name__}: {exc}"]
    status_code = status_code_for(exc)
    if status_code:
        parts.append(f"status_code={status_code}")
    request_id = getattr(exc, "request_id", None)
    if request_id:
        parts.append(f"request_id={request_id}")
    for attr in ("code", "type", "param"):
        value = getattr(exc, attr, None)
        if value:
            parts.append(f"{attr}={value}")
    body = getattr(exc, "body", None)
    if body:
        parts.append(f"body={body}")
    response = getattr(exc, "response", None)
    if response is not None:
        try:
            text = response.text
        except Exception:
            text = None
        if text:
            parts.append(f"response={text[:2000]}")
    return "; ".join(parts)


def edit_request(client: Any, args: argparse.Namespace, payload: dict[str, Any]) -> Any:
    image_handles = [path.open("rb") for path in args.image]
    mask_handle = args.mask.open("rb") if args.mask else None
    try:
        return client.images.edit(**clean_payload({
            **payload,
            "image": image_handles,
            "mask": mask_handle,
        }))
    finally:
        for handle in image_handles:
            handle.close()
        if mask_handle:
            mask_handle.close()


def main() -> int:
    args = parse_args()
    args.size = resolve_size(args.size)
    out_file = resolve_output_file_and_format(args)
    validate_options(args)
    validate_size(args.size, args.model)
    image_infos, mask_info, validation_warnings = check_files(args)
    warnings = budget_warnings(args)
    validate_output_targets(args, out_file)
    endpoint = "images.edit" if args.image else "images.generate"
    common_payload = clean_payload({
        "model": args.model,
        "prompt": args.prompt,
        "size": args.size,
        "quality": args.quality,
        "n": args.n,
        "background": args.background,
        "output_format": args.output_format,
        "output_compression": args.output_compression,
        "user": args.user,
    })

    if args.dry_run:
        preview = dict(common_payload)
        if args.image:
            preview["image"] = [str(path) for path in args.image]
        if args.mask:
            preview["mask"] = str(args.mask)
        if not args.image and args.moderation:
            preview["moderation"] = args.moderation
        result = {
            "endpoint": endpoint,
            "output": str(out_file),
            "outputs": [str(path) for path in output_paths(out_file, args.n)],
            "manifest": str(manifest_path(out_file)),
            "payload": preview,
        }
        if warnings:
            result["budget_warnings"] = warnings
        if validation_warnings:
            result["validation_warnings"] = validation_warnings
        print(json.dumps(result, indent=2))
        return 0

    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise SystemExit("error: OPENAI_API_KEY is not set; use --dry-run to inspect the payload")
    confirm_source_rights(args)
    confirm_budget(args, warnings)

    from openai import OpenAI

    client = OpenAI(api_key=api_key)
    try:
        if args.image:
            response = request_with_retries(
                lambda: edit_request(client, args, common_payload),
                args.retries,
            )
        else:
            response = request_with_retries(
                lambda: client.images.generate(**clean_payload({
                    **common_payload,
                    "moderation": args.moderation,
                })),
                args.retries,
            )
    except Exception as exc:
        print(f"error: OpenAI image request failed: {error_details(exc)}", file=sys.stderr)
        return 1

    output_bytes = extract_output_bytes(list(response.data))
    planned_outputs = output_paths(out_file, len(output_bytes))
    manifest = write_manifest(
        out_file,
        planned_outputs,
        endpoint,
        common_payload,
        image_infos,
        mask_info,
        warnings,
        validation_warnings,
        args.confirm_rights,
        args.force,
    )
    written = write_outputs(output_bytes, out_file, args.force)
    for path in written:
        print(path)
    if manifest:
        print(manifest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
