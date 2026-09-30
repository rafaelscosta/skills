#!/usr/bin/env python3
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1] / "SKILL.md"
EVIDENCE = json.loads((HERE / "evidence.json").read_text())


def load_many(folder, pattern):
    files = sorted((HERE / folder).glob(pattern))
    return files, [json.loads(p.read_text()) for p in files]


def fail(errors, message):
    errors.append(message)


errors = []
actual_hash = hashlib.sha256(SKILL.read_bytes()).hexdigest()
if actual_hash != EVIDENCE["candidate_skill_sha256"]:
    fail(errors, f"skill hash mismatch: {actual_hash}")

oracle_files, oracle = load_many("receipts/oracle", "judge-*.json")
baseline_files, baseline = load_many("receipts/baseline", "run-*.json")
treatment_files, treatment = load_many("receipts/treatment", "run-*.json")
if len(oracle_files) != EVIDENCE["oracle_judges"]:
    fail(errors, f"oracle receipt count={len(oracle_files)}")
if len(baseline_files) != EVIDENCE["baseline_runs"]:
    fail(errors, f"baseline receipt count={len(baseline_files)}")
if len(treatment_files) != EVIDENCE["treatment_runs"]:
    fail(errors, f"treatment receipt count={len(treatment_files)}")

target = EVIDENCE["expected_oracle_top"]
runner = EVIDENCE["expected_oracle_runner_up"]
if any(r.get("top_candidate") != target for r in oracle):
    fail(errors, "oracle is not unanimous on target")
if any(r.get("runner_up") != runner for r in oracle):
    fail(errors, "oracle is not unanimous on runner-up")

blocker_sets = [set(r.get("blocking_rejections", [])) for r in oracle]
consensus_blockers = set.intersection(*blocker_sets) if blocker_sets else set()
expected_blockers = set(EVIDENCE["expected_consensus_blockers"])
if consensus_blockers != expected_blockers:
    fail(errors, f"consensus blockers={sorted(consensus_blockers)}")

baseline_counts = Counter(r.get("selected_candidate") for r in baseline)
treatment_counts = Counter(r.get("selected_candidate") for r in treatment)
baseline_alignment = baseline_counts[target]
treatment_alignment = treatment_counts[target]
policy = EVIDENCE["promotion_policy"]
if treatment_alignment != policy["require_treatment_alignment"]:
    fail(errors, f"treatment alignment={treatment_alignment}")
if policy["require_strict_uplift_over_baseline"] and treatment_alignment <= baseline_alignment:
    fail(errors, f"no strict uplift: {baseline_alignment}->{treatment_alignment}")
if policy["forbid_consensus_blocker_selection"]:
    bad = [r.get("selected_candidate") for r in treatment if r.get("selected_candidate") in consensus_blockers]
    if bad:
        fail(errors, f"treatment selected blockers={bad}")

result = {
    "eval": EVIDENCE["id"],
    "result": "PASS" if not errors else "FAIL",
    "oracle_top": target,
    "oracle_unanimous": sum(r.get("top_candidate") == target for r in oracle),
    "baseline_alignment": f"{baseline_alignment}/{len(baseline)}",
    "treatment_alignment": f"{treatment_alignment}/{len(treatment)}",
    "baseline_counts": dict(sorted(baseline_counts.items())),
    "treatment_counts": dict(sorted(treatment_counts.items())),
    "consensus_blockers": sorted(consensus_blockers),
    "errors": errors,
}
print(json.dumps(result, indent=2, sort_keys=True))
sys.exit(1 if errors else 0)
