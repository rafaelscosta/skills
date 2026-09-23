#!/usr/bin/env python3
"""Capture a rendered guide HTML as PNG and/or PDF, with overflow diagnostics."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any


DIMENSION_RE = re.compile(r"expectedWidth:\s*(\d+).*?expectedHeight:\s*(\d+)", re.DOTALL)


def find_chromium_executable() -> str | None:
    """Find a Chromium-family browser on PATH or common desktop install paths."""
    for name in ("chromium", "google-chrome", "chromium-browser", "microsoft-edge", "brave-browser"):
        executable = shutil.which(name)
        if executable:
            return executable
    for candidate in (
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "/Applications/Chromium.app/Contents/MacOS/Chromium",
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    ):
        if Path(candidate).is_file():
            return candidate
    return None


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("html", type=Path, help="Standalone guide HTML")
    parser.add_argument("--png", type=Path, help="PNG output path")
    parser.add_argument("--pdf", type=Path, help="PDF output path")
    parser.add_argument("--width", type=int, help="Override viewport/page width")
    parser.add_argument("--height", type=int, help="Override viewport/page height")
    parser.add_argument("--scale", type=float, default=1.0, help="PNG device scale factor (default: 1)")
    parser.add_argument("--timeout", type=int, default=30_000, help="Navigation timeout in milliseconds")
    parser.add_argument("--strict", action="store_true", help="Fail when overflow is detected")
    return parser.parse_args()


def infer_dimensions(path: Path) -> tuple[int, int]:
    text = path.read_text(encoding="utf-8", errors="replace")
    match = DIMENSION_RE.search(text)
    if match:
        return int(match.group(1)), int(match.group(2))
    return 1080, 1350


def ensure_outputs(args: argparse.Namespace) -> None:
    if not args.png and not args.pdf:
        raise ValueError("provide --png and/or --pdf")
    if args.scale <= 0 or args.scale > 4:
        raise ValueError("--scale must be greater than 0 and at most 4")
    for path in (args.png, args.pdf):
        if path:
            path.parent.mkdir(parents=True, exist_ok=True)


def capture_with_playwright(
    html_path: Path,
    png_path: Path | None,
    pdf_path: Path | None,
    width: int,
    height: int,
    scale: float,
    timeout: int,
) -> dict[str, Any]:
    from playwright.sync_api import sync_playwright

    executable = find_chromium_executable()
    with sync_playwright() as playwright:
        launch_args: dict[str, Any] = {"headless": True, "args": ["--no-sandbox", "--disable-gpu"]}
        if executable:
            launch_args["executable_path"] = executable
        browser = playwright.chromium.launch(**launch_args)
        try:
            context = browser.new_context(
                viewport={"width": width, "height": height},
                device_scale_factor=scale,
            )
            page = context.new_page()
            page.set_default_timeout(timeout)
            page.set_content(html_path.read_text(encoding="utf-8"), wait_until="load", timeout=timeout)
            page.evaluate("document.fonts && document.fonts.ready")
            page.wait_for_timeout(150)
            diagnostics = page.evaluate("window.__guideDiagnostics || null") or {}
            if png_path:
                page.screenshot(
                    path=str(png_path),
                    clip={"x": 0, "y": 0, "width": width, "height": height},
                    animations="disabled",
                )
            if pdf_path:
                page.pdf(
                    path=str(pdf_path),
                    width=f"{width}px",
                    height=f"{height}px",
                    print_background=True,
                    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                    prefer_css_page_size=True,
                )
            context.close()
            return diagnostics
        finally:
            browser.close()


def capture_with_chromium(
    html_path: Path,
    png_path: Path | None,
    pdf_path: Path | None,
    width: int,
    height: int,
    scale: float,
) -> dict[str, Any]:
    executable = find_chromium_executable()
    if not executable:
        raise RuntimeError("Playwright is unavailable and no Chromium executable was found")
    url = html_path.resolve().as_uri()
    common = [
        executable,
        "--headless",
        "--no-sandbox",
        "--disable-gpu",
        "--hide-scrollbars",
        f"--window-size={width},{height}",
        f"--force-device-scale-factor={scale}",
    ]
    if png_path:
        subprocess.run([*common, f"--screenshot={png_path}", url], check=True, timeout=60)
    if pdf_path:
        subprocess.run([*common, f"--print-to-pdf={pdf_path}", "--no-pdf-header-footer", url], check=True, timeout=60)
    return {"warning": "fallback capture did not collect DOM overflow diagnostics"}


def has_overflow(diagnostics: dict[str, Any], width: int, height: int) -> bool:
    if diagnostics.get("overflow"):
        return True
    for key, limit in (("pageWidth", width), ("bodyWidth", width), ("pageHeight", height), ("bodyHeight", height)):
        value = diagnostics.get(key)
        if isinstance(value, (int, float)) and value > limit + 1:
            return True
    return False


def main() -> int:
    args = parse_args()
    try:
        ensure_outputs(args)
        html_path = args.html.expanduser().resolve()
        if not html_path.exists():
            raise ValueError(f"HTML file not found: {html_path}")
        inferred_width, inferred_height = infer_dimensions(html_path)
        width = args.width or inferred_width
        height = args.height or inferred_height
        try:
            diagnostics = capture_with_playwright(
                html_path,
                args.png,
                args.pdf,
                width,
                height,
                args.scale,
                args.timeout,
            )
        except (ImportError, ModuleNotFoundError):
            diagnostics = capture_with_chromium(
                html_path,
                args.png,
                args.pdf,
                width,
                height,
                args.scale,
            )
    except (ValueError, RuntimeError, OSError, subprocess.SubprocessError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    print(json.dumps({"width": width, "height": height, "scale": args.scale, "diagnostics": diagnostics}, ensure_ascii=False))
    overflow = has_overflow(diagnostics, width, height)
    if overflow:
        print("WARNING: guide overflow detected; inspect and revise the source", file=sys.stderr)
        return 1 if args.strict else 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
