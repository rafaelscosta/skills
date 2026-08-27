import importlib.util
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("score_clarity", ROOT / "scripts" / "score_clarity.py")
score_clarity = importlib.util.module_from_spec(spec)
spec.loader.exec_module(score_clarity)

BASE = {name: 2 for name in score_clarity.BASE_DIMENSIONS}
TRUSTED = {name: 2 for name in score_clarity.ALL_DIMENSIONS}


class ScoreClarityV2Tests(unittest.TestCase):
    def test_legacy_medium_payload_preserves_v1_contract(self):
        result = score_clarity.evaluate({"risk_level": "medium", "scores": dict(BASE)})
        self.assertTrue(result["passed"])
        self.assertEqual(result["scoring_contract"], "clarify-rubric/v1-legacy")
        self.assertEqual(result["maximum"], 28)
        self.assertEqual(result["threshold"], 24)

    def test_legacy_critical_gate_still_fails_below_two(self):
        scores = dict(BASE)
        scores["fidelity"] = 1
        result = score_clarity.evaluate({"risk_level": "critical", "scores": scores})
        self.assertFalse(result["passed"])
        self.assertIn("fidelity", result["failed_critical_dimensions"])

    def test_legacy_payload_rejects_visual_proof_dimensions_without_profile(self):
        scores = dict(BASE)
        scores["visual_delivery_proof"] = 2
        with self.assertRaisesRegex(ValueError, "explicit profile"):
            score_clarity.evaluate({"risk_level": "medium", "scores": scores})

    def test_trusted_visual_requires_all_sixteen_dimensions(self):
        scores = dict(TRUSTED)
        scores.pop("visual_invariant_coverage")
        with self.assertRaisesRegex(ValueError, "Missing dimensions"):
            score_clarity.evaluate({"profile": "trusted_visual", "scores": scores})

    def test_trusted_visual_all_two_passes(self):
        result = score_clarity.evaluate({"profile": "trusted_visual", "scores": dict(TRUSTED)})
        self.assertTrue(result["passed"])
        self.assertEqual(result["scoring_contract"], "clarify-rubric/v2")
        self.assertEqual(result["maximum"], 32)
        self.assertEqual(result["threshold"], 30)

    def test_trusted_visual_delivery_proof_is_hard_gate(self):
        scores = dict(TRUSTED)
        scores["visual_delivery_proof"] = 1
        result = score_clarity.evaluate({"profile": "trusted_visual", "scores": scores})
        self.assertFalse(result["passed"])
        self.assertIn("visual_delivery_proof", result["failed_required_two"])

    def test_operational_profile_remains_non_visual(self):
        result = score_clarity.evaluate({"profile": "operational", "scores": dict(BASE)})
        self.assertTrue(result["passed"])
        self.assertEqual(result["maximum"], 28)
        self.assertEqual(result["threshold"], 25)

    def test_non_visual_profile_rejects_visual_points_as_score_boost(self):
        scores = dict(TRUSTED)
        with self.assertRaisesRegex(ValueError, "not applicable"):
            score_clarity.evaluate({"profile": "operational", "scores": scores})

    def test_high_risk_profile_is_reachable_without_visual_dimensions(self):
        result = score_clarity.evaluate({"profile": "high_risk", "scores": dict(BASE)})
        self.assertTrue(result["passed"])
        self.assertEqual(result["maximum"], 28)
        self.assertEqual(result["threshold"], 27)

    def test_boolean_is_not_accepted_as_numeric_score(self):
        scores = dict(BASE)
        scores["audience_fit"] = True
        with self.assertRaisesRegex(ValueError, "integer from 0 to 2"):
            score_clarity.evaluate({"profile": "operational", "scores": scores})


if __name__ == "__main__":
    unittest.main()
