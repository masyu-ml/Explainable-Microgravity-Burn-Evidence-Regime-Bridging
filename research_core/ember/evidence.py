from __future__ import annotations
import csv
from pathlib import Path
from typing import Any, Dict, List
from ember.retrieval.gower import retrieve_family_gated

ROOT = Path(__file__).resolve().parents[1]


def _coerce(value: str) -> Any:
    if value == "":
        return None
    try:
        return float(value)
    except ValueError:
        return value


def load_evidence_catalog(path: Path | None = None) -> List[Dict[str, Any]]:
    path = path or (ROOT / "data" / "evidence_catalog.csv")
    with path.open(newline="", encoding="utf-8") as f:
        return [{k: _coerce(v) for k, v in row.items()} for row in csv.DictReader(f)]


def retrieve_evidence(query: Dict[str, Any], family: str, top_k: int = 5):
    records = load_evidence_catalog()
    numeric_ranges = {
        "gravity_g": (0.0, 1.0),
        "pressure_kpa": (20.0, 110.0),
        "oxygen_fraction": (0.13, 0.35),
        "forced_flow_m_s": (0.0, 0.65),
        "rod_radius_cm": (0.318, 1.905),
        "thickness_mm": (0.1, 10.0),
        "sample_length_m": (0.05, 0.30),
        "pyrolysis_length_m": (0.005, 0.20),
        "core_radius_mm": (0.1, 0.4),
        "insulation_thickness_mm": (0.1, 0.4),
        "channel_gap_mm": (1.0, 25.0),
    }
    weights = {
        "material": 3.0,
        "geometry": 2.0,
        "gravity_g": 2.0,
        "pressure_kpa": 1.5,
        "oxygen_fraction": 1.5,
        "forced_flow_m_s": 2.0,
        "rod_radius_cm": 1.5,
        "thickness_mm": 1.5,
        "sample_length_m": 0.5,
        "pyrolysis_length_m": 1.5,
        "core_radius_mm": 1.5,
        "insulation_thickness_mm": 1.5,
        "channel_gap_mm": 1.0,
    }
    return retrieve_family_gated(
        query=query,
        records=records,
        family=family,
        numeric_ranges=numeric_ranges,
        weights=weights,
        categorical=("material", "geometry"),
        hard_match_fields=("material",),
        top_k=top_k,
    )
