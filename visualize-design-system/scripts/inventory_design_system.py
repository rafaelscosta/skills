#!/usr/bin/env python3
"""Create a lightweight, repository-grounded design-system inventory.

The script intentionally avoids executing project code. It finds likely design-system
sources, extracts static CSS custom properties and JSON-like token leaves, detects
common UI tooling from package manifests, and emits a source-map JSON that Codex can
verify with targeted inspection.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    "node_modules",
    "dist",
    "build",
    "coverage",
    ".next",
    ".nuxt",
    ".svelte-kit",
    ".turbo",
    ".cache",
    "vendor",
    "target",
    "out",
}

TEXT_EXTENSIONS = {
    ".css",
    ".scss",
    ".sass",
    ".less",
    ".pcss",
    ".json",
    ".yaml",
    ".yml",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".vue",
    ".svelte",
    ".md",
    ".mdx",
}

COMPONENT_EXTENSIONS = {".js", ".jsx", ".ts", ".tsx", ".vue", ".svelte"}
DOC_EXTENSIONS = {".md", ".mdx"}
CSS_EXTENSIONS = {".css", ".scss", ".sass", ".less", ".pcss"}

CSS_VAR_RE = re.compile(r"(?P<name>--[A-Za-z0-9_-]+)\s*:\s*(?P<value>[^;}{]+)")
VARIANT_KEY_RE = re.compile(
    r"(?:variants?|compoundVariants?|defaultVariants?)\s*[:=]\s*[{[]|"
    r"\b(?:variant|size|state|tone|intent|appearance)\s*[:=]",
    re.IGNORECASE,
)

KNOWN_DEPENDENCIES = {
    "@storybook/react": "Storybook",
    "@storybook/vue3": "Storybook",
    "@storybook/svelte": "Storybook",
    "storybook": "Storybook",
    "tailwindcss": "Tailwind CSS",
    "class-variance-authority": "Class Variance Authority",
    "@radix-ui/react-slot": "Radix UI",
    "@mui/material": "Material UI",
    "@chakra-ui/react": "Chakra UI",
    "@mantine/core": "Mantine",
    "antd": "Ant Design",
    "@vanilla-extract/css": "vanilla-extract",
    "styled-components": "styled-components",
    "@emotion/react": "Emotion",
    "style-dictionary": "Style Dictionary",
    "@tokens-studio/sd-transforms": "Tokens Studio transforms",
    "lucide-react": "Lucide icons",
    "@heroicons/react": "Heroicons",
    "@playwright/test": "Playwright",
    "vitest": "Vitest",
    "jest": "Jest",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path, help="Repository or design-system root")
    parser.add_argument("--out", type=Path, required=True, help="Output JSON path")
    parser.add_argument(
        "--max-files",
        type=int,
        default=12000,
        help="Maximum files to scan before stopping (default: 12000)",
    )
    parser.add_argument(
        "--max-file-bytes",
        type=int,
        default=2_000_000,
        help="Skip content extraction for larger files (default: 2MB)",
    )
    return parser.parse_args()


def rel(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def iter_files(root: Path, max_files: int) -> tuple[list[Path], bool]:
    files: list[Path] = []
    truncated = False
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in IGNORE_DIRS and not d.startswith(".pytest")]
        for filename in filenames:
            files.append(Path(dirpath) / filename)
            if len(files) >= max_files:
                truncated = True
                return files, truncated
    return files, truncated


def safe_read_text(path: Path, max_bytes: int) -> str | None:
    try:
        if path.stat().st_size > max_bytes:
            return None
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None


def git_value(root: Path, args: list[str]) -> str | None:
    try:
        result = subprocess.run(
            ["git", "-C", str(root), *args],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            timeout=5,
        )
        value = result.stdout.strip()
        return value or None
    except (OSError, subprocess.SubprocessError):
        return None


def load_package_dependencies(package_file: Path) -> dict[str, str]:
    try:
        data = json.loads(package_file.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    deps: dict[str, str] = {}
    for key in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
        block = data.get(key)
        if isinstance(block, dict):
            deps.update({str(name): str(version) for name, version in block.items()})
    return deps


def detect_tools(dependencies: dict[str, str], files: Iterable[Path], root: Path) -> list[dict[str, Any]]:
    detected: dict[str, dict[str, Any]] = {}
    for dep, version in dependencies.items():
        for key, tool in KNOWN_DEPENDENCIES.items():
            if dep == key or dep.startswith(key + "/") or (key.endswith("slot") and dep.startswith("@radix-ui/")):
                detected.setdefault(tool, {"name": tool, "evidence": []})["evidence"].append(
                    {"kind": "dependency", "name": dep, "version": version}
                )
    names = {p.name for p in files}
    path_strings = {rel(p, root) for p in files}
    if "components.json" in names:
        detected.setdefault("shadcn/ui conventions", {"name": "shadcn/ui conventions", "evidence": []})[
            "evidence"
        ].append({"kind": "file", "path": "components.json"})
    if any(p.startswith(".storybook/") for p in path_strings):
        detected.setdefault("Storybook", {"name": "Storybook", "evidence": []})["evidence"].append(
            {"kind": "path", "path": ".storybook/"}
        )
    return sorted(detected.values(), key=lambda item: item["name"].lower())


def classify_file(path: Path, root: Path) -> set[str]:
    rp = rel(path, root).lower()
    name = path.name.lower()
    suffix = path.suffix.lower()
    categories: set[str] = set()

    if name in {"package.json", "components.json"} or name.startswith("tailwind.config"):
        categories.add("configuration")
    if rp.startswith(".storybook/") or "/.storybook/" in rp:
        categories.add("storybook-config")
    if ".stories." in name or ".story." in name:
        categories.add("story")
    if any(marker in name for marker in (".test.", ".spec.", ".visual.")):
        categories.add("test")
    if suffix in DOC_EXTENSIONS or "/docs/" in f"/{rp}/":
        categories.add("documentation")
    if suffix in CSS_EXTENSIONS:
        categories.add("style")
    if suffix in COMPONENT_EXTENSIONS and any(
        segment in rp.split("/") for segment in ("component", "components", "ui", "primitives")
    ):
        if not {"story", "test"} & categories and path.stem.lower() not in {"index", "types", "utils"}:
            categories.add("component")
    token_markers = ("token", "theme", "palette", "color", "spacing", "typography", "radius", "shadow")
    if any(marker in name for marker in token_markers) or any(
        segment in {"tokens", "token", "theme", "themes"} for segment in rp.split("/")
    ):
        if suffix in TEXT_EXTENSIONS:
            categories.add("token-source")
    if name.endswith(".tokens.json"):
        categories.add("token-source")
    return categories


def flatten_json_tokens(value: Any, prefix: str = "") -> list[tuple[str, Any]]:
    tokens: list[tuple[str, Any]] = []
    if isinstance(value, dict):
        if "$value" in value:
            tokens.append((prefix, value.get("$value")))
            return tokens
        if "value" in value and len(value) <= 8:
            tokens.append((prefix, value.get("value")))
            return tokens
        for key, child in value.items():
            if key.startswith("$"):
                continue
            child_prefix = f"{prefix}.{key}" if prefix else str(key)
            tokens.extend(flatten_json_tokens(child, child_prefix))
    elif isinstance(value, (str, int, float, bool)) and prefix:
        tokens.append((prefix, value))
    return tokens


def extract_json_tokens(path: Path, max_bytes: int) -> list[dict[str, Any]]:
    text = safe_read_text(path, max_bytes)
    if text is None:
        return []
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return []
    extracted: list[dict[str, Any]] = []
    for name, value in flatten_json_tokens(data):
        if not name:
            continue
        extracted.append({"name": name, "value": value})
        if len(extracted) >= 1000:
            break
    return extracted


def main() -> int:
    args = parse_args()
    root = args.root.expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"error: root is not a directory: {root}", file=sys.stderr)
        return 2

    files, truncated = iter_files(root, args.max_files)
    categories: dict[str, list[str]] = defaultdict(list)
    dependencies: dict[str, str] = {}
    css_variables: list[dict[str, Any]] = []
    json_tokens: list[dict[str, Any]] = []
    variant_signal_files: list[str] = []
    skipped_large: list[str] = []

    for path in files:
        rp = rel(path, root)
        file_categories = classify_file(path, root)
        for category in file_categories:
            categories[category].append(rp)

        if path.name == "package.json":
            dependencies.update(load_package_dependencies(path))

        if path.suffix.lower() in CSS_EXTENSIONS:
            text = safe_read_text(path, args.max_file_bytes)
            if text is None:
                skipped_large.append(rp)
            else:
                for match in CSS_VAR_RE.finditer(text):
                    css_variables.append(
                        {
                            "name": match.group("name"),
                            "value": match.group("value").strip(),
                            "source": rp,
                        }
                    )
                    if len(css_variables) >= 3000:
                        break

        if "token-source" in file_categories and path.suffix.lower() == ".json":
            for token in extract_json_tokens(path, args.max_file_bytes):
                token["source"] = rp
                json_tokens.append(token)
                if len(json_tokens) >= 3000:
                    break

        if "component" in file_categories:
            text = safe_read_text(path, args.max_file_bytes)
            if text is None:
                skipped_large.append(rp)
            elif VARIANT_KEY_RE.search(text):
                variant_signal_files.append(rp)

    for key in categories:
        categories[key] = sorted(set(categories[key]))
    css_variables = sorted(css_variables, key=lambda x: (x["name"], x["source"]))
    json_tokens = sorted(json_tokens, key=lambda x: (x["name"], x["source"]))

    tools = detect_tools(dependencies, files, root)
    commit = git_value(root, ["rev-parse", "HEAD"])
    branch = git_value(root, ["rev-parse", "--abbrev-ref", "HEAD"])

    source_records: list[dict[str, Any]] = []
    for category in (
        "configuration",
        "storybook-config",
        "token-source",
        "style",
        "component",
        "story",
        "test",
        "documentation",
    ):
        values = categories.get(category, [])
        for path in values[:250]:
            source_records.append({"path": path, "kind": category, "status": "discovered"})

    gaps: list[dict[str, str]] = []
    if not categories.get("token-source") and not css_variables:
        gaps.append({"topic": "tokens", "detail": "No obvious token source or CSS custom properties found."})
    if not categories.get("component"):
        gaps.append({"topic": "components", "detail": "No component source directory was confidently detected."})
    if not categories.get("story"):
        gaps.append({"topic": "render-harness", "detail": "No component stories were detected."})
    if not categories.get("documentation"):
        gaps.append({"topic": "documentation", "detail": "No Markdown/MDX documentation was detected."})

    output = {
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "repository": {
            "root": str(root),
            "commit": commit,
            "branch": branch,
            "scan_truncated": truncated,
            "files_scanned": len(files),
        },
        "technology": {
            "detected_tools": tools,
            "package_dependencies": dict(sorted(dependencies.items())),
            "render_harnesses": [
                tool["name"]
                for tool in tools
                if tool["name"] in {"Storybook", "Playwright"}
            ],
        },
        "inventory": {
            "counts": {key: len(value) for key, value in sorted(categories.items())},
            "files": {key: value[:250] for key, value in sorted(categories.items())},
            "lists_truncated_at": 250,
            "css_custom_properties": {
                "count": len(css_variables),
                "items": css_variables[:1000],
                "truncated": len(css_variables) > 1000,
            },
            "json_tokens": {
                "count": len(json_tokens),
                "items": json_tokens[:1000],
                "truncated": len(json_tokens) > 1000,
            },
            "variant_signal_files": sorted(set(variant_signal_files))[:250],
            "skipped_large_files": sorted(set(skipped_large))[:100],
        },
        "sources": source_records,
        "claims": [],
        "conflicts": [],
        "gaps": gaps,
        "assumptions": [
            "This is a static discovery pass. Dynamic TypeScript theme values and runtime behavior require targeted inspection."
        ],
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"wrote {args.out}")
    print(
        "summary: "
        f"{len(categories.get('component', []))} components, "
        f"{len(categories.get('story', []))} stories, "
        f"{len(css_variables)} CSS variables, "
        f"{len(json_tokens)} JSON token leaves"
    )
    if truncated:
        print(f"warning: scan stopped at --max-files={args.max_files}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
