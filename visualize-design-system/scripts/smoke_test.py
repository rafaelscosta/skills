#!/usr/bin/env python3
"""Run a representative end-to-end smoke test for the bundled skill scripts."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path


def run(command: list[str]) -> None:
    print("+", " ".join(command))
    subprocess.run(command, check=True)


def main() -> int:
    skill_dir = Path(__file__).resolve().parents[1]
    fixture = skill_dir / "tests" / "fixtures" / "minimal-design-system"
    example = skill_dir / "assets" / "guide-spec.example.json"
    all_sections = skill_dir / "tests" / "fixtures" / "guide-spec-all-sections.json"

    with tempfile.TemporaryDirectory(prefix="visualize-design-system-") as tmp:
        output = Path(tmp)
        source_map = output / "source-map.json"
        html = output / "guide.html"
        png = output / "guide.png"
        pdf = output / "guide.pdf"
        all_html = output / "all-sections.html"
        all_png = output / "all-sections.png"

        run([sys.executable, str(skill_dir / "scripts" / "inventory_design_system.py"), str(fixture), "--out", str(source_map)])
        run([sys.executable, str(skill_dir / "scripts" / "validate_guide_spec.py"), str(example), "--strict"])
        run([sys.executable, str(skill_dir / "scripts" / "render_guide.py"), str(example), "--output", str(html)])
        run([sys.executable, str(skill_dir / "scripts" / "capture_guide.py"), str(html), "--png", str(png), "--pdf", str(pdf), "--strict"])
        run([sys.executable, str(skill_dir / "scripts" / "validate_guide_spec.py"), str(all_sections), "--strict"])
        run([sys.executable, str(skill_dir / "scripts" / "render_guide.py"), str(all_sections), "--output", str(all_html)])
        run([sys.executable, str(skill_dir / "scripts" / "capture_guide.py"), str(all_html), "--png", str(all_png), "--strict"])

        inventory = json.loads(source_map.read_text(encoding="utf-8"))
        counts = inventory["inventory"]["counts"]
        assert counts.get("component", 0) >= 1, counts
        assert counts.get("story", 0) >= 1, counts
        assert inventory["inventory"]["css_custom_properties"]["count"] >= 5
        assert html.stat().st_size > 10_000
        assert png.stat().st_size > 10_000
        assert pdf.stat().st_size > 10_000
        assert all_html.stat().st_size > 10_000
        assert all_png.stat().st_size > 10_000
        assert "Unsupported section type" not in all_html.read_text(encoding="utf-8")

        try:
            from PIL import Image

            with Image.open(png) as image:
                assert image.size == (1080, 1350), image.size
            with Image.open(all_png) as image:
                assert image.size == (1400, 1800), image.size
        except ImportError:
            pass

    print("SMOKE TEST PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
