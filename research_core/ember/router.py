from __future__ import annotations
from ember.schemas import CombustionScenario
from ember.physics.thick_pmma_concurrent import ThickPMMAConcurrentAdapter
from ember.physics.pmma_rod_blowoff import PMMARodBlowoffAdapter
from ember.physics.sibal_concurrent import SIBALConcurrentAdapter
from ember.physics.kimwipes import KimwipesConcurrentAdapter
from ember.physics.ldpe_wire import LDPEWireP2GAdapter
from ember.physics.nca_pmma import ThinPMMANCAAdapter
from ember.normalization import canonical_material,canonical_geometry

class PhysicsModelRouter:
    def __init__(self):
        classes=[ThickPMMAConcurrentAdapter,PMMARodBlowoffAdapter,SIBALConcurrentAdapter,KimwipesConcurrentAdapter,LDPEWireP2GAdapter,ThinPMMANCAAdapter]
        self.adapters={c.model_id:c() for c in classes}
    def route(self,s:CombustionScenario):
        m,g=canonical_material(s.material),canonical_geometry(s.geometry)
        if (m,g)==('PMMA','ROD'): return self.adapters[PMMARodBlowoffAdapter.model_id]
        if (m,g)==('PMMA','THICK_SLAB'): return self.adapters[ThickPMMAConcurrentAdapter.model_id]
        if (m,g)==('SIBAL','THIN_FABRIC_CONCURRENT'): return self.adapters[SIBALConcurrentAdapter.model_id]
        if (m,g)==('KIMWIPES','THIN_SHEET_CONCURRENT'): return self.adapters[KimwipesConcurrentAdapter.model_id]
        if (m,g)==('LDPE','WIRE_OPPOSED'): return self.adapters[LDPEWireP2GAdapter.model_id]
        if (m,g)==('PMMA','THIN_SHEET_OPPOSED_NCA'): return self.adapters[ThinPMMANCAAdapter.model_id]
        return None
    def list_models(self): return [a.metadata() for a in self.adapters.values()]
