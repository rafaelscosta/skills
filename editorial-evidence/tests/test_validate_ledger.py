import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR = ROOT / "scripts" / "validate_ledger.py"
FIXTURES = ROOT / "tests" / "fixtures"


class LedgerValidatorTests(unittest.TestCase):
    def run_validator(self, name):
        proc = subprocess.run(
            [sys.executable, str(VALIDATOR), str(FIXTURES / name), "--json"],
            capture_output=True,
            text=True,
        )
        return proc, json.loads(proc.stdout)

    def test_valid_fixture_passes(self):
        proc, receipt = self.run_validator("valid-ledger.json")
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(receipt["status"], "PASSED")
        self.assertEqual(receipt["errors"], [])

    def test_invalid_fixture_fails_closed(self):
        proc, receipt = self.run_validator("invalid-ledger.json")
        self.assertEqual(proc.returncode, 1)
        self.assertEqual(receipt["status"], "FAILED")
        codes = {item["code"] for item in receipt["errors"]}
        self.assertIn("verified_without_support", codes)
        self.assertIn("freshness_check_missing", codes)
        self.assertIn("causal_review_missing", codes)


if __name__ == "__main__":
    unittest.main()
