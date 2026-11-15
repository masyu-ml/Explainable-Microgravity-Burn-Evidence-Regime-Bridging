"""Regression tests for the independent synthetic retrieval demonstration."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))
from gower_demo import numerical_similarity, ranked_neighbors, weighted_gower


class GowerDemoTests(unittest.TestCase):
    def test_identical_numeric(self):
        self.assertEqual(numerical_similarity(4, 4, 0, 10), 1.0)

    def test_numeric_bound(self):
        self.assertEqual(numerical_similarity(-100, 100, 0, 10), 0.0)

    def test_no_comparable_features(self):
        score, details = weighted_gower({"x": None}, {"x": 3}, {"x": (0, 10)}, {"x": 1})
        self.assertEqual((score, details), (0.0, {}))

    def test_categorical_case_insensitive(self):
        score, _ = weighted_gower(
            {"material": "PMMA"}, {"material": "pmma"},
            {}, {"material": 3}, ("material",)
        )
        self.assertEqual(score, 1.0)

    def test_ranking_with_material_gate(self):
        records = [
            {"record_id": "A", "family": "synthetic", "material": "PMMA", "oxygen": 21},
            {"record_id": "B", "family": "synthetic", "material": "SIBAL", "oxygen": 21},
            {"record_id": "C", "family": "other", "material": "PMMA", "oxygen": 21},
        ]
        ranked = ranked_neighbors(
            {"material": "PMMA", "oxygen": 21}, records, family="synthetic",
            numeric_ranges={"oxygen": (15, 30)}, weights={"material": 1, "oxygen": 1},
            categorical={"material"},
        )
        self.assertEqual([r["record_id"] for r in ranked], ["A"])


if __name__ == "__main__":
    unittest.main()
