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
parser.add_argument("--provenance",type=Path,help="Original run manifest with unique run/context IDs and sealed trace hashes")
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

# Receipt filenames/counts cannot prove independent generation contexts.
def validate_provenance(path, errors):
    if path is None:
        errors.append('original run provenance missing --provenance')
        return
    try:
        rows=json.loads(path.read_text())
        if not isinstance(rows,list): raise ValueError('run provenance must be a list')
        expected={str(p.relative_to(HERE)) for p in oracle_files+baseline_files+treatment_files}
        seen=set();run_ids=set();contexts=set();traces=set()
        for row in rows:
            if not isinstance(row,dict):raise ValueError('provenance row must be an object')
            receipt=row.get('receipt');run_id=row.get('run_id');context=row.get('context_id')
            if receipt not in expected or receipt in seen:raise ValueError('unknown or duplicate provenance receipt')
            seen.add(receipt)
            if not isinstance(run_id,str) or not run_id.strip() or run_id in run_ids:raise ValueError('missing or duplicate run_id')
            if not isinstance(context,str) or not context.strip() or context in contexts:raise ValueError('missing or duplicate context_id')
            run_ids.add(run_id);contexts.add(context)
            if hashlib.sha256((HERE/receipt).read_bytes()).hexdigest()!=row.get('receipt_sha256'):raise ValueError('provenance receipt hash mismatch')
            relative=Path(row.get('trace_path',''))
            if relative.is_absolute() or '..' in relative.parts:raise ValueError('trace path must stay within provenance directory')
            trace=path.parent/relative
            if trace.is_symlink() or not trace.resolve().is_relative_to(path.parent.resolve()) or not trace.is_file():raise ValueError('trace file unavailable or outside provenance directory')
            if trace.resolve() in traces:raise ValueError('duplicate trace_path')
            traces.add(trace.resolve())
            if trace.stat().st_size==0 or trace.stat().st_size>10*1024*1024:raise ValueError('invalid trace size')
            if hashlib.sha256(trace.read_bytes()).hexdigest()!=row.get('trace_sha256'):raise ValueError('trace hash mismatch')
        if seen!=expected:raise ValueError('provenance must bind every original oracle/baseline/treatment run')
    except (ValueError,TypeError,OSError) as exc:
        errors.append('invalid original run provenance: '+str(exc))
validate_provenance(args.provenance,errors)

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
