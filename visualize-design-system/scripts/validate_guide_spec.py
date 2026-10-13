#!/usr/bin/env python3
"""Validate a design-system visual guide specification.

Performs JSON Schema validation plus domain-specific checks for matrix dimensions,
unique IDs, local assets, text density, provenance, and basic color contrast.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any, Iterable

try:
    from jsonschema import Draft202012Validator
except ImportError:  # pragma: no cover - fallback is intentionally supported
    Draft202012Validator = None  # type: ignore[assignment]


PROVENANCE = {"implemented", "documented", "inferred", "proposed", "missing", "deprecated"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path, help="guide-spec.json")
    parser.add_argument(
        "--schema",
        type=Path,
        default=Path(__file__).resolve().parents[1] / "assets" / "guide-spec.schema.json",
        help="JSON Schema path",
    )
    parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    return parser.parse_args()


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ValueError(f"file not found: {path}") from None
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc}") from exc


def error_path(parts: Iterable[Any]) -> str:
    rendered = "$"
    for part in parts:
        rendered += f"[{part}]" if isinstance(part, int) else f".{part}"
    return rendered


def collect_text(value: Any) -> list[str]:
    found: list[str] = []
    if isinstance(value, str):
        found.append(value)
    elif isinstance(value, list):
        for item in value:
            found.extend(collect_text(item))
    elif isinstance(value, dict):
        for key, item in value.items():
            if key not in {"html", "path", "src", "token", "locator"}:
                found.extend(collect_text(item))
    return found


def normalize_hex(value: str) -> str | None:
    if not isinstance(value, str) or not value.startswith("#"):
        return None
    raw = value[1:]
    if len(raw) == 8:
        raw = raw[:6]
    if len(raw) != 6:
        return None
    try:
        int(raw, 16)
    except ValueError:
        return None
    return raw


def channel_to_linear(channel: int) -> float:
    value = channel / 255.0
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def luminance(color: str) -> float | None:
    raw = normalize_hex(color)
    if raw is None:
        return None
    r, g, b = (int(raw[i : i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * channel_to_linear(r) + 0.7152 * channel_to_linear(g) + 0.0722 * channel_to_linear(b)


def contrast_ratio(foreground: str, background: str) -> float | None:
    a = luminance(foreground)
    b = luminance(background)
    if a is None or b is None:
        return None
    lighter, darker = max(a, b), min(a, b)
    return (lighter + 0.05) / (darker + 0.05)


def check_domain(spec: dict[str, Any], spec_path: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    sections = spec.get("sections", [])
    ids: list[str] = [s.get("id", "") for s in sections if isinstance(s, dict)]
    duplicates = sorted({value for value in ids if value and ids.count(value) > 1})
    if duplicates:
        errors.append(f"duplicate section IDs: {', '.join(duplicates)}")

    for section_index, section in enumerate(sections):
        if not isinstance(section, dict):
            continue
        stype = section.get("type")
        prefix = f"sections[{section_index}] ({section.get('id', 'unknown')})"
        if stype == "matrix":
            columns = section.get("columns", [])
            column_ids = [c.get("id") for c in columns if isinstance(c, dict)]
            if len(set(column_ids)) != len(column_ids):
                errors.append(f"{prefix}: matrix column IDs must be unique")
            for row_index, row in enumerate(section.get("rows", [])):
                cells = row.get("cells", []) if isinstance(row, dict) else []
                if len(cells) != len(columns):
                    errors.append(
                        f"{prefix}: row {row_index} has {len(cells)} cells; expected {len(columns)}"
                    )
        elif stype == "decision":
            columns = section.get("columns", [])
            for row_index, row in enumerate(section.get("rows", [])):
                cells = row.get("cells", []) if isinstance(row, dict) else []
                if len(cells) != len(columns):
                    errors.append(
                        f"{prefix}: decision row {row_index} has {len(cells)} cells; expected {len(columns)}"
                    )

    for path, node in walk_nodes(spec):
        if isinstance(node, dict) and node.get("kind") == "image":
            src = node.get("src")
            if not src:
                errors.append(f"{path}: image sample requires src")
            elif isinstance(src, str) and not src.startswith(("http://", "https://", "data:")):
                target = (spec_path.parent / src).resolve()
                if not target.exists():
                    errors.append(f"{path}: local image not found: {src}")
        if isinstance(node, dict) and node.get("kind") == "html":
            if node.get("trusted_html") is not True:
                warnings.append(f"{path}: HTML sample will be escaped unless trusted_html=true")
        if isinstance(node, dict) and "provenance" in node:
            value = node.get("provenance")
            if value not in PROVENANCE:
                errors.append(f"{path}.provenance: unsupported status {value!r}")

    meta = spec.get("meta", {})
    canvas = meta.get("canvas", {}) if isinstance(meta, dict) else {}
    width = canvas.get("width", 0)
    height = canvas.get("height", 0)
    total_words = sum(len(text.split()) for text in collect_text(sections))
    if width == 1080 and height == 1350 and total_words > 420:
        warnings.append(
            f"high text density for 1080×1350: approximately {total_words} visible words; consider splitting"
        )
    if len(sections) > 6:
        warnings.append(f"{len(sections)} sections may weaken one-question focus")

    theme = spec.get("theme", {})
    if isinstance(theme, dict):
        contrast_checks = [
            ("text/background", theme.get("text"), theme.get("background"), 4.5),
            ("text/surface", theme.get("text"), theme.get("surface"), 4.5),
            ("muted/background", theme.get("muted"), theme.get("background"), 4.5),
            ("accent_text/accent", theme.get("accent_text", "#FFFFFF"), theme.get("accent"), 4.5),
        ]
        for label, fg, bg, threshold in contrast_checks:
            if isinstance(fg, str) and isinstance(bg, str):
                ratio = contrast_ratio(fg, bg)
                if ratio is not None and ratio < threshold:
                    warnings.append(f"contrast {label} is {ratio:.2f}:1; target is at least {threshold:.1f}:1")

    statuses = set()
    for _, node in walk_nodes(spec):
        if isinstance(node, dict) and node.get("provenance") in PROVENANCE:
            statuses.add(node["provenance"])
    if len(statuses) > 1 and not spec.get("provenance_legend", False):
        warnings.append("multiple provenance statuses are used but provenance_legend is false")

    if meta.get("status") in {"implemented", "documented"} and not spec.get("sources"):
        warnings.append("guide claims an existing-state status but contains no sources")

    return errors, warnings


def walk_nodes(value: Any, path: str = "$") -> Iterable[tuple[str, Any]]:
    yield path, value
    if isinstance(value, list):
        for index, item in enumerate(value):
            yield from walk_nodes(item, f"{path}[{index}]")
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from walk_nodes(item, f"{path}.{key}")


def main() -> int:
    args = parse_args()
    try:
        spec = load_json(args.spec)
        schema = load_json(args.schema)
    except ValueError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    errors: list[str] = []
    warnings: list[str] = []

    if Draft202012Validator is None:
        warnings.append("jsonschema is not installed; only domain checks were run")
        if not isinstance(spec, dict):
            errors.append("top-level JSON value must be an object")
        else:
            for key in ("schema_version", "meta", "theme", "sections"):
                if key not in spec:
                    errors.append(f"missing required key: {key}")
    else:
        validator = Draft202012Validator(schema)
        for issue in sorted(validator.iter_errors(spec), key=lambda e: list(e.absolute_path)):
            errors.append(f"{error_path(issue.absolute_path)}: {issue.message}")

    if isinstance(spec, dict):
        domain_errors, domain_warnings = check_domain(spec, args.spec.resolve())
        errors.extend(domain_errors)
        warnings.extend(domain_warnings)

    for message in errors:
        print(f"ERROR: {message}")
    for message in warnings:
        print(f"WARNING: {message}")

    if errors or (args.strict and warnings):
        print(f"FAILED: {len(errors)} error(s), {len(warnings)} warning(s)")
        return 1

    print(f"PASS: {len(warnings)} warning(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
