#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
from pathlib import Path

SENSITIVE_KEYS = {
    "condition",
    "repository_commit",
    "clarify_version",
    "visual_compiler_version",
    "integration",
    "skill_version",
}


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sanitize(value):
    if isinstance(value, dict):
        return {k: sanitize(v) for k, v in value.items() if k not in SENSITIVE_KEYS}
    if isinstance(value, list):
        return [sanitize(v) for v in value]
    return value


def copy_candidate(source: Path, destination: Path, label: str) -> dict:
    cases = source / "cases"
    if not cases.is_dir():
        raise ValueError(f"missing cases directory: {cases}")
    manifest = {"candidate": label, "cases": {}}
    for case_dir in sorted(p for p in cases.iterdir() if p.is_dir()):
        out = destination / "cases" / case_dir.name
        out.mkdir(parents=True, exist_ok=True)
        response = case_dir / "response.md"
        receipt = case_dir / "receipt.json"
        if not response.is_file() or not receipt.is_file():
            raise ValueError(f"case {case_dir.name} must contain response.md and receipt.json")
        shutil.copy2(response, out / "response.md")
        raw_receipt = json.loads(receipt.read_text(encoding="utf-8"))
        clean_receipt = sanitize(raw_receipt)
        clean_receipt["candidate"] = label
        (out / "receipt.json").write_text(
            json.dumps(clean_receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
        artifacts = case_dir / "artifacts"
        copied_artifacts = []
        if artifacts.is_dir():
            target_artifacts = out / "artifacts"
            target_artifacts.mkdir(parents=True, exist_ok=True)
            for item in sorted(p for p in artifacts.rglob("*") if p.is_file()):
                rel = item.relative_to(artifacts)
                target = target_artifacts / rel
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, target)
                copied_artifacts.append(str(Path("artifacts") / rel))
        manifest["cases"][case_dir.name] = {
            "response_sha256": sha256(out / "response.md"),
            "receipt_sha256": sha256(out / "receipt.json"),
            "artifacts": [
                {"path": rel, "sha256": sha256(out / rel)} for rel in copied_artifacts
            ],
        }
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description="Blind control/treatment outputs as candidate A/B.")
    ap.add_argument("control_dir")
    ap.add_argument("treatment_dir")
    ap.add_argument("output_dir")
    ap.add_argument("--seed", required=True, help="Private run seed; keep it away from the judge.")
    args = ap.parse_args()

    control = Path(args.control_dir).resolve()
    treatment = Path(args.treatment_dir).resolve()
    root = Path(args.output_dir).resolve()
    if root.exists() and any(root.iterdir()):
        raise SystemExit("output_dir must be absent or empty")
    blinded = root / "blinded"
    private = root / "private"
    blinded.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    bit = int(hashlib.sha256(args.seed.encode("utf-8")).hexdigest(), 16) & 1
    mapping = {"A": "control", "B": "treatment"} if bit == 0 else {"A": "treatment", "B": "control"}
    sources = {"control": control, "treatment": treatment}
    public = {"schema_version": "clarify-visual-ab-blinded/v1", "candidates": {}}
    for label in ("A", "B"):
        dest = blinded / f"candidate-{label}"
        dest.mkdir(parents=True, exist_ok=True)
        public["candidates"][label] = copy_candidate(sources[mapping[label]], dest, label)

    (blinded / "manifest.json").write_text(json.dumps(public, indent=2) + "\n", encoding="utf-8")
    private_map = {
        "schema_version": "clarify-visual-ab-condition-map/v1",
        "seed_sha256": hashlib.sha256(args.seed.encode("utf-8")).hexdigest(),
        "mapping": mapping,
        "blinded_manifest_sha256": sha256(blinded / "manifest.json"),
    }
    (private / "condition-map.json").write_text(json.dumps(private_map, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({
        "status": "sealed",
        "judge_package": str(blinded),
        "private_map": str(private / "condition-map.json"),
        "manifest_sha256": private_map["blinded_manifest_sha256"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
