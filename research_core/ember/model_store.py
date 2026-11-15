from __future__ import annotations
from pathlib import Path
import json
from ember.ml.bayesian_ignition import BayesianIgnitionModel

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_IGNITION_PATH = ROOT / "models" / "bass_ii_bayesian_ignition.json"


def save_ignition(model: BayesianIgnitionModel, path: str | Path = DEFAULT_IGNITION_PATH):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(model.to_dict(), separators=(",", ":")), encoding="utf-8")
    return path


def load_ignition(path: str | Path = DEFAULT_IGNITION_PATH) -> BayesianIgnitionModel | None:
    path = Path(path)
    if not path.exists():
        return None
    payload = json.loads(path.read_text(encoding="utf-8"))
    return BayesianIgnitionModel.from_dict(payload)
