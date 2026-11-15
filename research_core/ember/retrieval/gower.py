from __future__ import annotations
import math
from typing import Any, Dict, Iterable, List, Sequence
from ember.schemas import RetrievalResult


def _num_similarity(a: float, b: float, lo: float, hi: float) -> float:
    if hi <= lo:
        return 1.0 if a == b else 0.0
    return max(0.0, 1.0 - abs(a - b) / (hi - lo))


def gower_similarity(
    query: Dict[str, Any],
    record: Dict[str, Any],
    numeric_ranges: Dict[str, Sequence[float]],
    weights: Dict[str, float],
    categorical: Iterable[str] = (),
) -> tuple[float, Dict[str, float]]:
    categorical = set(categorical)
    numer = 0.0
    denom = 0.0
    contribution: Dict[str, float] = {}
    for key, w in weights.items():
        if w <= 0 or key not in query or key not in record:
            continue
        q, r = query[key], record[key]
        if q is None or r is None:
            continue
        if key in categorical:
            s = 1.0 if str(q).strip().lower() == str(r).strip().lower() else 0.0
        else:
            lo, hi = numeric_ranges[key]
            s = _num_similarity(float(q), float(r), float(lo), float(hi))
        numer += w * s
        denom += w
        contribution[key] = s
    return (numer / denom if denom else 0.0), contribution


def retrieve_family_gated(
    query: Dict[str, Any],
    records: List[Dict[str, Any]],
    family: str,
    numeric_ranges: Dict[str, Sequence[float]],
    weights: Dict[str, float],
    categorical: Iterable[str],
    hard_match_fields: Iterable[str] = ("material",),
    top_k: int = 5,
) -> List[RetrievalResult]:
    results = []
    for r in records:
        if r.get("family") != family:
            continue
        hard_fail = False
        for field in hard_match_fields:
            if field in query and field in r and str(query[field]).strip().lower() != str(r[field]).strip().lower():
                hard_fail = True
                break
        if hard_fail:
            continue
        score, contrib = gower_similarity(query, r, numeric_ranges, weights, categorical)
        results.append(RetrievalResult(
            record_id=str(r["record_id"]),
            score=score,
            family=family,
            source_id=str(r.get("source_id", "unknown")),
            fields={k: v for k, v in r.items() if k not in {"record_id", "source_id"}},
            contribution=contrib,
        ))
    return sorted(results, key=lambda x: x.score, reverse=True)[:top_k]
