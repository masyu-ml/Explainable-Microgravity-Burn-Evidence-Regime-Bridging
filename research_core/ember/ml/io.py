from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence
import pandas as pd
import numpy as np


@dataclass
class EmpiricalDataset:
    X: np.ndarray
    y: np.ndarray
    feature_names: list[str]
    provenance_levels: list[str]


def load_empirical_csv(path: str | Path, feature_names: Sequence[str], target_name: str, provenance_column: str = "evidence_level") -> EmpiricalDataset:
    df = pd.read_csv(path)
    missing = [c for c in [*feature_names, target_name, provenance_column] if c not in df.columns]
    if missing:
        raise ValueError(f"Missing columns: {missing}")
    clean = df[[*feature_names, target_name, provenance_column]].dropna()
    if len(clean) == 0:
        raise ValueError("No complete rows after dropping missing values")
    return EmpiricalDataset(
        X=clean[list(feature_names)].to_numpy(dtype=float),
        y=clean[target_name].to_numpy(dtype=float),
        feature_names=list(feature_names),
        provenance_levels=clean[provenance_column].astype(str).tolist(),
    )
