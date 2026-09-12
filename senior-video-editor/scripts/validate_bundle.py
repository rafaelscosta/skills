#!/usr/bin/env python3
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SKILLS = [
    "senior-video-editor",
    "video-edit-contract",
    "footage-intelligence",
    "story-edit",
    "attention-choreography",
    "supervising-video-editor",
]
errors = []

for name in SKILLS:
    base = ROOT / name
    for rel in ["SKILL.md", "config.yaml", "agents/openai.yaml"]:
        if not (base / rel).is_file():
            errors.append(f"missing {name}/{rel}")
    skill = (base / "SKILL.md").read_text() if (base / "SKILL.md").is_file() else ""
    m = re.search(r"^name:\s*([^\n]+)$", skill, re.M)
    if not m or m.group(1).strip() != name:
        errors.append(f"frontmatter name mismatch: {name}")
    if "Use " not in skill or "Do not use" not in skill:
        errors.append(f"routing boundary missing: {name}")
owner = (ROOT / "senior-video-editor" / "SKILL.md").read_text()
for routed in ["video-edit-contract", "footage-intelligence", "story-edit", "attention-choreography", "supervising-video-editor"]:
    if f"${routed}" not in owner:
        errors.append(f"owner does not route ${routed}")
if "performance-selection" not in owner or "timing-rhythm" not in owner:
    errors.append("empirical non-route boundaries missing")

promotion = ROOT / "attention-choreography" / "evals" / "EV-SVE-006" / "validate_promotion.py"
if not promotion.is_file():
    errors.append("EV-SVE-006 promotion validator missing")
else:
    run = subprocess.run([sys.executable, str(promotion)], capture_output=True, text=True)
    if run.returncode != 0:
        errors.append("EV-SVE-006 failed: " + run.stdout.strip())

for path in ROOT.glob("*/config.yaml"):
    text = path.read_text()
    if "publication_default: deny" not in text:
        errors.append(f"unsafe publication default: {path.parent.name}")

result = {"system": "senior-video-editor-v0.1", "skills": len(SKILLS), "result": "PASS" if not errors else "FAIL", "errors": errors}
print(json.dumps(result, indent=2, sort_keys=True))
sys.exit(1 if errors else 0)
