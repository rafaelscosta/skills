from __future__ import annotations

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

    def _write_condition(self, root: Path, condition: str):
        for case_id in ["refund-operational-flow", "approval-loop", "source-bound-causal"]:
            case = root / "cases" / case_id
            (case / "artifacts").mkdir(parents=True, exist_ok=True)
            (case / "response.md").write_text(f"# {condition} {case_id}\n", encoding="utf-8")
            (case / "artifacts" / "visual.html").write_text("<html>visual</html>", encoding="utf-8")
            (case / "receipt.json").write_text(json.dumps({
                "case_id": case_id,
                "condition": condition,
                "repository_commit": "a" * 40,
                "clarify_version": "x",
                "model": "GPT-5.6 Sol",
                "surface": "codex",
                "elapsed_ms": 100 if condition == "control" else 120,
                "tool_calls": 4 if condition == "control" else 5,
                "output_bytes": 100,
                "render_succeeded": True,
                "artifact_files": ["artifacts/visual.html"],
                "proof": {"semantic_validation": "passed"},
            }), encoding="utf-8")

    def test_sealer_blinds_sensitive_condition_fields(self):
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
            for candidate in ["A", "B"]:
                receipt = json.loads((sealed / "blinded" / f"candidate-{candidate}" / "cases" / "approval-loop" / "receipt.json").read_text())
                self.assertNotIn("condition", receipt)
                self.assertNotIn("repository_commit", receipt)
                self.assertNotIn("clarify_version", receipt)
                self.assertEqual(receipt["candidate"], candidate)
            private = json.loads((sealed / "private" / "condition-map.json").read_text())
            self.assertEqual(set(private["mapping"].values()), {"control", "treatment"})

    def _sealed_pair(self, td: Path):
        control = td / "control"; treatment = td / "treatment"; sealed = td / "sealed"
        self._write_condition(control, "control")
        self._write_condition(treatment, "treatment")
        subprocess.run([
            sys.executable, str(ROOT / "seal_pair.py"), str(control), str(treatment), str(sealed),
            "--seed", "score-seed"
        ], check=True, capture_output=True, text=True)
        return sealed

    def _judgment(self, sealed: Path, critical_regression: bool = False):
        mapping = json.loads((sealed / "private" / "condition-map.json").read_text())["mapping"]
        treatment = next(k for k, v in mapping.items() if v == "treatment")
        control = next(k for k, v in mapping.items() if v == "control")
        manifest_sha = sc.sha256(sealed / "blinded" / "manifest.json")
        cases = []
        for idx, case_id in enumerate(["refund-operational-flow", "approval-loop", "source-bound-causal"]):
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
            cases.append({
                "case_id": case_id,
                "A": candidate["A"],
                "B": candidate["B"],
                "winner": treatment if idx < 2 else "tie",
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


if __name__ == "__main__":
    unittest.main()
