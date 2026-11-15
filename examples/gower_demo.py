"""Standalone demonstration of the mixed-type retrieval method.

Only synthetic examples are used. This is not the production EMBER backend and
does not predict ignition, flame propagation or spacecraft fire safety.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence


def numerical_similarity(a: float, b: float, low: float, high: float) -> float:
    """Range-normalized numeric similarity, capped in [0, 1]."""
    if high <= low:
        return 1.0 if a == b else 0.0
    return max(0.0, min(1.0, 1.0 - abs(a - b) / (high - low)))


def weighted_gower(
    query: Mapping[str, Any],
    record: Mapping[str, Any],
    numeric_ranges: Mapping[str, Sequence[float]],
    weights: Mapping[str, float],
    categorical: Iterable[str] = (),
) -> tuple[float, dict[str, float]]:
    """Return Gower-style score and per-feature contributions.

    Features with missing values are excluded from the denominator. A score of
    zero when no features are comparable must be accompanied by a missing-data
    warning in the consuming application.
    """
    categories = set(categorical)
    numerator = denominator = 0.0
    contribution = {}
    for name, weight in weights.items():
        if weight <= 0 or name not in query or name not in record:
            continue
        a, b = query[name], record[name]
        if a is None or b is None:
            continue
        if name in categories:
            score = float(str(a).strip().lower() == str(b).strip().lower())
        else:
            lower, upper = numeric_ranges[name]
            score = numerical_similarity(float(a), float(b), lower, upper)
        numerator += weight * score
        denominator += weight
        contribution[name] = score
    return (numerator / denominator if denominator else 0.0), contribution


def ranked_neighbors(
    query: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
    *,
    family: str,
    numeric_ranges: Mapping[str, Sequence[float]],
    weights: Mapping[str, float],
    categorical: Iterable[str],
    required_matches: Iterable[str] = ("material",),
    top_k: int = 5,
) -> list[dict[str, Any]]:
    """Rank family-eligible synthetic records; this is retrieval, not classification."""
    ranked = []
    for record in records:
        if record.get("family") != family:
            continue
        if any(str(query[field]).lower() != str(record[field]).lower()
               for field in required_matches if field in query and field in record):
            continue
        score, contributions = weighted_gower(
            query, record, numeric_ranges, weights, categorical
        )
        ranked.append({
            "record_id": str(record["record_id"]),
            "score": score,
            "source_id": record.get("source_id", "synthetic"),
            "contributions": contributions,
        })
    return sorted(ranked, key=lambda row: row["score"], reverse=True)[:max(0, top_k)]


if __name__ == "__main__":
    examples = [
        {"record_id": "SYN-1", "family": "demo", "material": "PMMA", "oxygen": 20, "airflow": 10},
        {"record_id": "SYN-2", "family": "demo", "material": "PMMA", "oxygen": 25, "airflow": 35},
        {"record_id": "SYN-3", "family": "demo", "material": "SIBAL", "oxygen": 21, "airflow": 10},
    ]
    query = {"material": "PMMA", "oxygen": 21, "airflow": 12}
    output = ranked_neighbors(
        query, examples, family="demo",
        numeric_ranges={"oxygen": [15, 30], "airflow": [0, 50]},
        weights={"material": 3, "oxygen": 2, "airflow": 2},
        categorical={"material"}, required_matches=("material",),
    )
    for record in output:
        print(f'{record["record_id"]}: {record["score"]:.3f} (synthetic similarity)')
