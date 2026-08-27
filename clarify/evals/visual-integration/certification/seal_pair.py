#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
from pathlib import Path

CONTROL_COMMIT = "a10b7e80f3dbe29422226aa31758f7c679e829af"
TREATMENT_COMMIT = "78cb5cde584ddc9b022b7b4de91930f1ac76a1b1"
EXPECTED_CASES = {"refund-operational-flow", "approval-loop", "source-bound-causal"}
PROOF_KEYS = (
    "semantic_validation",
    "invariant_coverage",
    "layout_validation",
    "artifact_validation",
    "browser_evidence",
    "perceptual_review",
    "bindings_valid",
)
PROOF_VALUES = {"passed", "failed", "skipped", "not_provided"}
HASH_LINE = re.compile(r"^([0-9a-f]{64})\s+\*?(.+)$")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def clean_metric(value):
    return value if isinstance(value, (int, float)) and not isinstance(value, bool) else None


def standardized_receipt(raw: dict, label: str) -> dict:
    proof_in = raw.get("proof") if isinstance(raw.get("proof"), dict) else {}
    proof = {}
    for key in PROOF_KEYS:
        value = proof_in.get(key, "not_provided")
        proof[key] = value if value in PROOF_VALUES else "not_provided"
    return {
        "case_id": raw.get("case_id"),
        "candidate": label,
        "model": raw.get("model") if isinstance(raw.get("model"), str) else None,
        "surface": raw.get("surface") if isinstance(raw.get("surface"), str) else None,
        "elapsed_ms": clean_metric(raw.get("elapsed_ms")),
        "tool_calls": clean_metric(raw.get("tool_calls")),
        "output_bytes": clean_metric(raw.get("output_bytes")),
        "render_succeeded": raw.get("render_succeeded") if isinstance(raw.get("render_succeeded"), bool) else None,
        "proof": proof,
    }


def safe_relative(root: Path, relative: str) -> Path:
    rel = Path(relative)
    if rel.is_absolute() or ".." in rel.parts:
        raise ValueError(f"unsafe hashed path: {relative}")
    target = (root / rel).resolve()
    try:
        target.relative_to(root.resolve())
    except ValueError as exc:
        raise ValueError(f"hashed path escapes run root: {relative}") from exc
    return target


def verify_hash_manifest(root: Path) -> None:
    manifest = root / "hashes.sha256"
    if not manifest.is_file():
        raise ValueError(f"missing hashes.sha256 in {root}")
    entries: dict[str, str] = {}
    for line in manifest.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        match = HASH_LINE.match(line)
        if not match:
            raise ValueError(f"invalid hashes.sha256 line: {line!r}")
        digest, relative = match.groups()
        target = safe_relative(root, relative)
        if not target.is_file():
            raise ValueError(f"hashed file missing: {relative}")
        if sha256(target) != digest:
            raise ValueError(f"hash mismatch: {relative}")
        entries[relative] = digest

    required = {"run-metadata.json"}
    cases = root / "cases"
    if not cases.is_dir():
        raise ValueError(f"missing cases directory: {cases}")
    for item in cases.rglob("*"):
        if item.is_file():
            required.add(item.relative_to(root).as_posix())
    missing = sorted(required - set(entries))
    if missing:
        raise ValueError(f"hash manifest does not cover required files: {missing}")


def validate_condition(root: Path, condition: str, expected_commit: str) -> dict:
    metadata_path = root / "run-metadata.json"
    if not metadata_path.is_file():
        raise ValueError(f"missing run-metadata.json in {root}")
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    if metadata.get("schema_version") != "clarify-visual-ab-run-metadata/v1":
        raise ValueError(f"unexpected run metadata schema for {condition}")
    if metadata.get("condition") != condition:
        raise ValueError(f"run metadata condition mismatch for {condition}")
    if metadata.get("repository_commit") != expected_commit:
        raise ValueError(f"wrong frozen commit for {condition}")
    if metadata.get("case_count") != 3:
        raise ValueError(f"case_count must be 3 for {condition}")
    for flag in ("oracle_seen", "opposite_condition_seen", "prior_judgment_seen"):
        if metadata.get(flag) is not False:
            raise ValueError(f"{condition} metadata requires {flag}=false")
    for field in ("model", "surface", "reasoning_effort", "tool_budget_profile"):
        if not isinstance(metadata.get(field), str) or not metadata[field].strip():
            raise ValueError(f"{condition} metadata requires non-empty {field}")

    cases_root = root / "cases"
    case_set = {p.name for p in cases_root.iterdir() if p.is_dir()} if cases_root.is_dir() else set()
    if case_set != EXPECTED_CASES:
        raise ValueError(f"{condition} case set mismatch: {sorted(case_set)}")
    for case_id in EXPECTED_CASES:
        receipt_path = cases_root / case_id / "receipt.json"
        response_path = cases_root / case_id / "response.md"
        if not receipt_path.is_file() or not response_path.is_file():
            raise ValueError(f"{condition}/{case_id} missing response.md or receipt.json")
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if receipt.get("case_id") != case_id or receipt.get("condition") != condition:
            raise ValueError(f"{condition}/{case_id} receipt identity mismatch")
        if receipt.get("model") != metadata["model"] or receipt.get("surface") != metadata["surface"]:
            raise ValueError(f"{condition}/{case_id} receipt model/surface mismatch")

    verify_hash_manifest(root)
    return metadata


def copy_candidate(source: Path, destination: Path, label: str) -> dict:
    cases = source / "cases"
    manifest = {"candidate": label, "cases": {}}
    for case_dir in sorted(p for p in cases.iterdir() if p.is_dir()):
        out = destination / "cases" / case_dir.name
        out.mkdir(parents=True, exist_ok=True)
        response = case_dir / "response.md"
        receipt = case_dir / "receipt.json"
        shutil.copy2(response, out / "response.md")
        raw_receipt = json.loads(receipt.read_text(encoding="utf-8"))
        clean_receipt = standardized_receipt(raw_receipt, label)
        if clean_receipt["case_id"] != case_dir.name:
            raise ValueError(f"receipt case_id mismatch for {case_dir.name}")
        (out / "receipt.json").write_text(
            json.dumps(clean_receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

        artifacts = case_dir / "artifacts"
        copied_artifacts = []
        if artifacts.is_dir():
            target_artifacts = out / "artifacts"
            target_artifacts.mkdir(parents=True, exist_ok=True)
            files = sorted(p for p in artifacts.rglob("*") if p.is_file())
            for idx, item in enumerate(files, start=1):
                suffix = "".join(item.suffixes).lower()
                if len(suffix) > 20 or any(ch not in ".abcdefghijklmnopqrstuvwxyz0123456789" for ch in suffix):
                    suffix = ""
                generic = f"artifact-{idx:03d}{suffix}"
                target = target_artifacts / generic
                shutil.copy2(item, target)
                copied_artifacts.append(str(Path("artifacts") / generic))

        manifest["cases"][case_dir.name] = {
            "response_sha256": sha256(out / "response.md"),
            "receipt_sha256": sha256(out / "receipt.json"),
            "artifacts": [
                {"path": rel, "sha256": sha256(out / rel)} for rel in copied_artifacts
            ],
        }
    return manifest


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate, match, and blind control/treatment outputs as candidate A/B.")
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

    control_meta = validate_condition(control, "control", CONTROL_COMMIT)
    treatment_meta = validate_condition(treatment, "treatment", TREATMENT_COMMIT)
    for field in ("model", "surface", "reasoning_effort", "tool_budget_profile"):
        if control_meta[field] != treatment_meta[field]:
            raise SystemExit(f"matched-condition violation: {field} differs")

    blinded = root / "blinded"
    private = root / "private"
    blinded.mkdir(parents=True, exist_ok=True)
    private.mkdir(parents=True, exist_ok=True)

    bit = int(hashlib.sha256(args.seed.encode("utf-8")).hexdigest(), 16) & 1
    mapping = {"A": "control", "B": "treatment"} if bit == 0 else {"A": "treatment", "B": "control"}
    sources = {"control": control, "treatment": treatment}
    public = {
        "schema_version": "clarify-visual-ab-blinded/v1",
        "matched_model": control_meta["model"],
        "matched_surface": control_meta["surface"],
        "matched_reasoning_effort": control_meta["reasoning_effort"],
        "matched_tool_budget_profile": control_meta["tool_budget_profile"],
        "candidates": {},
    }
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
        "matched": {
            "model": control_meta["model"],
            "surface": control_meta["surface"],
            "reasoning_effort": control_meta["reasoning_effort"],
            "tool_budget_profile": control_meta["tool_budget_profile"],
        },
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
