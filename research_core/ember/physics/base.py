from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Dict
from ember.schemas import ApplicabilityReport, CombustionScenario, PhysicsFingerprint


class PhysicsAdapter(ABC):
    model_id: str
    title: str

    @abstractmethod
    def applicability(self, scenario: CombustionScenario) -> ApplicabilityReport:
        raise NotImplementedError

    @abstractmethod
    def fingerprint(self, scenario: CombustionScenario) -> PhysicsFingerprint:
        raise NotImplementedError

    @abstractmethod
    def inverse_design(self, *args, **kwargs):
        raise NotImplementedError

    def metadata(self) -> Dict:
        return {"model_id": self.model_id, "title": self.title}
