from __future__ import annotations
from ember.router import PhysicsModelRouter
from ember.schemas import CombustionScenario, InverseDesignResult, ApplicabilityStatus


def inverse_design(target: CombustionScenario, test_gravity_g: float = 1.0, strict_domain: bool = True, optimize_flow: bool = True) -> InverseDesignResult:
    router = PhysicsModelRouter()
    adapter = router.route(target)
    if adapter is None:
        return InverseDesignResult(
            model_id="none",
            status=ApplicabilityStatus.NO_VALIDATED_BRIDGE,
            target_fingerprint={}, proposed_scenario=None, proposed_fingerprint=None,
            objective_value=None,
            warnings=["No validated EMBER physics adapter matches this material/geometry."],
            provenance=[],
        )
    return adapter.inverse_design(target, test_gravity_g=test_gravity_g, strict_domain=strict_domain, optimize_flow=optimize_flow)
