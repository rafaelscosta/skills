import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent


class PromotionIntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.skill = Path(self.temporary.name) / "attention-choreography"
        self.eval = self.skill / "evals" / HERE.name
        shutil.copytree(HERE, self.eval, ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy2(HERE.parents[1] / "SKILL.md", self.skill / "SKILL.md")
        evidence_path = self.eval / "evidence.json"
        evidence = json.loads(evidence_path.read_text())
        self.arguments = []
        self.fixtures = {}
        for candidate in "ABCDE":
            fixture = Path(self.temporary.name) / f"{candidate}.bin"
            fixture.write_bytes(f"synthetic test fixture {candidate}".encode())
            evidence["external_fixture_sha256"][candidate] = hashlib.sha256(
                fixture.read_bytes()
            ).hexdigest()
            self.arguments.extend(["--fixture", f"{candidate}={fixture}"])
            self.fixtures[candidate] = fixture
        evidence_path.write_text(json.dumps(evidence))

    def run_validator(self, arguments=None):
        result = subprocess.run(
            [sys.executable, str(self.eval / "validate_promotion.py"),
             *(self.arguments if arguments is None else arguments)],
            capture_output=True, text=True,
        )
        return result.returncode, json.loads(result.stdout)

    def rewrite_receipt(self, folder, change):
        receipt = next((self.eval / "receipts" / folder).glob("*.json"))
        data = json.loads(receipt.read_text())
        receipt.write_text(json.dumps(change(data)))

    def assert_rejected(self, fragment, arguments=None):
        code, result = self.run_validator(arguments)
        self.assertEqual(code, 1)
        self.assertEqual(result["result"], "FAIL")
        self.assertTrue(any(fragment in error for error in result["errors"]), result)

    def test_complete_receipts_and_matching_bytes_pass(self):
        code, result = self.run_validator()
        self.assertEqual(code, 0, result)
        self.assertEqual(result["result"], "PASS")
        self.assertEqual(result["baseline_alignment"], "2/5")
        self.assertEqual(result["treatment_alignment"], "5/5")

    def test_missing_fixture_inputs_fail(self):
        self.assert_rejected("missing --fixture", [])

    def test_changed_fixture_bytes_fail(self):
        self.fixtures["C"].write_bytes(b"changed fixture")
        self.assert_rejected("fixture C: SHA-256 mismatch")

    def test_unreadable_fixture_fails(self):
        self.fixtures["D"].unlink()
        self.assert_rejected("fixture D: unavailable")

    def test_duplicate_fixture_binding_fails(self):
        self.assert_rejected("duplicate fixture binding", self.arguments + self.arguments[:2])

    def test_unknown_fixture_binding_fails(self):
        self.assert_rejected("invalid fixture binding", self.arguments + ["--fixture", "F=extra"])

    def test_incomplete_oracle_receipt_fails(self):
        self.rewrite_receipt("oracle", lambda d: {
            key: d[key] for key in ("top_candidate", "runner_up", "blocking_rejections")
        })
        self.assert_rejected("is a required property")

    def test_incomplete_selection_receipt_fails(self):
        self.rewrite_receipt("treatment", lambda d: {"selected_candidate": d["selected_candidate"]})
        self.assert_rejected("is a required property")

    def test_duplicate_ranking_fails(self):
        self.rewrite_receipt("oracle", lambda d: {**d, "ranking": ["A"] * 5})
        self.assert_rejected("non-unique elements")

    def test_malformed_receipt_fails(self):
        next((self.eval / "receipts" / "baseline").glob("*.json")).write_text("{")
        self.assert_rejected("invalid receipt")


if __name__ == "__main__":
    unittest.main()
