from __future__ import annotations
from fastapi import FastAPI, Query, HTTPException
from ember.schemas import (
    CombustionScenario, RodBoundaryEvaluateRequest, RodBoundaryRootsRequest,
    IgnitionPredictRequest, IgnitionBEDRequest,
)
from ember.service import EmberService

app = FastAPI(
    title="EMBER Regime-Bridging Scientific Core",
    version="2.0.0-research",
    description="Physics-aware cross-gravity combustion evidence, constrained empirical uncertainty, inverse design, and Bayesian experiment-design API. Research prototype; not a safety certification tool.",
)
service = EmberService()


def _translate_error(exc: Exception):
    if isinstance(exc, ValueError):
        raise HTTPException(status_code=422, detail=str(exc))
    if isinstance(exc, RuntimeError):
        raise HTTPException(status_code=503, detail=str(exc))
    raise exc


@app.get("/")
def root():
    return {
        "system": "EMBER — Explainable Microgravity Burn Evidence & Regime-Bridging",
        "version": "2.0.0-research",
        "status": "scientific core online",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health(): return service.health()

@app.get("/models")
def models(): return service.models()

@app.get("/sources")
def sources(): return service.sources()

@app.get("/readiness")
def readiness(): return service.readiness()


@app.get("/v2/registry")
def v2_registry(): return service.v2_registry()

@app.get("/v2/threshold")
def v2_threshold(material: str, gravity_g: float):
    try: return service.threshold_lookup(material, gravity_g)
    except (ValueError, RuntimeError) as e: _translate_error(e)

@app.get("/empirical/rod-boundary/minimum")
def rod_boundary_minimum(): return service.rod_boundary_minimum()

@app.post("/empirical/rod-boundary/evaluate")
def rod_boundary_evaluate(req: RodBoundaryEvaluateRequest):
    try: return service.rod_boundary_evaluate(req.stretch_s_inv, req.oxygen_pct)
    except (ValueError, RuntimeError) as e: _translate_error(e)

@app.post("/empirical/rod-boundary/roots")
def rod_boundary_roots(req: RodBoundaryRootsRequest):
    try: return service.rod_boundary_roots(req.oxygen_pct, req.max_stretch_s_inv)
    except (ValueError, RuntimeError) as e: _translate_error(e)

@app.get("/ml/ignition/status")
def ignition_status(): return service.ignition_status()

@app.get("/ml/ignition/calibration")
def ignition_calibration(): return service.calibration()

@app.post("/ml/ignition/predict")
def ignition_predict(req: IgnitionPredictRequest):
    try: return service.ignition_predict(req.oxygen_pct)
    except (ValueError, RuntimeError) as e: _translate_error(e)

@app.get("/bed/status")
def bed_status():
    status = service.ignition_status()
    return {
        "loaded": status.get("loaded", False),
        "scientific_ready": status.get("scientific_ready", False),
        "readiness_status": status.get("readiness_status"),
        "model": "small-sample Bayesian PMMA oxygen-boundary model",
        "criterion": "Bernoulli expected information gain",
        "training": status.get("training"),
        "scope": status.get("scope"),
    }

@app.post("/bed/rank")
def bed_rank(req: IgnitionBEDRequest):
    try:
        return service.ignition_bed(req.oxygen_candidates_pct, req.target_oxygen_pct, req.relevance_width_pct, req.top_k)
    except (ValueError, RuntimeError) as e: _translate_error(e)

@app.post("/fingerprint")
def fingerprint(scenario: CombustionScenario):
    try: return service.fingerprint(scenario)
    except (ValueError, RuntimeError) as e: _translate_error(e)

@app.post("/retrieve")
def retrieve(scenario: CombustionScenario, top_k: int = Query(5, ge=1, le=20)):
    try: return service.retrieve(scenario, top_k)
    except (ValueError, RuntimeError) as e: _translate_error(e)

@app.post("/inverse-design")
def inverse_design_endpoint(
    scenario: CombustionScenario,
    test_gravity_g: float = Query(1.0, ge=0.0),
    strict_domain: bool = True,
    optimize_flow: bool = True,
):
    try: return service.inverse(scenario, test_gravity_g, strict_domain, optimize_flow)
    except (ValueError, RuntimeError) as e: _translate_error(e)

@app.post("/report")
def regime_report(
    scenario: CombustionScenario,
    test_gravity_g: float = Query(1.0, ge=0.0),
    strict_domain: bool = True,
    optimize_flow: bool = True,
    top_k: int = Query(5, ge=1, le=20),
):
    try: return service.report(scenario, test_gravity_g, strict_domain, optimize_flow, top_k)
    except (ValueError, RuntimeError) as e: _translate_error(e)
