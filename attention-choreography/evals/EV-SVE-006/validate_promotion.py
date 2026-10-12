#!/usr/bin/env python3
import argparse
import hashlib
import json
import sys
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator

HERE = Path(__file__).resolve().parent
SKILL = HERE.parents[1] / "SKILL.md"
EVIDENCE = json.loads((HERE / "evidence.json").read_text())


def load_many(folder, pattern, schema_name, errors):
    files = sorted((HERE / folder).glob(pattern))
    schema = json.loads((HERE / schema_name).read_text())
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    receipts = []
    for path in files:
        try:
            receipt = json.loads(path.read_text())
        except (OSError, ValueError) as error:
            errors.append(f"{path.relative_to(HERE)}: invalid receipt: {error}")
            continue
        problems = list(validator.iter_errors(receipt))
        if problems:
            for error in problems:
                location = "/".join(str(part) for part in error.absolute_path)
                errors.append(f"{path.relative_to(HERE)}:{location}: {error.message}")
            continue
        receipts.append(receipt)
    return files, receipts


def validate_fixtures(bindings, expected, errors):
    fixtures = {}
    for binding in bindings:
        candidate, separator, filename = binding.partition("=")
        if not separator or candidate not in expected or not filename:
            errors.append(f"invalid fixture binding: {binding}; expected A=/path (A–E)")
            continue
        if candidate in fixtures:
            errors.append(f"duplicate fixture binding: {candidate}")
            continue
        fixtures[candidate] = Path(filename)
    for candidate, digest in expected.items():
        path = fixtures.get(candidate)
        if path is None:
            errors.append(f"fixture {candidate}: missing --fixture {candidate}=/path")
            continue
        try:
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError as error:
            errors.append(f"fixture {candidate}: unavailable: {error}")
            continue
        if actual != digest:
            errors.append(f"fixture {candidate}: SHA-256 mismatch: {actual}")


def fail(errors, message):
    errors.append(message)


parser = argparse.ArgumentParser(description="Verify receipts, skill and frozen A–E fixture bytes.")
parser.add_argument("--fixture", action="append", default=[], metavar="CANDIDATE=PATH",
                    help="Repeat once for each frozen contact sheet A–E.")
args = parser.parse_args()
errors = []
validate_fixtures(args.fixture, EVIDENCE["external_fixture_sha256"], errors)
actual_hash = hashlib.sha256(SKILL.read_bytes()).hexdigest()
if actual_hash != EVIDENCE["candidate_skill_sha256"]:
    fail(errors, f"skill hash mismatch: {actual_hash}")

oracle_files, oracle = load_many("receipts/oracle", "judge-*.json", "oracle.schema.json", errors)
baseline_files, baseline = load_many("receipts/baseline", "run-*.json", "selection.schema.json", errors)
treatment_files, treatment = load_many("receipts/treatment", "run-*.json", "selection.schema.json", errors)
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
