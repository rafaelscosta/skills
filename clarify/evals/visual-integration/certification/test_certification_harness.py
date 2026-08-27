from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def load(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod


vh = load("validate_harness", ROOT / "validate_harness.py")
sc = load("score_ab", ROOT / "score_ab.py")
sp = load("seal_pair", ROOT / "seal_pair.py")


class CertificationHarnessTests(unittest.TestCase):
    def test_checked_in_harness_passes(self):
        result = vh.validate(ROOT)
        self.assertEqual(result["status"], "passed", result["errors"])

    def test_validator_detects_oracle_leakage(self):
        with tempfile.TemporaryDirectory() as td:
            dst = Path(td)
            for name in vh.REQUIRED:
                src = ROOT / name
                dst.joinpath(name).write_bytes(src.read_bytes())
            with (dst / "inputs.yaml").open("a", encoding="utf-8") as f:
                f.write("\ncritical_invariants:\n  - leaked\n")
            result = vh.validate(dst)
            self.assertEqual(result["status"], "failed")
            self.assertTrue(any("judge-only" in e for e in result["errors"]))

    def _hash_manifest(self, root: Path):
        files = [root / "run-metadata.json"] + sorted(p for p in (root / "cases").rglob("*") if p.is_file())
        lines = []
        for path in files:
            digest = hashlib.sha256(path.read_bytes()).hexdigest()
            lines.append(f"{digest}  {path.relative_to(root).as_posix()}")
        (root / "hashes.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8")

    def _write_condition(
        self,
        root: Path,
        condition: str,
        elapsed: int | None = None,
        tools: int | None = None,
        model: str = "GPT-5.6 Sol",
        surface: str = "codex",
        reasoning_effort: str = "xhigh",
        tool_budget_profile: str = "matched-standard",
    ):
        if elapsed is None:
            elapsed = 100 if condition == "control" else 120
        if tools is None:
            tools = 4 if condition == "control" else 5
        for case_id in ["refund-operational-flow", "approval-loop", "source-bound-causal"]:
            case = root / "cases" / case_id
            (case / "artifacts").mkdir(parents=True, exist_ok=True)
            (case / "response.md").write_text(f"# {condition} {case_id}\n", encoding="utf-8")
            (case / "artifacts" / f"{condition}-internal-renderer-output.html").write_text("<html>visual</html>", encoding="utf-8")
            (case / "receipt.json").write_text(json.dumps({
                "case_id": case_id,
                "condition": condition,
                "repository_commit": "internal-only",
                "clarify_version": "internal-only",
                "model": model,
                "surface": surface,
                "elapsed_ms": elapsed,
                "tool_calls": tools,
                "output_bytes": 100,
                "render_succeeded": True,
                "artifact_files": [f"artifacts/{condition}-internal-renderer-output.html"],
                "evidence_files": [f"evidence/{condition}-internal-proof.json"],
                "proof": {"semantic_validation": "passed"},
                "notes": f"internal {condition} implementation note"
            }), encoding="utf-8")
        expected_commit = sp.CONTROL_COMMIT if condition == "control" else sp.TREATMENT_COMMIT
        (root / "run-metadata.json").write_text(json.dumps({
            "schema_version": "clarify-visual-ab-run-metadata/v1",
            "run_id": "test-run",
            "condition": condition,
            "repository_commit": expected_commit,
            "model": model,
            "surface": surface,
            "reasoning_effort": reasoning_effort,
            "tool_budget_profile": tool_budget_profile,
            "isolation": "fresh_condition_context",
            "case_count": 3,
            "oracle_seen": False,
            "opposite_condition_seen": False,
            "prior_judgment_seen": False,
            "started_at": None,
            "completed_at": None,
        }), encoding="utf-8")
        self._hash_manifest(root)

    def test_sealer_blinds_sensitive_fields_and_artifact_names(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            control = td / "control"; treatment = td / "treatment"; sealed = td / "sealed"
            self._write_condition(control, "control")
            self._write_condition(treatment, "treatment")
            proc = subprocess.run([
                sys.executable, str(ROOT / "seal_pair.py"), str(control), str(treatment), str(sealed),
                "--seed", "private-seed"
            ], capture_output=True, text=True)
            self.assertEqual(proc.returncode, 0, proc.stderr or proc.stdout)
            public = json.loads((sealed / "blinded" / "manifest.json").read_text())
            self.assertEqual(public["matched_model"], "GPT-5.6 Sol")
            self.assertEqual(public["matched_reasoning_effort"], "xhigh")
            for candidate in ["A", "B"]:
                case = sealed / "blinded" / f"candidate-{candidate}" / "cases" / "approval-loop"
                receipt = json.loads((case / "receipt.json").read_text())
                self.assertEqual(set(receipt), {
                    "case_id", "candidate", "model", "surface", "elapsed_ms", "tool_calls",
                    "output_bytes", "render_succeeded", "proof"
                })
                self.assertEqual(receipt["candidate"], candidate)
                artifact_names = [p.name for p in (case / "artifacts").iterdir()]
                self.assertEqual(artifact_names, ["artifact-001.html"])
            private = json.loads((sealed / "private" / "condition-map.json").read_text())
            self.assertEqual(set(private["mapping"].values()), {"control", "treatment"})

    def test_sealer_rejects_mismatched_model(self):
        with tempfile.TemporaryDirectory() as td:
            td = Path(td)
            control = td / "control"; treatment = td / "treatment"; sealed = td / "sealed"
            self._write_condition(control, "control", model="GPT-5.6 Sol")
            self._write_condition(treatment, "treatment", model="different-model")
            proc = subprocess.run([
                sys.executable, str(ROOT / "seal_pair.py"), str(control), str(treatment), str(sealed),
                "--seed", "private-seed"
            ], capture_output=True, text=True)
            self.assertNotEqual(proc.returncode, 0)
            self.assertIn("matched-condition violation", proc.stderr + proc.stdout)
            self.assertFalse((sealed / "blinded" / "manifest.json").exists())

    def _sealed_pair(self, td: Path, treatment_elapsed: int = 120, treatment_tools: int = 5):
        control = td / "control"; treatment = td / "treatment"; sealed = td / "sealed"
        self._write_condition(control, "control", 100, 4)
        self._write_condition(treatment, "treatment", treatment_elapsed, treatment_tools)
        subprocess.run([
            sys.executable, str(ROOT / "seal_pair.py"), str(control), str(treatment), str(sealed),
            "--seed", "score-seed"
        ], check=True, capture_output=True, text=True)
        return sealed

    def _judgment(self, sealed: Path, critical_regression: bool = False, treatment_wins: int = 2):
        mapping = json.loads((sealed / "private" / "condition-map.json").read_text())["mapping"]
        treatment = next(k for k, v in mapping.items() if v == "treatment")
        control = next(k for k, v in mapping.items() if v == "control")
        manifest_sha = sc.sha256(sealed / "blinded" / "manifest.json")
        cases = []
        case_ids = ["refund-operational-flow", "approval-loop", "source-bound-causal"]
        for idx, case_id in enumerate(case_ids):
            invariant = "critical"
            tstatus = "partial" if critical_regression and idx == 0 else "passed"
            candidate = {
                treatment: {
                    "critical_invariants": {invariant: tstatus},
                    "automatic_failures": [],
                    "scores": {"fidelity": 2},
                    "total": 2,
                },
                control: {
                    "critical_invariants": {invariant: "passed"},
                    "automatic_failures": [],
                    "scores": {"fidelity": 2},
                    "total": 2,
                },
            }
            winner = treatment if idx < treatment_wins else ("tie" if idx == treatment_wins else control)
            cases.append({
                "case_id": case_id,
                "A": candidate["A"],
                "B": candidate["B"],
                "winner": winner,
                "winner_reason": "test",
            })
        return {
            "schema_version": "clarify-visual-ab-judgment/v1",
            "blinded_manifest_sha256": manifest_sha,
            "judge": {"id": "judge", "type": "model"},
            "condition_mapping_seen": False,
            "cases": cases,
        }

    def test_post_unblind_scorer_promotes_valid_two_win_result(self):
        with tempfile.TemporaryDirectory() as td:
            sealed = self._sealed_pair(Path(td))
            judgment = self._judgment(sealed)
            cmap = json.loads((sealed / "private" / "condition-map.json").read_text())
            policy = json.loads((ROOT / "promotion-policy.json").read_text())
            result = sc.evaluate(judgment, cmap, policy, sealed / "blinded")
            self.assertEqual(result["status"], "valid")
            self.assertTrue(result["promotion_passed"], result)
            self.assertEqual(result["case_results"]["wins"], 2)

    def test_post_unblind_scorer_blocks_critical_regression(self):
        with tempfile.TemporaryDirectory() as td:
            sealed = self._sealed_pair(Path(td))
            judgment = self._judgment(sealed, critical_regression=True)
            cmap = json.loads((sealed / "private" / "condition-map.json").read_text())
            policy = json.loads((ROOT / "promotion-policy.json").read_text())
            result = sc.evaluate(judgment, cmap, policy, sealed / "blinded")
            self.assertFalse(result["promotion_passed"])
            self.assertTrue(result["critical_invariant_regressions"])

    def test_post_unblind_scorer_blocks_catastrophic_cost_without_sweep(self):
        with tempfile.TemporaryDirectory() as td:
            sealed = self._sealed_pair(Path(td), treatment_elapsed=250, treatment_tools=10)
            judgment = self._judgment(sealed, treatment_wins=2)
            cmap = json.loads((sealed / "private" / "condition-map.json").read_text())
            policy = json.loads((ROOT / "promotion-policy.json").read_text())
            result = sc.evaluate(judgment, cmap, policy, sealed / "blinded")
            self.assertFalse(result["promotion_passed"])
            self.assertTrue(result["cost"]["catastrophic"])
            self.assertIn("catastrophic treatment execution-cost regression", result["failure_reasons"])

    def test_post_unblind_scorer_rejects_wrong_case_set(self):
        with tempfile.TemporaryDirectory() as td:
            sealed = self._sealed_pair(Path(td))
            judgment = self._judgment(sealed)
            judgment["cases"][0]["case_id"] = "wrong-case"
            cmap = json.loads((sealed / "private" / "condition-map.json").read_text())
            policy = json.loads((ROOT / "promotion-policy.json").read_text())
            result = sc.evaluate(judgment, cmap, policy, sealed / "blinded")
            self.assertEqual(result["status"], "invalid")
            self.assertFalse(result["promotion_passed"])


if __name__ == "__main__":
    unittest.main()
