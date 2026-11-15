from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class EvidenceLevel(str, Enum):
    NASA_OBSERVED = "NASA_OBSERVED"
    NASA_EMPIRICAL_CORRELATION = "NASA_EMPIRICAL_CORRELATION"
    PEER_REVIEWED_OBSERVED = "PEER_REVIEWED_OBSERVED"
    PHYSICS_DERIVED = "PHYSICS_DERIVED"
    MODEL_ESTIMATED = "MODEL_ESTIMATED"
    EMBER_PROPOSED = "EMBER_PROPOSED"
    SYNTHETIC_FOR_ALGORITHM_TESTING = "SYNTHETIC_FOR_ALGORITHM_TESTING"


class ApplicabilityStatus(str, Enum):
    IN_DOMAIN = "IN_DOMAIN"
    PARTIAL = "PARTIAL"
    EXTRAPOLATED_PHYSICS = "EXTRAPOLATED_PHYSICS"
    OUT_OF_DOMAIN = "OUT_OF_DOMAIN"
    NO_VALIDATED_BRIDGE = "NO_VALIDATED_BRIDGE"


class CombustionScenario(BaseModel):
    material: str = Field(..., description="Fuel material, e.g. PMMA")
    geometry: str = Field(..., description="Model-family geometry label")
    gravity_g: float = Field(..., ge=0.0, description="Gravity as fraction of Earth g")
    pressure_kpa: float = Field(..., gt=0.0)
    oxygen_fraction: float = Field(..., gt=0.0, lt=1.0)
    forced_flow_m_s: Optional[float] = Field(None, ge=0.0)
    rod_radius_cm: Optional[float] = Field(None, gt=0.0)
    thickness_mm: Optional[float] = Field(None, gt=0.0)
    sample_length_m: Optional[float] = Field(None, gt=0.0)
    pyrolysis_length_m: Optional[float] = Field(None, gt=0.0, description="Measured/explicit pyrolysis length when required by an adapter")
    core_material: Optional[str] = None
    core_radius_mm: Optional[float] = Field(None, gt=0.0)
    insulation_thickness_mm: Optional[float] = Field(None, gt=0.0)
    channel_gap_mm: Optional[float] = Field(None, gt=0.0)
    external_heat_flux_kw_m2: Optional[float] = Field(None, ge=0.0)
    orientation: Optional[str] = None
    notes: Optional[str] = None


class ApplicabilityReport(BaseModel):
    status: ApplicabilityStatus
    model_id: str
    checks: Dict[str, bool]
    warnings: List[str] = []
    rationale: str


class PhysicsFingerprint(BaseModel):
    model_id: str
    values: Dict[str, float]
    applicability: ApplicabilityReport
    provenance: List[Dict[str, Any]]


class InverseDesignRequest(BaseModel):
    target: CombustionScenario
    test_gravity_g: float = Field(1.0, ge=0.0)
    strict_domain: bool = True
    optimize_flow: bool = True


class InverseDesignResult(BaseModel):
    model_id: str
    status: ApplicabilityStatus
    target_applicability_status: Optional[ApplicabilityStatus] = None
    proposed_applicability_status: Optional[ApplicabilityStatus] = None
    target_fingerprint: Dict[str, float]
    proposed_scenario: Optional[CombustionScenario]
    proposed_fingerprint: Optional[Dict[str, float]]
    objective_value: Optional[float]
    residuals: Dict[str, float] = {}
    unmatched_physics: Dict[str, Any] = {}
    warnings: List[str] = []
    provenance: List[Dict[str, Any]] = []


class RetrievalResult(BaseModel):
    record_id: str
    score: float
    family: str
    source_id: str
    fields: Dict[str, Any]
    contribution: Dict[str, float]


class RodBoundaryEvaluateRequest(BaseModel):
    stretch_s_inv: float = Field(..., ge=0.0)
    oxygen_pct: float = Field(..., gt=0.0, lt=100.0)


class RodBoundaryRootsRequest(BaseModel):
    oxygen_pct: float = Field(..., gt=0.0, lt=100.0)
    max_stretch_s_inv: float = Field(300.0, gt=0.0, le=5000.0)


class IgnitionPredictRequest(BaseModel):
    oxygen_pct: List[float] = Field(..., min_length=1, max_length=200)


class IgnitionBEDRequest(BaseModel):
    oxygen_candidates_pct: List[float] = Field(..., min_length=1, max_length=500)
    target_oxygen_pct: Optional[float] = Field(None, gt=0.0, lt=100.0)
    relevance_width_pct: float = Field(1.0, gt=0.0, le=20.0)
    top_k: int = Field(10, ge=1, le=100)
